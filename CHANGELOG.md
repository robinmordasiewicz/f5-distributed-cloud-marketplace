# Changelog

All notable changes to this marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2025-12-25

### Added

- **Enhanced documentation styling**: Modern visual design with F5 branding
  - Hero section with gradient background and animated glow effects
  - CSS design tokens for consistent theming
  - Enhanced feature cards with hover animations
  - Improved table styling with gradient headers
  - Stats grid component for metrics display
  - Announcement bar capability in overrides
- **Typography improvements**: Switched to Inter and JetBrains Mono fonts
- **Abbreviations glossary**: Auto-expanding technical terms (F5 XC, WAF, etc.)
- **SVG branding assets**: Custom logo and favicon with F5 gradient colors
- **Admonition customizations**: Custom icons and styled borders for all types
- add enhanced metadata and sophisticated structure (#24)
- update f5xc-console to v0.13.0 (#25)

### Changed

- Redesigned landing page with hero banner and stats section
- Updated color scheme to use F5 brand red (#E4002B) and orange (#FF6B4A)
- Enhanced navigation with sticky tabs and instant loading progress
- Improved code blocks with auto-titles and better copy button

## [3.1.0] - 2025-12-25

### Added

- **Agents directory**: Added intelligent orchestration agents
  - `xc-architect.md` - F5 XC architecture advisor for design decisions
  - `xc-troubleshooter.md` - Diagnostic agent for debugging issues
- **MCP configuration**: Added `.mcp.json` with explicit claude-in-chrome dependency
- **Enhanced marketplace metadata**: Added `metadata` block with pluginRoot, categories, keywords
- **Hooks infrastructure**: Added `hooks/hooks.json` for lifecycle automation
- **Testing infrastructure**: Added `tests/` directory with workflow tests and fixtures
- **Auto-merge for plugin-sync**: PRs now auto-merge after CI passes (#22)

### Changed

- Bumped marketplace version to 3.1.0
- Enhanced plugin discoverability with metadata block

## [3.0.1] - 2025-12-25

### Fixed

- merge duplicate changelog entries
- use PR instead of direct push for plugin-sync

## [3.0.0] - 2025-12-25

### Added

- **npm registry integration**: Plugins can now be sourced from npm registry
- Added `npm-info` command to plugin-manager.sh for fetching npm package metadata
- Added `schemas/plugins.schema.json` with npm source support
- Support for npm integrity hash (sha512) verification
- NPM_TOKEN environment variable support for private packages
- Scoped package support (@org/package format)
- **Automated plugin sync**: New workflow for automatic version updates
- Added `plugin-sync.yml` workflow with repository_dispatch support
- Added `sync-npm-plugins.sh` script for fetching latest versions
- Scheduled sync every 6 hours as fallback
- Documentation for webhook dispatch setup

### Changed

- **BREAKING**: Renamed plugin from `f5xc-chrome` to `f5xc-console`
- Plugin source changed from GitHub tarballs to npm registry
- Plugin now published as `@robinmordasiewicz/f5xc-console` on npmjs.org
- Updated plugin-manager.sh with source type routing (github/npm)
- Enhanced `list` command to show source type for each plugin

### Migration Guide

To migrate from 2.x to 3.0:

```bash
# Remove old plugin installation
rm -rf plugins/f5xc-chrome

# Install new npm-based plugin
./scripts/plugin-manager.sh install f5xc-console
```

### Webhook Setup for Plugin Repos

Add to your plugin's release workflow:

```yaml
- name: Notify marketplace
  uses: peter-evans/repository-dispatch@v3
  with:
    token: ${{ secrets.MARKETPLACE_DISPATCH_TOKEN }}
    repository: robinmordasiewicz/f5-distributed-cloud-marketplace
    event-type: plugin-release
    client-payload: '{"plugin": "f5xc-console", "version": "${{ env.VERSION }}"}'
```

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
