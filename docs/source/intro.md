# Introduction

## What is Upkit?

*Upkit* is a command line toolkit that helps create/organize your Unity3D projects. With a simple configuration file, Upkit automatically resolves the project dependencies, symbolic-links them and generates a ready-to-use Unity project for you. 

_For those in a hurry, please go to [Getting Started](#getting-started) to see *Upkit* in action._

<!-- ## How it works? -->

## Why should you use it? 

### Our usecase

If you are like us, these are what you need when developing a Unity project:
* Total separation of 3rd party assets, plugins, dependencies from your assets/codes, to reduce the project size.
* Quick package swapping for prototyping and production. 
* Simple dependency resolving, from Nuget or Git repositories, or elsewhere. 
* Simple configuration.

### Limitations of existing tools

At first glance, Upkit shares some similarities with Projeny, which is a great tool that we frequently used in our team. However, as Projeny model imposes a flat, exclusive package hierarchy, off-the-shelf packages do not often work well together. For example, two packages having the same native library folder `Plugins/Android` will clash. Even when there are no name clashes, Unity-compatible Nuget packages are not easily linked at times. 

Unity 2018 officially comes with an easy-to-use built-in Package Manager. As of this writing, however, most of the Asset Store packages are still unavailable in the Package Manager, except those from Unity Technologies. Another drawback with current Package Manager is that we cannot use it for internal cross-project packages. This means that most of the time, we have to fall back to traditional approaches. 

### Upkit remedies those issues and adds some more tricks

Upkit was initially designed as our solution to the aforementioned limitations, which is a tool sitting between Nuget (dependency resolving step) and Projeny (project linking step) in our pipeline. As our projects evolve, we decided to simplify the whole process by combining the two steps into Upkit, making it even easier to use by adding the following features:

* Single (YAML) file configuration, for dependency resolving, linking, etc.
* Link anything with *Linkspec* &dash; determining how  folders, files are linked to your Unity project.
* Create distributable packages (with Linkspec).
* Out-of-the-box support for Nuget and Git dependencies.

## Authors

* **Vu Le** - *Initial work* - [FindersEyes](https://github.com/finderseyes)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/finderseyes/upkit/LICENSE.md) file for details

## Acknowledgments

* This tool uses `xmltodict`, `pyyaml`, `yamlordereddictloader`, and `jinja2` under the hood. Thanks to the respected authors for the hard work.
