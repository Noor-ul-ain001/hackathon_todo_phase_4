# Check Dapr status (not waiting for full health)
Write-Host "Checking Dapr status..."
Start-Sleep -Seconds 30

# Check if Dapr pods are at least running (even if not fully healthy)
kubectl get pods -n dapr-system

Write-Host "`nProceeding with application deployment regardless of Dapr health status..."

# Create temporary files for k8s manifests
$pgManifest = @"
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
"@

# Write the manifest to a temporary file and apply it
$tempPgFile = [System.IO.Path]::GetTempFileName() + ".yaml"
$pgManifest | Out-File -FilePath $tempPgFile -Encoding UTF8
kubectl apply -f $tempPgFile
Remove-Item $tempPgFile

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

# Create secrets for the application
Write-Host "Creating secrets for the application..."
kubectl create secret generic todo-secrets `
  --from-literal=openai-api-key="YOUR_OPENAI_API_KEY_HERE" `
  --from-literal=openai-domain-key="YOUR_OPENAI_DOMAIN_KEY_HERE" `
  --dry-run=client -o yaml | kubectl apply -f -

# Build Docker images for the application
Write-Host "Building Docker images for backend and frontend..."
minikube image build -t todo-backend:latest ./backend
minikube image build -t todo-frontend:latest ./frontend

$backendManifest = @"
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
---
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
"@

# Write the backend manifest to a temporary file and apply it
$tempBackendFile = [System.IO.Path]::GetTempFileName() + ".yaml"
$backendManifest | Out-File -FilePath $tempBackendFile -Encoding UTF8
kubectl apply -f $tempBackendFile
Remove-Item $tempBackendFile

$frontendManifest = @"
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
"@

# Write the frontend manifest to a temporary file and apply it
$tempFrontendFile = [System.IO.Path]::GetTempFileName() + ".yaml"
$frontendManifest | Out-File -FilePath $tempFrontendFile -Encoding UTF8
kubectl apply -f $tempFrontendFile
Remove-Item $tempFrontendFile

# Create Dapr components for State, Pub/Sub, Bindings, and Secrets
Write-Host "Creating Dapr components..."
kubectl apply -f ./components/statestore.yaml
kubectl apply -f ./components/pubsub.yaml
kubectl apply -f ./components/cron-binding.yaml
kubectl apply -f ./components/app-config.yaml

Write-Host "`nWaiting for application pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=180s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=180s

Write-Host "`nApplication deployed!"
Write-Host "`nTo check the status of your pods: kubectl get pods"
Write-Host "To check the status of Dapr: dapr status -k"
Write-Host "To get the frontend URL: minikube service todo-frontend-service --url"
Write-Host "`nNote: Dapr components may still be initializing. This can take several minutes."
Write-Host "Monitor the Dapr pods with: kubectl get pods -n dapr-system"
Write-Host "`nPress any key to continue..."
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")