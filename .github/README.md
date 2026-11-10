# Manual source maintenance and Build

These are independent decisions. Neither workflow dispatches the other.

* **Bump version**: select a branch with the built-in ref selector and choose the
  required `mode` (`patch`, `minor`, or `major`; default `patch`). It validates the
  immutable dispatch SHA and exact remote branch, creates one nonempty direct
  child containing only version-source changes, and pushes only that branch.
  Tags, builds, releases, and dispatches are never part of Bump.
* **Build**: select a ref with the built-in selector. There are **no custom
  inputs**. Every checkout uses `github.sha`, not a moving branch or typed tag.
  Build derives the canonical `X.Y.Z` from source and publishes `vX.Y.Z` only if
  the tag and any draft/public release are absent. Leading zeroes and suffixes
  are rejected. There is no newly imposed default-branch-only restriction.

Publication concurrency is the constant repository-wide `release-publication`
group with cancellation disabled, including across selected refs. GitHub does
not promise FIFO ordering of pending runs.

## Version authority and intake repair

Intake is `ab1cf80dbb9d3c491677e36f2ba1aa5754117fd8` on `master`.
The original Bump at `4d4472dd4d2584d365b549e705165382623f7d8c` explicitly
coordinates `MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`, and plist version
keys, although its body incorrectly updates marketing alone.

The existing marketing authority remains **1.1.3**: all six stale source build
versions (1.1.0) and the two copied English display tokens (1.0.5) are aligned
to it. This is not a version increment. The six target/project configuration
identities and Development/Deployment/Default names are validated. Source
`Info.plist` retains `$(MARKETING_VERSION)` and the absence of `CFBundleVersion`.
Prebuilt/destination metadata, including stale UTF-16 localization, is untouched.

The only Bump-eligible sources are:

```
Bonjour.xcodeproj/project.pbxproj
Info.plist
English.lproj/InfoPlist.strings
```

In the current reference-based plist model, a canonical Bump actually changes
only the project and source localization. References, optional build-key absence,
encodings/BOMs, individual line endings, modes, and unrelated bytes are preserved.
Duplicate assignments (including quoted, inline, or replacing missing
assignments), unresolved/cyclic references, topology drift, and invalid metadata
fail before writes.

The CLI invocation used by Actions is:

```
python3 .github/scripts/bump.py patch --sha FULL_SELECTED_SHA --ref refs/heads/BRANCH
```

It works detached without ambient Git identity; both identities are explicit
Actions bot identities. Commits end with the literal Copilot App co-author
trailer. The committed `100755` pre-push hook is mandatory: its raw bytes, mode,
and nonsymlink executable type are rechecked every time, including immediately
after the final remote read. The hook validates the actual single advertisement,
selected old SHA, literal new SHA/HEAD, single parent, and source-only change set.
All pushes set both `push.followTags=false` and `--no-follow-tags`. Races stop
without force, amend, automatic retry, or rollback; inspect any retained local
child and the remote branch before a new deliberate run.

## Native policy and narrow retained outputs

The actual topology is an Ubuntu version job plus a macOS native job, **not**
a Windows build. The macOS command retains target `Bonjour`, configuration
`Default`, deployment override **11.0** (project 11.5), `arm64 x86_64`, and
`ONLY_ACTIVE_ARCH=NO`. There is no output-directory or signing-setting override.
The project signing phase remains untouched and acts only for Deployment.
Static `a/libjsoncpp.a`, all source/runtime/4D inputs, and the tracked Windows
and Windows64 `Bonjour.4DX` payloads are preserved. No dependencies are cloned,
no gitlinks are introduced, and no Windows/autocrlf exception is needed.

Original successful hosted run **36969725098**, job **110721005177**, native
step **5** at the intake SHA proves Default OBJROOT is **test/Plugins**, not
`build`. The credential-free log SHA-256 is
`e42b147a89370a8a79f75c8c9d8b8495c107768cafa680ca26e195e36ee4f8fe`.
Only `test/Plugins/Bonjour.build/` descendants and
`test/Plugins/XCBuildData/build.db`, `build.db-wal`, `build.db-shm`, and
32-lowercase-hex `.xcbuilddata/` descendants are final intermediate exemptions.
Observed empty module/cache/Default directories permit **no arbitrary files**.
Selected/indexed source under intermediate roots remains protected.

