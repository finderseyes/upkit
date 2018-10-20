import errno
import os
import shutil
from subprocess import call
from sys import platform


def guaranteed_list(x):
    if not x:
        return []
    elif isinstance(x, list):
        return x
    else:
        return [x]


def realpath(path):
    """
    Converts to real, canonical path.
    :param path:
    :return:
    """
    path = path if os.path.isabs(path) else os.path.abspath(path)
    return os.path.realpath(path)


def is_link(path):
    if platform == 'cygwin' or platform == 'win32':
        from upkit import win32
        return os.path.islink(path) or win32.is_junction(path)
    else:
        return os.path.islink(path)


def remove(path):
    if platform == 'cygwin' or platform == 'win32':
        call('cmd /c rm "%s"' % path, shell=True)
    else:
        call('rm "%s"' % path, shell=True)


def rmdir(path):
    if platform == 'cygwin' or platform == 'win32':
        call('cmd /c rmdir /Q /S "%s"' % path, shell=True)
    else:
        call('rm -rf "%s"' % path, shell=True)


def mkdir_p(path):
    """
    mkdir -p
    from https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python

    :param path:
    :return:
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def copy(source, target):
    is_directory = os.path.isdir(source)
    if is_directory:
        shutil.copytree(source, target)
    else:
        shutil.copy(source, target)


def fs_unlink(path):
    is_directory = os.path.isdir(path)

    if platform == 'cygwin' or platform == 'win32':
        if is_directory:
            call('cmd /c rmdir /Q "%s"' % path, shell=True)
        else:
            call('cmd /c del /Q "%s"' % path, shell=True)
    else:
        call('rm "%s"' % path, shell=True)


def fs_link(source, target, hard_link=True, forced=False):
    """
    
    :param source:
    :param target:
    :param hard_link:
    :param forced:
    :return:
    """
    source = realpath(source)
    target = os.path.abspath(target)

    if not os.path.exists(source):
        raise ValueError('Path "%s" does not exist.' % source)

    if os.path.exists(target):
        if not forced:
            raise RuntimeError('Path "%s" exists.' % target)

        if is_link(target):
            fs_unlink(target)
        else:
            raise RuntimeError('Path "%s" exists, but it is not a link.' % target)
    else:
        parent_dir = os.path.dirname(target)
        mkdir_p(parent_dir)

    is_directory = os.path.isdir(source)
    print('Create filesystem link: "%s" -> "%s"' % (source, target))

    if platform == 'cygwin' or platform == 'win32':
        if not is_directory:
            call('cmd /C mklink "%s" "%s"' % (target, source), shell=True)
        else:
            if hard_link:
                call('cmd /C mklink /J "%s" "%s"' % (target, source), shell=True)
            else:
                call('cmd /C mklink /D "%s" "%s"' % (target, source), shell=True)

    else:
        call('ln -s "%s" "%s"' % (source, target), shell=True)

