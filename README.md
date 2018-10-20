# upkit &mdash; Unity3D project/package toolkit

`upkit` is a command line toolkit that helps you create/organize your Unity3D projects and manage their dependencies. 

_If you are in a hurry, go to [Getting Started](#getting-started) to see it in action, otherwise, take a few minutes reading the following section to see what problems it tries to solve._

## Why should you use it? 

### Existing tools' limitations

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

These instructions will create a simple Unity3D project with a Nuget dependency (Newtonsoft.Json) using `upkit`.

The source code to this project can be also found under [`examples/appkit`](https://github.com/finderseyes/upkit/tree/develop/examples/appkit).

### Prerequisites

`upkit` requires Python (2.7 or above) to work. You will also need `pip` to install it.

For this example, you will also need `nuget` to resolve Nuget dependencies.

### Installing
Run the following command to install `upkit` from Github repository.

```
$ pip install git+https://github.com/finderseyes/upkit.git
```

### Create the project structure

We will need to create an initial structure for our project, as below: 

```
(project)/
├── dependencies/
├── project-packages/
│   ├── Scenes/
│   └── Scripts/
├── project-settings/
├── unity-projects/
├── packages.config
├── project-config.yaml
└── initialize.sh
```
In this folder:
* `dependencies` is where Nuget packages are installed.
* `project-packages` is where we create project scripts and scenes.
* `project-settings` is where Unity project setting files are stored. 
* `unity-projects` is where the actual Unity projects are generated.
* `packages.config` is Nuget packages file, declaring our project dependencies.
* `project-config.yaml` is the `upkit` configuration file. 
* `initialize.sh` is the script that we actually execute to link and generate Unity projects.

#### `packages.config`
Declaring project dependencies is simple, just a typical Nuget config file.
```xml
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="Newtonsoft.Json" version="11.0.2"/> 
</packages>
```

#### `project-config.yaml`
This is the main configuration file, which `upkit` uses to generate the Unity project. The configuration has two sections:
* `params` defines parameters used by the project. 
* `links` defines how the project and its packages should be linked. 

The following configuration should be self-explanatory. For more information please see the documentation.

```yaml
params:
  project_name: appkit
  platform: windows
  project_dir: '{{__dir__}}/unity-projects/{{project_name}}-{{platform}}'
  project_settings: '{{__dir__}}/project-settings'
  assets: '{{project_dir}}/Assets'
  plugins: '{{assets}}/Plugins'
  dependencies: '{{__dir__}}/dependencies'
  packages: '{{__dir__}}/project-packages'

links:
  - source: '{{project_settings}}'
    target: '{{project_dir}}/ProjectSettings'

  - source: '{{packages}}/Scripts'
    target: '{{assets}}/Scripts'

  - source: '{{packages}}/Scenes'
    target: '{{assets}}/Scenes'

  - source: '{{dependencies}}/Newtonsoft.Json.11.0.2/lib/net35'
    target: '{{plugins}}/Newtonsoft.Json'
```

#### `initialize.sh`
```bash
#!/usr/bin/env bash

# resolve Nuget dependencies
nuget restore packages.config -PackagesDirectory dependencies

# call upkit to link and generate Unity projects.
upkit link -c project-config.yaml -p platform=ios
upkit link -c project-config.yaml -p platform=android
```

### Generate Unity projects
It's simple, just run `initialize.sh` script. There will be two new folders, namely `appkit-ios` and `appkit-android`, under `unity-projects`. Open these folder in Unity and voilà, ready to go.
```
(project)/
├── unity-projects/
|   ├── appkit-ios/
|   └── appkit-android/
```

## Documentation

Work in progress.

## Authors

* **Vu Le** - *Initial work* - [FindersEyes](https://github.com/finderseyes)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This tool uses `xmltodict`, `pyyaml`, `yamlordereddictloader`, and `jinja2` under the hood. Thanks to the respected authors for the hard work.
