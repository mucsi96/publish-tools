#!/usr/bin/env python3


from pathlib import Path
from shutil import rmtree
from subprocess import run
import toml
import init
import sys
from build import ProjectBuilder
from src.github_utils import create_release, upload_release_asset
from src.version_utils import get_version

root_directory = Path(__file__).parent.parent


def set_package_version(version: int):
    with open('pyproject.toml', 'r') as file:
        package_data = toml.load(file)

    package_data['project']['version'] = f'{version}.0.0'

    with open('pyproject.toml', 'w') as file:
        toml.dump(package_data, file)


access_token = sys.argv[1]

if not access_token:
    print("GitHub access token is missing", flush=True, file=sys.stderr)
    exit(1)

version = get_version(src=root_directory, tag_prefix="version")

rmtree("build", ignore_errors=True)
rmtree("dist", ignore_errors=True)
rmtree("publish_tools.egg-info", ignore_errors=True)

set_package_version(version)

ProjectBuilder(source_dir='.').build(
    distribution='wheel', output_directory='dist')

run(['unzip', '-l', 'dist/*.whl'])

release_id = create_release(
    version=version, access_token=access_token, tag_prefix="version")
upload_release_asset(
    release_id=release_id,
    filename_pattern="dist/publish_tools-*.whl",
    access_token=access_token,
)
