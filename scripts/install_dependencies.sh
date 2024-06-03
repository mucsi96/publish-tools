#!/bin/bash

project=publish-tools
pyenv_version=3.12.3

brew update && brew install pyenv pyenv-virtualenv node

if ! pyenv virtualenvs | grep -q "$project"; then
    pyenv install $pyenv_version --skip-existing
    pyenv virtualenv $pyenv_version $project
    pyenv local $project
fi

pyenv activate $project

pip install -r requirements.txt

(cd src && npm install)