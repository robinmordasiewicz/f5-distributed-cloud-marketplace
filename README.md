# F5 Distributed Cloud Plugin Marketplace

[![Validate Marketplace](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/validate.yml)
[![Release](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/release.yml/badge.svg)](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A curated collection of Claude Code plugins for automating F5 Distributed Cloud (XC) operations.

## Quick Start

```bash
# 1. Add this marketplace (one time)
/plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace

# 2. Install a plugin
/plugin install f5xc-chrome

# 3. Use the commands
/xc:console login https://your-tenant.console.ves.volterra.io
```

## Prerequisites

1. **Claude Code** - [Install Claude Code](https://claude.com/claude-code)
2. **Claude in Chrome Extension** - Install from Chrome Web Store (for browser automation plugins)

## Available Plugins

| Plugin | Commands | Description |
|--------|----------|-------------|
| [f5xc-chrome](https://github.com/robinmordasiewicz/f5xc-chrome) | `/xc:console` | Browser automation for F5 XC console |

## Plugin Details

### f5xc-chrome

Automate F5 Distributed Cloud web console operations through Chrome browser.

**Commands:**
- `/xc:console login <url>` - Authenticate via Azure SSO
- `/xc:console crawl <url>` - Extract navigation metadata
- `/xc:console nav <target>` - Navigate to workspace/page
- `/xc:console create <type>` - Create resources (HTTP LB, Origin Pool, etc.)

**Requirements:**
- Claude in Chrome browser extension
- Azure AD credentials with F5 XC tenant access

## Installation Options

### Option 1: Marketplace (Recommended)
```bash
# Add marketplace
/plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace

# Browse available plugins
/plugin

# Install specific plugin
/plugin install f5xc-chrome
```

### Option 2: Direct GitHub Install
```bash
/plugin install robinmordasiewicz/f5xc-chrome
```

## Future Plugins

| Plugin | Commands | Purpose | Status |
|--------|----------|---------|--------|
| f5xc-chrome | `/xc:console` | Console automation | Available |
| f5xc-cli | `/xc:cli` | CLI operations | Planned |
| f5xc-terraform | `/xc:tf` | Infrastructure as Code | Planned |
| f5xc-docs | `/xc:docs` | Documentation lookup | Planned |
| f5xc-api | `/xc:api` | Direct API access | Planned |

## Contributing

We welcome contributions! To add a plugin to this marketplace:

### Adding a New Plugin

1. **Create your plugin** with a valid `.claude-plugin/plugin.json`
2. **Fork this repository**
3. **Add your plugin** to `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "your-plugin-name",
     "description": "What your plugin does",
     "version": "1.0.0",
     "author": {
       "name": "Your Name",
       "url": "https://github.com/yourusername"
     },
     "source": {
       "source": "github",
       "repo": "yourusername/your-plugin-repo"
     },
     "category": "automation",
     "tags": ["f5", "xc", "your-tags"]
   }
   ```
4. **Submit a Pull Request** with a description of your plugin

### Plugin Requirements

- Must have a valid `.claude-plugin/plugin.json` in your plugin repository
- Must follow Claude Code plugin standards
- Should include documentation in your plugin's README
- Source repository must be publicly accessible

### Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features (triggers minor version bump)
- `fix:` - Bug fixes (triggers patch version bump)
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks

## Troubleshooting

### Marketplace not found
```bash
# Verify the marketplace is added
/plugin marketplace list

# Re-add if necessary
/plugin marketplace remove f5-distributed-cloud
/plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace
```

### Plugin installation fails
```bash
# Check if the plugin source is accessible
# Visit: https://github.com/robinmordasiewicz/f5xc-chrome

# Try direct installation
/plugin install robinmordasiewicz/f5xc-chrome
```

### Commands not appearing
```bash
# Restart Claude Code after plugin installation
# Verify plugin is enabled
/plugin list
```

## License

MIT License - see [LICENSE](LICENSE) for details.

Individual plugins may have their own licenses - check each plugin's repository.

## Author

Robin Mordasiewicz - [GitHub](https://github.com/robinmordasiewicz)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.
