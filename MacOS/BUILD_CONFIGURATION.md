# Draft macOS build configuration

This optional developer tool reviews proposed Apple Silicon build inputs. The
legacy packaging workflow documented in [INSTALL](INSTALL) has no dependency on
this tool. The validator does not launch eSim, download or install dependencies,
write metadata, run native tools, or build, sign or notarize anything.

## Review inputs

- `build_config/release.schema.json` defines the proposed version, build number,
  application and package identifiers, deployment target and source digest.
- `build_config/dependencies.schema.json` defines the declared toolchain and
  dependency graph with exact versions, cache filenames, HTTPS origins and
  SHA-256 digests. Native inputs have an explicit minimum OS.
- `build_config/authorization.schema.json` defines a configuration-review
  record tied to the raw bytes of the release and dependency files.
- The two `*.proposed.json` templates are intentionally incomplete and fail
  validation as checked in. ARM64 and macOS 26.0 are draft scope values.

The validator uses the Python 3.9+ standard library on macOS and implements
only the JSON Schema keywords used in its v1 schemas. It checks the declared
dependency graph, platform and Python wheel tags and optional cache hashes.
It rejects universal2 wheels under the current draft policy. This policy needs
review before using the separate Qt6 development environment for packaging.

Keep filled-in drafts, actual review records and acquired inputs in a private
location such as the ignored `MacOS/.local-review/` directory. For completed
draft inputs, the command from the repository root is:

```sh
python3 -B -m MacOS.build_config_validate \
  --release MacOS/.local-review/release.json \
  --lock MacOS/.local-review/dependencies.json --check-draft
```

A valid draft returns `STRUCTURALLY_VALID_UNAPPROVED`. Without
`--check-draft`, a matching `--authorization` review record is required.
Digest matching binds that record to the input bytes. FOSSEE must establish the
record's authenticity and reviewer authority separately. Both successful modes
return `build_authorized: false`. A rejected input returns exit status 2.

Optional `--cache` hashes already acquired files in a flat directory.
Optional `--metadata-preview` compares an existing JSON preview with the
version and identifier mapping. These checks assume trusted ancestor paths and
private workspace custody. Cache digests and wheel filenames do not establish
artifact authenticity, binary compatibility or redistribution rights.

## Tests

The focused suite uses temporary synthetic manifests and cache fixtures. Run
it from the repository root:

```sh
python3 -B -m unittest discover -s MacOS/tests -p 'test_build_config_validate.py' -v
```

Before build integration, review the release identifiers, deployment target,
source snapshot, actual dependency versions and licenses, build metadata, and
installer signing and notarization separately. The existing build scripts and
installer hooks are outside this proposal.
