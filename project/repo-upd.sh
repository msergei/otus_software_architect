#!/bin/bash

git pull

git submodule sync --recursive
git submodule foreach git pull origin master

