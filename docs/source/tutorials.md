# Tutorials

## Create a reusable package

_Source code for this tutorial can be found in [examples/shared-package](https://github.com/finderseyes/upkit/tree/develop/examples/shared-package)_

In this tutorial we will create a package `DemoPackage` which exports the following items when linked to project:

```
• 
├── Assets/
│   └── DemoPackage/
│       └── Scenes/
└── Plugins/
    └── DemoPackage/
```

### Step 1: Create `app` and `demo-package` project
Run the following commands to create the projects:

```
$ upkit create-package app
$ upkit create-package demo-package
```
You will notice the following structure each generated project:
```
•
├── assets/ 		-> project Assets content
├── packages/		-> Unity 2018 packages folder
├── plugins/		-> project Plugins content
├── project/		-> the generated project
├── settings/		-> project settings 
├── linkspec.yaml	-> package linkspec
├── package.nuspec	-> predefined Nuspec file, if you want to build to a Nuget package
└── upkit.yaml		-> link configuration
```

Note we also use create `app` using `create-package` command, as it can also be shared to another project.

### Step 2: Build `demo-package`

Let's assume that `demo-package` has a few scripts and a demo scene as an example to its users. Create the following folders in `demo-packages`:
```
• (demo-package)
├── assets/ 
│   └── Scenes/
└── plugins/
    └── DemoPackage/
```
Then link it
```
$ cd demo-package && upkit link
```
Open `demo-package/project` in Unity, you will see the project structure as:

![Project structure](/../_images/tut1-001.png)

Add a scene to the `Assets/Scenes` and create something fancy under `Assets/Plugins/DemoPackage`. 

### Step 3: Update `demo-package` linkspec

The next step is to edit the package linkspec so that others can use it. The default generated `linkspec.yaml` would suffice in most cases, we want to modify it so that the package demo `Scenes` will be linked under `DemoPackage/Scenes` the target project to avoid name conflicts. 

Open `demo-package/linkspec.yaml` and modify its first link target from `target: '{{__assets__}}'` to `target: '{{__assets__}}/DemoPackage'`.

### Step 4: Link `demo-package` with `app`

Linking with `demo-package` is as simple as adding it as a source in `app/upkit.yaml`:

```yaml
# app/upkit.yaml
...
links:
  ...
  - source: '{{__dir__}}/../demo-package'
```
Finally, from `app` folder, run `$ upkit link`, then open the Unity project under `app/project`. That's it, the `demo-package` is linked to your app already.

## Repackage an existing Unity package  

_Work in progress_