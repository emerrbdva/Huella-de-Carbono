# 🚀 Carbon GHG Calculator - REST API

API REST para calcular emisiones de gases de efecto invernadero (GHG) según el protocolo GHG Protocol.

## 📋 Características

- ✅ **Cálculo de emisiones** para Scope 1, 2 y 3
- ✅ **521 factores de emisión** UK Gov 2025
- ✅ **Agregación automática** por scope y categoría
- ✅ **Documentación interactiva** con Swagger UI
- ✅ **CORS habilitado** para integraciones frontend
- ✅ **Validación con Pydantic** v2
- ✅ **100% GRATIS** para deploy en Railway o Render

## 🏃 Quick Start

### 1. Instalar Dependencias

```bash
pip install fastapi uvicorn python-multipart
```

O desde requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar API Localmente

```bash
# Desde el directorio raíz del proyecto
uvicorn api.main:app --reload --port 8000
```

### 3. Acceder a la Documentación

Una vez que la API esté corriendo, abre tu navegador en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📡 Endpoints

### GET /api/v1/health

Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "factors_loaded": 521,
  "timestamp": "2025-10-08T10:30:00"
}
```

### POST /api/v1/calculate

Calcula emisiones para una lista de actividades

**Request**:
```json
{
  "activities": [
    {
      "entity_id": "factory-001",
      "scope": 1,
      "category": "mobile_combustion",
      "activity_value": 1000.0,
      "activity_unit": "liters",
      "geography": "GBR",
      "year": 2025
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "entity_id": "factory-001",
      "scope": 1,
      "category": "mobile_combustion",
      "activity_value": 1000.0,
      "activity_unit": "liters",
      "emission_kg_co2e": 2684.42,
      "emission_tonnes_co2e": 2.68442,
      "factor_source": "UK Gov 2025",
      "calculation_date": "2025-10-08T10:30:00"
    }
  ],
  "total_emissions_kg": 2684.42,
  "total_emissions_tonnes": 2.68442,
  "aggregation_by_scope": {
    "1": 2.68442,
    "2": 0.0,
    "3": 0.0
  },
  "aggregation_by_category": {
    "mobile_combustion": 2.68442
  },
  "calculation_timestamp": "2025-10-08T10:30:00"
}
```

### GET /api/v1/factors

Lista factores de emisión disponibles

**Query Parameters**:
- `scope` (optional): Filter by GHG scope (1, 2, or 3)
- `category` (optional): Filter by category name
- `geography` (optional): Filter by geography code
- `limit` (optional): Max results (default: 100, max: 1000)

**Example**:
```bash
GET /api/v1/factors?scope=1&category=mobile&limit=10
```

**Response**:
```json
{
  "total_factors": 10,
  "factors": [
    {
      "category": "mobile_combustion",
      "unit": "liters",
      "value": 2.68442,
      "source": "UK Gov 2025",
      "geography": "GBR",
      "scope": 1,
      "year": 2025
    }
  ],
  "filters_applied": {
    "scope": "1",
    "category": "mobile"
  }
}
```

### GET /api/v1/categories

Lista todas las categorías de emisiones por scope

**Response**:
```json
{
  "total_categories": 27,
  "categories_by_scope": {
    "scope_1": [
      "mobile_combustion",
      "stationary_combustion",
      "process_emissions",
      "fugitive_emissions"
    ],
    "scope_2": [
      "purchased_electricity",
      "purchased_heat",
      "purchased_steam"
    ],
    "scope_3": [
      "business_travel",
      "employee_commuting",
      "..."
    ]
  }
}
```

## 💻 Ejemplos de Uso

### Python

```python
import requests

# Calculate emissions
response = requests.post(
    "http://localhost:8000/api/v1/calculate",
    json={
        "activities": [
            {
                "entity_id": "vehicle-001",
                "scope": 1,
                "category": "mobile_combustion",
                "activity_value": 500,
                "activity_unit": "liters",
                "geography": "GBR",
                "year": 2025
            }
        ]
    }
)

data = response.json()
print(f"Total emissions: {data['total_emissions_tonnes']:.2f} tonnes CO2e")
```

### cURL

```bash
# Health check
curl -X GET "http://localhost:8000/api/v1/health"

# Calculate emission
curl -X POST "http://localhost:8000/api/v1/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "activities": [
      {
        "entity_id": "test-001",
        "scope": 1,
        "category": "mobile_combustion",
        "activity_value": 500,
        "activity_unit": "liters",
        "geography": "GBR",
        "year": 2025
      }
    ]
  }'

# List factors
curl -X GET "http://localhost:8000/api/v1/factors?scope=1&limit=10"
```

### JavaScript/TypeScript

```typescript
// Calculate emissions
const response = await fetch('http://localhost:8000/api/v1/calculate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    activities: [
      {
        entity_id: 'vehicle-001',
        scope: 1,
        category: 'mobile_combustion',
        activity_value: 500,
        activity_unit: 'liters',
        geography: 'GBR',
        year: 2025
      }
    ]
  })
});

const data = await response.json();
console.log(`Total emissions: ${data.total_emissions_tonnes.toFixed(2)} tonnes CO2e`);
```

## 🚀 Deployment

### Opción 1: Railway (Recomendado - GRATIS hasta $5/mes)

1. Crear cuenta en [Railway.app](https://railway.app/)
2. Conectar tu repositorio GitHub
3. Crear nuevo proyecto
4. Configurar variables de entorno (si es necesario)
5. Railway detectará automáticamente que es una app FastAPI
6. ¡Deploy automático!

**railway.toml** (opcional):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn api.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/api/v1/health"
restartPolicyType = "on_failure"
```

### Opción 2: Render (GRATIS)

1. Crear cuenta en [Render.com](https://render.com/)
2. Conectar repositorio GitHub
3. Crear nuevo "Web Service"
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. ¡Deploy!

### Opción 3: Docker (Local o Cloud)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t carbon-ghg-api .

# Run
docker run -p 8000:8000 carbon-ghg-api
```

## 🔒 Seguridad

### CORS

Por defecto, la API permite requests desde cualquier origen (`allow_origins=["*"]`).

**Para producción**, especifica dominios permitidos:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-app.com",
        "https://dashboard.tu-app.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Rate Limiting (Futuro)

Para producción, considera agregar rate limiting con `slowapi`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/calculate")
@limiter.limit("10/minute")
async def calculate_emissions(request: Request, ...):
    ...
```

## 📊 Monitoreo

### Logs

La API usa logging estándar de Python. Para ver logs:

```bash
uvicorn api.main:app --log-level info
```

### Métricas (Futuro)

Para producción, considera agregar Prometheus/Grafana:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🧪 Testing

```bash
# Ejecutar tests de API
pytest tests/test_api.py -v

# Con coverage
pytest tests/test_api.py --cov=api --cov-report=html
```

## 📖 Documentación Adicional

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 License

MIT License - ver archivo `LICENSE` para detalles

## 📞 Soporte

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: your-email@example.com

---

**Hecho con ❤️ por el equipo Carbon GHG**
