# Data Model: Kubernetes Containerization for Todo App

## Overview
This document describes the data model and entity relationships for the containerized Todo application. Since Phase IV focuses on deployment and orchestration rather than data model changes, this document primarily defines the configuration and deployment entities used in the Kubernetes environment.

## Kubernetes Configuration Entities

### Helm Chart Configuration
- **Name**: Unique identifier for the Helm chart
- **Version**: Semantic version of the chart
- **Description**: Human-readable description of the chart's purpose
- **Dependencies**: List of chart dependencies with version constraints
- **Parameters**: Configurable values that can be overridden during installation

### Kubernetes Deployment Configuration
- **Name**: Name of the deployment resource
- **Replicas**: Desired number of pod replicas
- **Image**: Container image reference with tag
- **Environment Variables**: Configuration parameters passed to the container
- **Resources**: CPU and memory limits/requests
- **Health Probes**: Liveness and readiness probe configurations

### Kubernetes Service Configuration
- **Name**: Name of the service resource
- **Type**: Service type (ClusterIP, NodePort, LoadBalancer)
- **Ports**: Port mappings from service to pod
- **Selector**: Labels used to identify target pods
- **External Access**: Configuration for external traffic routing

### Kubernetes ConfigMap
- **Name**: Name of the ConfigMap resource
- **Data**: Key-value pairs of configuration data
- **Binary Data**: Binary configuration data (if applicable)
- **Labels**: Metadata for resource identification
- **Annotations**: Additional metadata for tooling

### Kubernetes Secret
- **Name**: Name of the Secret resource
- **Data**: Base64-encoded sensitive data
- **Type**: Secret type (Opaque, kubernetes.io/tls, etc.)
- **String Data**: Plaintext sensitive data (stored as base64 encoded)
- **Labels**: Metadata for resource identification

## Container Configuration Entities

### Docker Image Configuration
- **Base Image**: Parent image for the container
- **Exposed Ports**: Ports available from the container
- **Environment Variables**: Default configuration parameters
- **Volumes**: Mount points for persistent storage
- **Health Checks**: Commands to verify container health

### Environment-Specific Configuration
- **Database URL**: Connection string for PostgreSQL database
- **API Keys**: Authentication tokens for external services (Cohere, etc.)
- **Feature Flags**: Boolean flags to enable/disable features
- **Service Endpoints**: URLs of dependent services
- **Resource Limits**: Memory and CPU allocation constraints

## Deployment Parameters

### Scaling Configuration
- **Min Replicas**: Minimum number of running instances
- **Max Replicas**: Maximum number of running instances
- **CPU Threshold**: CPU utilization percentage that triggers scaling
- **Memory Threshold**: Memory utilization percentage that triggers scaling
- **Scaling Policy**: Rules governing scaling behavior

### Security Configuration
- **Image Pull Policy**: When to pull container images
- **Security Context**: User ID, group ID, and privilege settings
- **Network Policies**: Rules for inter-service communication
- **RBAC Permissions**: Role-based access control settings
- **TLS Configuration**: Certificate and encryption settings

## Relationships

### Helm Chart Relationships
- A Helm chart contains multiple Kubernetes resources (Deployments, Services, ConfigMaps, Secrets)
- Values from Helm parameters are applied to Kubernetes resource templates
- Dependencies between charts are defined in Chart.yaml

### Kubernetes Resource Relationships
- Deployments create and manage Pods
- Services route traffic to Pods based on selectors
- ConfigMaps and Secrets provide configuration to Pods
- PersistentVolumeClaims connect Pods to storage

### Configuration Hierarchy
- Global configuration settings affect all environments
- Environment-specific overrides modify global defaults
- Pod-level environment variables take precedence over ConfigMaps
- Command-line arguments override all other configuration sources

## Validation Rules

### Helm Chart Validation
- Chart version must follow semantic versioning
- Required parameters must be provided
- Dependency versions must satisfy constraints
- Template syntax must be valid

### Kubernetes Resource Validation
- Resource names must follow DNS-1123 naming conventions
- Required fields must be present in resource definitions
- Resource quotas must not exceed cluster limits
- Security policies must be satisfied

### Container Configuration Validation
- Image references must be valid
- Exposed ports must be in valid range (1-65535)
- Environment variable names must be valid identifiers
- Resource limits must not exceed cluster capacity

## State Transitions

### Deployment States
- **Pending**: Deployment created but not yet scheduled
- **Running**: Deployment has active pods
- **Scaled Down**: Deployment has reduced replica count
- **Failed**: Deployment has encountered an error
- **Terminated**: Deployment has been deleted

### Pod States
- **Pending**: Pod accepted but not all containers running
- **Running**: Pod bound to node and all containers running
- **Succeeded**: All containers terminated successfully
- **Failed**: At least one container terminated with error
- **Unknown**: State could not be obtained

### Service States
- **Active**: Service is routing traffic to pods
- **Inactive**: Service exists but no active endpoints
- **Updating**: Service configuration is being modified
- **Deleting**: Service is being removed