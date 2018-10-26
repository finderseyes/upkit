# Getting started with Upkit

These instructions will use `upkit` to create a simple Unity3D project which depends on Newtonsoft.Json on Nuget Gallery.

The source code to this project can be also found under [`examples/simple-app`](https://github.com/finderseyes/upkit/tree/develop/examples/simple-app).

## Prerequisites

* Python 2.7 or above, with `pip`.
* (optional) `nuget` for resolving Nuget dependencies.
* (optional) `git` for resolving Git dependencies.

## Installation

```
$ pip install upkit
```

## Step 1: Create Upkit project
Creating a new Upkit project is as simple as:

```
$ upkit create-package simple-app
```

## Step 2: Edit Upkit config file `upkit.yaml`
Upkit will create a new folder named `simple-app`, where you can find `upkit.yaml`. This file contains all the information Upkit needs in order to create your Unity project. Now, modify it to let Upkit know the project will depends on `NewtonSoft.Json`: 

```yaml
# upkit.yaml
params:
  project: '{{__dir__}}/project'
  
links:
  - target: '{{__assets__}}'    
    source: '{{__dir__}}/assets'
    content: ['*']

  - target: '{{__plugins__}}'
    source: '{{__dir__}}/plugins'
    content: ['*']

  - target: '{{__project__}}/ProjectSettings'
    source: '{{__dir__}}/settings'
    
  - target: '{{__project__}}/Packages'
    source: '{{__dir__}}/packages'

  # Add project dependencies here: 
  - source: 'nuget:Newtonsoft.Json@11.0.2#lib/net35'
    target: '{{__plugins__}}/Newtonsoft.Json'
```

Notice the second-last line where we instruct Upkit to resolve a Nuget library with `nuget:` scheme. Yes, it's that simple. 

## Step 3: Link to create Unity projects
The final step is to generate a Unity project, by calling: 

```
$ cd simple-app 
$ upkit link
```
Upkit will take a few seconds to resolve project's dependencies and generate a Unity project under `simple-app/project`. Open the folder in Unity as a project and you are ready to go.
