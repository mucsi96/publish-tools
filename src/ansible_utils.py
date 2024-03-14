import sys

from os import makedirs, path
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from ansible.parsing.vault import VaultSecret
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.dataloader import DataLoader


def read_file(file_path: Path):
    try:
        with open(file_path, 'rb') as file:
            return file.read().strip()
    except:
        print("Error reading file at", file_path, flush=True, file=sys.stderr)


def load_vars(vault_secret_file: Path, vars_file: Path):
    vault_secret = read_file(vault_secret_file)
    loader = DataLoader()
    loader.set_vault_secrets(
        [(DEFAULT_VAULT_ID_MATCH, VaultSecret(vault_secret))])
    return loader.load_from_file(str(vars_file))


def create_vault_key(vault_secret_file: Path):
    makedirs(path.dirname(vault_secret_file), exist_ok=True)

    if path.exists(vault_secret_file):
        raise Exception(f"The file '{vault_secret_file}' already exists.")

    alphabet = ascii_letters + digits + r"""!#%&*+,-.:;=?@[\]^_{}~"""
    password = ''.join(choice(alphabet) for i in range(50))
    with open(vault_secret_file, 'w') as file:
        file.write(password)
