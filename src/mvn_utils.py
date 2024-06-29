import xml.etree.ElementTree as xml
import sys

from subprocess import run
from pathlib import Path
from textwrap import dedent
from typing import List
from .github_utils import create_release

maven_namespace = "http://maven.apache.org/POM/4.0.0"


def get_package_info(root_path: Path):
    root = xml.parse(root_path / "pom.xml").getroot()
    namespace = {"maven": maven_namespace}
    group_id = root.find("maven:groupId", namespace)
    artifact_id = root.find("maven:artifactId", namespace)

    return {
        "group_id": group_id.text,  # type: ignore
        "artifact_id": artifact_id.text,  # type: ignore
    }


def set_package_version(root_path: Path, version: int):
    tree = xml.parse(root_path / "pom.xml")
    root = tree.getroot()
    namespace = {"maven": maven_namespace}
    version_tag = root.find("maven:version", namespace)

    version_tag.text = f"{version}.0.0"  # type: ignore

    tree.write(
        root_path / "pom.xml",
        encoding="utf-8",
        xml_declaration=True,
        default_namespace=maven_namespace,
    )


def publish_mvn_package(
    *,
    src: Path,
    version: int,
    tag_prefix: str,
    maven_username: str,
    maven_password: str,
    gpg_private_key: str,
    gpg_passphrase: str,
    github_access_token: str,
):

    if not maven_username:
        print("Maven username is missing", flush=True, file=sys.stderr)
        exit(1)
        
    if not maven_password:
        print("Maven password is missing", flush=True, file=sys.stderr)
        exit(1)
        
    if not gpg_private_key:
        print("GPG private key is missing", flush=True, file=sys.stderr)
        exit(1)
        
    if not gpg_passphrase:
        print("GPG passphrase is missing", flush=True, file=sys.stderr)
        exit(1)

    if not github_access_token:
        print("GitHub access token is missing", flush=True, file=sys.stderr)
        exit(1)

    package_name = get_package_info(src)
    
    set_package_version(src, version)

    run(['npm', 'publish', '--access=public'], cwd=src, check=True)
    
    print(package_name)
