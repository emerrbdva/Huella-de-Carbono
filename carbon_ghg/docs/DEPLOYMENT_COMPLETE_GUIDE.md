# 🚀 Guía Completa de Deployment - Carbon GHG Calculator

**Versión**: 1.0  
**Fecha**: 8 de octubre de 2025  
**Aplicación**: Carbon GHG Emissions Calculator  
**Framework**: Streamlit + Python 3.10+  

---

## 📋 Tabla de Contenidos

1. [Visión General](#vision-general)
2. [Pre-requisitos](#pre-requisitos)
3. [Opciones de Deployment](#opciones-de-deployment)
4. [Deployment Local](#deployment-local)
5. [Streamlit Cloud (GRATIS)](#streamlit-cloud)
6. [Docker Local](#docker-local)
7. [Render.com](#rendercom)
8. [Railway](#railway)
9. [Azure Container Instances](#azure-container-instances)
10. [AWS ECS Fargate](#aws-ecs-fargate)
11. [Google Cloud Run](#google-cloud-run)
12. [Configuración Avanzada](#configuracion-avanzada)
13. [Monitoreo y Logging](#monitoreo-y-logging)
14. [Troubleshooting](#troubleshooting)

---

## 🎯 Visión General

Esta guía cubre **8 opciones de deployment** desde desarrollo local hasta producción enterprise. Cada opción incluye:

- ✅ Paso a paso detallado
- 💰 Costos estimados
- ⚡ Complejidad técnica
- 🎯 Casos de uso recomendados
- 📊 Pros y contras

### **Comparación Rápida**

| Plataforma | Complejidad | Costo/mes | Tiempo Setup | Caso de Uso |
|------------|-------------|-----------|--------------|-------------|
| **Local** | ⭐ | $0 | 5 min | Desarrollo |
| **Streamlit Cloud** | ⭐ | $0 | 10 min | Prototipos, demos |
| **Docker Local** | ⭐⭐ | $0 | 15 min | Testing, staging |
| **Render.com** | ⭐⭐ | $7-25 | 20 min | Startups, SMBs |
| **Railway** | ⭐ | $5-20 | 15 min | Side projects |
| **Azure ACI** | ⭐⭐⭐ | $15-50 | 30 min | Enterprise, compliance |
| **AWS ECS** | ⭐⭐⭐⭐ | $20-100 | 45 min | Enterprise, alta escala |
| **GCP Cloud Run** | ⭐⭐ | $10-40 | 25 min | Pay-per-request, serverless |

---

## 📦 Pre-requisitos

### **Generales (Todas las Plataformas)**

```bash
# 1. Python 3.10+
python --version  # Debe ser 3.10 o superior

# 2. Git instalado
git --version

# 3. Cuenta de GitHub (para CI/CD)
# Crear en: https://github.com/signup

# 4. Repositorio del proyecto
git clone https://github.com/tu-usuario/carbon-ghg-calculator.git
cd carbon-ghg-calculator
```

### **Archivos Requeridos** ✅

Asegúrate de que tu proyecto tenga:

```
carbon_ghg/
├── app/
│   └── streamlit_app.py        ✅ App principal
├── requirements.txt            ✅ Dependencias
├── .streamlit/
│   └── config.toml             ✅ Configuración Streamlit
├── Dockerfile                  ✅ Para deployments con Docker
├── .dockerignore              ✅ Optimizar build
├── README.md                   ✅ Documentación
└── data/
    └── ghg-conversion-factors-2025-condensed-set.xlsx  ✅ Datos
```

---

## 🏠 1. Deployment Local

### **Descripción**
Correr la app en tu máquina local para desarrollo y testing.

### **Paso a Paso**

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr la aplicación
streamlit run app/streamlit_app.py

# 5. Abrir en navegador
# URL: http://localhost:8501
```

### **Configuración Opcional**

```toml
# .streamlit/config.toml
[server]
port = 8501
headless = true
runOnSave = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| Setup instantáneo | Solo accesible localmente |
| Sin costos | Requiere Python instalado |
| Hot reload automático | No escalable |
| Fácil debugging | Sin HTTPS |

### **Caso de Uso**
✅ Desarrollo diario, testing de features, debugging

---

## ☁️ 2. Streamlit Cloud (GRATIS)

### **Descripción**
Hosting gratuito oficial de Streamlit. **Opción más fácil y rápida** para demos públicas.

### **Paso a Paso**

#### **Preparar Repositorio**

```bash
# 1. Asegurarte de que tu código está en GitHub
git add .
git commit -m "Preparar para Streamlit Cloud"
git push origin main

# 2. Verificar archivos requeridos
# ✅ requirements.txt
# ✅ app/streamlit_app.py
# ✅ .streamlit/config.toml (opcional)
```

#### **Deployment en Streamlit Cloud**

1. **Ir a** https://streamlit.io/cloud
2. **Sign in** con GitHub
3. **Click** "New app"
4. **Configurar**:
   ```
   Repository: tu-usuario/carbon-ghg-calculator
   Branch: main
   Main file path: app/streamlit_app.py
   ```
5. **Advanced settings** (opcional):
   ```
   Python version: 3.10
   Requirements file: requirements.txt
   ```
6. **Click** "Deploy"
7. **Esperar** 2-3 minutos mientras se construye

#### **URL Final**
```
https://tu-usuario-carbon-ghg-calculator.streamlit.app
```

### **Secrets Management**

```toml
# En Streamlit Cloud Dashboard > Settings > Secrets
[api_keys]
ollama_api_key = "tu-api-key"
github_token = "ghp_xxxxxxxxxxxx"

[database]
connection_string = "postgresql://..."
```

### **Custom Domain** (Premium)

```bash
# 1. En Streamlit Cloud Dashboard > Settings > Custom domain
# 2. Agregar: calculator.tuempresa.com
# 3. Configurar DNS CNAME:
#    calculator.tuempresa.com -> tu-app.streamlit.app
```

### **Recursos**

| Recurso | Plan Free | Plan Team ($250/mes) |
|---------|-----------|---------------------|
| Apps públicas | 1 | Unlimited |
| Apps privadas | 3 | Unlimited |
| Viewers concurrentes | Unlimited | Unlimited |
| Memory | 1 GB | 8 GB |
| CPU | 0.78 cores | 2 cores |
| Storage | 50 GB | 100 GB |

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| **100% GRATIS** (plan free) | Limited a 1 app pública (free) |
| Setup en 10 minutos | Recursos limitados (1GB RAM) |
| Auto-deploy desde GitHub | No acceso a servidor |
| HTTPS incluido | Siempre público (en plan free) |
| Sin mantención | Streamlit logo en app |
| CI/CD automático | No custom domain (free) |

### **Caso de Uso**
✅ Demos, prototipos, proyectos personales, MVPs

---

## 🐳 3. Docker Local

### **Descripción**
Containerizar la app para desarrollo, testing y preparación para producción.

### **Archivos Necesarios**

#### **Dockerfile**

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### **.dockerignore**

```
# .dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.env
.git/
.gitignore
.vscode/
.idea/
*.md
!README.md
.pytest_cache/
htmlcov/
.coverage
```

### **Paso a Paso**

```bash
# 1. Build de la imagen
docker build -t carbon-ghg-calculator:latest .

# 2. Verificar imagen creada
docker images | grep carbon-ghg

# 3. Correr container
docker run -d \
  --name carbon-ghg-app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  carbon-ghg-calculator:latest

# 4. Verificar que está corriendo
docker ps | grep carbon-ghg

# 5. Ver logs
docker logs -f carbon-ghg-app

# 6. Abrir en navegador
# http://localhost:8501
```

### **Docker Compose** (Recomendado)

```yaml
# docker-compose.yml
version: '3.8'

services:
  streamlit:
    build: .
    container_name: carbon-ghg-streamlit
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./reports:/app/reports
    environment:
      - PYTHONUNBUFFERED=1
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

```bash
# Usar Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### **Optimizaciones**

```dockerfile
# Dockerfile optimizado (multi-stage build)
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py"]
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| Entorno consistente | Requiere Docker instalado |
| Fácil compartir | Overhead de recursos |
| Preparación para producción | Curva de aprendizaje |
| Aislamiento completo | Build time inicial |

### **Caso de Uso**
✅ Testing, staging, desarrollo en equipo, preparación para cloud

---

## 🎨 4. Render.com

### **Descripción**
Plataforma moderna PaaS con free tier y auto-deploy desde GitHub. **Excelente para startups**.

### **Paso a Paso**

#### **1. Preparar Archivos**

```bash
# render.yaml (opcional pero recomendado)
services:
  - type: web
    name: carbon-ghg-calculator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
```

#### **2. Deployment Manual**

1. **Sign up** en https://render.com
2. **Connect GitHub** repository
3. **New Web Service**
4. **Configurar**:
   ```
   Name: carbon-ghg-calculator
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
5. **Environment Variables**:
   ```
   PYTHON_VERSION=3.10.0
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_SERVER_PORT=$PORT
   ```
6. **Create Web Service**

#### **3. Auto-Deploy**

```bash
# Cada push a main despliega automáticamente
git add .
git commit -m "Update feature"
git push origin main
# Render detecta el push y redespliega (2-3 min)
```

### **Plans y Pricing**

| Plan | Precio | RAM | CPU | Bandwidth | Storage |
|------|--------|-----|-----|-----------|---------|
| **Free** | $0 | 512 MB | 0.5 | 100 GB/mes | 1 GB |
| **Starter** | $7/mes | 512 MB | 0.5 | 100 GB/mes | 10 GB |
| **Standard** | $25/mes | 2 GB | 1.0 | 250 GB/mes | 100 GB |
| **Pro** | $85/mes | 8 GB | 2.0 | 500 GB/mes | 500 GB |

### **Features Incluidas**

- ✅ Auto-deploy desde GitHub
- ✅ HTTPS gratuito (Let's Encrypt)
- ✅ Custom domains
- ✅ Logs persistentes
- ✅ Rollback fácil
- ✅ Health checks
- ✅ Secrets management

### **Custom Domain**

```bash
# 1. En Render Dashboard > Settings > Custom Domain
# 2. Agregar: app.tuempresa.com
# 3. Configurar DNS:
#    CNAME: app.tuempresa.com -> tu-app.onrender.com
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| Free tier generoso | Free tier "sleeps" tras inactividad |
| Auto-deploy GitHub | 512 MB RAM (free tier) |
| HTTPS automático | Cold starts (~30s en free) |
| Fácil escalado | No free GPU |
| Logs persistentes | US/EU regions only |
| $7/mes muy económico | Soporte limitado (free) |

### **Caso de Uso**
✅ Startups, SMBs, proyectos con tráfico moderado

---

## 🚂 5. Railway

### **Descripción**
Plataforma developer-friendly con $5 crédito gratis mensual. **Perfect para side projects**.

### **Paso a Paso**

#### **1. Sign Up**

```bash
# 1. Ir a https://railway.app
# 2. Sign in con GitHub
# 3. Obtener $5 crédito gratis (500 horas de free tier)
```

#### **2. Deploy desde GitHub**

1. **New Project** > **Deploy from GitHub repo**
2. **Seleccionar** tu repositorio
3. Railway detecta Python automáticamente
4. **Add variables** (opcional):
   ```
   PYTHON_VERSION=3.10
   PORT=8501
   ```
5. **Deploy**

#### **3. Configuración Custom**

```toml
# railway.toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"
healthcheckPath = "/_stcore/health"
healthcheckTimeout = 10
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### **Pricing**

| Plan | Precio | Included | Después |
|------|--------|----------|---------|
| **Free Trial** | $0 | $5 crédito | $0.000231/GB-hour RAM + $0.000463/vCPU-hour |
| **Developer** | $5/mes | 500 horas | Mismo rate |
| **Team** | $20/mes | 2000 horas | Mismo rate |

**Costo estimado** para Carbon GHG (512 MB, 0.5 vCPU, 24/7):
- RAM: 0.5 GB × 730h × $0.000231 = **$0.08/mes**
- CPU: 0.5 vCPU × 730h × $0.000463 = **$0.17/mes**
- **Total: ~$0.25/mes** (bien dentro de $5 free tier)

### **Features**

- ✅ $5 crédito gratis/mes
- ✅ Auto-deploy desde GitHub
- ✅ Custom domains
- ✅ HTTPS automático
- ✅ PostgreSQL, Redis incluidos
- ✅ CLI potente
- ✅ No sleep (siempre activo)

### **Railway CLI**

```bash
# 1. Instalar CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Link proyecto
railway link

# 4. Deploy desde CLI
railway up

# 5. Ver logs
railway logs

# 6. Variables de entorno
railway variables set PYTHON_VERSION=3.10
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| **$5 gratis/mes** suficiente | Requiere tarjeta (para $5 free) |
| No sleep (24/7 activo) | Pricing por uso (puede variar) |
| CLI excelente | Menos mature que Railway |
| Setup en 5 minutos | Pocas regiones (US, EU) |
| PostgreSQL/Redis gratis | Docs limitadas |

### **Caso de Uso**
✅ Side projects, MVPs, startups early-stage

---

## ☁️ 6. Azure Container Instances (ACI)

### **Descripción**
Servicio de Microsoft Azure para correr containers sin gestionar infraestructura. **Ideal para enterprise**.

### **Pre-requisitos**

```bash
# 1. Instalar Azure CLI
# Windows (PowerShell)
winget install Microsoft.AzureCLI

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Login
az login

# 3. Crear resource group
az group create \
  --name carbon-ghg-rg \
  --location eastus
```

### **Paso a Paso**

#### **1. Build y Push a Azure Container Registry**

```bash
# 1. Crear ACR
az acr create \
  --resource-group carbon-ghg-rg \
  --name carbonghgacr \
  --sku Basic

# 2. Login a ACR
az acr login --name carbonghgacr

# 3. Build imagen
docker build -t carbonghgacr.azurecr.io/carbon-ghg:latest .

# 4. Push imagen
docker push carbonghgacr.azurecr.io/carbon-ghg:latest
```

#### **2. Deploy Container Instance**

```bash
# 1. Obtener credentials de ACR
ACR_USERNAME=$(az acr credential show --name carbonghgacr --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name carbonghgacr --query "passwords[0].value" -o tsv)

# 2. Crear Container Instance
az container create \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --image carbonghgacr.azurecr.io/carbon-ghg:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server carbonghgacr.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label carbon-ghg-app \
  --ports 8501

# 3. Obtener URL pública
az container show \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --query ipAddress.fqdn \
  --output tsv
  
# Output: carbon-ghg-app.eastus.azurecontainer.io
```

#### **3. Con Variables de Entorno**

```bash
az container create \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --image carbonghgacr.azurecr.io/carbon-ghg:latest \
  --environment-variables \
    PYTHON_VERSION='3.10' \
    STREAMLIT_SERVER_HEADLESS='true' \
  --secure-environment-variables \
    API_KEY='secret-key-here'
```

#### **4. Con Azure File Share (Persistent Storage)**

```bash
# 1. Crear storage account
az storage account create \
  --resource-group carbon-ghg-rg \
  --name carbonghgstorage \
  --sku Standard_LRS

# 2. Crear file share
az storage share create \
  --name data \
  --account-name carbonghgstorage

# 3. Deploy con volume mount
az container create \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --image carbonghgacr.azurecr.io/carbon-ghg:latest \
  --azure-file-volume-account-name carbonghgstorage \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name data \
  --azure-file-volume-mount-path /app/data
```

### **Pricing** (East US region)

| Recurso | Precio |
|---------|--------|
| 1 vCPU | $0.0000012/segundo ($3.11/mes) |
| 1 GB RAM | $0.0000001344/segundo ($3.49/mes) |
| **Total (1 vCPU + 1 GB)** | **~$6.60/mes** |
| Bandwidth | $0.087/GB (primeros 10 TB) |

**Ejemplo**: App con 1 vCPU, 1 GB RAM, 24/7:
- vCPU: $3.11/mes
- RAM: $3.49/mes
- **Total: $6.60/mes** ✅

### **Features Enterprise**

- ✅ VNet integration (private networking)
- ✅ Managed identity (Azure AD)
- ✅ Azure Monitor integration
- ✅ Compliance certifications (ISO, SOC, HIPAA)
- ✅ SLA 99.9%
- ✅ Regional deployment (60+ regions)
- ✅ GPU support
- ✅ Spot instances (70% discount)

### **Monitoring**

```bash
# 1. Ver logs
az container logs \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --follow

# 2. SSH al container (debug)
az container exec \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --exec-command "/bin/bash"

# 3. Ver estado
az container show \
  --resource-group carbon-ghg-rg \
  --name carbon-ghg-app \
  --query "{Status:instanceView.state, CPU:containers[0].resources.requests.cpu, Memory:containers[0].resources.requests.memoryInGB}"
```

### **Auto-Restart Policy**

```bash
az container create \
  ... \
  --restart-policy OnFailure  # Options: Always, OnFailure, Never
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| Pay-per-second billing | No auto-scaling nativo |
| Enterprise-grade seguridad | Requiere conocimiento Azure |
| SLA 99.9% | Cold start (~10-15s) |
| 60+ regiones globales | No persistent storage (sin File Share) |
| Integration con Azure ecosystem | Más caro que alternatives |
| VNet/Private endpoint | No CI/CD built-in |

### **Caso de Uso**
✅ Enterprise, compliance requerido, integración Azure ecosystem

---

## 🚢 7. AWS ECS Fargate

### **Descripción**
Servicio de containers serverless de AWS. **Gold standard para producción enterprise**.

### **Pre-requisitos**

```bash
# 1. Instalar AWS CLI
# Windows
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Configurar credenciales
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-east-1
# Default output format: json
```

### **Arquitectura**

```
Internet
   ↓
Application Load Balancer (ALB)
   ↓
ECS Fargate Cluster
   ↓
Task Definition (Docker container)
   ↓
Container (Carbon GHG app)
   ↓
Amazon ECR (Docker registry)
```

### **Paso a Paso**

#### **1. Create ECR Repository**

```bash
# 1. Crear repositorio ECR
aws ecr create-repository \
  --repository-name carbon-ghg-calculator \
  --region us-east-1

# 2. Login a ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-east-1.amazonaws.com

# 3. Tag y push imagen
docker tag carbon-ghg:latest \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/carbon-ghg-calculator:latest
  
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/carbon-ghg-calculator:latest
```

#### **2. Create ECS Cluster**

```bash
aws ecs create-cluster \
  --cluster-name carbon-ghg-cluster \
  --region us-east-1
```

#### **3. Create Task Definition**

```json
// task-definition.json
{
  "family": "carbon-ghg-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "carbon-ghg-container",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/carbon-ghg-calculator:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STREAMLIT_SERVER_PORT",
          "value": "8501"
        },
        {
          "name": "STREAMLIT_SERVER_HEADLESS",
          "value": "true"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/carbon-ghg",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

```bash
# Registrar task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json
```

#### **4. Create Load Balancer (ALB)**

```bash
# 1. Crear security group
aws ec2 create-security-group \
  --group-name carbon-ghg-alb-sg \
  --description "Security group for Carbon GHG ALB" \
  --vpc-id vpc-xxxxx

# 2. Permitir tráfico HTTP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# 3. Crear Application Load Balancer
aws elbv2 create-load-balancer \
  --name carbon-ghg-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx

# 4. Crear target group
aws elbv2 create-target-group \
  --name carbon-ghg-tg \
  --protocol HTTP \
  --port 8501 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /_stcore/health

# 5. Crear listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

#### **5. Create ECS Service**

```bash
aws ecs create-service \
  --cluster carbon-ghg-cluster \
  --service-name carbon-ghg-service \
  --task-definition carbon-ghg-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx,subnet-yyyyy],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=carbon-ghg-container,containerPort=8501
```

### **Auto-Scaling**

```bash
# 1. Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/carbon-ghg-cluster/carbon-ghg-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# 2. Create scaling policy (CPU > 70%)
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/carbon-ghg-cluster/carbon-ghg-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name carbon-ghg-cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

```json
// scaling-policy.json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleInCooldown": 300,
  "ScaleOutCooldown": 60
}
```

### **CI/CD con GitHub Actions**

```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build, tag, and push image to Amazon ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: carbon-ghg-calculator
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster carbon-ghg-cluster \
            --service carbon-ghg-service \
            --force-new-deployment
```

### **Pricing** (us-east-1)

| Recurso | Configuración | Precio/hora | Precio/mes (24/7) |
|---------|--------------|-------------|-------------------|
| **Fargate CPU** | 0.5 vCPU | $0.04656 | $33.91 |
| **Fargate Memory** | 1 GB | $0.00511 | $3.72 |
| **ALB** | - | $0.0225 | $16.43 |
| **Data Transfer** | 10 GB/mes | - | $0.90 |
| **ECR Storage** | 1 GB | - | $0.10 |
| **CloudWatch Logs** | 1 GB ingestion | - | $0.50 |
| **Total (2 tasks)** | - | - | **~$110/mes** |

**Con Reserved Capacity** (1 año commitment):
- Ahorro: ~30-40%
- Total: **~$70-80/mes**

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| Auto-scaling nativo | Complejidad alta |
| Alta disponibilidad (multi-AZ) | Costo >$100/mes (producción) |
| Integración AWS ecosystem | Curva de aprendizaje empinada |
| SLA 99.99% | Requiere VPC, subnets, etc. |
| Serverless (no EC2 management) | Cold start ~10-20s |
| Enterprise-grade monitoring | Overhead de configuración |

### **Caso de Uso**
✅ Producción enterprise, alta escala (>1000 usuarios concurrentes), compliance estricto

---

## 🚀 8. Google Cloud Run

### **Descripción**
Servicio serverless de Google para containers. **Pay-per-request, ideal para tráfico variable**.

### **Pre-requisitos**

```bash
# 1. Instalar gcloud CLI
# Windows
# Descargar de: https://cloud.google.com/sdk/docs/install

# macOS
brew install --cask google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash

# 2. Inicializar y login
gcloud init
gcloud auth login

# 3. Crear proyecto
gcloud projects create carbon-ghg-calculator
gcloud config set project carbon-ghg-calculator

# 4. Habilitar APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### **Paso a Paso**

#### **1. Build y Deploy (Método Simple)**

```bash
# Deploy directo desde source (Cloud Build automático)
gcloud run deploy carbon-ghg-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --port 8501

# URL generada automáticamente:
# https://carbon-ghg-app-xxxxx-uc.a.run.app
```

#### **2. Build y Deploy (Con Artifact Registry)**

```bash
# 1. Crear repositorio en Artifact Registry
gcloud artifacts repositories create carbon-ghg-repo \
  --repository-format=docker \
  --location=us-central1

# 2. Configurar Docker para Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# 3. Build imagen
docker build -t us-central1-docker.pkg.dev/carbon-ghg-calculator/carbon-ghg-repo/carbon-ghg:latest .

# 4. Push imagen
docker push us-central1-docker.pkg.dev/carbon-ghg-calculator/carbon-ghg-repo/carbon-ghg:latest

# 5. Deploy desde Artifact Registry
gcloud run deploy carbon-ghg-app \
  --image us-central1-docker.pkg.dev/carbon-ghg-calculator/carbon-ghg-repo/carbon-ghg:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### **3. Configuración Avanzada**

```bash
gcloud run deploy carbon-ghg-app \
  --image us-central1-docker.pkg.dev/carbon-ghg-calculator/carbon-ghg-repo/carbon-ghg:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300s \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars PYTHON_VERSION=3.10,STREAMLIT_SERVER_HEADLESS=true \
  --set-secrets API_KEY=api-key-secret:latest
```

#### **4. Custom Domain**

```bash
# 1. Verificar dominio en Google Search Console
# https://search.google.com/search-console

# 2. Mapear dominio
gcloud run domain-mappings create \
  --service carbon-ghg-app \
  --domain app.tuempresa.com \
  --region us-central1

# 3. Configurar DNS (obtener de output anterior)
# CNAME: app.tuempresa.com -> ghs.googlehosted.com
```

#### **5. CI/CD con Cloud Build**

```yaml
# cloudbuild.yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/$PROJECT_ID/carbon-ghg-repo/carbon-ghg:$COMMIT_SHA', '.']
  
  # Push the container image to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/$PROJECT_ID/carbon-ghg-repo/carbon-ghg:$COMMIT_SHA']
  
  # Deploy container image to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'carbon-ghg-app'
      - '--image'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/carbon-ghg-repo/carbon-ghg:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'

images:
  - 'us-central1-docker.pkg.dev/$PROJECT_ID/carbon-ghg-repo/carbon-ghg:$COMMIT_SHA'
```

```bash
# Trigger manual
gcloud builds submit --config cloudbuild.yaml

# Trigger automático (GitHub)
gcloud builds triggers create github \
  --repo-name=carbon-ghg-calculator \
  --repo-owner=tu-usuario \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### **Pricing** (Pay-per-request)

| Recurso | Free Tier/mes | Precio después |
|---------|---------------|----------------|
| **Requests** | 2M requests | $0.40 por millón |
| **CPU time** | 180,000 vCPU-seconds | $0.00002400/vCPU-second |
| **Memory time** | 360,000 GiB-seconds | $0.00000250/GiB-second |
| **Networking** | 1 GB egress (NA) | $0.12/GB |

**Ejemplo**: App con tráfico bajo-medio (10,000 requests/mes, 1s avg latency, 1 GB RAM, 1 vCPU):

```
Requests: 10,000 < 2M = FREE
CPU time: 10,000 req × 1s × 1 vCPU = 10,000 vCPU-s < 180,000 = FREE
Memory time: 10,000 req × 1s × 1 GB = 10,000 GiB-s < 360,000 = FREE

Total: $0/mes (dentro de free tier) ✅
```

**Ejemplo 2**: Tráfico alto (500,000 requests/mes):

```
Requests: 500K - 2M (free) = 0 = FREE (no excede free tier)
CPU time: 500K × 1s × 1 vCPU = 500,000 vCPU-s
  - Free: 180,000 vCPU-s
  - Paid: 320,000 × $0.000024 = $7.68
Memory time: 500K × 1s × 1 GB = 500,000 GiB-s
  - Free: 360,000 GiB-s
  - Paid: 140,000 × $0.0000025 = $0.35

Total: ~$8/mes ✅
```

### **Features**

- ✅ **Scales to zero** (costo $0 cuando no hay tráfico)
- ✅ **Auto-scaling** (0 a thousands de instancias)
- ✅ **HTTPS automático** (TLS incluido)
- ✅ **Custom domains** con certificados gestionados
- ✅ **Free tier generoso** (2M requests/mes)
- ✅ **Global load balancing**
- ✅ **WebSockets support**
- ✅ **VPC connector** (private services)

### **Monitoring**

```bash
# Ver logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=carbon-ghg-app" --limit 50

# Métricas en Cloud Console
# https://console.cloud.google.com/run
```

### **Pros y Contras**

| Pros ✅ | Contras ❌ |
|---------|-----------|
| **Pay-per-request** (solo pagas lo que usas) | Cold start ~2-5s (primera request) |
| **Scale to zero** (ahorro máximo) | Request timeout máx 60min |
| **Free tier MUY generoso** | Menos control que Kubernetes |
| **Setup en 10 minutos** | Requiere cuenta GCP |
| **Auto-scaling instantáneo** | Limited regions vs AWS |
| **Global CDN incluido** | Billing puede ser confuso |

### **Caso de Uso**
✅ Tráfico variable/impredecible, demos, MVPs, prototipos, apps con peak traffic

---

## ⚙️ Configuración Avanzada

### **1. Environment Variables**

```bash
# Streamlit Cloud
# Dashboard > Settings > Secrets
[database]
connection_string = "postgresql://..."

[api_keys]
openai_key = "sk-..."
```

```bash
# Render.com / Railway
# Dashboard > Environment Variables
PYTHON_VERSION=3.10
STREAMLIT_SERVER_HEADLESS=true
DATABASE_URL=postgresql://...
```

```bash
# Docker / Docker Compose
# .env file
PYTHON_VERSION=3.10
STREAMLIT_SERVER_PORT=8501
DATABASE_URL=postgresql://...
```

### **2. Custom Domains y HTTPS**

#### **Streamlit Cloud**
```
1. Settings > Custom domain
2. Add: app.tuempresa.com
3. DNS: CNAME app.tuempresa.com -> your-app.streamlit.app
```

#### **Render / Railway**
```
1. Dashboard > Settings > Custom Domain
2. Add: app.tuempresa.com
3. DNS: CNAME app.tuempresa.com -> your-app.onrender.com (o railway.app)
```

#### **Azure / AWS / GCP**
```
1. Registrar dominio en provider
2. Configurar DNS apuntando a load balancer
3. Certificado SSL automático (Let's Encrypt o managed certificates)
```

### **3. Database Integration**

```python
# app/streamlit_app.py
import streamlit as st
import psycopg2
import os

# Connection from environment variable
@st.cache_resource
def get_database_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

conn = get_database_connection()

# Query
@st.cache_data(ttl=600)
def load_activities_from_db():
    return pd.read_sql("SELECT * FROM activities", conn)

df = load_activities_from_db()
```

### **4. Secrets Management**

#### **Streamlit Secrets**
```python
# .streamlit/secrets.toml (local)
[database]
host = "localhost"
port = 5432
user = "admin"
password = "secret123"

# En código
import streamlit as st
db_config = st.secrets["database"]
conn = psycopg2.connect(**db_config)
```

#### **Docker Secrets**
```bash
# Crear secret
echo "my-secret-password" | docker secret create db_password -

# Usar en docker-compose
services:
  app:
    secrets:
      - db_password
secrets:
  db_password:
    external: true
```

#### **Azure Key Vault**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://carbon-ghg-vault.vault.azure.net/",
    credential=credential
)

api_key = client.get_secret("api-key").value
```

### **5. Logging y Monitoring**

```python
# app/streamlit_app.py
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Log eventos
logger.info("Usuario cargó CSV con 150 actividades")
logger.warning("Factor no encontrado para categoría: custom_fuel")
logger.error("Error al generar reporte Excel", exc_info=True)
```

---

## 📊 Monitoreo y Logging

### **Application Performance Monitoring (APM)**

#### **1. Sentry (Error Tracking)**

```python
# Instalación
pip install sentry-sdk

# app/streamlit_app.py
import sentry_sdk
sentry_sdk.init(
    dsn="https://xxxxx@o123456.ingest.sentry.io/123456",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Capturar excepciones automáticamente
try:
    result = compute_emission(activity, factor)
except Exception as e:
    sentry_sdk.capture_exception(e)
    st.error(f"Error: {e}")
```

#### **2. New Relic**

```python
pip install newrelic

# newrelic.ini
[newrelic]
license_key = YOUR_LICENSE_KEY
app_name = Carbon GHG Calculator

# Iniciar con New Relic
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program streamlit run app/streamlit_app.py
```

#### **3. Datadog**

```python
pip install ddtrace

# Correr con Datadog
DD_SERVICE=carbon-ghg DD_ENV=production DD_VERSION=1.0 \
  ddtrace-run streamlit run app/streamlit_app.py
```

### **Logs Centralizados**

#### **ELK Stack (Elasticsearch + Logstash + Kibana)**

```yaml
# docker-compose-elk.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

---

## 🔧 Troubleshooting

### **1. App no inicia**

```bash
# Verificar logs
docker logs carbon-ghg-app

# Común: Puerto ya en uso
# Solución: Cambiar puerto
streamlit run app/streamlit_app.py --server.port=8502

# Común: Dependencias faltantes
pip install -r requirements.txt --upgrade
```

### **2. Performance lenta**

```bash
# 1. Verificar cache funcionando
# Ver logs de Streamlit para "Cache hit"

# 2. Profiling
py-spy record -o profile.svg -- streamlit run app/streamlit_app.py

# 3. Aumentar recursos
# Docker: --memory 2g --cpus 2
# Cloud: Upgrade plan
```

### **3. Errores de memoria**

```bash
# Síntoma: MemoryError o app se cuelga

# Solución 1: Aumentar memoria
docker run --memory 2g ...

# Solución 2: Procesar en chunks
def process_large_file(file_path):
    for chunk in pd.read_csv(file_path, chunksize=1000):
        process_chunk(chunk)
```

### **4. Cold starts lentos**

```bash
# Cloud Run / Azure ACI
# Solución: min_instances > 0
gcloud run deploy ... --min-instances 1

# AWS Fargate
# Solución: Provisioned Concurrency
aws ecs update-service --desired-count 2
```

---

## 📚 Recursos Adicionales

### **Documentación Oficial**

- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS ECS Guide](https://docs.aws.amazon.com/ecs/)
- [Azure Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/)
- [Google Cloud Run](https://cloud.google.com/run/docs)

### **Tutoriales**

- [Streamlit Cloud Tutorial](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Docker Compose Tutorial](https://docs.docker.com/compose/gettingstarted/)
- [GitHub Actions for CI/CD](https://docs.github.com/en/actions)

---

## 🎯 Recomendación Final

### **Para Desarrollo**
→ **Local** o **Docker Local**

### **Para Demo/MVP**
→ **Streamlit Cloud (FREE)** o **Railway ($5 free tier)**

### **Para Startup/SMB**
→ **Render.com ($7-25/mes)** o **Google Cloud Run (pay-per-use)**

### **Para Enterprise**
→ **AWS ECS Fargate** o **Azure Container Instances**

---

**Autor**: GitHub Copilot  
**Fecha**: 8 de octubre de 2025  
**Versión**: 1.0  
**Estado**: ✅ **GUÍA COMPLETADA**
