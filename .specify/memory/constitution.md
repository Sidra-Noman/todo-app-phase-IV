<!--
Sync Impact Report:
- Version change: 2.0.1 → 3.0.0 (major update for Phase IV cloud-native deployment principles)
- Modified principles: Updated from Phase III AI-focused to Phase IV cloud-native Kubernetes deployment
- Added sections: Infrastructure & Orchestration, Docker AI (Gordon) integration, Helm chart deployment
- Removed sections: Some Phase III specific constraints that don't apply to Phase IV
- Templates requiring updates: ⚠ pending plan-template.md, spec-template.md, tasks-template.md
- Follow-up TODOs: None
-->

# Todo App Constitution - Phase IV (Local Kubernetes Deployment)

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Spec-first approach: Specification → Plan → Tasks → Implement.
All development MUST follow the spec → plan → tasks → implement sequence.
Changes to scope MUST go through specification updates first.

Rationale: Ensures clear requirements understanding, prevents scope creep,
and maintains architectural coherence across the team and tools.

### II. Cloud-Native Deployment Architecture

Deployment MUST leverage local Kubernetes (Minikube) for container orchestration.
All services MUST be packaged as containerized applications using Docker.
Frontend and backend services MUST be deployed as separate, independently scalable units.
The application stack MUST support deterministic, reproducible deployment patterns.

Rationale: Enables scalable, resilient infrastructure with consistent deployment
across environments and supports modern DevOps practices for operational excellence.

### III. Containerized Service Architecture

All services MUST be containerized using Docker.
Container images MUST be versioned and stateless.
Services MUST be designed for horizontal scaling and fault tolerance.
Docker AI (Gordon) MAY be leveraged for AI-assisted containerization processes.

Rationale: Ensures consistent environments across development, testing, and production,
enables efficient resource utilization, and supports rapid deployment and scaling.

### IV. Infrastructure as Code

Kubernetes deployments MUST use Helm charts for packaging and deployment.
Configuration MUST be managed through Kubernetes ConfigMaps and Secrets.
Deployment manifests MUST be version-controlled alongside application code.
kubectl-ai/Kagent MAY be leveraged for AI-assisted DevOps operations.

Rationale: Enables repeatable, auditable deployments with proper configuration
management and supports collaboration across development and operations teams.

### V. Deterministic and Reproducible Deployments

All deployment processes MUST be deterministic and reproducible.
Build and deployment pipelines MUST produce identical results for identical inputs.
Versioned artifacts MUST be used for all deployments.
Rollback procedures MUST be tested and available for all deployments.

Rationale: Ensures deployment reliability, enables confidence in release processes,
and maintains consistent system behavior during changes.

## AI & Model Standards

### Cohere Integration Requirements

The AI-powered chatbot from Phase III MUST continue to use Cohere as the AI model provider exclusively.
Cohere API key is the single source of AI authentication and authorization.
OpenAI Agents SDK patterns MAY be followed conceptually, but all model calls
MUST be executed via Cohere's API directly.
AI components MUST interact with the system only through MCP tools.
AI components MUST NEVER directly access the database or backend services directly.

Rationale: Maintains consistent AI provider strategy, ensures proper
abstraction layers, and provides security isolation between AI and data layers.

### AI Call Execution Standards

All AI calls MUST be executed via the backend services only.
All model requests MUST be traceable to authenticated users.
Backend services MUST maintain the same AI integration patterns established in Phase III.
Conversation state from the AI chatbot MUST persist to PostgreSQL as established in Phase III.

Rationale: Preserves established AI integration patterns, maintains security boundaries,
and ensures proper audit trails for AI interactions in the cloud-native environment.

## Infrastructure & Orchestration

### Kubernetes Deployment Requirements

Kubernetes (Minikube) MUST be used for the local cluster environment.
Helm charts MUST be used for deploying frontend, backend, and MCP server components.
All services MUST be configured for stateless operation except for PostgreSQL.
Service discovery MUST be handled through Kubernetes DNS.
Network policies SHOULD be implemented to control service-to-service communication.

Rationale: Establishes standardized deployment approach, ensures consistent
infrastructure patterns, and enables proper service isolation in the containerized environment.

### Docker AI (Gordon) and AI-Assisted DevOps

