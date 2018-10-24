# Upkit &mdash; Unity3D project/package toolkit

`upkit` is a command line toolkit that helps create/organize your Unity3D projects. With a simple configuration file, Upkit automatically resolves the project dependencies and generates a ready-to-use Unity project for you. 

_For those in a hurry, please go to [Getting Started](#getting-started) to see it in action._

## Why should you use it? 

### Existing tools' limitations

At first glance, Upkit shares some similarities with Projeny, which is a great tool that we frequently used in our team. However, as `Projeny` model imposes a flat, exclusive package hierarchy (everything must be a folder in either `Assets` or `Plugins` folder), off-the-shelf packages do not often work well together. For example, two packages having different native 

There are tools that already helped with managing dependencies. In fact, we are big fans of the great tool `Projeny` for its simplicity, CI friendliness, and have used it frequently in our team. However, as `Projeny` model imposes a flat, exclusive package hierarchy (everything must be in either `Assets` or `Plugins` folder), it is not always possible to link external packages directly without repackaging. For example, two packages having different native libraries under the same folder `Plugins/Android` will not work together unless we copy these native libraries to another folder, namely `Plugins_Android` and link it under `Plugins/Android`. 

As for Unity built-in Package Manager, although looking promising, it does not offer the following capabilities that we need:
* Management of our private asset packages, legacy Unity packages, and even Nuget packages.
* CI friendliness. 

### `upkit` remedies those issues and adds some tricks

`upkit` was initially designed as a tool sitting between `nuget` (dependency resolving) and `Projeny` (project linking) in our pipeline, where extra links are generated before the actual project structure is created. As the tool evolves, `upkit` gradually becomes a superset to some of `Projeny` main features, to a point that it replaces `Projeny` completely in our pipeline.

In particular, `upkit` provides the following main features:
* Packages can be linked to any location in the project folder, not just `Assets` and `Plugins`.
* Packages can have sub-links pointing to anywhere in its content, not just its root. Therefore external or Nuget packages can be linked without repackaging.
* File-level links, not just folders.
* Packages can have their `linkspec.yaml` file to define how they should be linked (for cross-project reusable packages).
* Simple configuration, yet extensible with parameters.


## Getting Started

These instructions will use `upkit` to create a simple Unity3D project which depends on Newtonsoft.Json on Nuget Gallery.

The source code to this project can be also found under [`examples/simple-app`](https://github.com/finderseyes/upkit/tree/develop/examples/appkit).

### Prerequisites

* Python 2.7 or above, with `pip`.
* `nuget` for resolving Nuget dependencies.

### Installation

```
$ pip install upkit
```

### Step 1: Create Upkit project
Creating a new Upkit project is as simple as:

```
$ upkit create-package simple-app
```

### Step 2: Edit Upkit config file `upkit.yaml`
Upkit will create a new folder named `simple-app`, where you can find `upkit.yaml`. This file contains all the information Upkit needs in order to create your Unity project. Now, modify it to let Upkit know the project will depends on `NewtonSoft.Json`: 

```yaml
params:
  project: '{{__dir__}}/project'
  
links:
  - target: '{{__assets__}}'
    content: ['{{__dir__}}/assets/*']

  - target: '{{__plugins__}}'
    content: ['{{__dir__}}/plugins/*']

  - target: '{{__project__}}/ProjectSettings'
    source: '{{__dir__}}/settings'
    
  - target: '{{__project__}}/Packages'
    source: '{{__dir__}}/packages'

  # Add project dependencies here: 
  - source: 'nuget:Newtonsoft.Json@11.0.2#lib/net35'
    target: '{{__plugins__}}/Newtonsoft.Json'
```

Notice the second-last line where we instruct Upkit to resolve a Nuget library with `nuget:` scheme. Yes, it's that simple. As of version `0.4.0`, Upkit also support the following scheme:
* `git:` to resolve a package directly from a Git repository.

### Step 3: Link to create Unity projects
The final step is to generate a Unity project, by calling: 

```
$ cd simple-app 
$ upkit link -w dependencies
```

Upkit will take a few seconds to resolve project's dependencies and generate a Unity project under `simple-app/project`. Open the folder in Unity as a project and you are ready to go.

## Documentation

Work in progress.

## Authors

* **Vu Le** - *Initial work* - [FindersEyes](https://github.com/finderseyes)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This tool uses `xmltodict`, `pyyaml`, `yamlordereddictloader`, and `jinja2` under the hood. Thanks to the respected authors for the hard work.
