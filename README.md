# publish-tools
Tools for package publishing

# GPG

1. Install GNU GPG

```bash
brew install gnupg
```

2. Generate GPG keys

```bash
gpg --generate-key
```

3. Get key id

```bash
gpg --list-secret-keys --keyid-format=long
```

4. Export the gpg private key

```bash
gpg --export-secret-keys -a <key-id> > secret.txt
```

