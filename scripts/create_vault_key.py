#!/usr/bin/env python3

from pathlib import Path
import sys

root_directory = Path(__file__).parent.parent
sys.path.append(str(root_directory))

from src.ansible_utils import create_vault_key

root_directory = Path(__file__).parent.parent

create_vault_key(root_directory / '.ansible/vault_key')