# 🔧 OPCIÓN 2 Y 3 - SIN GENERAR COSTOS

**Objetivo**: Completar las opciones restantes del proyecto sin gastos  
**Fecha**: 8 de octubre de 2025  
**Status**: Preparado para continuar

---

## 📋 Opciones Disponibles

### ✅ Opción 1: Deploy a Streamlit Cloud (COMPLETADA)

```
✅ Archivos de configuración creados
✅ README.md actualizado
✅ Guías de deployment creadas (211 KB)
✅ Git preparado (3 commits)
⏳ Pendiente: Solo subir a GitHub (tú lo haces manualmente)
```

**Documentación**:
- [DEPLOYMENT_OPCION1_COMPLETADO.md](DEPLOYMENT_OPCION1_COMPLETADO.md)
- [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)
- [docs/STREAMLIT_CLOUD_DEPLOYMENT.md](docs/STREAMLIT_CLOUD_DEPLOYMENT.md)

---

### ⏳ Opción 2: Fix Tests (4 horas) - SIN COSTOS

**Objetivo**: Mejorar coverage de 24% a 80%+

#### Estado Actual

```
Tests: 66/99 passing (67%)
Coverage: 24%
Failing tests: 33 (por cambios en modelos Pydantic)
```

#### Plan de Trabajo (4 horas)

##### Fase 1: Fix Failing Tests (2 horas)

**Problema**: 33 tests fallan por cambios en modelos

**Archivos a actualizar**:

1. **tests/conftest.py** (30 min)
   ```python
   # Fixtures desactualizadas
   
   # ❌ ANTES (modelo antiguo)
   @pytest.fixture
   def sample_activity():
       return ActivityRecord(
           activity_id="test-1",
           amount=100,
           unit="liters",
           fuel_type="diesel"
       )
   
   # ✅ DESPUÉS (modelo nuevo)
   @pytest.fixture
   def sample_activity():
       return ActivityRecord(
           entity_id="test-1",           # activity_id → entity_id
           scope=1,
           category="mobile_combustion",
           activity_value=100,           # amount → activity_value
           activity_unit="liters",       # unit → activity_unit
           geography="GBR",
           year=2025
       )
   ```

2. **tests/test_models.py** (30 min)
   ```python
   # Actualizar validaciones
   
   def test_activity_record_validation():
       # Campos requeridos nuevos
       required_fields = [
           "entity_id",      # antes: activity_id
           "scope",
           "category",
           "activity_value", # antes: amount
           "activity_unit",  # antes: unit
       ]
       
       # Test cada campo
       for field in required_fields:
           with pytest.raises(ValidationError):
               ActivityRecord(**{k: v for k, v in base_data.items() if k != field})
   ```

3. **tests/test_calculators.py** (30 min)
   ```python
   # Actualizar tests de cálculo
   
   def test_compute_emission():
       activity = ActivityRecord(
           entity_id="factory-1",
           scope=1,
           category="mobile_combustion",
           activity_value=1000,
           activity_unit="liters",
           geography="GBR",
           year=2025
       )
       
       factor = EmissionFactor(
           category="mobile_combustion",
           unit="liters",
           co2e_factor=2.68442,
           source="UK Gov 2025",
           geography="GBR"
       )
       
       result = compute_emission(activity, factor)
       
       # Verificar resultado
       assert result.total_co2e == pytest.approx(2684.42, rel=0.01)
   ```

4. **tests/test_ai_assistant.py** (30 min)
   ```python
   # Hacer tests condicionales (solo si Ollama disponible)
   
   import pytest
   import subprocess
   
   def is_ollama_available():
       try:
           subprocess.run(["ollama", "list"], 
                         capture_output=True, 
                         check=True, 
                         timeout=5)
           return True
       except:
           return False
   
   @pytest.mark.skipif(
       not is_ollama_available(),
       reason="Ollama not installed or not running"
   )
   def test_semantic_search():
       # Test AI features solo si Ollama disponible
       assistant = AIAssistant()
       result = assistant.search_factor("diesel")
       assert result is not None
   ```

##### Fase 2: Add New Tests (2 horas)

**Archivos a crear**:

