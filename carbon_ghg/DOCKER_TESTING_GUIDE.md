# 🐳 DOCKER TESTING - Guía de Ejecución

**Fecha**: Octubre 8, 2025  
**Status**: ⏳ PENDIENTE - Docker Desktop no iniciado  
**Tiempo estimado**: 30 minutos

---

## ⚠️ PRERREQUISITO

### Docker Desktop no está en ejecución

**Error encontrado**:
```
ERROR: error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**Solución**:
1. Abre **Docker Desktop** desde el menú inicio de Windows
2. Espera a que el ícono de Docker en la bandeja del sistema muestre "Docker Desktop is running"
3. Verifica con: `docker ps` (debe retornar una lista vacía, no un error)

---

## 📋 CHECKLIST DE DOCKER TESTING

### Paso 1: Iniciar Docker Desktop (2 min)
```powershell
# 1. Abrir Docker Desktop manualmente
# - Buscar en inicio: "Docker Desktop"
# - Click en el icono
# - Esperar a que esté "Running" (verde en la bandeja del sistema)

# 2. Verificar que está corriendo
docker ps

# Salida esperada: Lista vacía (tabla con headers pero sin containers)
# CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### Paso 2: Build de Imagen (3-5 min)
```powershell
cd "c:\Python\Huella de Carbono\carbon_ghg"

# Construir imagen multi-stage
docker build -t carbon-ghg:1.0 .

# Verificar imagen creada
docker images carbon-ghg

# Salida esperada:
# REPOSITORY    TAG   IMAGE ID       CREATED         SIZE
# carbon-ghg    1.0   xxxxxxxxxxxxx  X seconds ago   ~450MB
```

### Paso 3: Test Básico - Sin IA (5 min)
```powershell
# Levantar servicio (sin Ollama)
docker-compose up -d

# Verificar que está corriendo
docker ps

# Salida esperada:
# Debe mostrar container "carbon_ghg_app" con status "Up X seconds"
# Puerto: 0.0.0.0:8501->8501/tcp

# Ver logs (opcional)
docker-compose logs -f

# Abrir en navegador
start http://localhost:8501

# Probar funcionalidad:
# 1. ✅ Página carga correctamente
# 2. ✅ Sidebar visible con navegación
# 3. ✅ Cargar sample_activities.csv desde data/
# 4. ✅ Ver resultados de cálculos
# 5. ✅ Verificar visualizaciones (Sankey, Treemap, Temporal)

# Detener
docker-compose down
```

### Paso 4: Test con IA Profile (10 min) - OPCIONAL
```powershell
# Levantar con Ollama
docker-compose --profile with-ai up -d

# Verificar ambos servicios
docker ps

# Salida esperada: 2 containers
# - carbon_ghg_app (8501)
# - ollama (11434)

# Esperar a que Ollama descargue modelo (primera vez ~5 min)
docker-compose logs ollama -f

# En el navegador (localhost:8501):
# 1. Ir a tab "🤖 Asistente IA"
# 2. Probar categorización automática
# 3. Probar búsqueda semántica
# 4. Ver recomendaciones

# Detener todo
docker-compose --profile with-ai down
```

### Paso 5: Verificar Volúmenes (2 min)
```powershell
# Listar volúmenes creados
docker volume ls | Select-String "carbon"

# Salida esperada:
# carbon_ghg_data
# carbon_ghg_reports
# carbon_ghg_ollama_data (si usaste profile with-ai)

# Ver contenido de volumen (opcional)
docker run --rm -v carbon_ghg_data:/data alpine ls -la /data

# Limpiar volúmenes (después de todas las pruebas)
docker-compose down -v
```

### Paso 6: Health Checks (2 min)
```powershell
# Ver estado de health check
docker inspect carbon_ghg_app | Select-String -Pattern "Health" -Context 5

# Salida esperada:
# "Health": {
#     "Status": "healthy",
#     "FailingStreak": 0,
#     "Log": [...]
# }

# Verificar directamente
docker exec carbon_ghg_app curl -f http://localhost:8501/_stcore/health
```

### Paso 7: Performance Testing (3 min)
```powershell
# Ver uso de recursos
docker stats --no-stream carbon_ghg_app

# Salida esperada:
# CONTAINER        CPU %    MEM USAGE / LIMIT     MEM %
# carbon_ghg_app   0-5%     ~200-400MB / 2GB      10-20%

# Cargar archivo grande (1000+ actividades)
# Medir tiempo de respuesta en navegador
# Objetivo: <10 segundos para cálculos
```

---

## ✅ CHECKLIST DE VALIDACIÓN

### Funcionalidad Básica:
- [ ] Docker Desktop iniciado y corriendo
- [ ] Imagen construida exitosamente (~450MB)
- [ ] Container levanta sin errores
- [ ] Puerto 8501 accesible desde navegador
- [ ] UI de Streamlit carga correctamente
- [ ] Sample data se puede cargar
- [ ] Cálculos funcionan correctamente
- [ ] Visualizaciones se generan

