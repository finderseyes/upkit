import os
import shutil
from sys import platform
from subprocess import call, check_output


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
        import win32
        return win32.islink(path)
    else:
        return os.path.islink(path)


def remove(path):
    if platform == 'cygwin' or platform == 'win32':
        call('cmd /c rm "%s"' % path, shell=True)
    else:
        call('rm "%s"' % path, shell=True)


def fs_unlink(path):
    if platform == 'cygwin' or platform == 'win32':
        call('cmd /c rm "%s"' % path, shell=True)
    if platform == 'darwin':
        call('sh -c "hln -u \"%s\""' % path, shell=True)
    else:
        call('unlink "%s"' % path, shell=True)


def fs_link(source, target, hard_link=True):
    """
    
    :param source:
    :param target:
    :param hard_link:
    :return:
    """
    source = realpath(source)
    target = os.path.abspath(target)

    is_directory = os.path.isdir(source)

    print('Create filesystem link: "%s" -> "%s"' % (source, target))

    if os.path.exists(target):
        if is_link(target):
            fs_unlink(target)
        else:
            raise RuntimeError('Folder exists.')

    if platform == 'cygwin' or platform == 'win32':
        if hard_link:
            if is_directory:
                call('cmd /C mklink /J "%s" "%s"' % (target, source), shell=True)
            else:
                call('cmd /C mklink /H "%s" "%s"' % (target, source), shell=True)
        else:
            if is_directory:
                call('cmd /C mklink /D "%s" "%s"' % (target, source), shell=True)
            else:
                call('cmd /C mklink "%s" "%s"' % (target, source), shell=True)

    else:
        call('ln -s "%s" "%s"' % (source, target), shell=True)
    # elif platform == 'darwin':
    #     if hard_link:
    #         call('sh -c "hln %s %s"' % (source, target), shell=True)
    #     else:
    #         call('ln -s "%s" "%s"' % (source, target), shell=True)
    # else:
    #     if hard_link:
    #         call('ln "%s" "%s"' % (source, target), shell=True)
    #     else:
    #         call('ln -s "%s" "%s"' % (source, target), shell=True)

