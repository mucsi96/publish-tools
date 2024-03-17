#!/usr/bin/env python3

from os import environ, makedirs
from posixpath import dirname
from tempfile import NamedTemporaryFile
import init
import sys
from pathlib import Path
from src.ansible_utils import load_vars
from src.docker_utils import build_and_push_docker_img

root_directory = Path(__file__).parent.parent
secrets = load_vars(sys.argv[2], root_directory / 'vars/vault.yaml')

build_and_push_docker_img(
    src=root_directory / 'src',
    tag_prefix="docker-image",
    image_name="publish-tools-test",
    docker_username=environ.get('GITHUB_REPOSITORY_OWNER'),
    docker_password=secrets['docker_password'],
    github_access_token=sys.argv[1]
)
