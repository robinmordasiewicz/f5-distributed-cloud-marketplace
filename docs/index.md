---
hide:
  - navigation
  - toc
---

<div class="hero-section" markdown>
<div class="hero-content" markdown>

<h1 class="hero-title">F5 Distributed Cloud<br><span class="highlight">Plugin Marketplace</span></h1>

<p class="hero-subtitle">
Automate F5 XC operations with Claude Code. Intelligent browser automation,
natural language commands, and enterprise-grade security for network engineers and DevOps teams.
</p>

<div class="hero-badges">
<span class="hero-badge">:material-check-circle: Open Source</span>
<span class="hero-badge">:material-shield-check: Enterprise Ready</span>
<span class="hero-badge">:material-lightning-bolt: AI-Powered</span>
</div>

[Get Started :material-arrow-right:](getting-started.md){ .hero-cta }

</div>
</div>

<div class="stats-grid" markdown>
<div class="stat-item">
<div class="stat-number">1</div>
<div class="stat-label">Active Plugin</div>
</div>
<div class="stat-item">
<div class="stat-number">23+</div>
<div class="stat-label">Workflows</div>
</div>
<div class="stat-item">
<div class="stat-number">100%</div>
<div class="stat-label">Automation</div>
</div>
<div class="stat-item">
<div class="stat-number">MIT</div>
<div class="stat-label">Licensed</div>
</div>
</div>

---

## :material-puzzle-outline: Key Features

<div class="grid cards" markdown>

- :material-lightning-bolt:{ .lg .middle } **Automation First**

    ---

    Automate repetitive F5 XC console tasks with intelligent browser automation
    powered by Claude's understanding of your intent.

    [:octicons-arrow-right-24: Learn more](plugins/f5xc-console.md)

- :material-brain:{ .lg .middle } **AI-Powered Intelligence**

    ---

    Natural language commands translate to precise console actions.
    Just describe what you want, and Claude handles the details.

    [:octicons-arrow-right-24: See examples](getting-started.md#using-plugins)

- :material-security:{ .lg .middle } **Enterprise Security**

    ---

    Built for enterprise environments with Azure AD SSO,
    multi-tenant support, and secure authentication flows.

    [:octicons-arrow-right-24: Security details](getting-started.md#authentication)

- :material-source-repository:{ .lg .middle } **Open Source**

    ---

    MIT licensed and community-driven. Contribute workflows,
    report issues, and help shape the future of F5 automation.

    [:octicons-arrow-right-24: Contribute](contributing.md)

</div>

---

## :material-package-variant: Available Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| [**f5xc-console**](plugins/f5xc-console.md) | Browser automation for F5 XC console operations | <span class="status-dot active"></span> Available |
| **f5xc-cli** | CLI operations and scripting integration | <span class="status-dot pending"></span> Planned |
| **f5xc-terraform** | Infrastructure as Code integration | <span class="status-dot pending"></span> Planned |
| **f5xc-docs** | Documentation and API reference lookup | <span class="status-dot pending"></span> Planned |

---

## :material-rocket-launch: Quick Start

!!! tip "Get up and running in 60 seconds"

    === "Step 1: Add Marketplace"
        ```bash
        /plugin marketplace add robinmordasiewicz/f5-distributed-cloud-marketplace
        ```

    === "Step 2: Install Plugin"
        ```bash
        /plugin install f5xc-console
        ```

    === "Step 3: Start Automating"
        ```text
        You: "Navigate to the shared namespace and show me all HTTP load balancers"
        Claude: Navigating to shared namespace... Found 3 HTTP load balancers...
        ```

---

## :material-comment-quote: What You Can Do

<div class="grid cards" markdown>

- :material-web: **Load Balancers**

    Create, configure, and manage HTTP/HTTPS load balancers with natural language commands.

- :material-server-network: **Origin Pools**

    Set up origin pools, configure health checks, and manage backend servers.

- :material-shield-lock: **WAF Policies**

    Deploy and configure Web Application Firewall policies for application security.

- :material-map-marker-path: **Multi-Tenant Navigation**

    Navigate complex multi-tenant environments with intelligent namespace switching.

</div>

---

## :material-help-circle: Getting Help

<div class="grid cards" markdown>

- :material-book-open-outline: [**Getting Started Guide**](getting-started.md)

    Complete walkthrough from installation to your first automation.

- :material-lifebuoy: [**Troubleshooting**](troubleshooting.md)

    Common issues and solutions for plugin and automation problems.

- :material-github: [**GitHub Issues**](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues)

    Report bugs, request features, or ask questions.

- :material-map: [**Roadmap**](roadmap.md)

    See what's coming next and planned features.

</div>

---

<div style="text-align: center; padding: 2rem 0;" markdown>

**Ready to automate your F5 Distributed Cloud workflows?**

[Get Started :material-arrow-right:](getting-started.md){ .md-button .md-button--primary }
[View on GitHub :material-github:](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace){ .md-button }

</div>
