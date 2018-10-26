# Upkit Commands

## `link` command

**Usage**
Resolves and links dependencies for a project with a given configuration.

**Syntax**
```
$ upkit link [-w PACKAGE_FOLDER] [-p PARAMS] [config] 
```

**Parameters**
* `config` (optional, default to `upkit.yaml`) is the path to the link configuration file.
* `-w` (optional, default to `.packages`) is the path to the folder containing resolved Nuget and Git packages.
* `-p` (optional) defines a parameter to use when linking, and can be passed multiple times for multiple parameters, for example `upkit link -p a=1 -p b=2`. 
	* If there is an existing parameter in the given configuration file, its value will be overwriten by the value in `-p` parameter.

## `create-package` command
**Usage**
Creates an empty package, which can be used as the boilerplate for a new Upkit project. 

**Syntax**
```
$ upkit create-package [--link] location
```

**Parameters**
* `location` (required) is the name or location of an empty folder for the new package. 
* `--link` (optional, default to `False`) to execute `link` command after the project is generated.