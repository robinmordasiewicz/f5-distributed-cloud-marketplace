# Contributing

We welcome contributions to the F5 Distributed Cloud plugin marketplace!
This guide explains how to add plugins, improve existing ones, or enhance the marketplace.

## Ways to Contribute

### 1. Add a New Plugin

Create and publish your own F5 XC automation plugin.

### 2. Improve Existing Plugins

Submit bug fixes, features, or documentation improvements.

### 3. Enhance the Marketplace

Improve validation, automation, or documentation.

## Adding a Plugin to the Marketplace

### Step 1: Create Your Plugin

Your plugin repository must have a valid `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "What your plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/yourusername"
  },
  "license": "MIT",
  "keywords": ["f5", "xc", "your-tags"],
  "commands": "./commands/",
  "skills": "./skills/"
}
```

### Step 2: Fork the Marketplace

```bash
git clone https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace
cd f5-distributed-cloud-marketplace
```

### Step 3: Add Your Plugin Entry

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
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
  ]
}
```

### Step 4: Submit a Pull Request

1. Create a feature branch
2. Commit your changes
3. Push to your fork
4. Open a Pull Request

## Plugin Requirements

### Required Files

| File | Description |
|------|-------------|
| `.claude-plugin/plugin.json` | Plugin manifest with metadata |
| `README.md` | Plugin documentation |
| `LICENSE` | Open source license |

### Recommended Structure

```text
your-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── your-command.md
├── skills/
│   └── your-skill/
│       └── SKILL.md
├── README.md
├── LICENSE
└── CHANGELOG.md
```

### Quality Standards

- [ ] Plugin installs without errors
- [ ] Commands work as documented
- [ ] Source repository is publicly accessible
- [ ] License is clearly specified
- [ ] Documentation is clear and complete

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat:` | New features | Minor |
| `fix:` | Bug fixes | Patch |
| `docs:` | Documentation | None |
| `chore:` | Maintenance | None |
| `refactor:` | Code restructuring | None |
| `test:` | Testing | None |

### Examples

```bash
# New feature
git commit -m "feat: add support for origin pool creation"

# Bug fix
git commit -m "fix: resolve authentication timeout issue"

# Documentation
git commit -m "docs: update installation instructions"

# Breaking change
git commit -m "feat!: redesign command interface"
```

## Development Setup

### Clone the Repository

```bash
git clone https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace
cd f5-distributed-cloud-marketplace
```

### Install Dependencies

For documentation development:

```bash
pip install mkdocs-material mkdocs-minify-plugin
```

### Local Documentation Preview

```bash
# Generate plugin docs
python scripts/generate-plugin-docs.py

# Serve locally
mkdocs serve
```

Visit `http://localhost:8000` to preview.

## Validation

Before submitting, ensure your changes pass validation:

```bash
# Validate marketplace.json syntax
python -m json.tool .claude-plugin/marketplace.json

# Check plugin sources are accessible
python scripts/generate-plugin-docs.py
```

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the technical merits

## Getting Help

- :material-github: [Open an Issue](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues)
- :material-message: Start a Discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
