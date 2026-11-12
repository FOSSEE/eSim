# eSim 2.6 macOS migration status

The `installers` branch contains an older PyQt5-based macOS packaging flow.
The eSim 2.6 work used a separate source tree and was qualified as a supervised
development GUI. It has not produced an eSim 2.6 installer.

| Area | Development findings |
| --- | --- |
| Source and state | The resource and state-path prototype separated shipped resources from writable per-session data. Managed project paths and optional-feature boundaries were reviewed against the 2.6 source. These changes span application modules and require an upstream 2.6 source baseline for review. |
| Qt runtime | The isolated ARM64 GUI shell was exercised with Python 3.11.18, PyQt6 6.11.0, Qt 6.11.2 and PyQt6-sip 13.13.0. These are historical qualification versions. |
| macOS menus | With native menus enabled, dropdowns did not open during the controlled eSim retest. A development-only adapter selected an in-window menu bar. All five menus opened in a later supervised session, restricted actions stayed disabled, and the application exited normally. The original cursor crash did not recur in that session. Native menu behavior remains unresolved. |
| Projects | The first controlled project run stopped during workspace initialization before creating or opening a project. A narrower permission for the workspace writability probe passed synthetic verification. Project creation, save, close and reopen still need end-to-end qualification. |
| Native tools | KiCad, ngspice, HDL and converter integrations remained disabled in the qualified GUI session. Their macOS runtime behavior is unqualified. |
| Distribution | Earlier installer hardening used an existing eSim 2.5 payload. Integrity checks on an unsigned candidate establish neither installation acceptance nor a signed or notarized release. |

A future application port should review the resource/state changes against the
chosen upstream 2.6 revision and keep the development-only isolation and
authorization controls separate from a release launch path. Before packaging,
review the exact runtime and native tool versions, supported macOS targets,
dependency licenses and redistribution terms. Preserve the upstream license and
notices for any imported application source.
