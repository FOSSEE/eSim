# eSim Debian packaging scaffold

This folder contains a ready-to-use Debian package template for eSim.

## What it does

- installs the application payload under `/opt/esim`
- adds a launcher at `/usr/bin/esim`
- adds a desktop entry for menu integration

## How to use

1. Put the eSim application files in a directory, for example `/path/to/esim-app`
2. Run:

```bash
chmod +x build-deb.sh
./build-deb.sh 1.0.0 amd64 /path/to/esim-app
```

3. The resulting package will be created as:

```text
esim_1.0.0_amd64.deb
```

## Notes

- Replace the version and architecture as needed.
- Update `DEBIAN/control` with the real runtime dependencies of your eSim build.
- If your app starts from a different executable, edit `usr/bin/esim`.
- If you have an icon, place it in the appropriate hicolor icon path before building.

This is a packaging scaffold because the eSim source tree was not available in this chat session.
