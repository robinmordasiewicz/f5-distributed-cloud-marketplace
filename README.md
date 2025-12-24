# F5 Distributed Cloud Plugin Marketplace

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

To add a plugin to this marketplace:

1. Create your plugin repository with `.claude-plugin/plugin.json`
2. Open an issue or PR to add it to this marketplace

## License

MIT License - see individual plugin repositories for their licenses.

## Author

Robin Mordasiewicz - [GitHub](https://github.com/robinmordasiewicz)