Docker AI (Gordon) MUST be leveraged for containerization processes where appropriate.
kubectl-ai/Kagent MAY be used for AI-assisted Kubernetes operations.
AI-assisted DevOps tools SHOULD be used to streamline deployment and management tasks.
Container build processes SHOULD incorporate AI assistance for optimization.

Rationale: Leverages AI capabilities to enhance DevOps efficiency while
maintaining proper oversight and governance of infrastructure operations.

### Container Image Standards

All container images MUST be versioned with semantic versioning.
Container images MUST be stateless with no persistent data stored within containers.
Image build processes MUST be reproducible and deterministic.
Images MUST be scanned for vulnerabilities before deployment.

Rationale: Ensures consistent, secure, and manageable container images
that support reliable deployment and scaling in the Kubernetes environment.

## Security & Authentication

### Identity and Access Control

User identity MUST be derived exclusively from Better Auth authentication system.
All services MUST respect the same authentication and authorization controls.
Better Auth integration MUST be properly configured in the containerized environment.
Authentication state MUST be properly managed across containerized services.

Rationale: Maintains data privacy, prevents unauthorized access,
and ensures authentication security is preserved in the cloud-native deployment.

### Container and Cluster Security

Container images MUST run with minimal required privileges.
Kubernetes RBAC policies MUST be implemented to control access to cluster resources.
Secrets MUST be managed through Kubernetes Secrets, not environment variables.
Network encryption MUST be enforced for service-to-service communication.

Rationale: Protects the containerized infrastructure from security vulnerabilities
and ensures proper access controls across the Kubernetes cluster.

## Constraints

### Development Methodology

- NO manual deployment configurations outside of Helm charts and Kubernetes manifests
- NO direct Kubernetes imperative commands for production deployments
- NO hardcoded environment-specific configurations in application code
- NO persistent data stored in application containers
- NO bypassing of CI/CD processes for deployments
- NO manual intervention in cluster configuration without proper documentation

Rationale: Maintains consistency with cloud-native deployment methodology,
ensures infrastructure as code principles, and prevents configuration drift
that could compromise deployment reliability.

### Infrastructure Scope Limitations

Kubernetes deployment is limited to Minikube for local development and testing.
Production deployment considerations are explicitly out of scope for this phase.
Advanced Kubernetes features like custom controllers are out of scope.
Only essential services (frontend, backend, MCP server, PostgreSQL) are to be containerized.

Rationale: Maintains focus on core requirements, prevents infrastructure complexity,
and ensures the cloud-native deployment remains manageable and testable.

## Success Criteria

### Functional Requirements

- Application MUST successfully deploy to Minikube using Helm charts
- Frontend and backend services MUST be properly containerized and accessible
- Existing AI chatbot functionality from Phase III MUST continue to operate correctly
- Database connectivity MUST work properly in the containerized environment
- All services MUST scale appropriately in the Kubernetes environment
- MCP tools from Phase III MUST remain functional in the containerized setup

Rationale: Defines measurable outcomes that validate successful implementation
of the cloud-native Kubernetes deployment while maintaining system integrity and functionality.

### Operational Requirements

- Deployment process MUST be reproducible and documented
- Services MUST recover automatically from container failures
- Resource utilization MUST be within acceptable limits
- Network connectivity between services MUST be properly configured
- Authentication via Better Auth MUST work correctly in containerized environment
- Database persistence MUST survive container restarts

Rationale: Ensures the deployed system meets operational standards for
reliability, performance, and maintainability in the Kubernetes environment.

## Governance

This constitution serves as the authoritative technology policy for the project.
All development decisions MUST comply with these principles.
Infrastructure-related decisions require special scrutiny to ensure compliance with
cloud-native, security, and deployment principles outlined above.

**Amendment Procedure**:
1. Proposed amendments MUST be documented with rationale
2. Infrastructure-related amendments require explicit consent from project stakeholders
3. Breaking changes to deployment or security principles require full team review
4. Amendments take effect upon merge to the main branch

**Compliance**:
- All design documents (plan.md) MUST include a Constitution Check section
- Features that violate infrastructure or security principles MUST be rejected
- Periodic reviews ensure ongoing alignment with these principles
- Helm chart and Kubernetes manifest designs MUST be reviewed for constitutional compliance

**Supremacy**: This constitution supersedes all other development practices and guidelines.

**Version**: 3.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-28