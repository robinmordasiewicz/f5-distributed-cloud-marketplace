#!/usr/bin/env python3
"""
Generate plugin documentation from marketplace.json and plugin.json metadata.

This script:
1. Reads .claude-plugin/marketplace.json
2. Fetches plugin.json from each plugin's GitHub repository
3. Merges marketplace metadata with plugin metadata
4. Generates docs/plugins/index.md (plugin overview table)
5. Generates docs/plugins/{name}.md for each plugin

Generated files should be in .gitignore as they're built at deploy time.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# Configuration
MARKETPLACE_PATH = ".claude-plugin/marketplace.json"
DOCS_OUTPUT_DIR = "docs/plugins"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
GITHUB_API_BASE = "https://api.github.com/repos"


def load_marketplace() -> dict:
    """Load the marketplace.json file."""
    with open(MARKETPLACE_PATH, "r") as f:
        return json.load(f)


def fetch_plugin_json(repo: str) -> Optional[dict]:
    """Fetch plugin.json from a GitHub repository."""
    # Try common locations for plugin.json
    paths = [
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude-plugin/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude-plugin/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/main/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/master/plugin.json",
    ]

    for url in paths:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "F5XC-Marketplace-Docs/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError:
            continue
        except Exception as e:
            print(f"  Warning: Error fetching from {url}: {e}", file=sys.stderr)
            continue

    return None


def fetch_repo_info(repo: str) -> Optional[dict]:
    """Fetch repository metadata from GitHub API."""
    url = f"{GITHUB_API_BASE}/{repo}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "F5XC-Marketplace-Docs/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  Warning: Error fetching repo info for {repo}: {e}", file=sys.stderr)
        return None


def merge_metadata(marketplace_entry: dict, plugin_json: Optional[dict], repo_info: Optional[dict]) -> dict:
    """Merge metadata from marketplace, plugin.json, and GitHub API."""
    merged = dict(marketplace_entry)

    if plugin_json:
        # Plugin.json fields take precedence for certain fields
        for field in ["version", "description", "license", "keywords", "homepage"]:
            if field in plugin_json and plugin_json[field]:
                merged[field] = plugin_json[field]

        # Merge author information
        if "author" in plugin_json:
            if isinstance(plugin_json["author"], dict):
                merged["author"] = {**merged.get("author", {}), **plugin_json["author"]}
            elif isinstance(plugin_json["author"], str):
                merged.setdefault("author", {})["name"] = plugin_json["author"]

        # Copy component paths if available
        for component in ["commands", "agents", "skills", "hooks", "mcpServers"]:
            if component in plugin_json:
                merged[component] = plugin_json[component]

    if repo_info:
        # Add GitHub-specific metadata
        merged["stars"] = repo_info.get("stargazers_count", 0)
        merged["updated_at"] = repo_info.get("updated_at", "")
        merged["topics"] = repo_info.get("topics", [])
        merged["default_branch"] = repo_info.get("default_branch", "main")

    return merged


def generate_plugin_page(plugin: dict) -> str:
    """Generate markdown content for a single plugin page."""
    name = plugin.get("name", "Unknown Plugin")
    description = plugin.get("description", "No description available.")
    version = plugin.get("version", "N/A")
    license_type = plugin.get("license", "MIT")

    # Get source information
    source = plugin.get("source", {})
    repo = source.get("repo", "") if isinstance(source, dict) else ""
    repo_url = f"https://github.com/{repo}" if repo else ""

    # Author information
    author = plugin.get("author", {})
    author_name = author.get("name", "Unknown") if isinstance(author, dict) else str(author)
    author_url = author.get("url", "") if isinstance(author, dict) else ""

    # Categories and tags
    category = plugin.get("category", "automation")
    tags = plugin.get("tags", [])
    keywords = plugin.get("keywords", [])
    all_tags = list(set(tags + keywords))

    # Component information
    has_commands = "commands" in plugin
    has_skills = "skills" in plugin
    has_agents = "agents" in plugin
    has_mcp = "mcpServers" in plugin

    # Build the markdown
    lines = [
        "---",
        f"title: {name}",
        f"description: {description}",
        "---",
        "",
        f"# {name}",
        "",
        f"![Version](https://img.shields.io/badge/version-{version}-blue)",
        f"![License](https://img.shields.io/badge/license-{license_type}-green)",
        f"![Category](https://img.shields.io/badge/category-{category}-orange)",
        "",
        f"> {description}",
        "",
    ]

    # Add badges for available components
    if has_commands or has_skills or has_agents or has_mcp:
        components = []
        if has_commands:
            components.append(":material-console: Commands")
        if has_skills:
            components.append(":material-puzzle: Skills")
        if has_agents:
            components.append(":material-robot: Agents")
        if has_mcp:
            components.append(":material-server: MCP Servers")
        lines.extend([
            "## Components",
            "",
            " | ".join(components),
            "",
        ])

    # Installation section
    lines.extend([
        "## Installation",
        "",
        "=== \"From Marketplace\"",
        "",
        "    ```bash",
        f"    /plugin install {name}",
        "    ```",
        "",
        "=== \"Direct from GitHub\"",
        "",
        "    ```bash",
        f"    /plugin install {repo}",
        "    ```",
        "",
    ])

    # Commands section (placeholder - would be populated from plugin.json)
    if has_commands:
        lines.extend([
            "## Available Commands",
            "",
            "| Command | Description |",
            "|---------|-------------|",
            f"| `/xc:console login` | Authenticate via Azure SSO |",
            f"| `/xc:console crawl` | Extract navigation metadata |",
            f"| `/xc:console nav` | Navigate to workspace/page |",
            f"| `/xc:console create` | Create resources |",
            "",
        ])

    # Requirements section
    lines.extend([
        "## Requirements",
        "",
        "- Claude Code installed and configured",
        "- Claude in Chrome browser extension",
        "- Azure AD credentials with F5 XC tenant access",
        "",
    ])

    # Tags section
    if all_tags:
        lines.extend([
            "## Tags",
            "",
            " ".join([f"`{tag}`" for tag in all_tags]),
            "",
        ])

    # Links section
    lines.extend([
        "## Links",
        "",
    ])

    if repo_url:
        lines.append(f"- :material-github: [Source Repository]({repo_url})")

    if author_url:
        lines.append(f"- :material-account: [Author: {author_name}]({author_url})")
    elif author_name:
        lines.append(f"- :material-account: Author: {author_name}")

    lines.extend([
        "",
        "---",
        "",
        f"*Last generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
    ])

    return "\n".join(lines)


def generate_index_page(plugins: list[dict], marketplace: dict) -> str:
    """Generate the plugin overview/index page."""
    marketplace_name = marketplace.get("name", "Plugin Marketplace")
    marketplace_version = marketplace.get("version", "1.0.0")

    lines = [
        "---",
        "title: Plugin Overview",
        "description: All available plugins in the F5 Distributed Cloud marketplace",
        "---",
        "",
        "# Plugin Overview",
        "",
        f"*Marketplace Version: {marketplace_version}*",
        "",
        "This page lists all plugins available in the F5 Distributed Cloud marketplace.",
        "",
        "## Available Plugins",
        "",
        "| Plugin | Version | Category | Description |",
        "|--------|---------|----------|-------------|",
    ]

    for plugin in plugins:
        name = plugin.get("name", "unknown")
        version = plugin.get("version", "N/A")
        category = plugin.get("category", "automation")
        description = plugin.get("description", "No description")

        # Truncate description if too long
        if len(description) > 60:
            description = description[:57] + "..."

        lines.append(f"| [{name}]({name}.md) | {version} | {category} | {description} |")

    lines.extend([
        "",
        "## Quick Install",
        "",
        "```bash",
        "# Add this marketplace",
        "/plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace",
        "",
        "# Install any plugin",
        "/plugin install <plugin-name>",
        "```",
        "",
        "## Plugin Categories",
        "",
    ])

    # Group by category
    categories: dict[str, list] = {}
    for plugin in plugins:
        cat = plugin.get("category", "automation")
        categories.setdefault(cat, []).append(plugin)

    for category, cat_plugins in sorted(categories.items()):
        lines.append(f"### {category.title()}")
        lines.append("")
        for plugin in cat_plugins:
            lines.append(f"- [{plugin['name']}]({plugin['name']}.md) - {plugin.get('description', 'No description')}")
        lines.append("")

    lines.extend([
        "---",
        "",
        f"*Last generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
    ])

    return "\n".join(lines)


def main():
    """Main entry point."""
    print("Generating plugin documentation...")

    # Ensure output directory exists
    output_path = Path(DOCS_OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load marketplace
    print(f"Loading {MARKETPLACE_PATH}...")
    marketplace = load_marketplace()
    plugins_data = marketplace.get("plugins", [])

    if not plugins_data:
        print("No plugins found in marketplace.json")
        return

    print(f"Found {len(plugins_data)} plugin(s)")

    # Process each plugin
    processed_plugins = []
    for plugin in plugins_data:
        name = plugin.get("name", "unknown")
        source = plugin.get("source", {})
        repo = source.get("repo", "") if isinstance(source, dict) else ""

        print(f"\nProcessing: {name}")

        # Fetch additional metadata
        plugin_json = None
        repo_info = None

        if repo:
            print(f"  Fetching plugin.json from {repo}...")
            plugin_json = fetch_plugin_json(repo)
            if plugin_json:
                print("  Found plugin.json")
            else:
                print("  No plugin.json found (using marketplace metadata only)")

            print(f"  Fetching repo info...")
            repo_info = fetch_repo_info(repo)

        # Merge metadata
        merged = merge_metadata(plugin, plugin_json, repo_info)
        processed_plugins.append(merged)

        # Generate plugin page
        plugin_content = generate_plugin_page(merged)
        plugin_file = output_path / f"{name}.md"

        print(f"  Writing {plugin_file}...")
        with open(plugin_file, "w") as f:
            f.write(plugin_content)

    # Generate index page
    print("\nGenerating plugin index...")
    index_content = generate_index_page(processed_plugins, marketplace)
    index_file = output_path / "index.md"

    with open(index_file, "w") as f:
        f.write(index_content)

    print(f"\nDone! Generated {len(processed_plugins) + 1} files in {DOCS_OUTPUT_DIR}/")

    # List generated files
    for f in sorted(output_path.glob("*.md")):
        print(f"  - {f}")


if __name__ == "__main__":
    main()
