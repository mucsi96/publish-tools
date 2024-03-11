#!/usr/bin/env python3

from os import environ
import sys
from pathlib import Path
from setuptools import sandbox

root_directory = Path(__file__).parent

sys.path.append(str(root_directory))

from src.github_utils import create_release, upload_release_asset
from src.version_utils import get_version

access_token = sys.argv[1]

if not access_token:
    print("GitHub access token is missing", flush=True, file=sys.stderr)
    exit(1)

changed, version = get_version(src="src", tag_prefix="lib")

if not changed:
    exit()

environ["LIB_VERSION"] = str(version)
sandbox.run_setup("setup.py", ["bdist_wheel"])

release_id = create_release(version=version, access_token=access_token, tag_prefix="lib")
upload_release_asset(
    release_id=release_id,
    filename_pattern="dist/publish-tools-*.whl",
    access_token=access_token,
)
