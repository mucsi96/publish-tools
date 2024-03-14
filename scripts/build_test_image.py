#!/usr/bin/env python3

from os import makedirs
from posixpath import dirname
import init
import sys
from pathlib import Path
from src.ansible_utils import load_vars
from src.docker_utils import build_and_push_docker_img

root_directory = Path(__file__).parent.parent
access_token = sys.argv[1]
vault_key = sys.argv[2]
vault_key_file = root_directory / '.ansible/vault_key'

makedirs(dirname(vault_key_file))
with open(vault_key_file, 'w') as file:
    file.write(vault_key)

print(len(vault_key))

data = load_vars(vault_key_file,
                 root_directory / 'vars/vault.yaml')
docker_username = data['docker_username']
docker_password = data['docker_password']


if not access_token:
    print("GitHub access token is missing", flush=True, file=sys.stderr)
    exit(1)

build_and_push_docker_img(src="src", tag_prefix="docker-image",
                          image_name="publish-tools-test", docker_username=docker_username, docker_password=docker_password, github_access_token=access_token)
