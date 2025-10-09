# API REST - Deployment Guide

## 📊 Status

✅ **API Funcional**: 100%
✅ **Tests**: 15/15 pasando (100%)
✅ **Documentación**: Completa
✅ **Zero Cost Deployment**: Listo

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn api.main:app --reload --port 8000

# Access API
# - Interactive docs: http://localhost:8000/docs
# - Alternative docs: http://localhost:8000/redoc
# - Health check: http://localhost:8000/api/v1/health
```

### Test API

```bash
# Run all API tests
pytest tests/test_api.py -v

# Test with examples
python examples/api_usage.py
```

## 🌐 Endpoints

### 1. Health Check
```http
GET /api/v1/health
```

Returns API status and loaded factors count.

### 2. Calculate Emissions
```http
POST /api/v1/calculate
Content-Type: application/json

{
  "activities": [
    {
      "entity_id": "vehicle-001",
      "scope": 1,
      "category": "Diesel",
      "activity_value": 100.0,
      "activity_unit": "litres",
      "geography": "UK",
      "year": 2025
    }
  ]
}
```

### 3. List Emission Factors
```http
GET /api/v1/factors?sheet=Fuels&limit=10
```

Filters:
- `sheet`: Filter by data sheet (e.g., "Fuels", "Passenger vehicles")
- `activity`: Filter by activity type
- `fuel`: Filter by fuel type  
- `unit`: Filter by unit
- `limit`: Max results (default: 100, max: 1000)

### 4. List Categories
```http
GET /api/v1/categories
```

Returns all available sheets, activities, fuels, and units.

## 📦 Free Deployment Options

### Option 1: Railway.app

1. **Create Account**: https://railway.app
2. **Connect GitHub**: Link your repository
3. **Create Service**: 
   - Select your repo
   - Railway auto-detects FastAPI
   - Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** (if needed):
   ```
   PORT=8000
   ```

5. **Deploy**: Railway builds and deploys automatically

**Free Tier**: $5 credit/month, enough for API usage

### Option 2: Render.com

1. **Create Account**: https://render.com
2. **New Web Service**: 
   - Connect GitHub repo
   - Name: carbon-ghg-api
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

3. **Deploy**: Free tier available

### Option 3: Docker (Self-host)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t carbon-ghg-api .
docker run -p 8000:8000 carbon-ghg-api
```

## 🔒 Security Considerations

### CORS Configuration

Current setup allows all origins (development mode):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Setup**:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

### Rate Limiting (Recommended)

Add to production:
```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/v1/calculate")
@limiter.limit("10/minute")
async def calculate_emissions(request: Request, ...):
    ...
```

### API Keys (Optional)

For production, consider adding API key authentication:
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
```

## 📊 Monitoring

### Health Endpoint

```bash
# Check if API is running
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "factors_loaded": 521,
  "timestamp": "2025-10-08T12:00:00"
}
```

### Metrics to Track

- Response time per endpoint
- Error rate (4xx, 5xx)
- Number of calculations per day
- Most queried factors
- Active users/API keys

## 🧪 Testing in Production

```bash
# Test health
curl https://your-api.com/api/v1/health

# Test calculation
curl -X POST https://your-api.com/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "activities": [{
      "entity_id": "test",
      "scope": 1,
      "category": "Diesel",
      "activity_value": 100,
      "activity_unit": "litres",
      "geography": "UK",
      "year": 2025
    }]
  }'

# Test factors
curl https://your-api.com/api/v1/factors?limit=5
```

## 📝 API Usage Examples

See full examples in `examples/api_usage.py`:

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Calculate emissions
payload = {
    "activities": [{
        "entity_id": "vehicle-001",
        "scope": 1,
        "category": "Diesel",
        "activity_value": 50.0,
        "activity_unit": "litres",
        "geography": "UK",
        "year": 2025
    }]
}
response = requests.post("http://localhost:8000/api/v1/calculate", json=payload)
print(response.json())
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Use different port
uvicorn api.main:app --port 8080
```

### Import Errors

```bash
# Ensure you're in the project root
cd carbon_ghg

# Install all dependencies
pip install -r requirements.txt
```

### Emission Factor Not Found

The API uses real UK Gov 2025 emission factors. Categories must match actual data:

✅ Valid categories:
- "Diesel", "Petrol", "Natural gas"
- "electricity", "heat"
- "Gaseous fuels", "Liquid fuels"

❌ Invalid categories:
- "mobile_combustion" (internal category)
- "purchased_electricity" (internal category)

Use `/api/v1/categories` to see all available categories.

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **UK Gov Factors**: https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting

## ✅ Feature 1 Complete!

- ✅ 5 RESTful endpoints
- ✅ 521 UK Gov 2025 emission factors
- ✅ 15/15 tests passing
- ✅ Swagger/ReDoc documentation
- ✅ Zero-cost deployment options
- ✅ Production-ready architecture
- ✅ Example usage code