Cleanup deletes only the six named generated bundle leaves and
`test/Plugins/Bonjour.build`. It never deletes XCBuildData, whole bundles,
resources outside the exact copied leaves, Default siblings, prebuilt Windows,
or Thumbnail.png. Before its first deletion it validates **all** targets,
ancestors, descendants, regular/directory types, readability, links, nested Git
markers, and selected/indexed inputs. An invalid late target leaves earlier
bytes intact.
Every traversed directory below the legitimate checkout root is probed with
`lstat` for a `.git` marker, including ancestors outside the output subtree.
Any marker type (including directories, dangling links, and FIFOs) is rejected;
only actual ENOENT means absence. Permission, EIO, and ENOTDIR failures abort
before the first deletion. The checkout root's own Git metadata is not treated
as a nested repository.
Every enclosing directory must also have read **and** search permission bits
and pass `os.access(R_OK | X_OK)` before its marker probe. This includes
`test/`, `test/Plugins`, and late bundle-leaf parents, not just output subtrees
or immediate deletion parents. Search-only ancestors must not permit cleanup
to delete outputs before a later native failure. Each permission/marker/error
regression restores the same fixture and proves a fresh native positive after
that individual negative, retaining all generated-leaf snapshots on rejection.

Preflight requires a globally clean checkout, including ignored unexpected
files. Final validation instead retains freshly overwritten **tracked**
executable/plist/localization/signature and copied resources. It separately
checks immutable HEAD, exact index modes/blobs, both `git ls-files -v` **and**
`-f`, and raw nongenerated bytes. It never resets outputs to fake cleanliness.
All nine packaged leaves must be nonempty regular nonsymlink files at final
publication; pre-sign verification deliberately does not require the signature.
Copied constants/manifest must match source exactly; both Windows payloads and
Thumbnail.png must match the selected raw blobs/modes. XML/binary built plist
and compiled or text localization must match source authority.

Developer ID keychain import, notary profile, runtime signing, strict/deep
verification, ZIP/DMG policy, and stapling are preserved. Architecture checks
require exact arm64 and x86_64 tokens, permit extras as before, and do not invent
a runtime dylib architecture policy. Both notarytool exit success **and** strict
JSON `Accepted` are required for each artifact; staple and final strict signing
verification must also succeed.

## Create-only publication and manual recovery

Both early (before credentials/native) and final (after all signing, notary, and
stapling) gates require explicit nonempty `GH_TOKEN`, exact API-canonical
`miyako/4d-plugin-apple-bonjour`, selected `GITHUB_SHA`, and tag availability.
They read draft-inclusive release pages **until an empty page**, exact matching
API refs, and `ls-remote`. Authentication/404/network/later-page failures,
duplicate JSON keys, nonfinite numbers, malformed schema, or existing tags,
including same-SHA races, abort.

Publication uses separate create-only operations: POST tag ref at selected SHA;
verify exact API ref and remote advertisement; POST one new public release;
upload exact `Bonjour-VERSION.zip` and `Bonjour-VERSION.dmg` only to its new
positive integer ID, never a previously listed ID. Responses must match
asset names, integer sizes, and uploaded state. Original release notes policy
is preserved: empty body, generated notes disabled.

**Failure retains partial state.** There is no automatic DELETE, PATCH,
clobber/update, reuse, retry, or rollback. The diagnostic records confirmed or
possibly created tag/release ID/assets. A maintainer must inspect that state
and deliberately decide recovery before any later run; rerunning the same
version is not a repair mechanism. Neither tests nor migration authorizes
production ref/release/asset mutation or Actions dispatch.

## Offline validation

With Python 3, PyYAML (`tests/requirements.txt`), and actionlint available:

```
PYTHONDONTWRITEBYTECODE=1 python3 tests/run_offline.py
actionlint .github/workflows/*.yml
```

The runner discovers the full suite and fails on **any skip**. It uses only
disposable local Git/bare fixtures and closed-PATH native/credential/API stubs.
It executes the actual workflow Bash and actual helpers/hooks; no real native,
4D, signing, keychain, notarization, or GitHub API calls are made. Fixtures are
created under `tests/.helper-*` and removed after each test. Original fixtures
are pinned to intake; live expectations derive from selected source, allowing
the entire suite to run on a genuinely bumped child.
The native entrypoint disables bytecode before local imports: correctness does
not depend on workflow or harness `PYTHONDONTWRITEBYTECODE` or `python -B`.
Regressions explicitly omit both protections while running metadata and extracted
native phases, then execute real final publication against fake gh with exact
retained-byte assertions. Caches are neither exempted nor deleted to pass guards.

Reference adaptations are from hash-verified immutable UTI
`5decf4be07f8297d256dfb559ef9466525fe9045` and libarchive
`9547d09522fc422ddd754fb088165b3d1d1d3073` helpers, carrying the mandatory
shell-execute-v2 hook-integrity fix. The separately completed all-16-pin
dedicated reading gate is not a claim that native services or these target
changes have been proven hosted. Final exact-commit and detached/no-identity
genuine-Bump dual proofs, publication review, and any production actions belong
to the coordinator.
