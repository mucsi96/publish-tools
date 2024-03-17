#!/usr/bin/env python3

from os import environ, makedirs
from posixpath import dirname
from tempfile import NamedTemporaryFile
import init
import sys
from pathlib import Path
from src.ansible_utils import load_vars
from src.npm_utils import publish_npm_package

root_directory = Path(__file__).parent.parent
secrets = load_vars(sys.argv[2], root_directory / 'vars/vault.yaml')

publish_npm_package(
    src=root_directory / 'src',
    tag_prefix="npm-package",
    npm_access_token=secrets['npm_access_token'],
    github_access_token=sys.argv[1]
)
