# Pinned eSim 2.6 source staging

This is a source-integrity milestone. It reads an already available local Git
object database and writes two independent source copies in a new private staging
run. It never imports source modules, checks out files, fetches, applies patches,
initializes submodules, builds or runs eSim, or executes installer hooks.

## Source contract

The production revision is fixed in source_stage.py to
`d86c1891b4e1aced7ce84b910d6fba17025bd87c`. There is no CLI revision override.
The caller must supply a trusted local SHA-1 Git repository containing that
commit and all referenced supported objects. A normal repository with a real
.git directory or a bare repository is accepted; linked worktree .git files and
symlinked repository paths are outside this implementation's contract.

The object reader invokes only the selected local Git's cat-file --batch command.
Its environment excludes caller Git overrides and disables replacement objects,
optional locks, terminal prompting and lazy fetching. It bypasses checkout,
smudge filters, export-ignore and source hooks. Git and its object database are
trusted local inputs. Source acquisition is a separate step.

The reader independently recalculates each commit/tree/blob Git object ID. The
commit supplies the root tree. Tree inventory is traversed directly, with bounded
object size, path depth and entry count. It rejects traversal, .git components,
control characters, colon/backslash names, trailing dots/spaces, duplicate names,
and case or Unicode-normalization collisions. Only modes 40000, 100644 and
100755 are accepted. Symlinks and gitlinks are refused; no entries are silently
omitted, renamed, dereferenced or initialized.

For each file the manifest stores its path, Git mode/blob ID, byte size and
SHA-256 digest. It also stores the raw commit in hex and root tree ID. Rechecking
reconstructs all directory tree objects and binds the complete file inventory
back to the pinned commit. Rehashing a locally edited manifest cannot authorize
an omitted file or a replacement source revision. This uses the existing Git
SHA-1 identity anchor and adds SHA-256 file/delivery checks. It does not provide
a new publisher signature or independently prove repository custody.

## Output and preservation

Output is fixed relative to this module, independent of shell CWD:

    MacOS/.migration-work/source-staging/<pinned-revision>/<run-id>/
        pristine-source/
        candidate-source/
        manifest.json
        COMPLETE.json

Run IDs are single 1–64 character ASCII leaves using letters, digits, underscore
and hyphen, starting with a letter or digit. No arbitrary output-directory CLI
exists. Existing runs, including incomplete/failed runs, cannot be reused. The
staging base and run directories must be user-owned mode 0700 with trusted
non-symlinked ancestors. Unsafe existing directories cause refusal.

All objects are checked before run allocation. The new run is allocated with an
exclusive mkdir. Source files are created exclusively with O_NOFOLLOW and preserve
Git's executable/regular permission distinction. Candidate and pristine files
have independent inodes, not hard links to each other or the source. Directory
permissions remain 0700. Existing MacOS/src is never an output target.

The two copies are identical in this milestone; candidate patch application is
future work. Pristine is a role, not OS-enforced immutability: keep it private
and always reverify it before consumption. Changing either copy invalidates the
current verifier. Future patch support needs a separate reviewed post-patch
manifest and cannot simply rewrite the pinned baseline contract.

Both trees are verified before COMPLETE.json is published, and the source object
reader must exit successfully first. Completion records bind the manifest digest
and verified revision/tree/file count. A run with no completion, a FAILED.json
record, unexpected entries, changed bytes/modes, links, missing files or a corrupt
manifest/completion record is refused. A failure during copying retains the
partial run plus a minimal failure record when that can be safely written.
Source-reader or completion-publication failures can leave an incomplete run
without a failure record; absence of verified completion still makes it unusable.
No recursive cleanup API exists. Inspect failed outputs and remove only the
owned disposable run through a separately reviewed cleanup step.

Manifest and completion bytes are deterministic for identical supported input.
They contain no machine-specific paths, timestamps or run IDs. Filesystem inode
numbers/timestamps are not reproducibility claims. Resource limits are 128 MiB
per Git object, 2 GiB of staged file content per tree, 50,000 entries and 64 nested
tree levels. Two copies plus verification require substantial disk space.

## Future usage

These examples document future execution. No real eSim source was staged during
this milestone. Run from the integration repository root with Python 3.9+ on
macOS/POSIX and a trusted Git installation on PATH:

