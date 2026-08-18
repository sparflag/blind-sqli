# Blind Oracle (`blind-sqli`)

**Category:** sql injection · **Difficulty:** hard · **Points:** 350

A search endpoint reveals nothing but true/false timing. Extract the seed one character at a time with a boolean/time-based blind injection, then Fernet-decrypt your flag blob.

## Run it

```bash
docker build -t sparflag/blind-sqli .
# `deca-ai start blind-sqli` (or the web UI) prints the docker run line with your
# SPARFLAG_SERVER + SPARFLAG_INSTANCE_TOKEN
```

## Recover the flag

The delivery blob is Fernet ciphertext. Discover the key seed, derive the Fernet key, then decrypt.

The plaintext flag is never written to disk or served — only the encoded delivery blob
is. When you have it:

```bash
deca-ai submit blind-sqli 'sparflag{...}'
```

## Hints

- The page looks identical — but does it behave identically?
- Use SUBSTRING() and ASCII() comparisons to test one character at a time.
- Binary-search each byte of the seed via true/false (or time) responses.
