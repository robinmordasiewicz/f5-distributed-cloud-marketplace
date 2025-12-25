#!/usr/bin/env bash
#
# Plugin Manager for F5 Distributed Cloud Marketplace
# Registry-based plugin installation without git submodules
#
# Usage:
#   ./scripts/plugin-manager.sh install <plugin-name> [version]
#   ./scripts/plugin-manager.sh update <plugin-name>
#   ./scripts/plugin-manager.sh list
#   ./scripts/plugin-manager.sh sync
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKETPLACE_ROOT="$(dirname "$SCRIPT_DIR")"
PLUGINS_JSON="$MARKETPLACE_ROOT/plugins.json"
PLUGINS_DIR="$MARKETPLACE_ROOT/plugins"
CACHE_DIR="${CLAUDE_PLUGINS_CACHE:-$HOME/.claude/plugins/cache}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# Check dependencies
check_deps() {
    for cmd in curl jq tar; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command not found: $cmd"
            exit 1
        fi
    done
}

# Get plugin info from registry
get_plugin_info() {
    local plugin_name="$1"
    local field="$2"
    jq -r ".plugins[\"$plugin_name\"].$field // empty" "$PLUGINS_JSON"
}

# Get version info
get_version_info() {
    local plugin_name="$1"
    local version="$2"
    local field="$3"
    jq -r ".plugins[\"$plugin_name\"].versions[\"$version\"].$field // empty" "$PLUGINS_JSON"
}

# List all available plugins
cmd_list() {
    log_info "Available plugins in registry:"
    echo ""
    jq -r '.plugins | to_entries[] | "\(.key)\t\(.value.latest)\t\(.value.description)"' "$PLUGINS_JSON" | \
        while IFS=$'\t' read -r name version desc; do
            printf "  ${GREEN}%-20s${NC} ${YELLOW}v%-10s${NC} %s\n" "$name" "$version" "$desc"
        done
    echo ""

    # Show installed plugins
    if [[ -d "$PLUGINS_DIR" ]]; then
        log_info "Installed plugins:"
        for plugin_dir in "$PLUGINS_DIR"/*/; do
            if [[ -d "$plugin_dir" ]]; then
                local name=$(basename "$plugin_dir")
                local version_file="$plugin_dir/.version"
                local version="unknown"
                [[ -f "$version_file" ]] && version=$(cat "$version_file")
                printf "  ${GREEN}%-20s${NC} ${YELLOW}v%-10s${NC}\n" "$name" "$version"
            fi
        done
    fi
}

# Install a plugin
cmd_install() {
    local plugin_name="$1"
    local version="${2:-$(get_plugin_info "$plugin_name" "latest")}"

    if [[ -z "$version" ]]; then
        log_error "Plugin not found: $plugin_name"
        exit 1
    fi

    local tarball_url=$(get_version_info "$plugin_name" "$version" "tarball")
    if [[ -z "$tarball_url" ]]; then
        log_error "Version not found: $plugin_name@$version"
        exit 1
    fi

    local plugin_dir="$PLUGINS_DIR/$plugin_name"
    local cache_plugin_dir="$CACHE_DIR/f5-distributed-cloud/$plugin_name/$version"

    log_info "Installing $plugin_name@$version..."

    # Create temp directory
    local tmp_dir=$(mktemp -d)
    trap "rm -rf $tmp_dir" EXIT

    # Download tarball
    log_info "Downloading from $tarball_url"
    curl -sL "$tarball_url" -o "$tmp_dir/plugin.tar.gz"

    # Extract
    log_info "Extracting..."
    tar -xzf "$tmp_dir/plugin.tar.gz" -C "$tmp_dir"

    # Find extracted directory (GitHub adds repo-version prefix)
    local extracted_dir=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -1)

    # Remove old installation
    [[ -d "$plugin_dir" ]] && rm -rf "$plugin_dir"

    # Move to plugins directory
    mkdir -p "$PLUGINS_DIR"
    mv "$extracted_dir" "$plugin_dir"

    # Write version file
    echo "$version" > "$plugin_dir/.version"

    # Also update cache for Claude Code
    mkdir -p "$cache_plugin_dir"
    cp -r "$plugin_dir/"* "$cache_plugin_dir/"

    log_success "Installed $plugin_name@$version to $plugin_dir"
    log_success "Cached at $cache_plugin_dir"
}

# Update a plugin to latest
cmd_update() {
    local plugin_name="$1"
    local latest=$(get_plugin_info "$plugin_name" "latest")

    if [[ -z "$latest" ]]; then
        log_error "Plugin not found: $plugin_name"
        exit 1
    fi

    local current="unknown"
    local version_file="$PLUGINS_DIR/$plugin_name/.version"
    [[ -f "$version_file" ]] && current=$(cat "$version_file")

    if [[ "$current" == "$latest" ]]; then
        log_info "$plugin_name is already at latest version ($latest)"
        return 0
    fi

    log_info "Updating $plugin_name from $current to $latest"
    cmd_install "$plugin_name" "$latest"
}

# Sync all plugins to their latest versions
cmd_sync() {
    log_info "Syncing all plugins to latest versions..."

    local plugins=$(jq -r '.plugins | keys[]' "$PLUGINS_JSON")

    for plugin in $plugins; do
        cmd_update "$plugin"
    done

    log_success "All plugins synced"
}

# Update Claude Code installed_plugins.json
update_claude_registry() {
    local plugin_name="$1"
    local version="$2"
    local install_path="$3"
    local claude_plugins="$HOME/.claude/plugins/installed_plugins.json"

    if [[ ! -f "$claude_plugins" ]]; then
        log_warn "Claude plugins registry not found at $claude_plugins"
        return 0
    fi

    local registry_name="${plugin_name}@f5-distributed-cloud"
    local plugin_json_name=$(jq -r '.name // empty' "$install_path/.claude-plugin/plugin.json" 2>/dev/null || echo "$plugin_name")

    # Update the registry entry
    local tmp_file=$(mktemp)
    jq --arg name "$registry_name" \
       --arg path "$install_path" \
       --arg version "$version" \
       --arg now "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)" \
       '.plugins[$name] = [{
         "scope": "user",
         "installPath": $path,
         "version": $version,
         "installedAt": .plugins[$name][0].installedAt // $now,
         "lastUpdated": $now,
         "isLocal": true
       }]' "$claude_plugins" > "$tmp_file"

    mv "$tmp_file" "$claude_plugins"
    log_success "Updated Claude registry for $plugin_name"
}

# Main
main() {
    check_deps

    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        install)
            [[ $# -lt 1 ]] && { log_error "Usage: $0 install <plugin-name> [version]"; exit 1; }
            cmd_install "$@"
            ;;
        update)
            [[ $# -lt 1 ]] && { log_error "Usage: $0 update <plugin-name>"; exit 1; }
            cmd_update "$@"
            ;;
        list)
            cmd_list
            ;;
        sync)
            cmd_sync
            ;;
        help|--help|-h)
            echo "Plugin Manager for F5 Distributed Cloud Marketplace"
            echo ""
            echo "Usage:"
            echo "  $0 install <plugin-name> [version]  Install a plugin"
            echo "  $0 update <plugin-name>             Update plugin to latest"
            echo "  $0 list                             List available/installed plugins"
            echo "  $0 sync                             Sync all plugins to latest"
            echo ""
            ;;
        *)
            log_error "Unknown command: $cmd"
            echo "Run '$0 help' for usage"
            exit 1
            ;;
    esac
}

main "$@"
