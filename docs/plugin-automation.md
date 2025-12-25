# Plugin Automation

This document describes how plugins are automatically synchronized from npm registry to the marketplace.

## Overview

When a plugin repository (e.g., `f5xc-console`) publishes a new release to npm, it can
trigger a webhook to notify this marketplace. The marketplace then:

1. Fetches the latest version metadata from npm registry
2. Updates `plugins.json` with the new version
3. Commits the changes to trigger documentation rebuild
4. Deploys updated documentation to GitHub Pages

## Webhook Dispatch Setup

### For Plugin Repositories

To enable automatic sync when your plugin publishes a new release, add this step to your release workflow:

```yaml
# In your plugin's .github/workflows/release.yml
- name: Notify marketplace of new release
  if: success()
  uses: peter-evans/repository-dispatch@v3
  with:
    token: ${{ secrets.MARKETPLACE_DISPATCH_TOKEN }}
    repository: robinmordasiewicz/f5-distributed-cloud-marketplace
    event-type: plugin-release
    client-payload: |
      {
        "plugin": "f5xc-console",
        "version": "${{ env.NEW_VERSION }}",
        "repository": "${{ github.repository }}",
        "npm_package": "@robinmordasiewicz/f5xc-console"
      }
```

### Required Secrets

The plugin repository needs a Personal Access Token (PAT) with `repo` scope that has write access to the marketplace repository:

1. Create a PAT at https://github.com/settings/tokens
2. Grant `repo` scope (for repository dispatch)
3. Add as secret `MARKETPLACE_DISPATCH_TOKEN` in your plugin repository

### Alternative: Fine-grained Token

For better security, use a fine-grained PAT:

1. Create at https://github.com/settings/personal-access-tokens
2. Repository access: Select `robinmordasiewicz/f5-distributed-cloud-marketplace`
3. Permissions: Contents (read/write)
4. Add as secret in your plugin repository

## Sync Triggers

The marketplace syncs plugins in three ways:

| Trigger | Description |
|---------|-------------|
| `repository_dispatch` | Immediate sync when plugin sends webhook |
| `workflow_dispatch` | Manual trigger from GitHub Actions UI |
| `schedule` | Every 6 hours as fallback |

## Manual Sync

To manually trigger a sync:

1. Go to Actions → Plugin Sync
2. Click "Run workflow"
3. Select plugin to sync (or "all")
4. Click "Run workflow"

## Local Testing

Test the sync script locally:

```bash
# Sync all npm plugins
./scripts/sync-npm-plugins.sh

# Check current plugin versions
./scripts/plugin-manager.sh list

# Get npm package info
./scripts/plugin-manager.sh npm-info f5xc-console
```

## Workflow Files

| File | Purpose |
|------|---------|
| `.github/workflows/plugin-sync.yml` | Handles webhook dispatch and syncs |
| `scripts/sync-npm-plugins.sh` | Fetches npm metadata and updates files |
| `scripts/plugin-manager.sh` | CLI for manual plugin management |

## Payload Format

The webhook dispatch expects this payload format:

```json
{
  "plugin": "f5xc-console",
  "version": "0.10.1",
  "repository": "robinmordasiewicz/f5xc-console",
  "npm_package": "@robinmordasiewicz/f5xc-console"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `plugin` | Yes | Plugin key in plugins.json |
| `version` | No | Specific version (defaults to npm latest) |
| `repository` | No | Source repository for logging |
| `npm_package` | No | npm package name (read from plugins.json) |
