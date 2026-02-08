@echo off
REM Deployment script for Todo App on Kubernetes
REM This script assumes Kubernetes is enabled in Docker Desktop

echo Starting deployment of Todo App to Kubernetes...

REM Check if kubectl is available
kubectl version --client >nul 2>&1
if %errorlevel% neq 0 (
    echo kubectl is not installed or not in PATH
    exit /b 1
)

REM Check if Helm is available
helm version >nul 2>&1
if %errorlevel% neq 0 (
    echo helm is not installed or not in PATH
    exit /b 1
)

echo Checking Kubernetes connectivity...
kubectl cluster-info >nul 2>&1
if %errorlevel% neq 0 (
    echo Cannot connect to Kubernetes cluster. Please ensure:
    echo 1. Docker Desktop is running
    echo 2. Kubernetes is enabled in Docker Desktop settings
    exit /b 1
)

echo Kubernetes cluster is accessible!

REM If minikube is supposed to be used, start it
echo Starting Minikube with Docker driver...
minikube start --driver=docker
if %errorlevel% neq 0 (
    echo Failed to start Minikube. Please check Docker Desktop settings.
    echo Make sure Kubernetes is enabled in Docker Desktop settings.
    exit /b 1
)

echo Minikube is running!

REM Load Docker images into Minikube
echo Setting Docker environment to Minikube...
FOR /F "tokens=*" %%i IN ('minikube docker-env') DO %%i

REM Verify images exist
docker images | findstr todo-backend >nul
if %errorlevel% neq 0 (
    echo Building backend image...
    cd ../backend && docker build -t todo-backend:latest . && cd ../Phase-IV
) else (
    echo Backend image already exists
)

docker images | findstr todo-frontend >nul
if %errorlevel% neq 0 (
    echo Building frontend image...
    cd ../frontend && docker build -t todo-frontend:latest . && cd ../Phase-IV
) else (
    echo Frontend image already exists
)

echo Deploying Todo App with Helm...

REM Install Helm charts
helm install todo-backend ./helm/todo-app-backend
if %errorlevel% neq 0 (
    echo Failed to install backend chart
    exit /b 1
)

helm install todo-frontend ./helm/todo-app-frontend
if %errorlevel% neq 0 (
    echo Failed to install frontend chart
    exit /b 1
)

echo Applications deployed successfully!
echo Check status with: kubectl get pods,svc
echo Access the frontend: minikube service todo-frontend --url