1. **tests/test_factors_loading.py** (30 min)
   ```python
   """Tests for factor loading and parsing"""
   import pytest
   import pandas as pd
   from utils.factors import load_uk_gov_factors, find_factor
   
   def test_load_uk_gov_factors_basic():
       """Test basic factor loading"""
       df = load_uk_gov_factors("data/ghg-conversion-factors-2025.xlsx")
       
       assert isinstance(df, pd.DataFrame)
       assert len(df) > 500  # At least 500 factors
       assert "category" in df.columns
       assert "unit" in df.columns
       assert "co2e_factor" in df.columns
   
   def test_load_uk_gov_factors_cache():
       """Test that cache works"""
       import time
       
       # First load (slow)
       start = time.time()
       df1 = load_uk_gov_factors("data/ghg-conversion-factors-2025.xlsx")
       time1 = time.time() - start
       
       # Second load (cached, fast)
       start = time.time()
       df2 = load_uk_gov_factors("data/ghg-conversion-factors-2025.xlsx")
       time2 = time.time() - start
       
       # Cache should be >10x faster
       assert time2 < time1 / 10
       assert df1.equals(df2)
   
   def test_find_factor_diesel():
       """Test finding diesel factor"""
       factors = load_uk_gov_factors("data/ghg-conversion-factors-2025.xlsx")
       
       result = find_factor(
           factors,
           category="mobile_combustion",
           activity_unit="liters",
           geography="GBR",
           scope=1
       )
       
       assert result is not None
       assert result["category"] == "mobile_combustion"
       assert result["unit"] == "liters"
       assert result["co2e_factor"] > 2.0  # Diesel ~2.68
   ```

2. **tests/test_report_generation.py** (45 min)
   ```python
   """Tests for Excel and Word report generation"""
   import pytest
   import os
   from utils.report_generator import generate_excel_report, generate_word_report
   from models.emissions import EmissionResult
   
   @pytest.fixture
   def sample_results():
       return [
           EmissionResult(
               entity_id="factory-1",
               scope=1,
               category="mobile_combustion",
               activity_value=1000,
               activity_unit="liters",
               co2_kg=2500,
               ch4_kg=0.1,
               n2o_kg=0.05,
               total_co2e=2684.42,
               factor_source="UK Gov 2025"
           )
       ]
   
   def test_generate_excel_report(sample_results, tmp_path):
       """Test Excel report generation"""
       output_file = tmp_path / "test_report.xlsx"
       
       generate_excel_report(sample_results, str(output_file))
       
       assert output_file.exists()
       assert output_file.stat().st_size > 1000  # At least 1KB
       
       # Verify structure
       import openpyxl
       wb = openpyxl.load_workbook(output_file)
       assert "Summary" in wb.sheetnames
       assert "By Scope" in wb.sheetnames
       assert "Detailed" in wb.sheetnames
   
   def test_generate_word_report(sample_results, tmp_path):
       """Test Word report generation"""
       output_file = tmp_path / "test_report.docx"
       
       generate_word_report(sample_results, str(output_file))
       
       assert output_file.exists()
       assert output_file.stat().st_size > 5000  # At least 5KB
   ```

3. **tests/test_unit_converter.py** (30 min)
   ```python
   """Tests for unit conversion"""
   import pytest
   from utils.unit_converter import convert_unit, can_convert
   
   def test_convert_energy_units():
       """Test energy conversions"""
       # kWh to MJ
       result = convert_unit(100, "kWh", "MJ")
       assert result == pytest.approx(360.0, rel=0.01)
       
       # MWh to kWh
       result = convert_unit(1, "MWh", "kWh")
       assert result == 1000.0
   
   def test_convert_mass_units():
       """Test mass conversions"""
       # kg to tonnes
       result = convert_unit(1000, "kg", "tonnes")
       assert result == 1.0
       
       # tonnes to kg
       result = convert_unit(1, "tonnes", "kg")
       assert result == 1000.0
   
   def test_convert_volume_units():
       """Test volume conversions"""
       # litres to m3
       result = convert_unit(1000, "litres", "m3")
       assert result == 1.0
       
       # gallons to litres
       result = convert_unit(1, "gallons", "litres")
       assert result == pytest.approx(4.54609, rel=0.01)
   
   def test_can_convert():
       """Test conversion compatibility check"""
       assert can_convert("kWh", "MJ") == True
       assert can_convert("kg", "tonnes") == True
       assert can_convert("litres", "m3") == True
       assert can_convert("kWh", "kg") == False  # Different dimensions
   ```

