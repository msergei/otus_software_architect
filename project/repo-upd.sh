#!/bin/bash
git pull

git submodule sync --recursive
git submodule update --init --recursive --remote
git pull --recurse-submodules
git submodule foreach git checkout master
git submodule foreach git pull origin master
