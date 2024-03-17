#!/usr/bin/env python3

from pathlib import Path
import init
from src.github_utils import create_pages_artifact

root_directory = Path(__file__).parent.parent

create_pages_artifact(directory=root_directory / 'test')