### Funcionalidad con IA (Opcional):
- [ ] Profile with-ai levanta 2 containers
- [ ] Ollama descarga modelo llama3:latest
- [ ] Categorización automática funciona
- [ ] Búsqueda semántica retorna resultados
- [ ] Recomendaciones se generan

### DevOps:
- [ ] Volúmenes se crean correctamente
- [ ] Health checks pasan (healthy)
- [ ] Logs accesibles via docker-compose logs
- [ ] Performance aceptable (<400MB RAM)
- [ ] Cleanup funciona (docker-compose down -v)

---

## 🐛 TROUBLESHOOTING

### Error: "Cannot connect to Docker daemon"
```powershell
# Solución 1: Iniciar Docker Desktop
# Solución 2: Reiniciar servicio
net stop com.docker.service
net start com.docker.service
```

### Error: "Port 8501 already in use"
```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :8501

# Opción 1: Matar proceso
Stop-Process -Id <PID> -Force

# Opción 2: Cambiar puerto en docker-compose.yml
# ports: "8502:8501"
```

### Error: "Image build failed"
```powershell
# Limpiar cache y rebuild
docker builder prune -a
docker build --no-cache -t carbon-ghg:1.0 .
```

### Error: Streamlit no carga
```powershell
# Ver logs detallados
docker-compose logs app

# Verificar health
docker exec carbon_ghg_app curl http://localhost:8501/_stcore/health

# Reiniciar container
docker-compose restart app
```

### Error: Ollama no descarga modelo
```powershell
# Ver logs de Ollama
docker-compose logs ollama

# Entrar al container y descargar manualmente
docker exec -it ollama ollama pull llama3:latest

# Verificar modelos disponibles
docker exec ollama ollama list
```

---

## 📊 RESULTADOS ESPERADOS

### Build Success:
```
[+] Building 120.5s (18/18) FINISHED
 => [builder 1/6] FROM python:3.12-slim
 => [builder 2/6] WORKDIR /app
 => [builder 3/6] RUN apt-get update && apt-get install
 => [builder 4/6] COPY requirements.txt .
 => [builder 5/6] RUN pip install --user
 => [runtime 1/8] FROM python:3.12-slim
 => [runtime 2/8] RUN useradd -m -u 1000 appuser
 => [runtime 3/8] WORKDIR /app
 => [runtime 4/8] COPY --from=builder
 => [runtime 5/8] COPY --chown=appuser:appuser
 => [runtime 6/8] EXPOSE 8501
 => [runtime 7/8] USER appuser
 => [runtime 8/8] CMD ["streamlit", "run", "app/streamlit_app.py"]
 => exporting to image
 => naming to docker.io/library/carbon-ghg:1.0

Successfully built xxxxxxxxxxxxx
Successfully tagged carbon-ghg:1.0
```

### Container Running:
```
CONTAINER ID   IMAGE            COMMAND                  STATUS
abc123def456   carbon-ghg:1.0   "streamlit run app/…"   Up 30 seconds (healthy)
```

### Browser Success:
- URL: http://localhost:8501
- Título: "Carbon GHG Calculator 🌍"
- Sidebar con 6 pestañas
- Datos de ejemplo cargables
- Gráficos interactivos funcionando

---

## 🎯 CRITERIOS DE ÉXITO

### Mínimo (10 min):
1. ✅ Imagen construida
2. ✅ Container corriendo
3. ✅ UI accesible en navegador
4. ✅ Sample data carga

### Completo (30 min):
1. ✅ Todo lo anterior
2. ✅ Cálculos funcionan correctamente
3. ✅ Visualizaciones se generan
4. ✅ Health checks pasan
5. ✅ Volúmenes persisten datos
6. ✅ Performance aceptable

### Avanzado (60 min - Opcional):
1. ✅ Todo lo anterior
2. ✅ Profile with-ai funciona
3. ✅ Ollama responde correctamente
4. ✅ IA features operativas
5. ✅ Stress test con 1000+ actividades

---

## 📝 SIGUIENTE PASO DESPUÉS DE DOCKER

Una vez completado Docker testing:

### Opción 1: User Manual (1 hora)
- Crear `docs/USER_GUIDE.md`
- Incluir guía de plantilla Excel
- Screenshots del workflow
- Casos de uso comunes

### Opción 2: Pasar a Prioridad Media
- Implementar cache (@lru_cache, @st.cache_data)
- API Reference documentation
- Developer Guide

---

## 🚀 COMANDO RÁPIDO PARA EMPEZAR

```powershell
# 1. Iniciar Docker Desktop (manual)

# 2. Verificar
docker ps

# 3. Build
cd "c:\Python\Huella de Carbono\carbon_ghg"
docker build -t carbon-ghg:1.0 .

# 4. Run
docker-compose up -d

# 5. Test
start http://localhost:8501

# 6. Stop
docker-compose down
```

---

**Preparado**: Octubre 8, 2025  
**Prerequisito**: ⚠️ Iniciar Docker Desktop  
**Tiempo total**: 30 minutos  
**Dificultad**: Fácil  
**Status**: LISTO PARA EJECUTAR (una vez Docker Desktop iniciado)
