@echo off
echo Building and Deploying Todo Intelligence Platform to Minikube

REM Build Docker images for the application
echo Building Docker images for backend and frontend...
minikube image build -t todo-backend:latest ./backend
minikube image build -t todo-frontend:latest ./frontend

if %errorlevel% neq 0 (
    echo Failed to build Docker images
    pause
    exit /b 1
)

REM Create secrets for the application
echo Creating secrets for the application...
kubectl create secret generic todo-secrets ^
  --from-literal=openai-api-key="YOUR_OPENAI_API_KEY_HERE" ^
  --from-literal=openai-domain-key="YOUR_OPENAI_DOMAIN_KEY_HERE" ^
  --dry-run=client -o yaml | kubectl apply -f -

if %errorlevel% neq 0 (
    echo Failed to create secrets
    pause
    exit /b 1
)

REM Deploy the PostgreSQL database
echo Deploying PostgreSQL database...
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: todo_db
            - name: POSTGRES_USER
              value: todo_user
            - name: POSTGRES_PASSWORD
              value: todo_password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: default
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP
EOF

if %errorlevel% neq 0 (
    echo Failed to deploy PostgreSQL
    pause
    exit /b 1
)

REM Deploy the backend with Dapr sidecar
echo Deploying backend with Dapr sidecar...
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend-deployment
  namespace: default
  labels:
    app: todo-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/components-path: "/components"
        dapr.io/config: "app-config"
        dapr.io/log-as-json: "true"
        dapr.io/app-protocol: "http"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
        - name: todo-backend
          image: todo-backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              value: "postgresql://todo_user:todo_password@postgres-service:5432/todo_db"
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: openai-api-key
            - name: CORS_ORIGINS
              value: '["http://*", "https://*"]'
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
EOF

if %errorlevel% neq 0 (
    echo Failed to deploy backend
    pause
    exit /b 1
)

REM Deploy the frontend
echo Deploying frontend...
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend-deployment
  namespace: default
  labels:
    app: todo-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-frontend"
        dapr.io/app-port: "3000"
        dapr.io/components-path: "/components"
        dapr.io/config: "app-config"
        dapr.io/log-as-json: "true"
        dapr.io/app-protocol: "http"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
        - name: todo-frontend
          image: todo-frontend:latest
          ports:
            - containerPort: 3000
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "http://todo-backend-service:8000"
            - name: NEXT_PUBLIC_OPENAI_DOMAIN_KEY
              valueFrom:
                secretKeyRef:
                  name: todo-secrets
                  key: openai-domain-key
          livenessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
EOF

if %errorlevel% neq 0 (
    echo Failed to deploy frontend
    pause
    exit /b 1
)

REM Create services for the deployments
echo Creating services for backend and frontend...
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
  namespace: default
spec:
  selector:
    app: todo-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend-service
  namespace: default
spec:
  selector:
    app: todo-frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
EOF

if %errorlevel% neq 0 (
    echo Failed to create services
    pause
    exit /b 1
)

REM Create Dapr components for State, Pub/Sub, Bindings, and Secrets
echo Creating Dapr components...
kubectl apply -f - <<EOF
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
EOF

kubectl apply -f - <<EOF
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
EOF

kubectl apply -f - <<EOF
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
EOF

kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: app-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
EOF

echo.
echo Application deployed successfully!
echo Backend URL: http://(minikube ip):8000
echo Frontend URL: http://(minikube ip):3000
echo.
pause