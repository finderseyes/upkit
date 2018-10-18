#!/usr/bin/env bash

nuget restore packages.config -PackagesDirectory dependencies
unity-tools link-package -c link-config.yaml -d temp