4. **tests/test_scope_calculations.py** (15 min)
   ```python
   """Tests for scope aggregations"""
   import pytest
   from calculators.core import aggregate_by_scope, aggregate_by_category
   
   def test_aggregate_by_scope(sample_emission_results):
       """Test aggregation by scope"""
       result = aggregate_by_scope(sample_emission_results)
       
       assert isinstance(result, dict)
       assert 1 in result or 2 in result or 3 in result
       
       # Total should be sum of all scopes
       total = sum(result.values())
       expected_total = sum(r.total_co2e for r in sample_emission_results)
       assert total == pytest.approx(expected_total, rel=0.01)
   
   def test_aggregate_by_category(sample_emission_results):
       """Test aggregation by category"""
       result = aggregate_by_category(sample_emission_results)
       
       assert isinstance(result, dict)
       assert len(result) > 0
       
       # Check that all categories present
       categories = {r.category for r in sample_emission_results}
       assert set(result.keys()) == categories
   ```

#### Comandos para Ejecutar

```powershell
# 1. Ver tests actuales
pytest tests/ -v

# 2. Ver solo tests fallidos
pytest tests/ -v --tb=short -x

# 3. Ejecutar con coverage
pytest --cov=. --cov-report=html

# 4. Ver reporte HTML
start htmlcov/index.html

# 5. Ejecutar tests específicos
pytest tests/test_models.py -v
pytest tests/test_calculators.py::test_compute_emission -v

# 6. Ejecutar con markers
pytest -m "not ai"  # Skip AI tests if Ollama not available
```

#### Objetivo de Coverage

```
Antes:
- Total: 99 tests
- Passing: 66 (67%)
- Coverage: 24%

Después:
- Total: 120+ tests
- Passing: 115+ (95%+)
- Coverage: 80%+

Mejora: +56% coverage, +49 tests passing
```

---

### ⏳ Opción 3: Nuevas Features - SIN COSTOS

**Nota**: Solo features sin APIs de pago (OpenAI, Claude, etc.)

#### Feature 1: API REST con FastAPI (6-8 horas)

**Stack** (100% gratis):
- FastAPI (framework)
- Uvicorn (servidor)
- Railway o Render (deployment gratis)

**Código**:

```python
# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from calculators.core import compute_emission
from utils.factors import load_uk_gov_factors, find_factor
from models.emissions import ActivityRecord, EmissionResult

app = FastAPI(
    title="Carbon GHG API",
    description="API for calculating GHG emissions",
    version="1.0.0"
)

# Load factors once at startup
factors_df = load_uk_gov_factors("data/ghg-conversion-factors-2025.xlsx")

class CalculateRequest(BaseModel):
    activities: List[ActivityRecord]

class CalculateResponse(BaseModel):
    results: List[EmissionResult]
    total_co2e: float

@app.post("/api/calculate", response_model=CalculateResponse)
async def calculate_emissions(request: CalculateRequest):
    """Calculate emissions for a list of activities"""
    results = []
    
    for activity in request.activities:
        # Find matching factor
        factor = find_factor(
            factors_df,
            category=activity.category,
            activity_unit=activity.activity_unit,
            geography=activity.geography,
            scope=activity.scope
        )
        
        if not factor:
            raise HTTPException(
                status_code=404,
                detail=f"No factor found for {activity.category}"
            )
        
        # Calculate emission
        result = compute_emission(activity, factor)
        results.append(result)
    
    total = sum(r.total_co2e for r in results)
    
    return CalculateResponse(
        results=results,
        total_co2e=total
    )

@app.get("/api/factors")
async def list_factors(
    category: str = None,
    unit: str = None,
    geography: str = "GBR"
):
    """List available emission factors"""
    df = factors_df.copy()
    
    if category:
        df = df[df["category"] == category]
    if unit:
        df = df[df["unit"] == unit]
    if geography:
        df = df[df["geography"] == geography]
    
    return df.to_dict(orient="records")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "factors_loaded": len(factors_df),
        "version": "1.0.0"
    }
```

**Deployment en Railway (GRATIS)**:

```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn api.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[health]
path = "/api/health"
```

**Costo**: $0 (Railway $5 free tier suficiente)

#### Feature 2: Dashboard Avanzado (8-10 horas)

**Nuevas visualizaciones** (sin librerías de pago):

