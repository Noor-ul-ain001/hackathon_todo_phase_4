@echo off
echo Testing Dapr Capabilities

echo Waiting for all pods to be ready...
kubectl wait --for=condition=ready pod --all --timeout=300s

echo.
echo 1. Testing Service Invocation...
curl -v http://todo-backend-service:8000/health

echo.
echo 2. Testing State Management...
dapr state get --app-id todo-backend --key test-state

echo.
echo 3. Testing Pub/Sub (Publishing a message)...
curl -X POST http://localhost:3500/v1.0/publish/pubsub/my-topic -H "Content-Type: application/json" -d '{"message": "Hello Dapr"}'

echo.
echo 4. Testing Bindings (Triggering a binding)...
curl -X POST http://localhost:3500/v1.0/bindings/cron-binding -H "Content-Type: application/json" -d '{"data": {"operation": "create"}}'

echo.
echo 5. Testing Secrets Management...
dapr get secret --app-id todo-backend --key openai-api-key

echo.
echo 6. Checking Dapr sidecar logs...
kubectl logs deployment/todo-backend-deployment -c daprd
kubectl logs deployment/todo-frontend-deployment -c daprd

echo.
echo All Dapr capabilities tested!
pause