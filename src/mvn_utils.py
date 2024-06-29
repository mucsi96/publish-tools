import xml.etree.ElementTree as xml
import sys

from subprocess import run
from pathlib import Path
from textwrap import dedent
from typing import List
from .github_utils import create_release

def get_package_info(root_path: Path):
    root = xml.parse(root_path / 'pom.xml').getroot()
    namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    group_id = root.find('maven:groupId', namespace)
    artifact_id = root.find('maven:artifactId', namespace)

    return {
        'group_id': group_id.text, # type: ignore
        'artifact_id': artifact_id.text # type: ignore
    }


def set_package_version(root_path: Path, version: int):
    tree = xml.parse(root_path / 'pom.xml')
    root = tree.getroot()
    namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
    version_tag = root.find('maven:version', namespace)
    
    version_tag.text = f'{version}.0.0' # type: ignore

    tree.write(root_path / 'pom.xml', encoding='utf-8', xml_declaration=True)


# def authenticate(src: Path, npm_access_token: str):
#     with open(src / '.npmrc', 'w') as file:
#         file.write(
#             f'//registry.npmjs.org/:_authToken={npm_access_token}')
#         file.close()
#     run(['npm', 'whoami'], cwd=src, check=True)


def publish_mvn_package(
    *,
    src: Path,
    version: int,
    tag_prefix: str,
    npm_access_token: str,
    github_access_token: str
):

    if not npm_access_token:
        print('NPM access token is missing', flush=True, file=sys.stderr)
        exit(1)

    if not github_access_token:
        print('GitHub access token is missing', flush=True, file=sys.stderr)
        exit(1)

    package_name = get_package_info(src)
    set_package_version(src, version)
    
    print(package_name)