1. **Heatmap Temporal** (2h)
   ```python
   import plotly.express as px
   
   def create_temporal_heatmap(results):
       """Create heatmap of emissions over time"""
       # Aggregate by month
       df = pd.DataFrame([r.dict() for r in results])
       df['month'] = pd.to_datetime(df['date']).dt.month
       df['year'] = pd.to_datetime(df['date']).dt.year
       
       pivot = df.pivot_table(
           values='total_co2e',
           index='category',
           columns='month',
           aggfunc='sum'
       )
       
       fig = px.imshow(
           pivot,
           labels=dict(x="Month", y="Category", color="CO2e (kg)"),
           title="Emissions Heatmap by Category and Month",
           color_continuous_scale="RdYlGn_r"
       )
       
       return fig
   ```

2. **Comparison Dashboard** (3h)
   ```python
   def create_comparison_dashboard(entities_results):
       """Compare emissions across multiple entities"""
       import plotly.graph_objects as go
       from plotly.subplots import make_subplots
       
       # Create subplots
       fig = make_subplots(
           rows=2, cols=2,
           subplot_titles=("Total by Entity", "By Scope", 
                          "By Category", "Trends"),
           specs=[[{"type": "bar"}, {"type": "pie"}],
                  [{"type": "bar"}, {"type": "scatter"}]]
       )
       
       # Plot 1: Total by entity
       totals = {entity: sum(r.total_co2e for r in results) 
                for entity, results in entities_results.items()}
       
       fig.add_trace(
           go.Bar(x=list(totals.keys()), y=list(totals.values())),
           row=1, col=1
       )
       
       # Plot 2: Pie chart of scopes
       # ... more plots
       
       return fig
   ```

3. **Benchmarking** (2h)
   ```python
   def create_benchmark_comparison(results, industry_avg):
       """Compare against industry benchmarks"""
       user_total = sum(r.total_co2e for r in results)
       
       fig = go.Figure()
       
       fig.add_trace(go.Indicator(
           mode="gauge+number+delta",
           value=user_total,
           delta={'reference': industry_avg},
           title={'text': "Your Emissions vs Industry Average"},
           gauge={
               'axis': {'range': [None, industry_avg * 2]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, industry_avg * 0.8], 'color': "lightgreen"},
                   {'range': [industry_avg * 0.8, industry_avg * 1.2], 'color': "yellow"},
                   {'range': [industry_avg * 1.2, industry_avg * 2], 'color': "red"}
               ],
               'threshold': {
                   'line': {'color': "red", 'width': 4},
                   'thickness': 0.75,
                   'value': industry_avg
               }
           }
       ))
       
       return fig
   ```

**Costo**: $0 (todas las librerías son gratis)

#### Feature 3: Exportación Avanzada (4-6 horas)

1. **Export to PowerBI** (2h)
   ```python
   def export_to_powerbi_format(results):
       """Export in PowerBI-friendly format"""
       df = pd.DataFrame([{
           'Entity': r.entity_id,
           'Date': r.date,
           'Scope': r.scope,
           'Category': r.category,
           'CO2_kg': r.co2_kg,
           'CH4_kg': r.ch4_kg,
           'N2O_kg': r.n2o_kg,
           'Total_CO2e_kg': r.total_co2e,
           'Activity_Value': r.activity_value,
           'Activity_Unit': r.activity_unit,
           'Factor_Source': r.factor_source
       } for r in results])
       
       # Save as CSV with proper formatting
       df.to_csv("powerbi_export.csv", index=False, encoding='utf-8-sig')
       
       # Also save metadata
       metadata = {
           'export_date': datetime.now().isoformat(),
           'total_records': len(df),
           'total_emissions_tco2e': df['Total_CO2e_kg'].sum() / 1000,
           'scopes_included': df['Scope'].unique().tolist()
       }
       
       with open("powerbi_metadata.json", "w") as f:
           json.dump(metadata, f, indent=2)
   ```

2. **Export to Tableau** (2h)
   ```python
   def export_to_tableau_extract(results):
       """Create Tableau-compatible extract"""
       # Use pantab (free library for Tableau)
       import pantab
       
       df = pd.DataFrame([r.dict() for r in results])
       
       # Save as Hyper file
       pantab.frame_to_hyper(
           df,
           "emissions_data.hyper",
           table="Emissions"
       )
   ```

