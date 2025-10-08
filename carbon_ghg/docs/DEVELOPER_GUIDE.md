# 👨‍💻 Developer Guide - Carbon GHG Calculator

**Versión**: 1.0  
**Fecha**: 8 de octubre de 2025  
**Audiencia**: Desarrolladores, Contribuidores  
**Nivel**: Intermedio a Avanzado

---

## 📑 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Setup de Desarrollo](#setup-de-desarrollo)
4. [Flujo de Datos](#flujo-de-datos)
5. [Extensibilidad](#extensibilidad)
6. [Testing y QA](#testing-y-qa)
7. [Deployment](#deployment)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Contribuir al Proyecto](#contribuir-al-proyecto)

---

## 📖 Introducción

Bienvenido a la guía de desarrollo del **Carbon GHG Calculator**. Este documento te ayudará a:

- ✅ Entender la arquitectura interna del sistema
- ✅ Configurar tu entorno de desarrollo local
- ✅ Extender el sistema con nuevas funcionalidades
- ✅ Implementar tests robustos
- ✅ Contribuir al proyecto siguiendo mejores prácticas

### **Filosofía de Diseño**

El Carbon GHG Calculator sigue estos principios:

1. **Simplicidad sobre Complejidad**: Código legible > código "inteligente"
2. **Modularidad**: Componentes independientes y reutilizables
3. **Type Safety**: Uso extensivo de type hints y dataclasses
4. **Performance**: Optimizaciones con caching donde importa
5. **Extensibilidad**: Fácil agregar nuevas fuentes de datos, categorías, etc.

---

## 🏗️ Arquitectura del Sistema

### **Diagrama de Alto Nivel**

```
┌──────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                       │
│                   (app/streamlit_app.py)                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │    Tabs     │  │   Sidebar    │  │  Components  │        │
│  │ (Data, Calc)│  │  (Config)    │  │  (Charts)    │        │
│  └─────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────┬─────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
┌──────────┐  ┌───────────┐  ┌────────────┐
│ BUSINESS │  │   MODELS  │  │  UTILITIES │
│  LOGIC   │  │           │  │            │
│          │  │           │  │            │
│calculators│  │ emissions │  │  factors   │
│  core.py │  │  .py      │  │  .py       │
│          │  │           │  │            │
│          │  │  Activity │  │ validator  │
│compute_  │  │  Record   │  │  .py       │
│emission  │  │           │  │            │
│          │  │ Emission  │  │ unit_      │
│aggregate_│  │  Factor   │  │ converter  │
│by_scope  │  │           │  │  .py       │
│          │  │ Emission  │  │            │
│get_total │  │  Result   │  │ report_    │
│          │  │           │  │ generator  │
└──────────┘  └───────────┘  └────────────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
                     ▼
            ┌────────────────┐
            │   DATA LAYER   │
            │                │
            │  Excel/CSV     │
            │  Databases     │
            │  APIs          │
            └────────────────┘
```

### **Módulos y Responsabilidades**

| Módulo | Propósito | Dependencias |
|--------|-----------|--------------|
| **app/** | UI y presentación | streamlit, plotly |
| **calculators/** | Lógica de cálculo | models, utils |
| **models/** | Estructuras de datos | dataclasses, datetime |
| **utils/** | Utilidades | pandas, logging |
| **tests/** | Suite de pruebas | pytest, fixtures |

---

### **Patrón de Diseño**

El sistema sigue una **arquitectura en capas**:

```python
# CAPA 1: Datos (Data Layer)
CSV/Excel → pandas.DataFrame

# CAPA 2: Modelos (Models Layer)
DataFrame → ActivityRecord (dataclass)

# CAPA 3: Negocio (Business Logic Layer)
ActivityRecord + EmissionFactor → compute_emission() → EmissionResult

# CAPA 4: Presentación (Presentation Layer)
EmissionResult → Streamlit Charts/Tables
```

**Beneficios**:
- ✅ Separación de responsabilidades
- ✅ Fácil de testear (mockear capas)
- ✅ Reutilizable (lógica independiente de UI)
- ✅ Escalable (agregar nuevas capas sin romper existentes)

---

## 🛠️ Setup de Desarrollo

### **Pre-requisitos**

- **Python**: 3.10+ (recomendado 3.12)
- **Git**: Para control de versiones
- **IDE**: VS Code, PyCharm, o tu preferido
- **Docker**: Opcional, para testing en containers

### **1. Clonar el Repositorio**

```bash
git clone https://github.com/tu-org/carbon-ghg-calculator.git
cd carbon-ghg-calculator
```

### **2. Crear Entorno Virtual**

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar Dependencias**

```bash
# Dependencias base (producción)
pip install -r requirements.txt

# Dependencias de desarrollo (testing, linting, etc.)
pip install -r requirements-dev.txt
```

**requirements-dev.txt** (crear si no existe):
```txt
# Testing
pytest==7.4.4
pytest-cov==4.1.0
pytest-mock==3.12.0

# Linting & Formatting
black==23.12.1
flake8==7.0.0
mypy==1.8.0
isort==5.13.2

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0

# Development Tools
ipython==8.19.0
jupyter==1.0.0
py-spy==0.3.14  # Profiling
```

### **4. Configurar IDE**

#### **VS Code (.vscode/settings.json)**
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

#### **PyCharm**
- Settings → Tools → Python Integrated Tools → Default test runner: pytest
- Settings → Tools → Black: Enable "Black formatter"

### **5. Verificar Setup**

```bash
# Ejecutar tests
pytest tests/ -v

# Output esperado:
# tests/test_basic.py::test_activity_record_creation PASSED
# tests/test_basic.py::test_emission_factor_creation PASSED
# ...
# ====================== 25 passed in 2.34s ======================

# Verificar imports
python -c "from models.emissions import ActivityRecord; print('✅ OK')"

# Ejecutar app (opcional)
streamlit run app/streamlit_app.py
```

---

## 🔄 Flujo de Datos

### **1. Ingesta de Datos**

```python
# Entrada: CSV/Excel
data/mis_actividades.csv
↓
# Lectura con pandas
df = pd.read_csv("data/mis_actividades.csv")
↓
# Validación
from utils.data_validator import validate_activity_data
valid_activities, report = validate_activity_data(df)
↓
# Conversión a dataclass
ActivityRecord.from_csv_row(row) × N filas
↓
# Output: List[ActivityRecord]
[ActivityRecord(...), ActivityRecord(...), ...]
```

### **2. Búsqueda de Factores**

```python
# Entrada: ActivityRecord
activity = ActivityRecord(
    category="mobile_combustion",
    unit="litres",
    ...
)
↓
# Carga de factores (cacheada)
factors_df = load_uk_gov_factors("data/factors.xlsx")
↓
# Búsqueda con matching lógico
factor_result = find_factor(
    factors_df,
    category=activity.category,
    unit=activity.unit,
    geography=activity.geography
)
↓
# Output: Tuple[float, str, Dict]
(2.68442, "UK2025", {"unit": "litres", ...})
```

### **3. Cálculo de Emisiones**

```python
# Entrada: ActivityRecord + EmissionFactor
activity = ActivityRecord(activity_value=1000, unit="litres")
factor = EmissionFactor(value=2.68442, unit="litres")
↓
# Cálculo (con conversión de unidades si es necesario)
result = compute_emission(activity, factor)
↓
# Fórmula aplicada
E = Activity Data (1000) × Emission Factor (2.68442)
E = 2684.42 kg CO2e
↓
# Output: EmissionResult
EmissionResult(
    emission_kgCO2e=2684.42,
    emission_tCO2e=2.68442,
    ...
)
```

### **4. Agregación y Presentación**

```python
# Entrada: List[EmissionResult]
results = [result1, result2, ..., resultN]
↓
# Agregaciones
by_scope = aggregate_emissions_by_scope(results)
by_category = aggregate_emissions_by_category(results)
totals = get_total_emissions(results)
↓
# Visualizaciones (cacheadas)
fig_sankey = create_sankey_chart(results)  # Plotly Figure
fig_treemap = create_treemap_chart(results)  # Plotly Figure
↓
# Renderizado en Streamlit
st.plotly_chart(fig_sankey)
st.plotly_chart(fig_treemap)
```

---

## 🔧 Extensibilidad

### **Caso 1: Agregar Nueva Categoría GHG**

Supongamos que quieres agregar `crypto_mining` como nueva categoría en Scope 2.

#### **Paso 1: Modificar `models/emissions.py`**

```python
# models/emissions.py

# Agregar a SCOPE_2_CATEGORIES
SCOPE_2_CATEGORIES = {
    "purchased_electricity": "Purchased Electricity",
    "purchased_heat_steam": "Purchased Heat & Steam (Cooling)",
    "crypto_mining": "Cryptocurrency Mining (Electricity)",  # ✅ NUEVO
}

# Actualizar CATEGORY_SCOPES
CATEGORY_SCOPES = {
    # ... existing ...
    "crypto_mining": 2,  # ✅ NUEVO
}
```

#### **Paso 2: Agregar Factor de Emisión**

Opción A: Usar factor existente (electricity)
```python
# No requiere cambios, find_factor() encontrará factor de electricidad
```

Opción B: Agregar factor personalizado en Excel
```csv
Sheet,Level 1,Level 2,Unit,kg CO2e
Crypto Mining,Bitcoin Mining,Average,kWh,0.450
Crypto Mining,Ethereum Mining,Average,kWh,0.380
```

#### **Paso 3: Actualizar Tests**

```python
# tests/test_emissions.py

def test_crypto_mining_category():
    """Test nueva categoría crypto_mining"""
    activity = ActivityRecord(
        entity_id="Mining_Farm_001",
        scope=2,
        category="crypto_mining",  # ✅ Nueva categoría
        activity_value=10000,
        activity_unit="kWh"
    )
    
    factor = EmissionFactor(
        source="Custom",
        gas="CO2e",
        value=0.450,  # kg CO2e / kWh
        unit="kWh",
        year=2025,
        scope=2,
        category="crypto_mining"
    )
    
    result = compute_emission(activity, factor)
    
    assert result.emission_kgCO2e == 4500.0
    assert result.category_label == "Cryptocurrency Mining (Electricity)"
    assert result.scope == 2
```

#### **Paso 4: Actualizar Documentación**

```markdown
# docs/USER_GUIDE.md

## Categorías Soportadas

### Scope 2 (Emisiones Indirectas - Energía)

1. **purchased_electricity**: Electricidad comprada de la red
2. **purchased_heat_steam**: Calor, vapor o refrigeración comprados
3. **crypto_mining**: Minería de criptomonedas (Nuevo en v1.1) ✨
```

#### **Paso 5: Probar end-to-end**

```python
# script de prueba
activity_df = pd.DataFrame([{
    "entity_id": "Mining_Farm",
    "scope": 2,
    "category": "crypto_mining",
    "activity_value": 50000,
    "activity_unit": "kWh"
}])

valid_activities, _ = validate_activity_data(activity_df)
# ... calcular emisiones ...
# ... verificar resultado ...
```

---

### **Caso 2: Agregar Nueva Fuente de Factores**

Supongamos que quieres soportar factores de **EPA USA 2024**.

#### **Paso 1: Crear Parser**

```python
# utils/factors.py

def load_epa_factors(file_path: str, year: int = 2024) -> pd.DataFrame:
    """
    Carga factores de emisión de EPA USA.
    
    Args:
        file_path: Ruta al archivo Excel de EPA eGRID
        year: Año de los factores (2023, 2024, etc.)
    
    Returns:
        DataFrame normalizado (mismas columnas que UK Gov)
    """
    try:
        # Leer Excel EPA
        df = pd.read_excel(file_path, sheet_name="eGRID")
        
        # Normalizar columnas
        normalized = pd.DataFrame({
            'Sheet': 'EPA_eGRID',
            'Level 1': df['Plant Primary Fuel'],
            'Level 2': df['Fuel Type'],
            'Level 3': None,
            'Unit': 'kWh',  # EPA usa kWh como estándar
            'GHG': 'CO2e',
            'kg CO2e': df['CO2e Emission Factor (lb/MWh)'] * 0.453592 / 1000,  # lb/MWh → kg/kWh
            'kg CO2': df['CO2 Emission Factor (lb/MWh)'] * 0.453592 / 1000,
            'kg CH4': df['CH4 Emission Factor (lb/MWh)'] * 0.453592 / 1000,
            'kg N2O': df['N2O Emission Factor (lb/MWh)'] * 0.453592 / 1000,
            'Year': year,
            'Geography': 'US',
            'Description': df['Plant Name'] + ' - ' + df['Fuel Type']
        })
        
        logger.info(f"Loaded {len(normalized)} EPA factors from {file_path}")
        return normalized
        
    except Exception as e:
        logger.error(f"Error loading EPA factors: {e}")
        raise
```

#### **Paso 2: Integrar en `find_factor()`**

```python
# utils/factors.py

def find_factor(
    factors_df: pd.DataFrame,
    category: str,
    unit: str,
    geography: Optional[str] = "UK",
    source_priority: List[str] = ["UK2025", "EPA2024", "IPCC2014"],  # ✅ Nuevo parámetro
    **kwargs
) -> Optional[Tuple[float, str, Dict[str, Any]]]:
    """
    Busca factor de emisión con prioridad de fuentes.
    
    Args:
        source_priority: Lista ordenada de fuentes preferidas
    """
    # Filtrar por geografía primero
    if geography == "US":
        # Priorizar EPA para USA
        source_priority = ["EPA2024", "UK2025", "IPCC2014"]
    
    # Buscar por prioridad
    for source in source_priority:
        filtered = factors_df[factors_df['Source'] == source]
        match = _search_in_dataframe(filtered, category, unit, **kwargs)
        if match is not None:
            return match  # Retornar primer match con prioridad
    
    # Fallback: buscar en todas las fuentes
    return _search_in_dataframe(factors_df, category, unit, **kwargs)
```

#### **Paso 3: Combinar Fuentes**

```python
# app/streamlit_app.py

# Cargar múltiples fuentes
uk_factors = load_uk_gov_factors("data/uk_2025.xlsx")
epa_factors = load_epa_factors("data/epa_2024.xlsx")

# Combinar en un solo DataFrame
all_factors = pd.concat([uk_factors, epa_factors], ignore_index=True)

# find_factor() ahora buscará en ambas fuentes
factor_result = find_factor(
    all_factors,
    category="purchased_electricity",
    unit="kWh",
    geography="US"  # Priorizará EPA
)
```

---

### **Caso 3: Agregar Nueva Visualización**

Supongamos que quieres agregar un **Mapa de Calor** de emisiones por mes y categoría.

#### **Paso 1: Crear Función de Generación**

```python
# app/streamlit_app.py

@st.cache_data(ttl=300)  # Cache por 5 minutos
def create_heatmap_chart(results: tuple) -> go.Figure:
    """
    Crea mapa de calor de emisiones por mes y categoría.
    
    Args:
        results: Tuple de EmissionResult
        
    Returns:
        Figura Plotly con heatmap
    """
    import plotly.graph_objects as go
    import pandas as pd
    
    # Extraer datos
    heatmap_data = []
    for r in results:
        month = getattr(r.activity_record, 'month', None)
        if month is None:
            continue  # Skip si no hay mes
        
        heatmap_data.append({
            'Mes': month,
            'Categoría': r.category_label,
            'Emisión (tCO2e)': r.emission_tCO2e
        })
    
    if not heatmap_data:
        return None
    
    df = pd.DataFrame(heatmap_data)
    
    # Pivot para matriz (mes × categoría)
    pivot = df.pivot_table(
        index='Categoría',
        columns='Mes',
        values='Emisión (tCO2e)',
        aggfunc='sum',
        fill_value=0
    )
    
    # Crear heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[f'Mes {m}' for m in pivot.columns],
        y=pivot.index,
        colorscale='Reds',
        hovertemplate='<b>%{y}</b><br>%{x}<br>%{z:.2f} tCO2e<extra></extra>'
    ))
    
    fig.update_layout(
        title='Mapa de Calor: Emisiones por Mes y Categoría',
        xaxis_title='Mes',
        yaxis_title='Categoría',
        height=500
    )
    
    return fig
```

#### **Paso 2: Integrar en UI**

```python
# app/streamlit_app.py

# En tab de Resultados
with tab4:
    # ... código existente ...
    
    # 🆕 NUEVA VISUALIZACIÓN
    st.markdown("---")
    st.subheader("🔥 Mapa de Calor Temporal")
    
    with st.expander("📊 Ver Heatmap", expanded=False):
        fig_heatmap = create_heatmap_chart(tuple(results))
        
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.info("💡 El mapa de calor muestra patrones estacionales de emisiones. Celdas más oscuras = mayores emisiones.")
        else:
            st.info("📊 Necesitas datos con columna 'month' para generar el heatmap.")
```

---

### **Caso 4: Agregar AI Features Personalizadas**

Supongamos que quieres agregar **predicción de emisiones futuras** con ML.

#### **Paso 1: Crear Módulo de ML**

```python
# utils/ml_predictor.py

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Tuple
import pandas as pd

class EmissionPredictor:
    """
    Predictor de emisiones basado en datos históricos.
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_fitted = False
    
    def fit(self, results: List[EmissionResult]):
        """
        Entrena modelo con datos históricos.
        
        Args:
            results: Lista de EmissionResult con atributo 'month'
        """
        # Extraer features (X) y target (y)
        X, y = [], []
        
        for r in results:
            month = getattr(r.activity_record, 'month', None)
            if month is None:
                continue
            
            year = getattr(r.activity_record, 'year', 2024)
            
            # Feature: timestamp numérico
            timestamp = year * 12 + month
            X.append([timestamp])
            
            # Target: emisión
            y.append(r.emission_tCO2e)
        
        if len(X) < 2:
            raise ValueError("Necesitas al menos 2 meses de datos históricos")
        
        # Entrenar
        self.model.fit(np.array(X), np.array(y))
        self.is_fitted = True
    
    def predict_next_months(self, n_months: int = 6) -> List[Tuple[str, float]]:
        """
        Predice emisiones para los próximos N meses.
        
        Args:
            n_months: Número de meses a predecir
            
        Returns:
            Lista de (periodo, emisión_predicha)
        """
        if not self.is_fitted:
            raise ValueError("Modelo no entrenado. Llama a fit() primero.")
        
        from datetime import datetime, timedelta
        
        predictions = []
        current_date = datetime.now()
        
        for i in range(1, n_months + 1):
            future_date = current_date + timedelta(days=30 * i)
            timestamp = future_date.year * 12 + future_date.month
            
            emission = self.model.predict([[timestamp]])[0]
            
            period = future_date.strftime("%Y-%m")
            predictions.append((period, max(0, emission)))  # No negativas
        
        return predictions
```

#### **Paso 2: Integrar en Streamlit**

```python
# app/streamlit_app.py

# En tab de Resultados
st.markdown("---")
st.subheader("🔮 Predicción de Emisiones Futuras (ML)")

with st.expander("🤖 Predicción con Machine Learning", expanded=False):
    try:
        from utils.ml_predictor import EmissionPredictor
        
        # Verificar que hay datos temporales
        has_months = any(
            getattr(r.activity_record, 'month', None) is not None
            for r in results
        )
        
        if not has_months:
            st.warning("⚠️ Necesitas datos con columna 'month' para predicciones.")
        else:
            # Entrenar modelo
            predictor = EmissionPredictor()
            predictor.fit(results)
            
            # Predecir próximos 6 meses
            predictions = predictor.predict_next_months(n_months=6)
            
            # Mostrar tabla
            pred_df = pd.DataFrame(predictions, columns=['Periodo', 'Emisión Predicha (tCO2e)'])
            st.dataframe(pred_df, use_container_width=True)
            
            # Gráfico de predicción
            import plotly.express as px
            fig_pred = px.line(
                pred_df,
                x='Periodo',
                y='Emisión Predicha (tCO2e)',
                markers=True,
                title='Predicción de Emisiones - Próximos 6 Meses'
            )
            st.plotly_chart(fig_pred, use_container_width=True)
            
            st.info("💡 Predicción basada en regresión lineal de datos históricos. Usar solo como referencia.")
    
    except Exception as e:
        st.error(f"Error en predicción ML: {e}")
```

---

## 🧪 Testing y QA

### **Estructura de Tests**

```
tests/
├── __init__.py
├── conftest.py           # Fixtures compartidos
├── test_basic.py         # Tests de modelos básicos
├── test_integration.py   # Tests de integración
├── test_ai_simplified.py # Tests de AI features
├── test_calculations.py  # Tests de cálculos (crear)
└── test_validators.py    # Tests de validación (crear)
```

### **Fixtures Recomendados**

```python
# tests/conftest.py

import pytest
import pandas as pd
from models.emissions import ActivityRecord, EmissionFactor

@pytest.fixture
def sample_factors():
    """Fixture con factores de emisión de ejemplo"""
    return pd.DataFrame({
        'Sheet': ['Fuels', 'Fuels', 'Electricity'],
        'Level 1': ['Diesel', 'Petrol', 'Grid'],
        'Unit': ['litres', 'litres', 'kWh'],
        'kg CO2e': [2.68442, 2.31279, 0.213],
        'Year': [2025, 2025, 2025],
        'Geography': ['UK', 'UK', 'UK']
    })

@pytest.fixture
def sample_activity():
    """Fixture con actividad de ejemplo"""
    return ActivityRecord(
        entity_id="Test_Entity",
        scope=1,
        category="mobile_combustion",
        activity_value=1000,
        activity_unit="litres",
        geography="UK",
        year=2025
    )

@pytest.fixture
def sample_factor():
    """Fixture con factor de emisión de ejemplo"""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68442,
        unit="litres",
        year=2025,
        geography="UK",
        scope=1,
        category="mobile_combustion"
    )
```

### **Tipos de Tests**

#### **1. Tests Unitarios**

```python
# tests/test_calculations.py

def test_compute_emission_basic(sample_activity, sample_factor):
    """Test cálculo básico de emisión"""
    from calculators.core import compute_emission
    
    result = compute_emission(sample_activity, sample_factor)
    
    assert result.emission_kgCO2e == pytest.approx(2684.42, rel=1e-2)
    assert result.emission_tCO2e == pytest.approx(2.68442, rel=1e-2)
    assert result.scope == 1

def test_compute_emission_unit_conversion(sample_activity, sample_factor):
    """Test conversión automática de unidades"""
    # Activity en kg, factor en litres
    activity_kg = ActivityRecord(
        entity_id="Test",
        scope=1,
        category="mobile_combustion",
        activity_value=850,  # kg de diesel
        activity_unit="kg",  # Diferente unidad
        geography="UK",
        year=2025
    )
    
    # Debe convertir kg → litres (densidad diesel ≈ 0.85 kg/L)
    result = compute_emission(activity_kg, sample_factor, auto_convert_units=True)
    
    assert result.emission_kgCO2e > 0  # Debe calcular algo
```

#### **2. Tests de Integración**

```python
# tests/test_integration.py

def test_full_calculation_pipeline(sample_factors):
    """Test pipeline completo: CSV → Cálculo → Resultados"""
    import tempfile
    from pathlib import Path
    
    # 1. Crear CSV temporal
    csv_content = """entity_id,scope,category,activity_value,activity_unit,geography,year
Company_A,1,mobile_combustion,1000,litres,UK,2025
Company_B,2,purchased_electricity,5000,kWh,UK,2025
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(csv_content)
        csv_path = f.name
    
    try:
        # 2. Cargar y validar
        df = pd.read_csv(csv_path)
        valid_activities, report = validate_activity_data(df)
        
        assert len(valid_activities) == 2
        assert report.success_rate == 100.0
        
        # 3. Calcular emisiones
        results = []
        for activity in valid_activities:
            factor_result = find_factor(
                sample_factors,
                activity.category,
                activity.activity_unit
            )
            
            if factor_result:
                value, source, metadata = factor_result
                ef = EmissionFactor(
                    source=source,
                    gas="CO2e",
                    value=value,
                    unit=metadata['unit'],
                    year=2025,
                    scope=activity.scope,
                    category=activity.category
                )
                result = compute_emission(activity, ef)
                results.append(result)
        
        # 4. Verificar resultados
        assert len(results) == 2
        
        totals = get_total_emissions(results)
        assert totals['total_tonnes_co2e'] > 0
        assert len(totals['by_scope']) > 0
        
    finally:
        # Limpiar archivo temporal
        Path(csv_path).unlink()
```

#### **3. Tests de Regresión**

```python
# tests/test_regression.py

def test_known_emissions_calculation():
    """
    Test de regresión: Valores conocidos no deben cambiar.
    
    Caso: 1000 litres diesel → 2684.42 kg CO2e (UK 2025)
    """
    activity = ActivityRecord(
        entity_id="Regression_Test",
        scope=1,
        category="mobile_combustion",
        activity_value=1000,
        activity_unit="litres"
    )
    
    factor = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68442,  # Valor conocido de UK Gov 2025
        unit="litres",
        year=2025,
        scope=1,
        category="mobile_combustion"
    )
    
    result = compute_emission(activity, factor)
    
    # ✅ VALOR ESPERADO (no debe cambiar entre versiones)
    EXPECTED_KG = 2684.42
    EXPECTED_TONNES = 2.68442
    
    assert result.emission_kgCO2e == pytest.approx(EXPECTED_KG, abs=0.01)
    assert result.emission_tCO2e == pytest.approx(EXPECTED_TONNES, abs=0.00001)
```

### **Coverage Target**

```bash
# Ejecutar tests con coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Target mínimo
# - models/: 90%+
# - calculators/: 80%+
# - utils/: 70%+
# - app/: 30%+ (UI es difícil de testear)
```

---

## 🚀 Deployment

### **Opciones de Deployment**

| Plataforma | Complejidad | Costo | Recomendado Para |
|------------|-------------|-------|------------------|
| **Streamlit Cloud** | ⭐ Baja | Gratis | Prototipos, demos |
| **Docker + AWS ECS** | ⭐⭐⭐ Alta | $20-50/mes | Producción corporativa |
| **Render.com** | ⭐⭐ Media | $7-25/mes | Startups, equipos pequeños |
| **Railway** | ⭐ Baja | $5-20/mes | Side projects |
| **Azure Container Instances** | ⭐⭐ Media | Pay-per-use | Empresas con Azure |

### **Deployment con Docker**

Ya tienes `Dockerfile` y `docker-compose.yml` configurados. Ver [DOCKER_TESTING_GUIDE.md](DOCKER_TESTING_GUIDE.md).

```bash
# Build
docker build -t carbon-ghg:1.0 .

# Run
docker-compose up -d

# Verify
curl http://localhost:8501
```

### **Deployment en Streamlit Cloud**

1. **Push a GitHub**
   ```bash
   git push origin main
   ```

2. **Ir a** [share.streamlit.io](https://share.streamlit.io)

3. **Conectar repositorio** y seleccionar:
   - Main file: `app/streamlit_app.py`
   - Python version: 3.12
   - Requirements: `requirements.txt`

4. **Deploy!** (toma ~3-5 minutos)

5. **URL pública**: `https://tu-app.streamlit.app`

### **CI/CD con GitHub Actions**

```yaml
# .github/workflows/ci.yml

name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install linters
      run: |
        pip install black flake8 mypy
    
    - name: Run Black
      run: black --check .
    
    - name: Run Flake8
      run: flake8 . --max-line-length=100
    
    - name: Run MyPy
      run: mypy . --ignore-missing-imports

  docker:
    runs-on: ubuntu-latest
    needs: [test, lint]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t carbon-ghg:latest .
    
    - name: Test Docker image
      run: |
        docker run -d -p 8501:8501 carbon-ghg:latest
        sleep 10
        curl -f http://localhost:8501 || exit 1
```

---

## 💡 Best Practices

### **1. Code Style**

```python
# ✅ BUENO: Type hints claros
def compute_emission(
    activity: ActivityRecord,
    emission_factor: EmissionFactor,
    auto_convert_units: bool = True
) -> EmissionResult:
    """
    Calcula emisión de CO2e para una actividad.
    
    Args:
        activity: Registro de actividad
        emission_factor: Factor de emisión aplicable
        auto_convert_units: Convertir unidades automáticamente
        
    Returns:
        Resultado del cálculo con emisiones
        
    Raises:
        UnitConversionError: Si unidades incompatibles y auto_convert=False
    """
    # Implementación...

# ❌ MALO: Sin types, sin docstring
def calc(a, f, c=True):
    # Implementación...
```

### **2. Error Handling**

```python
# ✅ BUENO: Excepciones específicas con contexto
try:
    factor_result = find_factor(factors_df, category, unit)
except FactorNotFoundError as e:
    logger.error(f"Factor not found for {category}/{unit}: {e}")
    raise ValueError(
        f"No emission factor found for category '{category}' with unit '{unit}'. "
        f"Available units: {get_available_units(factors_df, category)}"
    ) from e

# ❌ MALO: Catch genérico sin contexto
try:
    factor_result = find_factor(factors_df, category, unit)
except:
    pass  # Silencia error
```

### **3. Logging**

```python
# ✅ BUENO: Logging con niveles apropiados
logger.info(f"Loading {len(factors_df)} emission factors from {source}")
logger.debug(f"Searching for factor: category={category}, unit={unit}")
logger.warning(f"Factor not found for {category}, using fallback")
logger.error(f"Invalid activity value: {value}")

# ❌ MALO: Solo prints
print("Loading factors...")  # No controlable, no configurable
```

### **4. Performance**

```python
# ✅ BUENO: Usar generators para listas grandes
def process_activities_generator(activities):
    for activity in activities:
        result = compute_emission(activity, factor)
        yield result  # Lazy evaluation

# Uso
for result in process_activities_generator(large_list):
    save_to_db(result)  # Procesa de a uno, no carga todo en RAM

# ❌ MALO: Cargar todo en memoria
def process_activities(activities):
    return [compute_emission(a, f) for a in activities]  # 100k items → RAM explota

results = process_activities(large_list)  # OOM
```

### **5. Testing**

```python
# ✅ BUENO: Test con AAA pattern (Arrange, Act, Assert)
def test_emission_calculation():
    # Arrange
    activity = ActivityRecord(...)
    factor = EmissionFactor(...)
    expected_emission = 2684.42
    
    # Act
    result = compute_emission(activity, factor)
    
    # Assert
    assert result.emission_kgCO2e == pytest.approx(expected_emission)

# ❌ MALO: Test sin estructura clara
def test_something():
    a = ActivityRecord(...)
    assert compute_emission(a, EmissionFactor(...)).emission_kgCO2e > 0  # ¿Qué está testando?
```

---

## 🔧 Troubleshooting

### **Problema 1: ImportError**

```python
# Error
ImportError: cannot import name 'ActivityRecord' from 'models.emissions'

# Solución
# 1. Verificar que __init__.py existe
# models/__init__.py

from .emissions import (
    ActivityRecord,
    EmissionFactor,
    EmissionResult,
    SCOPE_1_CATEGORIES,
    SCOPE_2_CATEGORIES,
    SCOPE_3_CATEGORIES
)

__all__ = [
    'ActivityRecord',
    'EmissionFactor',
    'EmissionResult',
    'SCOPE_1_CATEGORIES',
    'SCOPE_2_CATEGORIES',
    'SCOPE_3_CATEGORIES'
]

# 2. Usar import absoluto
from models.emissions import ActivityRecord  # ✅
from models import ActivityRecord  # ✅ (si está en __init__.py)
from .emissions import ActivityRecord  # ❌ (solo en mismo paquete)
```

### **Problema 2: Tests fallan con "fixture not found"**

```python
# Error
pytest tests/test_calculations.py
E   fixture 'sample_factors' not found

# Solución: Verificar que conftest.py está en lugar correcto
tests/
├── conftest.py  # ✅ AQUÍ (raíz de tests/)
├── test_calculations.py
└── subfolder/
    ├── conftest.py  # También válido para subfolder
    └── test_other.py
```

### **Problema 3: Streamlit no recarga cambios**

```bash
# Problema: Cambios en código no se reflejan

# Solución 1: Rerun manual
# En browser: Presiona "R" o click en "Rerun"

# Solución 2: Configurar auto-reload
# .streamlit/config.toml
[server]
runOnSave = true

# Solución 3: Limpiar cache
import streamlit as st
st.cache_data.clear()  # En código
# O presiona "C" en browser
```

### **Problema 4: Docker healthcheck unhealthy**

```bash
# Error
docker ps
# carbon-ghg-streamlit   Up 2 minutes (unhealthy)

# Causa: curl no está en python:3.12-slim

# Solución 1: Instalar curl en Dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Solución 2: Usar Python para healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# Solución 3: Ignorar (app funciona igual, healthcheck es cosmético)
```

---

## 🤝 Contribuir al Proyecto

### **1. Fork y Clone**

```bash
# Fork en GitHub (botón "Fork")
# Luego:
git clone https://github.com/TU_USERNAME/carbon-ghg-calculator.git
cd carbon-ghg-calculator
git remote add upstream https://github.com/ORIGINAL_REPO/carbon-ghg-calculator.git
```

### **2. Crear Branch**

```bash
# Nombrar según convención
git checkout -b feature/agregar-prediccion-ml
git checkout -b fix/corregir-validacion-scopes
git checkout -b docs/actualizar-api-reference
```

### **3. Hacer Cambios**

- ✅ Código con type hints
- ✅ Docstrings en funciones públicas
- ✅ Tests para nueva funcionalidad
- ✅ Actualizar documentación si es necesario

### **4. Commit con Conventional Commits**

```bash
git commit -m "feat: agregar predicción de emisiones con ML"
git commit -m "fix: corregir validación de scopes 1-3"
git commit -m "docs: actualizar API reference con nuevas funciones"
git commit -m "test: agregar tests para ml_predictor"
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `test`: Agregar o modificar tests
- `refactor`: Refactorización sin cambiar funcionalidad
- `perf`: Mejoras de rendimiento
- `chore`: Mantenimiento (deps, config, etc.)

### **5. Push y Pull Request**

```bash
git push origin feature/agregar-prediccion-ml

# Ir a GitHub y crear Pull Request
# Template de PR:

## Descripción
Agrega funcionalidad de predicción de emisiones futuras usando regresión lineal.

## Cambios
- ✅ Nuevo módulo `utils/ml_predictor.py`
- ✅ Integración en `app/streamlit_app.py`
- ✅ Tests en `tests/test_ml_predictor.py`
- ✅ Documentación actualizada en `docs/DEVELOPER_GUIDE.md`

## Testing
- [x] Tests pasan localmente
- [x] Coverage > 80% en nuevo código
- [x] Probado manualmente en UI

## Screenshots
(Si aplica)
```

### **6. Code Review**

Esperar feedback de mantenedores. Hacer cambios solicitados:

```bash
# Hacer cambios
git add .
git commit -m "refactor: aplicar feedback de code review"
git push origin feature/agregar-prediccion-ml

# PR se actualiza automáticamente
```

### **7. Merge**

Una vez aprobado, los mantenedores harán merge a `main`.

---

## 📞 Soporte

### **Canales de Comunicación**

- **Issues**: [GitHub Issues](https://github.com/tu-org/carbon-ghg/issues) para bugs y feature requests
- **Discussions**: [GitHub Discussions](https://github.com/tu-org/carbon-ghg/discussions) para preguntas generales
- **Email**: dev@carbon-ghg-calculator.com

### **Recursos Adicionales**

- [USER_GUIDE.md](USER_GUIDE.md) - Guía de usuario
- [API_REFERENCE.md](API_REFERENCE.md) - Referencia de API
- [DOCKER_TESTING_GUIDE.md](DOCKER_TESTING_GUIDE.md) - Guía de Docker

---

**¡Gracias por contribuir al Carbon GHG Calculator!** 🌱

**Versión**: 1.0  
**Última actualización**: 8 de octubre de 2025  
**Mantenedores**: Carbon GHG Calculator Team  
**Licencia**: MIT
