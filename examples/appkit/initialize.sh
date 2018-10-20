#!/usr/bin/env bash

nuget restore packages.config -PackagesDirectory dependencies

upkit link -c project-config.yaml -p platform=ios
upkit link -c project-config.yaml -p platform=android