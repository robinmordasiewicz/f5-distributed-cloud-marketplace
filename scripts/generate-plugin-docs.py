#!/usr/bin/env python3
"""Generate plugin documentation from marketplace.json and plugin.json metadata.

This script:
1. Reads .claude-plugin/marketplace.json
2. Fetches plugin.json from each plugin's GitHub repository
3. Merges marketplace metadata with plugin metadata
4. Generates docs/plugins/index.md (plugin overview table)
5. Generates docs/plugins/{name}.md for each plugin

Generated files should be in .gitignore as they're built at deploy time.
"""

from __future__ import annotations

import json
import logging
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


# Configuration
MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")
DOCS_OUTPUT_DIR = Path("docs/plugins")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
GITHUB_API_BASE = "https://api.github.com/repos"
REQUEST_TIMEOUT = 10


class AuthorInfo(TypedDict, total=False):
    """Author information structure."""

    name: str
    email: str
    url: str


class SourceInfo(TypedDict, total=False):
    """Plugin source information."""

    source: str
    repo: str
    url: str


class PluginEntry(TypedDict, total=False):
    """Plugin entry in marketplace.json."""

    name: str
    description: str
    version: str
    author: AuthorInfo | str
    homepage: str
    repository: str
    license: str
    keywords: list[str]
    category: str
    tags: list[str]
    source: SourceInfo | str
    commands: list[str] | str
    agents: list[str] | str
    skills: list[str] | str
    hooks: str
    mcpServers: str
    strict: bool


class MarketplaceData(TypedDict):
    """Marketplace.json structure."""

    name: str
    version: str
    description: str
    license: str
    owner: AuthorInfo
    plugins: list[PluginEntry]
    homepage: str
    repository: str


class ProcessedPlugin(TypedDict, total=False):
    """Processed plugin with merged metadata."""

    name: str
    description: str
    version: str
    author: AuthorInfo
    homepage: str
    repository: str
    license: str
    keywords: list[str]
    category: str
    tags: list[str]
    source: SourceInfo
    commands: list[str] | str
    agents: list[str] | str
    skills: list[str] | str
    hooks: str
    mcpServers: str
    stars: int
    updated_at: str
    topics: list[str]
    default_branch: str


def load_marketplace() -> MarketplaceData:
    """Load the marketplace.json file.

    Returns:
        Parsed marketplace data.

    Raises:
        FileNotFoundError: If marketplace.json doesn't exist.
        json.JSONDecodeError: If JSON is invalid.
    """
    with MARKETPLACE_PATH.open(encoding="utf-8") as f:
        data: MarketplaceData = json.load(f)
    return data


def validate_url_scheme(url: str) -> bool:
    """Validate that a URL uses a safe scheme (https only).

    Args:
        url: The URL to validate.

    Returns:
        True if the URL scheme is safe, False otherwise.
    """
    return url.startswith("https://")


