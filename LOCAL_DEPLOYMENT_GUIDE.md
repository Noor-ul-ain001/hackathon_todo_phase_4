# Todo Intelligence Platform - Local Deployment with Dapr on Minikube

This guide explains how to deploy the Todo Intelligence Platform locally using Minikube and Dapr with full capabilities: Pub/Sub, State Management, Bindings (cron), Secrets, and Service Invocation.

## Prerequisites

Before starting, ensure you have the following installed:

- Docker Desktop (with Hyper-V or WSL2 backend)
- Minikube
- kubectl
- Dapr CLI
- Git

## Step-by-Step Deployment

### 1. Start Docker Desktop

Make sure Docker Desktop is running before proceeding with Minikube startup.

### 2. Run the Setup Script

Execute the setup script to initialize Minikube and install Dapr:

```bash
setup-minikube-dapr.bat
```

This script will:
- Verify Docker is running
- Start Minikube with the Docker driver
- Install Dapr runtime to the Kubernetes cluster
- Enable high availability and mTLS

### 3. Deploy the Application

Once Minikube and Dapr are running, deploy the application:

```bash
deploy-app.bat
```

This script will:
- Build Docker images for the backend and frontend
- Create necessary secrets
- Deploy PostgreSQL database
- Deploy backend and frontend with Dapr sidecars
- Create services for accessing the applications
- Configure Dapr components for all required capabilities

### 4. Test Dapr Capabilities

After deployment, test all Dapr capabilities:

```bash
test-dapr-capabilities.bat
```

This script will test:
- Service Invocation
- State Management
- Pub/Sub
- Bindings
- Secrets Management

## Dapr Components Configuration

The deployment includes the following Dapr components:

### State Management
- Component: `statestore`
- Type: `state.redis`
- Used for storing and retrieving application state

### Pub/Sub (Publish/Subscribe)
- Component: `pubsub`
- Type: `pubsub.redis`
- Used for event-driven communication between services

### Bindings (Cron)
- Component: `cron-binding`
- Type: `bindings.cron`
- Used for scheduled tasks and periodic operations

### Secrets Management
- Integrated with Kubernetes secrets
- Secure access to sensitive information

### Service Invocation
- Enabled by default with Dapr sidecars
- Allows services to communicate securely with automatic mTLS

## Accessing the Applications

After successful deployment:

- Frontend: Access via `minikube service todo-frontend-service` to get the URL
- Backend: Available internally at `http://todo-backend-service:8000`

## Troubleshooting

### Common Issues

1. **Minikube won't start**: Ensure Docker Desktop is running and you have sufficient resources allocated.

2. **Dapr not initializing**: Check that Kubernetes cluster is accessible and you have cluster-admin rights.

3. **Images not building**: Ensure you're in the correct directory and have Docker access.

4. **Services not accessible**: Use `minikube service list` to see available services and their URLs.

### Useful Commands

```bash
# Check Minikube status
minikube status

# Check Dapr status
dapr status -k

# View Dapr sidecar logs
kubectl logs -l app=todo-backend -c daprd
kubectl logs -l app=todo-frontend -c daprd

# Access Dapr dashboard
dapr dashboard -k

# Get service URLs
minikube service todo-frontend-service --url
```

## Architecture Overview

The deployed system consists of:

- **Frontend**: Next.js application with Dapr sidecar
- **Backend**: Python/FastAPI application with Dapr sidecar
- **Database**: PostgreSQL for persistent storage
- **Dapr Sidecars**: Providing distributed capabilities
- **Dapr Components**: Configured for state, pub/sub, bindings, and secrets

This setup enables all required Dapr capabilities:
- Service Invocation for inter-service communication
- State Management for storing application state
- Pub/Sub for event-driven architecture
- Bindings for integration with external systems
- Secrets Management for secure access to sensitive data