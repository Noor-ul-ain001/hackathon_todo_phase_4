@echo off
echo Starting Minikube with adjusted settings to match Docker's current memory allocation...

REM Start Minikube with settings that should work with your current Docker configuration
minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=15g

if %errorlevel% neq 0 (
    echo Failed to start Minikube with adjusted settings
    echo Please ensure Docker Desktop is running and has sufficient resources allocated
    echo Recommended: At least 4GB RAM allocated to Docker Desktop
    pause
    exit /b 1
)

echo Minikube started successfully!
echo.
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