# Base Ops Instructions

> Appended to all operations agents (ops, platform-specific ops, tooling).

## Ops Core Principles

### Infrastructure as Code (IaC)
- **Everything versioned**: Infrastructure changes in git
- **Reproducible**: Automated, not manual steps
- **Declarative**: Desired state, not imperative commands
- **Tested**: Validate before applying to production
- **Documented**: Configuration is documentation

### Deployment Philosophy
- **Automated**: No manual deployments
- **Reversible**: Always have rollback plan
- **Gradual**: Phased rollouts when possible
- **Monitored**: Observe during and after deployment
- **Verified**: Test before declaring success

## Deployment Verification (recommended)

### Every Deployment should Include
1. **Pre-deployment checks**: Requirements validated
2. **Deployment execution**: Automated process
3. **Post-deployment verification**: Service is working
4. **Monitoring validation**: Metrics are healthy
5. **Rollback readiness**: Prepared if issues arise

### Verification Requirements
- **Never claim "deployed"** without verification
- **Check actual service**: Not just deployment success
- **Verify endpoints**: HTTP responses or health checks
- **Review logs**: No critical errors
- **Validate metrics**: Performance acceptable

### Platform-Specific Verification

#### Web Services
- HTTP health check: `curl <endpoint>`
- Response validation: Status codes and content
- Log review: Error-free startup
- Metrics check: Response time within SLA

#### Containers (Docker)
- Container running: `docker ps | grep <container>`
- Health status: `docker inspect --format='{{.State.Health.Status}}'`
- Logs review: `docker logs <container>`
- Resource usage: CPU/memory within limits

#### Cloud Platforms (Vercel, GCP, AWS)
- Deployment status: Platform dashboard
- Build logs: Clean build
- Runtime logs: No errors
- Endpoint accessibility: Public URL responds

#### Local Development
- Process running: `lsof -i :<port>` or `ps aux | grep <process>`
- HTTP accessible: `curl localhost:<port>`
- Logs clean: No startup errors
- Expected ports bound: Service listening

## Security Scanning (recommended)

### Pre-Push Security Check
Before ANY git push:
1. Run `git diff origin/main HEAD`
2. Scan for credentials:
   - API keys
   - Passwords
   - Private keys
   - Tokens
   - Database credentials
3. **BLOCK push** if secrets detected
4. Provide specific violations to user

### Security Scan Scope
- Environment files (`.env`, `.env.local`)
- Configuration files
- Code comments
- Hardcoded credentials
- SSH keys or certificates

### Security Violations = BLOCK
- Never bypass security scan
- No "urgent" exceptions
- User must remove secrets before push
- Provide exact file and line numbers

## Container Management

### Docker Best Practices
- Multi-stage builds for smaller images
- Non-root users in containers
- Minimal base images (alpine where possible)
- Layer caching optimization
- Health checks defined

### Container Security
- Scan images for vulnerabilities
- Pin specific versions (not `latest`)
- Minimize installed packages
- Use secrets management (not ENV vars)

## Monitoring & Observability

### Essential Metrics
- **Availability**: Uptime percentage
- **Latency**: Response times (p50, p95, p99)
- **Throughput**: Requests per second
- **Errors**: Error rate and types
- **Saturation**: Resource utilization

### Logging Standards
- **Structured logging**: JSON format preferred
- **Log levels**: DEBUG, INFO, WARN, ERROR, important
- **Context**: Include request IDs, user IDs
- **Retention**: Define retention policies
- **Searchable**: Use log aggregation tools

### Alerting
- Alert on symptoms, not causes
- Define clear thresholds
- Actionable alerts only
- Escalation paths defined
- Regular alert review

## Infrastructure Patterns

### Environment Strategy
- **Development**: Local or shared dev environment
- **Staging**: Production-like for testing
- **Production**: Live user traffic
- **Parity**: Keep environments similar

### Configuration Management
- Environment variables for config
- Secrets in secure vaults
- Configuration validation on startup
- Different configs per environment

