import json
import sys

from subprocess import run
from pathlib import Path
from textwrap import dedent
from typing import List
from .github_utils import create_release
from .version_utils import get_version


def get_npm_package_name(root_path: Path):
    with open(root_path / 'package.json', 'r') as file:
        package_data = json.load(file)
        return package_data['name']


def publish_npm_package(
    *,
    src: Path,
    tag_prefix: str,
    npm_access_token: str,
    github_access_token: str,
    ignore: List[str] = [],
):
    package_name = get_npm_package_name(src)

    if not npm_access_token:
        print('NPM access token is missing', flush=True, file=sys.stderr)
        exit(1)

    if not github_access_token:
        print('GitHub access token is missing', flush=True, file=sys.stderr)
        exit(1)

    changed, version = get_version(
        src=src, tag_prefix=tag_prefix, ignore=ignore)

    if not changed:
        return

    with open(src / '.npmrc', 'w') as file:
        file.write(f'registry=https://registry.npmjs.org')

    run('npm publish', env={
        'NODE_AUTH_TOKEN': npm_access_token}, cwd=src, shell=True, check=True)

    create_release(
        tag_prefix=tag_prefix,
        version=version,
        access_token=github_access_token,
        body=dedent(f'''
            [NPM package](https://www.npmjs.com/package/{package_name})

            ```json
            "{package_name}": "{version}"
            ```
        ''')
    )
    print(
        f'NPM package pushed successfully for {tag_prefix}:{version}', flush=True)
