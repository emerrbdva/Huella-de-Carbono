# Dockerfile para Carbon GHG Calculator
# Multi-stage build para optimizar el tamaño de la imagen

# Etapa 1: Builder
FROM python:3.12-slim as builder

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --user --no-warn-script-location -r requirements.txt

# Etapa 2: Runtime
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/data /app/reports && \
    chown -R appuser:appuser /app

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde el builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Actualizar PATH para el usuario appuser
ENV PATH=/home/appuser/.local/bin:$PATH

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Asegurar permisos correctos
RUN chmod -R 755 /app && \
    chmod -R 777 /app/data /app/reports

# Cambiar a usuario no-root
USER appuser

# Exponer puerto de Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando por defecto: iniciar Streamlit
CMD ["streamlit", "run", "app/streamlit_app.py"]
