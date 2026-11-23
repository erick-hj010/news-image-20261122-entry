# Verifying byte-identical double runs

`main.py` copies a fixed image, so two runs in a clean directory must
produce exactly the same bytes as each other and as the bundled
`entry_src.png`.

## Commands

```sh
mkdir -p /tmp/verify-run1 /tmp/verify-run2
OUTPUT_PATH=/tmp/verify-run1/entry.png python3 main.py
OUTPUT_PATH=/tmp/verify-run2/entry.png python3 main.py
sha256sum entry_src.png /tmp/verify-run1/entry.png /tmp/verify-run2/entry.png
```

## Expected result

All three SHA-256 digests are identical:

```
848e56a00be08cc59caceb11831ebc39be03e18d935be4b9dc3aa3a25744b526
```

The image is 1024×1024 PNG, 190,397 bytes (under the 1 MiB limit).
