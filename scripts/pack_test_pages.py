#!/usr/bin/env python3

from pathlib import Path
import sys

root_directory = Path(__file__).parent
sys.path.append(str(root_directory))

from src.github_utils import create_pages_artifact


create_pages_artifact(directory="test")
