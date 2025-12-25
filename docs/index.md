# F5 Distributed Cloud Plugin Marketplace

Welcome to the official plugin marketplace for automating F5 Distributed Cloud (XC) operations with Claude Code.

## What is this Marketplace?

This marketplace provides a curated collection of Claude Code plugins designed specifically for
network engineers, DevOps teams, and platform engineers working with F5 Distributed Cloud.

!!! tip "Quick Start"
    ```bash
    # Add this marketplace to Claude Code
    /plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace

    # Install a plugin
    /plugin install f5xc-chrome
    ```

## Key Features

<div class="grid cards" markdown>

- :material-lightning-bolt:{ .lg .middle } __Automation First__

    ---

    Automate repetitive F5 XC console tasks with intelligent browser automation and API integration.

- :material-puzzle:{ .lg .middle } __Modular Design__

    ---

    Install only the plugins you need. Each plugin is independently versioned and maintained.

- :material-security:{ .lg .middle } __Enterprise Ready__

    ---

    Built with security in mind, supporting Azure AD SSO and enterprise authentication flows.

- :material-source-repository:{ .lg .middle } __Open Source__

    ---

    MIT licensed and community-driven. Contributions welcome!

</div>

## Available Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| [f5xc-chrome](plugins/f5xc-chrome.md) | Browser automation for F5 XC console | :material-check-circle:{ .green } Available |
| f5xc-cli | CLI operations and scripting | :material-clock-outline: Planned |
| f5xc-terraform | Infrastructure as Code integration | :material-clock-outline: Planned |
| f5xc-docs | Documentation and API lookup | :material-clock-outline: Planned |

## Why Use This Marketplace?

### Streamlined Workflow

Instead of manually navigating the F5 XC console, use natural language commands to:

- Create and configure HTTP load balancers
- Manage origin pools and health checks
- Deploy WAF policies
- Navigate complex multi-tenant environments

### AI-Powered Assistance

Claude Code understands your intent and translates it into precise console actions:

```text
You: "Create an HTTP load balancer for my API with WAF protection"
Claude: Navigates to the correct namespace, creates the LB, configures origins,
        attaches WAF policy, and validates the configuration.
```

### Consistent Operations

Reduce human error with repeatable, auditable automation sequences that follow best practices.

## Prerequisites

Before using plugins from this marketplace:

1. __Claude Code__ - [Install Claude Code](https://claude.com/claude-code)
2. __Claude in Chrome Extension__ - Required for browser automation plugins

## Getting Help

- :material-book-open-outline: [Getting Started Guide](getting-started.md)
- :material-lifebuoy: [Troubleshooting](troubleshooting.md)
- :material-github: [GitHub Issues](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues)

## License

This marketplace and its plugins are released under the [MIT License](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/blob/main/LICENSE).
