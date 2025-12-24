# F5 Distributed Cloud Plugin Marketplace

[![Validate Marketplace](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/validate.yml)
[![Release](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/release.yml/badge.svg)](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/release.yml)
[![Documentation](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/docs.yml/badge.svg)](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/actions/workflows/docs.yml)
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

## Documentation

**[View Full Documentation](https://robinmordasiewicz.github.io/f5-distributed-cloud-marketplace/)**

- [Getting Started](https://robinmordasiewicz.github.io/f5-distributed-cloud-marketplace/getting-started/)
- [Available Plugins](https://robinmordasiewicz.github.io/f5-distributed-cloud-marketplace/plugins/)
- [Contributing](https://robinmordasiewicz.github.io/f5-distributed-cloud-marketplace/contributing/)
- [Troubleshooting](https://robinmordasiewicz.github.io/f5-distributed-cloud-marketplace/troubleshooting/)

## Available Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| [f5xc-chrome](https://github.com/robinmordasiewicz/f5xc-chrome) | Browser automation for F5 XC console | Available |

## Prerequisites

1. **Claude Code** - [Install Claude Code](https://claude.com/claude-code)
2. **Claude in Chrome Extension** - Required for browser automation plugins

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Robin Mordasiewicz - [GitHub](https://github.com/robinmordasiewicz)
