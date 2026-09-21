# Changelog

## [1.0.1] - 2026-09-22

### Added

- MIT License.
- Public repository metadata.
## [1.0.0] - 2026-09-21

### Added

- Versioned skill metadata.
- Workspace audit script with secret and large-file checks.
- Non-overwriting workspace initializer with English and Chinese templates.
- Workspace specification and decision-record references.
- README, usage guidance, validation commands, and Git ignore rules.

### Fixed

- Avoid false positives for standard CA certificate files such as `cacert.pem`.
- Emit ASCII-safe JSON for reliable PowerShell decoding of non-ASCII paths.