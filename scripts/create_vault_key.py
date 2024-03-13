#!/usr/bin/env python3

import init
from pathlib import Path
from src.ansible_utils import create_vault_key

root_directory = Path(__file__).parent.parent

create_vault_key(root_directory / '.ansible/vault_key')
