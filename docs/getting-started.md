# Getting Started

This guide walks you through installing and using plugins from the F5 Distributed Cloud marketplace.

## Prerequisites

### 1. Install Claude Code

Claude Code is Anthropic's official CLI for AI-powered software engineering.

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code
```

Or visit [claude.com/claude-code](https://claude.com/claude-code) for installation instructions.

### 2. Install Claude in Chrome Extension

For browser automation plugins (like `f5xc-chrome`), you need the Claude in Chrome extension:

1. Open Chrome Web Store
2. Search for "Claude in Chrome"
3. Click "Add to Chrome"
4. Grant necessary permissions

## Adding the Marketplace

Add this marketplace to your Claude Code installation:

=== "Interactive"

    ```
    /plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace
    ```

=== "CLI"

    ```bash
    claude plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace
    ```

Verify the marketplace is added:

```text
/plugin marketplace list
```

## Installing Plugins

### Browse Available Plugins

```text
/plugin
```

This shows all plugins from configured marketplaces.

### Install a Specific Plugin

=== "From Marketplace"

    ```
    /plugin install f5xc-chrome
    ```

=== "Direct from GitHub"

    ```
    /plugin install robinmordasiewicz/f5xc-chrome
    ```

### Verify Installation

```text
/plugin list
```

## Using Plugins

### f5xc-chrome Plugin

The `f5xc-chrome` plugin provides browser automation for the F5 XC console.

#### Login to F5 XC Console

```text
/xc:console login https://your-tenant.console.ves.volterra.io
```

This initiates Azure SSO authentication and logs you into the console.

#### Navigate to a Workspace

```text
/xc:console nav "Web App & API Protection"
```

#### Crawl Navigation Metadata

```text
/xc:console crawl https://your-tenant.console.ves.volterra.io
```

Extracts navigation structure for intelligent command routing.

#### Create Resources

```text
/xc:console create http-lb
```

Guides you through creating an HTTP Load Balancer.

## Best Practices

### Authentication

!!! warning "Credential Security"
    Never hardcode credentials in scripts. Use Azure AD SSO for authentication.

### Session Management

The browser automation maintains session state. For long-running operations:

1. Verify you're logged in before starting
2. Handle session timeouts gracefully
3. Use `/xc:console login` to re-authenticate if needed

### Error Handling

If a command fails:

1. Check the browser console for errors
2. Verify network connectivity
3. Ensure you have proper permissions in F5 XC

## Next Steps

- Explore [Plugin Documentation](plugins/index.md)
- Check the [Roadmap](roadmap.md) for upcoming features
- Learn how to [Contribute](contributing.md)
