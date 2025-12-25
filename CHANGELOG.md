# Changelog

All notable changes to this marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## [2.0.0] - 2025-12-25

### Changed

- **BREAKING**: Migrated from git submodules to registry-based plugin management
- Plugins are now downloaded from GitHub Releases instead of tracked as submodules
- Added `plugins.json` registry manifest for version management
- Added `scripts/plugin-manager.sh` for installing/updating plugins

### Added

- Plugin registry system with version pinning
- `plugin-manager.sh sync` command to install all plugins
- SHA256 checksums for tarball integrity (optional)
- Support for private and public plugin repositories

### Removed

- Git submodule dependency on f5xc-chrome
- `.gitmodules` file

### Migration Guide

To migrate from 1.x to 2.0:
```bash
# Remove old submodule if present
git submodule deinit -f plugins/f5xc-chrome

# Install plugins from registry
./scripts/plugin-manager.sh sync
```

## [1.1.2] - 2025-12-25

### Changed

- update f5xc-chrome submodule to v0.6.0 (#14)

## [1.1.1] - 2025-12-25

### Changed

- update f5xc-chrome submodule to v0.3.0 (#12)

## [1.1.0] - 2025-12-25

### Added

- update to v0.2.0 with multi-provider auth (#10)
- add comprehensive code quality enforcement
- add MkDocs Material documentation with dynamic plugin page generation
- align with Anthropic marketplace best practices

### Fixed

- use local path for plugin source instead of external GitHub
- Use peaceiris/actions-gh-pages for branch-based deployment
- Release workflow uses PR-based approach for branch protection compliance

### Changed

- update f5xc-chrome submodule for cleaner command path

## [1.0.0] - 2024-12-24

### Added

- Initial release of F5 Distributed Cloud plugin marketplace
- Added `f5xc-chrome` plugin for browser automation of F5 XC console
- Automated CI/CD release pipeline with conventional commits
- Marketplace validation workflow