def fetch_json_from_url(url: str) -> dict[str, Any] | None:
    """Fetch JSON from a URL with error handling.

    Args:
        url: The URL to fetch from (must be https://).

    Returns:
        Parsed JSON data or None if fetch failed.
    """
    if not validate_url_scheme(url):
        logger.warning("Refusing to fetch non-HTTPS URL: %s", url)
        return None

    try:
        req = urllib.request.Request(  # noqa: S310 - URL scheme validated above
            url,
            headers={"User-Agent": "F5XC-Marketplace-Docs/1.0"},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:  # noqa: S310
            return json.loads(response.read().decode("utf-8"))  # type: ignore[no-any-return]
    except urllib.error.HTTPError as e:
        if e.code != 404:  # noqa: PLR2004
            logger.warning("HTTP error %d fetching %s", e.code, url)
        return None
    except urllib.error.URLError as e:
        logger.warning("URL error fetching %s: %s", url, e.reason)
        return None
    except json.JSONDecodeError as e:
        logger.warning("JSON decode error from %s: %s", url, e)
        return None
    except TimeoutError:
        logger.warning("Timeout fetching %s", url)
        return None


def fetch_plugin_json(repo: str) -> dict[str, Any] | None:
    """Fetch plugin.json from a GitHub repository.

    Tries multiple common locations for the plugin.json file.

    Args:
        repo: GitHub repository in owner/repo format.

    Returns:
        Parsed plugin.json data or None if not found.
    """
    paths = [
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude-plugin/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude-plugin/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/main/plugin.json",
        f"{GITHUB_RAW_BASE}/{repo}/master/plugin.json",
    ]

    for url in paths:
        result = fetch_json_from_url(url)
        if result is not None:
            return result

    return None


def fetch_repo_info(repo: str) -> dict[str, Any] | None:
    """Fetch repository metadata from GitHub API.

    Args:
        repo: GitHub repository in owner/repo format.

    Returns:
        Repository metadata or None if fetch failed.
    """
    url = f"{GITHUB_API_BASE}/{repo}"
    return fetch_json_from_url(url)


def _merge_author_info(
    existing: AuthorInfo | str | None,
    new_author: AuthorInfo | str,
) -> AuthorInfo:
    """Merge author information from two sources.

    Args:
        existing: Existing author info (may be None, str, or dict).
        new_author: New author info to merge in.

    Returns:
        Merged author information as a dict.
    """
    # Convert string author to dict
    if isinstance(new_author, str):
        new_author = {"name": new_author}

    # If existing is a dict, merge with new; otherwise use new
    if isinstance(existing, dict):
        return {**existing, **new_author}
    return new_author


def _apply_plugin_json_fields(
    merged: ProcessedPlugin,
    plugin_json: dict[str, Any],
) -> None:
    """Apply fields from plugin.json to merged metadata.

    Args:
        merged: The merged plugin data to update (modified in place).
        plugin_json: The plugin.json data to apply.
    """
    # Plugin.json fields take precedence for certain fields
    for field in ("version", "description", "license", "keywords", "homepage"):
        if value := plugin_json.get(field):
            merged[field] = value

    # Merge author information
    if author_data := plugin_json.get("author"):
        merged["author"] = _merge_author_info(merged.get("author"), author_data)

    # Copy component paths if available
    for component in ("commands", "agents", "skills", "hooks", "mcpServers"):
        if component in plugin_json:
            merged[component] = plugin_json[component]


def _apply_repo_info(merged: ProcessedPlugin, repo_info: dict[str, Any]) -> None:
    """Apply GitHub repository info to merged metadata.

    Args:
        merged: The merged plugin data to update (modified in place).
        repo_info: The GitHub API repo info.
    """
    merged["stars"] = repo_info.get("stargazers_count", 0)
    merged["updated_at"] = repo_info.get("updated_at", "")
    merged["topics"] = repo_info.get("topics", [])
    merged["default_branch"] = repo_info.get("default_branch", "main")


def merge_metadata(
    marketplace_entry: PluginEntry,
    plugin_json: dict[str, Any] | None,
    repo_info: dict[str, Any] | None,
) -> ProcessedPlugin:
    """Merge metadata from marketplace, plugin.json, and GitHub API.

    Args:
        marketplace_entry: Plugin entry from marketplace.json.
        plugin_json: Fetched plugin.json data (may be None).
        repo_info: Fetched GitHub repo info (may be None).

    Returns:
        Merged plugin metadata.
    """
    merged: ProcessedPlugin = dict(marketplace_entry)  # type: ignore[assignment]

    if plugin_json:
        _apply_plugin_json_fields(merged, plugin_json)

    if repo_info:
        _apply_repo_info(merged, repo_info)

    return merged


def _extract_author_info(plugin: ProcessedPlugin) -> tuple[str, str]:
    """Extract author name and URL from plugin metadata.

    Args:
        plugin: The plugin metadata.

    Returns:
        Tuple of (author_name, author_url).
    """
    author = plugin.get("author", {})
    if isinstance(author, dict):
        return author.get("name", "Unknown"), author.get("url", "")
    return str(author) if author else "Unknown", ""


def _build_component_badges(plugin: ProcessedPlugin) -> list[str]:
    """Build component badge strings for the plugin.

    Args:
        plugin: The plugin metadata.

    Returns:
        List of component badge strings.
    """
    component_map = {
        "commands": ":material-console: Commands",
        "skills": ":material-puzzle: Skills",
        "agents": ":material-robot: Agents",
        "mcpServers": ":material-server: MCP Servers",
    }
    return [badge for key, badge in component_map.items() if key in plugin]


def _build_commands_section(plugin: ProcessedPlugin) -> list[str]:
    """Build the commands section markdown.

    Args:
        plugin: The plugin metadata.

    Returns:
        List of markdown lines for the commands section.
    """
    if "commands" not in plugin:
        return []

    lines = ["## Available Commands", ""]
    commands = plugin.get("commands", [])

    if isinstance(commands, list) and commands:
        lines.extend(["| Command | Description |", "|---------|-------------|"])
        lines.extend(f"| `{cmd}` | See documentation |" for cmd in commands if isinstance(cmd, str))
    else:
        lines.append("See plugin documentation for available commands.")
    lines.append("")
    return lines


def _build_links_section(
    repo_url: str,
    author_name: str,
    author_url: str,
) -> list[str]:
    """Build the links section markdown.

    Args:
        repo_url: The repository URL (may be empty).
        author_name: The author name.
        author_url: The author URL (may be empty).

    Returns:
        List of markdown lines for the links section.
    """
    lines = ["## Links", ""]
    if repo_url:
        lines.append(f"- :material-github: [Source Repository]({repo_url})")
    if author_url:
        lines.append(f"- :material-account: [Author: {author_name}]({author_url})")
    elif author_name and author_name != "Unknown":
        lines.append(f"- :material-account: Author: {author_name}")
    return lines


def generate_plugin_page(plugin: ProcessedPlugin) -> str:
    """Generate markdown content for a single plugin page.

    Args:
        plugin: Processed plugin metadata.

    Returns:
        Generated markdown content.
    """
    name = plugin.get("name", "Unknown Plugin")
    description = plugin.get("description", "No description available.")
    version = plugin.get("version", "N/A")
    license_type = plugin.get("license", "MIT")
    category = plugin.get("category", "automation")

    # Get source and author information
    source = plugin.get("source", {})
    repo = source.get("repo", "") if isinstance(source, dict) else ""
    repo_url = f"https://github.com/{repo}" if repo else ""
    author_name, author_url = _extract_author_info(plugin)

    # Merge tags and keywords
    all_tags = list(set(plugin.get("tags", []) + plugin.get("keywords", [])))

    # Build the markdown header (no H1 - title comes from frontmatter)
    lines = [
        "---",
        f"title: {name}",
        f"description: {description}",
        "---",
        "",
        f"![Version](https://img.shields.io/badge/version-{version}-blue)",
        f"![License](https://img.shields.io/badge/license-{license_type}-green)",
        f"![Category](https://img.shields.io/badge/category-{category}-orange)",
        "",
        f"> {description}",
        "",
    ]

    # Add component badges
    component_badges = _build_component_badges(plugin)
    if component_badges:
        lines.extend(["## Components", "", " | ".join(component_badges), ""])

    # Installation section (use fenced code blocks, not indented)
    lines.extend(
        [
            "## Installation",
            "",
            "**From Marketplace:**",
            "",
            "```bash",
            f"/plugin install {name}",
            "```",
            "",
            "**Direct from GitHub:**",
            "",
            "```bash",
            f"/plugin install {repo}",
            "```",
            "",
        ]
    )

    # Commands section
    lines.extend(_build_commands_section(plugin))

    # Requirements section
    lines.extend(["## Requirements", "", "- Claude Code installed and configured"])
    is_browser_plugin = "chrome" in name.lower() or "browser" in description.lower()
    if is_browser_plugin:
        lines.append("- Claude in Chrome browser extension")
    lines.extend(["", ""])

    # Tags section
    if all_tags:
        lines.extend(["## Tags", "", " ".join(f"`{tag}`" for tag in sorted(all_tags)), ""])

    # Links section
    lines.extend(_build_links_section(repo_url, author_name, author_url))

    # Timestamp
    timestamp = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.extend(["", "---", "", f"*Last generated: {timestamp}*"])

    return "\n".join(lines)


def generate_index_page(plugins: list[ProcessedPlugin], marketplace: MarketplaceData) -> str:
    """Generate the plugin overview/index page.

    Args:
        plugins: List of processed plugins.
        marketplace: Marketplace metadata.

    Returns:
        Generated markdown content.
    """
    marketplace_version = marketplace.get("version", "1.0.0")

    lines = [
        "---",
        "title: Plugin Overview",
        "description: All available plugins in the F5 Distributed Cloud marketplace",
        "---",
        "",
        f"Marketplace Version: `{marketplace_version}`",
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
        max_desc_len = 60
        if len(description) > max_desc_len:
            description = description[: max_desc_len - 3] + "..."

        lines.append(f"| [{name}]({name}.md) | {version} | {category} | {description} |")

    lines.extend(
        [
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
        ]
    )

    # Group by category
    categories: dict[str, list[ProcessedPlugin]] = {}
    for plugin in plugins:
        cat = plugin.get("category", "automation")
        categories.setdefault(cat, []).append(plugin)

    for category, cat_plugins in sorted(categories.items()):
        lines.append(f"### {category.title()}")
        lines.append("")
        for plugin in cat_plugins:
            plugin_name = plugin.get("name", "unknown")
            plugin_desc = plugin.get("description", "No description")
            # Truncate description to avoid line length issues (keep under 100 chars)
            max_cat_desc_len = 80
            if len(plugin_desc) > max_cat_desc_len:
                plugin_desc = plugin_desc[: max_cat_desc_len - 3] + "..."
            lines.append(f"- [{plugin_name}]({plugin_name}.md) - {plugin_desc}")
        lines.append("")

    # Timestamp
    timestamp = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.extend(
        [
            "---",
            "",
            f"*Last generated: {timestamp}*",
        ]
    )

    return "\n".join(lines)


def validate_generated_markdown(filepath: Path) -> list[str]:
    """Validate generated markdown meets quality standards.

    Args:
        filepath: Path to the generated markdown file.

    Returns:
        List of validation errors (empty if valid).
    """
    errors: list[str] = []
    content = filepath.read_text(encoding="utf-8")

    # Check required sections exist
    required_sections = ["## Installation", "## Links"]
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Check badges are properly formatted
    if "![Version]" not in content:
        errors.append("Missing version badge")

    # Validate YAML frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")

    return errors


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    logger.info("Generating plugin documentation...")

    # Ensure output directory exists
    DOCS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load marketplace
    logger.info("Loading %s...", MARKETPLACE_PATH)
    try:
        marketplace = load_marketplace()
    except FileNotFoundError:
        logger.error("Marketplace file not found: %s", MARKETPLACE_PATH)
        return 1
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in marketplace file: %s", e)
        return 1

    plugins_data = marketplace.get("plugins", [])

    if not plugins_data:
        logger.warning("No plugins found in marketplace.json")
        return 0

    logger.info("Found %d plugin(s)", len(plugins_data))

    # Process each plugin
    processed_plugins: list[ProcessedPlugin] = []
    validation_errors: list[str] = []

    for plugin in plugins_data:
        name = plugin.get("name", "unknown")
        source: SourceInfo | str | dict[str, Any] = plugin.get("source", {})
        repo = source.get("repo", "") if isinstance(source, dict) else ""

        logger.info("Processing: %s", name)

        # Fetch additional metadata
        plugin_json: dict[str, Any] | None = None
        repo_info: dict[str, Any] | None = None

        if repo:
            logger.info("  Fetching plugin.json from %s...", repo)
            plugin_json = fetch_plugin_json(repo)
            if plugin_json:
                logger.info("  Found plugin.json")
            else:
                logger.info("  No plugin.json found (using marketplace metadata only)")

            logger.info("  Fetching repo info...")
            repo_info = fetch_repo_info(repo)

        # Merge metadata
        merged = merge_metadata(plugin, plugin_json, repo_info)
        processed_plugins.append(merged)

        # Generate plugin page
        plugin_content = generate_plugin_page(merged)
        plugin_file = DOCS_OUTPUT_DIR / f"{name}.md"

        logger.info("  Writing %s...", plugin_file)
        plugin_file.write_text(plugin_content, encoding="utf-8")

        # Validate generated content
        errors = validate_generated_markdown(plugin_file)
        if errors:
            for error in errors:
                validation_errors.append(f"{name}: {error}")

    # Generate index page
    logger.info("Generating plugin index...")
    index_content = generate_index_page(processed_plugins, marketplace)
    index_file = DOCS_OUTPUT_DIR / "index.md"
    index_file.write_text(index_content, encoding="utf-8")

    logger.info(
        "Done! Generated %d files in %s/",
        len(processed_plugins) + 1,
        DOCS_OUTPUT_DIR,
    )

    # List generated files
    for f in sorted(DOCS_OUTPUT_DIR.glob("*.md")):
        logger.info("  - %s", f)

    # Report validation errors
    if validation_errors:
        logger.warning("Validation warnings:")
        for error in validation_errors:
            logger.warning("  - %s", error)

    return 0


if __name__ == "__main__":
    sys.exit(main())
