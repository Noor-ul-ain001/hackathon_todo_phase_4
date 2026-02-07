# Dapr Components for Todo Intelligence Platform

This directory contains Dapr component configurations for the Todo Intelligence Platform.

## Components Included

### 1. State Store
Configures Redis as the state store for managing application state.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

### 2. Pub/Sub
Configures Redis as the message broker for publish/subscribe messaging.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

### 3. Cron Binding
Configures a cron binding for scheduled tasks.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: cron-binding
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "@every 30s"
```

### 4. App Configuration
Configuration for Dapr runtime features.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: app-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
  httpPipeline:
    handlers: []
  features:
    - name: InputBindingInvocation
      enabled: true
```

## Deployment Notes

These components will be deployed as part of the application deployment process. The deployment scripts handle creating these components in the Kubernetes cluster.

For local development, you can apply these components manually using:

```bash
kubectl apply -f dapr-components/
```

Each component is configured to work with the deployed infrastructure and integrates with the application services.