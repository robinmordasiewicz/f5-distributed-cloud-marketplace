# Roadmap

This roadmap outlines the planned development of F5 Distributed Cloud plugins. Priorities may shift based on community feedback and contributions.

## Current Status

### Available Now

| Plugin | Version | Description |
|--------|---------|-------------|
| f5xc-chrome | 0.1.0 | Browser automation for F5 XC console |

## Planned Plugins

### Q1 2025

#### f5xc-cli

Command-line interface plugin for scripted operations.

**Planned Features:**

- [ ] Resource listing and querying
- [ ] Configuration export/import
- [ ] Batch operations
- [ ] Output formatting (JSON, YAML, table)

**Use Cases:**

```bash
# List all HTTP load balancers
/xc:cli list http-lb --namespace production

# Export configuration
/xc:cli export http-lb my-lb --format yaml
```

---

#### f5xc-terraform

Infrastructure as Code integration with Terraform.

**Planned Features:**

- [ ] Terraform resource generation
- [ ] State file integration
- [ ] Drift detection
- [ ] Module templates

**Use Cases:**

```bash
# Generate Terraform for existing resources
/xc:tf generate http-lb my-lb

# Validate Terraform configuration
/xc:tf validate ./infrastructure/
```

---

### Q2 2025

#### f5xc-docs

Documentation and API reference lookup.

**Planned Features:**

- [ ] Inline documentation lookup
- [ ] API reference integration
- [ ] Example code generation
- [ ] Best practices suggestions

**Use Cases:**

```bash
# Lookup documentation
/xc:docs http-lb configuration

# Get API examples
/xc:docs api origin-pool create
```

---

#### f5xc-api

Direct API access for advanced automation.

**Planned Features:**

- [ ] REST API client
- [ ] GraphQL support
- [ ] Token management
- [ ] Rate limiting

**Use Cases:**

```bash
# Direct API call
/xc:api GET /config/namespaces

# Create via API
/xc:api POST /config/http_loadbalancers --data @config.json
```

---

### Future Considerations

#### f5xc-monitor

Monitoring and alerting integration.

- Performance metrics collection
- Alert threshold configuration
- Dashboard generation

#### f5xc-security

Security assessment and hardening.

- WAF policy analysis
- Security posture assessment
- Compliance checking

#### f5xc-migrate

Migration tooling for onboarding.

- Configuration import from other platforms
- DNS migration assistance
- Traffic cutover planning

## Feature Requests

Have an idea for a new plugin or feature? We'd love to hear it!

1. Check [existing issues](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues) for similar requests
2. [Open a new issue](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/issues/new) with your proposal
3. Include use cases and expected behavior

## Contributing

Want to help build these plugins? See our [Contributing Guide](contributing.md) to get started.

## Version History

See the [Changelog](https://github.com/robinmordasiewicz/f5-distributed-cloud-marketplace/blob/main/CHANGELOG.md) for detailed release notes.
