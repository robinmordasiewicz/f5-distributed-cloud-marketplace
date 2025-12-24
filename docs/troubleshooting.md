# Troubleshooting

Common issues and solutions for the F5 Distributed Cloud plugin marketplace.

## Installation Issues

### Marketplace Not Found

**Symptom:** Error when trying to install plugins from the marketplace.

**Solution:**

```bash
# Verify the marketplace is added
/plugin marketplace list

# Re-add if necessary
/plugin marketplace remove f5-distributed-cloud
/plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace
```

---

### Plugin Installation Fails

**Symptom:** Error during plugin installation.

**Possible Causes:**

1. Network connectivity issues
2. Plugin repository not accessible
3. Outdated Claude Code version

**Solutions:**

=== "Check Network"

    ```bash
    # Verify you can reach GitHub
    curl -I https://github.com/robinmordasiewicz/f5xc-chrome
    ```

=== "Direct Install"

    ```bash
    # Try direct installation instead of marketplace
    /plugin install robinmordasiewicz/f5xc-chrome
    ```

=== "Update Claude Code"

    ```bash
    npm update -g @anthropic-ai/claude-code
    ```

---

### Commands Not Appearing

**Symptom:** Plugin installed but commands not available.

**Solution:**

1. Restart Claude Code after plugin installation
2. Verify plugin is enabled:

```bash
/plugin list
```

---

## Browser Automation Issues

### Chrome Extension Not Connected

**Symptom:** Browser commands fail with connection errors.

**Solutions:**

1. Ensure Claude in Chrome extension is installed
2. Check extension is enabled in Chrome
3. Verify MCP connection in Claude Code settings

---

### Login Timeout

**Symptom:** `/xc:console login` times out before completing authentication.

**Possible Causes:**

- Slow network connection
- Azure AD authentication delays
- Browser popup blocked

**Solutions:**

1. Increase timeout in plugin settings
2. Check for blocked popups in Chrome
3. Manually complete authentication if needed

---

### Navigation Fails

**Symptom:** `/xc:console nav` cannot find the target page.

**Solutions:**

1. Run crawl to update navigation metadata:

```bash
/xc:console crawl https://your-tenant.console.ves.volterra.io
```

2. Verify you're logged into the correct tenant
3. Check that the target exists in your namespace

---

### Session Expired

**Symptom:** Commands fail after period of inactivity.

**Solution:**

Re-authenticate:

```bash
/xc:console login https://your-tenant.console.ves.volterra.io
```

---

## Configuration Issues

### Wrong Tenant

**Symptom:** Commands affect unexpected resources.

**Solution:**

1. Verify current session:

```bash
/xc:console status
```

2. Login to correct tenant:

```bash
/xc:console login https://correct-tenant.console.ves.volterra.io
```

---

### Namespace Mismatch

**Symptom:** Resources not found or created in wrong namespace.

**Solution:**

Navigate to correct namespace before creating resources:

```bash
/xc:console nav namespace my-namespace
```

---

## Performance Issues

### Slow Command Execution

**Symptom:** Commands take longer than expected.

**Possible Causes:**

- Large DOM in console
- Network latency
- Complex page rendering

**Solutions:**

1. Wait for page to fully load
2. Reduce concurrent operations
3. Use CLI plugin for batch operations (when available)

---

### Memory Usage

**Symptom:** Browser becomes unresponsive.

**Solutions:**

1. Close unnecessary browser tabs
2. Restart Chrome periodically during long sessions
3. Monitor Chrome memory in Task Manager

---

## Getting More Help

### Gather Diagnostic Information

When reporting issues, include:

1. **Claude Code Version:**
   ```bash
   claude --version
   ```

2. **Plugin Version:**
   ```bash
   /plugin list
   ```

3. **Chrome Version:** Check `chrome://version`

4. **Error Messages:** Full error text or screenshot

5. **Steps to Reproduce:** What commands led to the issue

### Report an Issue

1. Search [existing issues](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues)
2. If not found, [create a new issue](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues/new)
3. Use the bug report template
4. Include diagnostic information

### Community Support

- GitHub Discussions (coming soon)
- Stack Overflow tag: `f5-distributed-cloud`

## FAQ

??? question "Can I use this with multiple F5 XC tenants?"

    Yes, you can switch between tenants by logging in to different URLs:
    ```bash
    /xc:console login https://tenant1.console.ves.volterra.io
    # ... work on tenant 1 ...
    /xc:console login https://tenant2.console.ves.volterra.io
    # ... work on tenant 2 ...
    ```

??? question "Are my credentials stored?"

    No credentials are stored by the plugins. Authentication is handled through Azure AD SSO with session cookies managed by Chrome.

??? question "Can I automate without browser?"

    The `f5xc-cli` and `f5xc-api` plugins (planned) will provide headless automation. See the [Roadmap](roadmap.md) for availability.

??? question "How do I update plugins?"

    ```bash
    /plugin update f5xc-chrome
    ```
    Or reinstall to get the latest version.