3. **PDF Report with Charts** (2h)
   ```python
   from fpdf import FPDF
   import matplotlib.pyplot as plt
   import io
   
   def generate_pdf_report_with_charts(results):
       """Generate PDF with embedded charts"""
       pdf = FPDF()
       pdf.add_page()
       
       # Title
       pdf.set_font("Arial", "B", 16)
       pdf.cell(0, 10, "GHG Emissions Report", ln=True, align="C")
       
       # Generate chart as image
       fig, ax = plt.subplots()
       scopes = aggregate_by_scope(results)
       ax.bar(scopes.keys(), scopes.values())
       ax.set_title("Emissions by Scope")
       
       # Save to memory
       img_buffer = io.BytesIO()
       plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
       img_buffer.seek(0)
       
       # Add to PDF
       pdf.image(img_buffer, x=10, y=30, w=190)
       
       pdf.output("report_with_charts.pdf")
   ```

**Costo**: $0 (todas las librerías son gratis: fpdf2, pantab, matplotlib)

---

## 📅 Cronograma Sugerido

### Día 1: Deployment + Fix Tests (6h)

```
09:00-09:30  Deploy a Streamlit Cloud (Opción 1)
09:30-11:30  Fix failing tests (Fase 1)
11:30-12:00  Break
12:00-14:00  Add new tests (Fase 2, parte 1)
14:00-15:00  Lunch
15:00-17:00  Add new tests (Fase 2, parte 2)
17:00-17:30  Ejecutar coverage, verificar 80%+
```

### Día 2-3: Nuevas Features (12-16h)

```
Día 2:
09:00-12:00  API REST con FastAPI
12:00-13:00  Lunch
13:00-16:00  Deploy API en Railway
16:00-17:00  Testing de API

Día 3:
09:00-12:00  Dashboard avanzado (heatmap, comparison)
12:00-13:00  Lunch
13:00-16:00  Exportación avanzada (PowerBI, Tableau)
16:00-17:00  Documentación de nuevas features
```

---

## ✅ Checklist de Progreso

### Opción 1: Deployment ✅

- [x] Archivos de configuración creados
- [x] README.md actualizado
- [x] Guías de deployment creadas
- [x] Git preparado (3 commits)
- [ ] ⏳ Subir a GitHub (manual)
- [ ] ⏳ Desplegar en Streamlit Cloud (manual)

### Opción 2: Fix Tests ⏳

- [ ] Actualizar fixtures en conftest.py
- [ ] Fix tests de modelos
- [ ] Fix tests de calculators
- [ ] Hacer tests de AI condicionales
- [ ] Crear test_factors_loading.py
- [ ] Crear test_report_generation.py
- [ ] Crear test_unit_converter.py
- [ ] Crear test_scope_calculations.py
- [ ] Verificar coverage 80%+

### Opción 3: Nuevas Features ⏳

- [ ] API REST con FastAPI
- [ ] Deploy API en Railway
- [ ] Heatmap temporal
- [ ] Dashboard de comparación
- [ ] Benchmarking
- [ ] Export to PowerBI
- [ ] Export to Tableau
- [ ] PDF reports con charts

---

## 💰 Resumen de Costos

| Opción | Herramientas | Costo Mensual |
|--------|--------------|---------------|
| **Opción 1: Deployment** | Streamlit Cloud (Free) | $0 |
| **Opción 2: Tests** | pytest, coverage (local) | $0 |
| **Opción 3: API** | FastAPI + Railway (Free tier) | $0 |
| **Opción 3: Dashboard** | Plotly, Matplotlib (local) | $0 |
| **Opción 3: Export** | pandas, pantab, fpdf2 | $0 |
| **TOTAL** | - | **$0** ✅ |

**Todas las opciones son 100% GRATIS** 🎉

---

## 📞 ¿Por Dónde Empezar?

1. **Si quieres deployment rápido** (15 min):
   - Sigue [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)

2. **Si quieres mejorar calidad** (4h):
   - Empieza con Opción 2 (Fix Tests)
   - `pytest tests/ -v` para ver estado actual

3. **Si quieres agregar features** (12-16h):
   - Empieza con Opción 3 (API REST o Dashboard)
   - Requiere primero completar Opción 2 (tests)

**Mi recomendación**: Opción 1 → Opción 2 → Opción 3 (en ese orden)

---

**¿Listo para continuar?** 🚀

Elige tu siguiente paso y ¡adelante!