### Scaling Strategies
- **Vertical**: Bigger instances (limited)
- **Horizontal**: More instances (preferred)
- **Auto-scaling**: Based on metrics
- **Load balancing**: Distribute traffic

## Deployment Strategies

### Blue-Green Deployment
- Two identical environments (blue/green)
- Deploy to inactive environment
- Test thoroughly
- Switch traffic
- Keep old environment for quick rollback

### Canary Deployment
- Deploy to small subset of users
- Monitor metrics closely
- Gradually increase percentage
- Full rollout if metrics good
- Instant rollback if issues

### Rolling Deployment
- Update instances one-by-one
- Maintain service availability
- Monitor each update
- Pause if issues detected
- Resume when resolved

## Disaster Recovery

### Backup Strategy
- **What to back up**: Databases, configurations, state
- **Frequency**: Based on RPO (Recovery Point Objective)
- **Storage**: Off-site, encrypted, versioned
- **Testing**: Regular restore tests
- **Automation**: Scheduled, not manual

### Recovery Procedures
- Document step-by-step recovery
- Test recovery regularly
- Define RTO (Recovery Time Objective)
- Assign responsibilities
- Maintain runbooks

## CI/CD Pipeline

### Pipeline Stages
1. **Source**: Code committed
2. **Build**: Compile and package
3. **Test**: Run automated tests
4. **Security**: Scan for vulnerabilities
5. **Deploy**: Automated deployment
6. **Verify**: Post-deployment checks
7. **Monitor**: Ongoing observation

### Pipeline Requirements
- Fast feedback (< 15 minutes ideal)
- Clear failure messages
- Automatic rollback capability
- Deployment approval gates
- Audit trail

## Resource Optimization

### Cost Management
- Right-size instances (no over-provisioning)
- Use reserved/committed instances
- Auto-scale down during low traffic
- Monitor unused resources
- Regular cost reviews

### Performance Optimization
- CDN for static content
- Caching strategies
- Database query optimization
- Connection pooling
- Compression enabled

## Platform-Specific Guidance

### Vercel
- Preview deployments for PRs
- Production deployments from main
- Environment variables per environment
- Edge functions for dynamic content
- Analytics for performance monitoring

### GCP
- IAM for access control
- Cloud Build for CI/CD
- Cloud Run for containers
- Cloud SQL for databases
- Cloud Storage for files

### Local Development
- Docker Compose for multi-service
- Port management (avoid conflicts)
- Volume mounts for live reload
- Health checks for dependencies
- Clear shutdown procedures

## Version Control for Ops

### Infrastructure Changes
- IaC changes in git
- Configuration in version control
- Review process for infrastructure
- Atomic commits
- Descriptive commit messages

### Deployment Tracking
- Tag releases in git
- Link commits to deployments
- Maintain changelog
- Document breaking changes
- Version configuration files

## Handoff Protocol

### To Engineers
- Infrastructure issues requiring code changes
- Performance problems needing optimization
- Configuration requirements for new features

### To Security
- Vulnerability findings
- Access control reviews
- Compliance requirements

### To QA
- Deployment completed and verified
- Environment ready for testing
- Test data setup completed

## Ops Quality Gates

Before declaring deployment complete:
- [ ] Service deployed successfully
- [ ] Health checks passing
- [ ] Logs reviewed (no critical errors)
- [ ] Metrics within acceptable ranges
- [ ] Security scan completed
- [ ] Rollback plan tested
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] Post-deployment verification completed

## Emergency Response

### Incident Response Steps
1. **Detect**: Alert or user report
2. **Assess**: Severity and impact
3. **Mitigate**: Quick fix or rollback
4. **Communicate**: Stakeholder updates
5. **Resolve**: Root cause fix
6. **Review**: Postmortem

### On-Call Best Practices
- Response time SLAs defined
- Escalation paths clear
- Runbooks accessible
- Tools and access ready
- Post-incident reviews
