@echo off
echo Setting up Minikube and Dapr for the Todo Intelligence Platform

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop before continuing.
    echo Visit: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker is running, proceeding with Minikube setup...

REM Start Minikube with Docker driver
echo Starting Minikube with Docker driver...
minikube start --driver=docker

if %errorlevel% neq 0 (
    echo Failed to start Minikube
    pause
    exit /b 1
)

REM Enable required Minikube addons
minikube addons enable ingress
minikube addons enable registry

echo Installing Dapr runtime to Kubernetes cluster...
dapr init -k --enable-ha=true --enable-mtls=true

if %errorlevel% neq 0 (
    echo Failed to install Dapr
    pause
    exit /b 1
)

echo Dapr installation completed successfully!

REM Verify Dapr installation
kubectl get pods -n dapr-system

echo.
echo Setup complete! Minikube is running with Dapr.
echo To access the dashboard, run: dapr dashboard -k
echo.
pause