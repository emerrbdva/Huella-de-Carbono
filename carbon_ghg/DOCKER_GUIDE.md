# 🐳 Guía de Docker para Carbon GHG Calculator

Esta guía completa te ayudará a desplegar Carbon GHG Calculator usando Docker en minutos.

## 📋 Prerrequisitos

- **Docker Desktop** instalado ([Descargar aquí](https://www.docker.com/products/docker-desktop/))
- **Docker Compose** (incluido con Docker Desktop)
- **8 GB RAM** disponibles (mínimo 4 GB)
- **Puerto 8501** disponible (para Streamlit)
- **Puerto 11434** disponible (opcional, para Ollama/AI)

## 🚀 Inicio Rápido (2 minutos)

### Opción 1: Solo la aplicación (sin IA)

```powershell
# En la raíz del proyecto
cd "c:\Python\Huella de Carbono\carbon_ghg"

# Construir y levantar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f carbon-ghg-app

# Abrir en navegador
# http://localhost:8501
```

### Opción 2: Aplicación + Ollama (con IA)

```powershell
# Activar perfil con IA
docker-compose --profile with-ai up -d

# Esperar a que Ollama esté listo (~30 segundos)
docker-compose logs -f ollama

# Descargar modelo llama3 (primera vez, ~4 GB)
docker exec -it carbon-ghg-ollama ollama pull llama3

# Verificar modelo
docker exec -it carbon-ghg-ollama ollama list

# Abrir aplicación
# http://localhost:8501
```

## 🏗️ Construcción Manual

### 1. Construir la imagen Docker

```powershell
# Desde la raíz del proyecto
docker build -t carbon-ghg:latest .

# Ver imagen creada
docker images | grep carbon-ghg
```

### 2. Ejecutar contenedor individual

```powershell
# Modo básico
docker run -d \
  --name carbon-ghg-app \
  -p 8501:8501 \
  -v ${PWD}/data:/app/data:ro \
  -v ${PWD}/reports:/app/reports:rw \
  carbon-ghg:latest

# Verificar logs
docker logs -f carbon-ghg-app
```

## 📦 Arquitectura de Contenedores

### Estructura Multi-stage Build

```
Etapa 1: Builder
├── Python 3.12-slim
├── Instala dependencias de compilación
├── Instala paquetes Python
└── Genera /root/.local

Etapa 2: Runtime
├── Python 3.12-slim (limpio)
├── Copia solo /root/.local (sin build tools)
├── Usuario no-root (appuser)
├── Expone puerto 8501
└── Health check cada 30s
```

### Servicios en docker-compose.yml

| Servicio | Puerto | Descripción | Perfil |
|----------|--------|-------------|--------|
| `carbon-ghg-app` | 8501 | Streamlit UI | default |
| `ollama` | 11434 | API de IA local | with-ai |

### Volúmenes Montados

| Host | Contenedor | Modo | Propósito |
|------|------------|------|-----------|
| `./data` | `/app/data` | ro | Factores de emisión (solo lectura) |
| `./reports` | `/app/reports` | rw | Reportes generados |
| `./config` | `/app/config` | ro | Configuración |
| `ollama-data` | `/root/.ollama` | rw | Modelos Ollama (persistente) |

## 🔧 Comandos Útiles

### Gestión de Contenedores

```powershell
# Ver contenedores activos
docker-compose ps

# Detener todo
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reiniciar servicio específico
docker-compose restart carbon-ghg-app

# Ver logs en tiempo real
docker-compose logs -f

# Logs de servicio específico
docker-compose logs -f carbon-ghg-app
```

### Acceso a Contenedores

```powershell
# Shell interactivo en la app
docker exec -it carbon-ghg-streamlit bash

# Ver archivos dentro del contenedor
docker exec carbon-ghg-streamlit ls -la /app

# Ejecutar comando puntual
docker exec carbon-ghg-streamlit python -c "import pandas; print(pandas.__version__)"

# Verificar factores de emisión cargados
docker exec carbon-ghg-streamlit python -c "from utils.factors import load_uk_gov_factors; df=load_uk_gov_factors('data/ghg-conversion-factors-2025-condensed-set.xlsx', 2025); print(f'Loaded {len(df)} factors')"
```

### Health Checks

```powershell
# Ver estado de salud
docker inspect carbon-ghg-streamlit --format='{{.State.Health.Status}}'

# Ver logs de health check
docker inspect carbon-ghg-streamlit --format='{{range .State.Health.Log}}{{.Output}}{{end}}'

# Forzar health check manual
docker exec carbon-ghg-streamlit curl -f http://localhost:8501/_stcore/health
```

## 🐛 Troubleshooting

### Problema 1: Puerto 8501 ocupado

```powershell
# Verificar qué está usando el puerto
netstat -ano | findstr :8501

# Cambiar puerto en docker-compose.yml
services:
  carbon-ghg-app:
    ports:
      - "9501:8501"  # Usar puerto 9501 en el host
```

### Problema 2: Contenedor no arranca

```powershell
# Ver logs completos
docker-compose logs carbon-ghg-app

# Verificar imagen
docker images carbon-ghg

# Reconstruir sin caché
docker-compose build --no-cache

# Verificar recursos
docker system df
```

### Problema 3: Datos no visibles

```powershell
# Verificar montaje de volúmenes
docker inspect carbon-ghg-streamlit --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{printf "\n"}}{{end}}'

# Verificar permisos
docker exec carbon-ghg-streamlit ls -la /app/data

# Copiar archivo manualmente si es necesario
docker cp ./data/sample_activities.csv carbon-ghg-streamlit:/app/data/
```

### Problema 4: Ollama no responde

```powershell
# Verificar que Ollama está corriendo
docker ps | grep ollama

# Ver logs de Ollama
docker-compose logs -f ollama

# Reiniciar Ollama
docker-compose restart ollama

# Verificar conectividad
docker exec carbon-ghg-ollama ollama list

# Probar desde la app
docker exec carbon-ghg-streamlit python -c "import requests; print(requests.get('http://ollama:11434/api/tags').json())"
```

### Problema 5: Importación de módulos falla

```powershell
# Verificar PYTHONPATH
docker exec carbon-ghg-streamlit env | grep PYTHON

# Verificar módulos instalados
docker exec carbon-ghg-streamlit pip list

# Reinstalar dependencias
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🚀 Optimización de Rendimiento

### Reducir Tamaño de Imagen

```dockerfile
# En Dockerfile, usar slim variants
FROM python:3.12-slim  # ~120 MB vs python:3.12 (~900 MB)

# Multi-stage build elimina build tools
# Imagen final: ~450 MB vs ~1.2 GB
```

### Caché de Build Layers

```powershell
# Construir con BuildKit (más rápido)
$env:DOCKER_BUILDKIT=1
docker-compose build

# Ver caché de build
docker builder du

# Limpiar caché antiguo
docker builder prune --filter "until=24h"
```

### Recursos del Contenedor

```yaml
# En docker-compose.yml
services:
  carbon-ghg-app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

## 📊 Monitoring y Logs

### Métricas de Contenedor

```powershell
# Estadísticas en tiempo real
docker stats carbon-ghg-streamlit

# Historial de uso
docker stats --no-stream

# Inspección completa
docker inspect carbon-ghg-streamlit | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Logs Avanzados

```powershell
# Últimas 100 líneas
docker-compose logs --tail=100 carbon-ghg-app

# Desde hace 1 hora
docker-compose logs --since 1h

# Exportar logs a archivo
docker-compose logs --no-color > app-logs.txt

# Buscar error específico
docker-compose logs | Select-String -Pattern "ERROR"
```

## 🔐 Seguridad

### Mejores Prácticas Implementadas

✅ **Usuario no-root**: Contenedor corre como `appuser` (UID 1000)  
✅ **Volúmenes read-only**: `/app/data` y `/app/config` son solo lectura  
✅ **No secretos en imagen**: Usar variables de entorno o secrets  
✅ **Health checks**: Reinicio automático si falla  
✅ **Network aislada**: Red bridge privada `carbon-ghg-net`  

### Escaneo de Seguridad

```powershell
# Instalar Trivy (escáner de vulnerabilidades)
# https://github.com/aquasecurity/trivy/releases

# Escanear imagen
trivy image carbon-ghg:latest

# Solo vulnerabilidades CRITICAL y HIGH
trivy image --severity CRITICAL,HIGH carbon-ghg:latest

# Generar reporte HTML
trivy image --format template --template "@contrib/html.tpl" -o report.html carbon-ghg:latest
```

## 📦 Distribución

### Exportar Imagen

```powershell
# Guardar imagen a archivo .tar
docker save carbon-ghg:latest -o carbon-ghg-v1.0.tar

# Comprimir (reduce ~40%)
Compress-Archive -Path carbon-ghg-v1.0.tar -DestinationPath carbon-ghg-v1.0.tar.gz

# Cargar en otra máquina
docker load -i carbon-ghg-v1.0.tar
```

### Subir a Registry (opcional)

```powershell
# Tag para Docker Hub (ejemplo)
docker tag carbon-ghg:latest username/carbon-ghg:1.0

# Login
docker login

# Push
docker push username/carbon-ghg:1.0

# Pull en otra máquina
docker pull username/carbon-ghg:1.0
```

## 🎯 Casos de Uso

### Desarrollo Local

```powershell
# Montar código fuente para hot reload
docker-compose up -d
# Editar código en host, se refleja en contenedor
```

### Producción

```powershell
# Usar versión específica
docker-compose -f docker-compose.prod.yml up -d

# Con proxy reverso (Nginx)
# Ver ejemplo en docs/nginx-config.md
```

### CI/CD

```yaml
# GitHub Actions ejemplo
- name: Build Docker Image
  run: docker build -t carbon-ghg:${{ github.sha }} .

- name: Run Tests in Container
  run: |
    docker run carbon-ghg:${{ github.sha }} pytest tests/ -v

- name: Push to Registry
  run: docker push carbon-ghg:${{ github.sha }}
```

## 📚 Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Streamlit in Docker](https://docs.streamlit.io/deploy/deploy-docker)
- [Ollama Docker Guide](https://github.com/ollama/ollama/blob/main/docs/docker.md)

## 🆘 Soporte

Si encuentras problemas:

1. Revisa logs: `docker-compose logs -f`
2. Verifica health: `docker inspect carbon-ghg-streamlit`
3. Limpia y reconstruye: `docker-compose down -v && docker-compose build --no-cache`
4. Consulta la sección de Troubleshooting arriba

---

**Última actualización**: Día 3 - Diciembre 2024  
**Versión Docker**: 1.0  
**Compatibilidad**: Windows 10/11, Linux, macOS