```sh
python3 -B -m MacOS.source_stage \
  --source-repository /path/to/trusted/local/esim-repository \
  --run-id review-01
```

To recheck the exact two unchanged trees:

```sh
python3 -B -m MacOS.source_stage --verify --run-id review-01
```

The command reports VERIFIED_SOURCE_ONLY and returns 0 only after full checking.
A refusal returns 1. Neither status authorizes application, GUI, simulation,
package-build or installer execution. The module has no relationship to the
historical development launch authorization records and changes none of them.

## Known blockers for the pinned upstream revision

Read-only inspection of the official recursive Git-tree metadata found:

- Case-colliding directories such as library/SubcircuitLibrary versus
  library/subcircuitLibrary, plus MC1496 versus mc1496 inside the capitalized tree.
- Two gitlinks at library/SubcircuitLibrary/esim_ic_files/sn54ls48/eSim and
  library/SubcircuitLibrary/sn54ls48/eSim, both referencing
  de13d725c1ffd3e0754b22c0070c0a8be8b829e3.

The conservative first implementation refuses these entries on every platform,
including case-sensitive filesystems. It therefore cannot yet materialize the
complete pinned upstream tree. No automatic exclusion or collision remapping was
introduced. Real-source staging is NO-GO until the mentor reviews a canonical
resource selection/submodule policy or an approved upstream correction. A later
policy must enumerate every omitted or transformed path and preserve its
upstream provenance. It must not silently claim a reduced snapshot is the whole
commit. The current integration clone also lacks the target application commit's
objects; supplying them is a separate explicit local-input/acquisition step.

The metadata inspection above is an upstream-readiness finding, not validation
of the full local Git transport or a real staged snapshot. The Git subprocess
transport is mocked in the tests. No upstream object database was downloaded or
checked out by this implementation.

## Synthetic verification

Reviewed tests use only standard-library code, temporary fixtures under the
integration clone's ignored .migration-work directory and an in-memory cat-file
protocol. Commit-shaped bytes are synthetic fixtures; no Git commit or branch is
created. No real Git subprocess, app module, installer, simulator or dependency
installation runs in the tests. Fixtures include source files that would raise
if executed; they remain inert data. Cleanup removes each test's own temporary
fixture tree and leaves the empty ignored fixture parent.

Coverage includes reproducibility, export-ignored developer file inclusion,
independent copies/modes, existing source preservation, exclusive and competing
run allocation, bad source hashes/types/missing objects, bounded input, malformed
Git/JSON, duplicate/case/Unicode names, link/submodule refusal, unsafe output
parents/ownership, write failure, partial-run refusal, manifest omission, candidate
and pristine tampering, hard links, and default CLI refusal/status handling.

Commands actually run after reviewing the test code:

```sh
python3 -B -m unittest discover -s MacOS/tests -p 'test_source_stage.py' -v
TMPDIR="$PWD/MacOS/.migration-work" python3 -B -m unittest discover -s MacOS/tests -v
```

The initial focused version passed 23 tests. After hardening JSON and destination
preflight checks, final full discovery passed **61 tests in 0.228 seconds**, zero
failures/errors/skips, comprising **27 new staging tests and 34 existing synthetic
configuration tests**. Python 3.9 grammar parsing passed for the new module/tests.
This is synthetic verification only. Native Git transport, real upstream staging,
application runtime and packaging are still unqualified.

## Security assumptions

The private root and no-overwrite checks protect against accidental destination
reuse and ordinary redirection. They are not an OS sandbox or a complete defense
against a hostile process running as the same user/root or every concurrent
ancestor replacement. Trusted workspace custody and Git installation are required.
The existing pinned commit is the trust anchor; mutable refs or caller-supplied
hashes cannot replace it through this CLI.

Reads of the local Git process are bounded in size but have no per-object wall
clock deadline; a hung or broken trusted Git can require manual interruption.
The reader has a bounded shutdown wait and kills only its own child on shutdown
timeout. Forced termination can leave a partial run; reuse is still refused.
Filesystem-specific behavior and non-POSIX platforms are not certified. Future
native tool execution and distribution trust need independent qualification.
