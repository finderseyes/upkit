#!/usr/bin/env bash

nuget restore packages.config -PackagesDirectory dependencies
unity-tools link -c project-config.yaml