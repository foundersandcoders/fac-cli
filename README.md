# Kiro AI IDE Project

A modern development environment with intelligent automation, spec-driven development, and comprehensive tooling.

## Project Overview

This project demonstrates the capabilities of Kiro AI IDE-style development with:
- **Spec-driven development** using EARS format requirements
- **Automated code review** and quality assurance
- **Intelligent test generation** for multiple languages
- **Security scanning** and vulnerability detection
- **Clean architecture** patterns with functional programming

## Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git for version control

### Setup
```bash
# Clone the repository  
git clone <repository-url>
cd fac-cli

# Install Python dependencies
pip install -r requirements.txt

# Configure Airtable credentials
cp .env.example .env
# Edit .env file with your Airtable API key and view URL

# Test the CLI
./fac.py help
./fac.py gr  # Fetch gateway recent data
```

### Airtable Configuration
1. Get your Airtable API key from https://airtable.com/create/tokens
2. Navigate to your Airtable view and copy the URL (e.g., `https://airtable.com/appEXAMPLE123456/tblEXAMPLE789012/viwEXAMPLE345678`)
3. Add both to your `.env` file - the CLI automatically converts user-friendly URLs to API format

## Project Structure

```
/
├── .kiro/                     # Kiro AI IDE configuration
│   ├── config.json           # Main configuration
│   ├── hooks/                # Automated development hooks
│   │   ├── code-review.sh    # Automated code review
│   │   ├── test-generator.sh # Test generation
│   │   └── security-scanner.sh # Security analysis
│   └── steering/             # Code generation standards
│       └── code-standards.md # Coding standards and patterns
├── src/                      # Source code (Clean Architecture)
│   ├── domain/              # Core business logic
│   ├── application/         # Use cases and orchestration
│   ├── infrastructure/      # External interfaces
│   └── presentation/        # User interfaces
├── tests/                   # Test files
├── docs/                    # Documentation
├── requirements.md          # EARS format requirements
├── design.md               # Architecture specification
├── tasks.md                # Implementation roadmap
└── README.md               # This file
```

## Development Workflow

### 1. Spec-Driven Development
- Requirements are defined in `requirements.md` using EARS format
- Architecture is documented in `design.md`
- Implementation follows the roadmap in `tasks.md`

### 2. Automated Quality Assurance
```bash
# Run automated code review
.kiro/hooks/code-review.sh src/module.js

# Generate tests for new code
.kiro/hooks/test-generator.sh src/new-feature.py

# Run security scan
.kiro/hooks/security-scanner.sh .
```

### 3. Testing Strategy
- **Test-Driven Development**: Write failing tests first
- **90%+ Coverage**: Comprehensive test coverage required
- **Multiple Test Types**: Unit, integration, and end-to-end tests
- **Automated Generation**: Tests auto-generated for new code

### 4. Code Quality Standards
- **Functional Programming**: Preferred over object-oriented patterns
- **Pure Functions**: Side-effect free when possible
- **Immutable Data**: Avoid mutation, use immutable structures
- **Clean Architecture**: Clear separation of concerns
- **Security First**: Built-in security scanning and best practices

## Available Commands

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run test suite
npm run test:watch   # Watch mode testing
npm run lint         # Code linting
npm run format       # Code formatting

# Quality Assurance
make review          # Run code review
make test-gen        # Generate missing tests
make security        # Security scan
make quality         # Full quality check

# Deployment
make deploy-staging  # Deploy to staging
make deploy-prod     # Deploy to production
```

## Kiro AI IDE Features

### Agent Hooks
Automated actions triggered by development events:
- **Code Review**: Intelligent analysis of code changes
- **Test Generation**: Automatic test creation for new code
- **Security Scanning**: Vulnerability detection and prevention
- **Documentation**: Auto-generated API docs and guides

### Steering System
AI-guided development following established patterns:
- **Architecture Patterns**: Clean architecture, functional programming
- **Naming Conventions**: Consistent across languages and frameworks
- **Quality Gates**: Automated quality checks and enforcement
- **Best Practices**: Security, performance, and maintainability

### Autonomous Behavior
Proactive development assistance:
- **Context Awareness**: Understanding of full codebase context
- **Cross-File Refactoring**: Intelligent code modifications
- **Dependency Management**: Automated dependency updates
- **Performance Optimization**: Proactive performance improvements

## Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

- **Domain Layer**: Core business logic and rules
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External dependencies and I/O
- **Presentation Layer**: User interfaces and APIs

### Design Patterns
- **Functional Programming**: Immutable data, pure functions
- **Dependency Injection**: Loose coupling, testable code
- **Repository Pattern**: Data access abstraction
- **Command Query Responsibility Segregation (CQRS)**: When applicable

## Testing

### Test Structure
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests
├── e2e/           # End-to-end user scenarios
├── performance/   # Performance and load tests
└── security/      # Security-specific tests
```

### Test Standards
- **Arrange-Act-Assert**: Clear test structure
- **Descriptive Names**: Test names should read like specifications
- **Edge Cases**: Comprehensive edge case coverage
- **Error Scenarios**: Test error handling and recovery

## Security

### Built-in Security Features
- **Input Validation**: All inputs validated and sanitised
- **Secret Management**: No hardcoded secrets, environment variables used
- **Secure Communications**: HTTPS/TLS for all network traffic
- **Dependency Scanning**: Regular vulnerability scans
- **Access Control**: Role-based permissions where applicable

### Security Practices
- Regular security scans using `.kiro/hooks/security-scanner.sh`
- Automated dependency vulnerability checks
- Code review for security implications
- Penetration testing for critical components

## Performance

### Performance Targets
- **API Response Time**: < 100ms (95th percentile)
- **Page Load Time**: < 2 seconds first contentful paint
- **Test Suite Runtime**: < 30 seconds full suite
- **Build Time**: < 60 seconds production build

### Optimization Strategies
- Caching at multiple levels
- Database query optimization
- Code splitting and lazy loading
- Performance monitoring and alerting

## Contributing

### Development Process
1. **Review Requirements**: Check `requirements.md` for current specifications
2. **Follow Architecture**: Adhere to patterns in `design.md`
3. **Write Tests First**: Test-driven development required
4. **Run Quality Checks**: Use automated hooks for review
5. **Update Documentation**: Keep docs synchronized with code

### Code Review Checklist
- [ ] Follows coding standards in `.kiro/steering/code-standards.md`
- [ ] Includes comprehensive tests (90%+ coverage)
- [ ] Passes security scan
- [ ] Updates relevant documentation
- [ ] Follows conventional commit messages

## Monitoring and Observability

### Metrics Collection
- Application performance metrics
- Business intelligence metrics
- Infrastructure and system metrics
- User experience metrics

### Logging Strategy
- Structured logging (JSON format)
- Correlation IDs for request tracing
- Appropriate log levels (ERROR, WARN, INFO, DEBUG)
- No sensitive data in logs

## Deployment

### Environments
- **Development**: Local development with hot reload
- **Testing**: Automated CI/CD testing environment
- **Staging**: Production-like integration testing
- **Production**: Live system with full monitoring

### Deployment Strategy
- Blue-green deployments for zero downtime
- Feature flags for gradual rollouts
- Automated rollback capabilities
- Health checks and monitoring

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions:
- Review the documentation in `/docs`
- Check the issue tracker
- Follow the contributing guidelines
- Contact the development team

---

*This project demonstrates advanced development practices using Kiro AI IDE-style automation and intelligent development workflows.*