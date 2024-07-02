#!/usr/bin/env python3

from os import environ, makedirs
from posixpath import dirname
from tempfile import NamedTemporaryFile
import init
import sys
from pathlib import Path
from src.ansible_utils import load_vars
from src.mvn_utils import publish_mvn_package
from src.version_utils import get_version

root_directory = Path(__file__).parent.parent
secrets = load_vars(sys.argv[2], root_directory / 'vars/vault.yaml')

version= get_version(
    src=root_directory,
    tag_prefix="mvn-package",
)

publish_mvn_package(
    src=root_directory / 'src',
    version=version,
    tag_prefix="mvn-package",
    maven_username=secrets['maven_username'],
    maven_password=secrets['maven_password'],
    gpg_private_key=secrets['gpg_private_key'],
    gpg_passphrase=secrets['gpg_passphrase'],
    github_access_token=sys.argv[1]
)
