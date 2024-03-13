#!/usr/bin/env python3

import sys
from pathlib import Path

root_directory = Path(__file__).parent.parent
sys.path.append(str(root_directory))

from src.ansible_utils import load_vars
from src.docker_utils import build_and_push_docker_img

root_directory = Path(__file__).parent.parent
data = load_vars(root_directory / '.ansible/vault_key',
                 root_directory / 'vars/vault.yaml')
docker_username = data['docker_username']
docker_password = data['docker_password']

access_token = sys.argv[1]

if not access_token:
    print("GitHub access token is missing", flush=True, file=sys.stderr)
    exit(1)

build_and_push_docker_img(src="src", tag_prefix="docker-image",
                          image_name="publish-tools-test", docker_username=docker_username, docker_password=docker_password, github_access_token=access_token)
