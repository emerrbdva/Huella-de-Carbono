# 📚 API Reference - Carbon GHG Calculator

**Versión**: 1.0  
**Fecha**: 8 de octubre de 2025  
**Licencia**: MIT  
**Autor**: Carbon GHG Calculator Team

---

## 📑 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Módulo: calculators](#módulo-calculators)
3. [Módulo: models](#módulo-models)
4. [Módulo: utils](#módulo-utils)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Tipos de Datos](#tipos-de-datos)
7. [Manejo de Errores](#manejo-de-errores)

---

## 📖 Introducción

Esta documentación describe la API pública del **Carbon GHG Calculator**, un sistema profesional para cálculo de emisiones de gases de efecto invernadero (GEI) alineado con el **GHG Protocol**.

### **Arquitectura General**

```
┌─────────────────────────────────────────────────────────────┐
│                       STREAMLIT APP                         │
│                    (app/streamlit_app.py)                   │
└────────────────────────┬───────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ CALCULATORS  │  │    MODELS    │  │    UTILS     │
│   (core.py)  │  │ (emissions)  │  │ (factors,    │
│              │  │              │  │  validator)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### **Flujo de Datos**

```
1. ENTRADA (CSV/Excel)
   │
   ├─> utils.data_validator.validate_activity_data()
   │
   ├─> models.emissions.ActivityRecord (parse)
   │
   ├─> utils.factors.load_uk_gov_factors() (factores)
   │
   ├─> utils.factors.find_factor() (búsqueda)
   │
   ├─> calculators.core.compute_emission() (cálculo)
   │
   ├─> models.emissions.EmissionResult (resultado)
   │
   └─> utils.report_generator.generate_excel_report() (export)
```

---

## 🔢 Módulo: calculators

### `calculators.core`

Funciones principales para cálculo de emisiones GEI.

---

#### `compute_emission()`

Calcula la emisión de CO₂e para una actividad específica.

```python
def compute_emission(
    activity: ActivityRecord,
    emission_factor: EmissionFactor,
    auto_convert_units: bool = True
) -> EmissionResult
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `activity` | `ActivityRecord` | ✅ Sí | - | Registro de actividad con datos de consumo |
| `emission_factor` | `EmissionFactor` | ✅ Sí | - | Factor de emisión aplicable |
| `auto_convert_units` | `bool` | ❌ No | `True` | Convertir automáticamente unidades si no coinciden |

##### **Retorna**

`EmissionResult` - Objeto con resultado del cálculo y metadata.

##### **Fórmula Aplicada**

```
E (kg CO₂e) = AD × EF
```

Donde:
- **E**: Emisión en kg CO₂e
- **AD**: Activity Data (valor de actividad)
- **EF**: Emission Factor (factor de emisión)

##### **Ejemplo Básico**

```python
from models.emissions import ActivityRecord, EmissionFactor
from calculators.core import compute_emission

# 1. Crear actividad
activity = ActivityRecord(
    entity_id="Empresa_XYZ",
    scope=1,
    category="mobile_combustion",
    activity_value=1000,  # litros
    activity_unit="litres",
    geography="UK",
    year=2025
)

# 2. Crear factor de emisión
factor = EmissionFactor(
    source="UK2025",
    gas="CO2e",
    value=2.68442,  # kg CO2e / litre
    unit="litres",
    year=2025,
    geography="UK",
    scope=1,
    category="mobile_combustion"
)

# 3. Calcular emisión
result = compute_emission(activity, factor)

# 4. Acceder a resultados
print(f"Emisión: {result.emission_kgCO2e:.2f} kg CO2e")
print(f"Emisión: {result.emission_tCO2e:.4f} ton CO2e")
# Output:
# Emisión: 2684.42 kg CO2e
# Emisión: 2.6844 ton CO2e
```

##### **Conversión Automática de Unidades**

Si `auto_convert_units=True`, la función intenta convertir unidades incompatibles:

```python
from utils.unit_converter import convert_unit

# Actividad en kg
activity = ActivityRecord(..., activity_value=500, activity_unit="kg")

# Factor en tonnes
factor = EmissionFactor(..., value=3.5, unit="tonnes")

# Conversión automática: 500 kg → 0.5 tonnes
result = compute_emission(activity, factor, auto_convert_units=True)
# E = 0.5 tonnes × 3.5 = 1.75 kg CO2e
```

Unidades soportadas:
- **Masa**: kg, tonnes, lbs, g
- **Volumen**: litres, m³, gallons
- **Energía**: kWh, MWh, GWh, GJ
- **Distancia**: km, miles, passenger.km, tonne.km

##### **Excepciones**

| Excepción | Cuándo ocurre | Solución |
|-----------|---------------|----------|
| `UnitConversionError` | Unidades incompatibles y `auto_convert_units=False` | Verificar unidades o activar auto_convert |
| `ValueError` | `activity_value` es negativo o cero | Usar valores > 0 |
| `TypeError` | Parámetros incorrectos | Verificar tipos de datos |

---

#### `aggregate_emissions_by_scope()`

Agrupa y suma emisiones por alcance (Scope 1, 2, 3).

```python
def aggregate_emissions_by_scope(
    results: List[EmissionResult]
) -> Dict[int, float]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `results` | `List[EmissionResult]` | ✅ Sí | Lista de resultados de emisiones |

##### **Retorna**

`Dict[int, float]` - Diccionario con suma por scope:

```python
{
    1: 45.67,  # Scope 1 en tCO2e
    2: 12.34,  # Scope 2 en tCO2e
    3: 89.01   # Scope 3 en tCO2e
}
```

##### **Ejemplo**

```python
from calculators.core import compute_emission, aggregate_emissions_by_scope

# Lista de resultados
results = [
    compute_emission(activity1, factor1),  # Scope 1
    compute_emission(activity2, factor2),  # Scope 1
    compute_emission(activity3, factor3),  # Scope 2
    compute_emission(activity4, factor4),  # Scope 3
]

# Agregar por scope
by_scope = aggregate_emissions_by_scope(results)

print(by_scope)
# Output:
# {1: 123.45, 2: 67.89, 3: 234.56}

# Total por scope
for scope, tonnes in by_scope.items():
    print(f"Scope {scope}: {tonnes:.2f} tCO2e")
# Output:
# Scope 1: 123.45 tCO2e
# Scope 2: 67.89 tCO2e
# Scope 3: 234.56 tCO2e
```

---

#### `aggregate_emissions_by_category()`

Agrupa y suma emisiones por categoría GHG Protocol.

```python
def aggregate_emissions_by_category(
    results: List[EmissionResult]
) -> Dict[str, float]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `results` | `List[EmissionResult]` | ✅ Sí | Lista de resultados de emisiones |

##### **Retorna**

`Dict[str, float]` - Diccionario con suma por categoría:

```python
{
    "mobile_combustion": 45.67,
    "stationary_combustion": 23.45,
    "purchased_electricity": 67.89,
    "business_travel": 12.34,
    ...
}
```

##### **Ejemplo**

```python
from calculators.core import aggregate_emissions_by_category

# Agregar por categoría
by_category = aggregate_emissions_by_category(results)

# Top 3 categorías
sorted_categories = sorted(
    by_category.items(),
    key=lambda x: x[1],
    reverse=True
)[:3]

print("Top 3 categorías:")
for category, tonnes in sorted_categories:
    print(f"  {category}: {tonnes:.2f} tCO2e")
# Output:
# Top 3 categorías:
#   purchased_electricity: 234.56 tCO2e
#   mobile_combustion: 123.45 tCO2e
#   business_travel: 89.01 tCO2e
```

---

#### `get_total_emissions()`

Calcula el total de emisiones y estadísticas agregadas.

```python
def get_total_emissions(
    results: List[EmissionResult]
) -> Dict[str, Any]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `results` | `List[EmissionResult]` | ✅ Sí | Lista de resultados de emisiones |

##### **Retorna**

`Dict[str, Any]` - Diccionario con estadísticas:

```python
{
    "total_tonnes_co2e": 425.90,     # Total en toneladas
    "total_kg_co2e": 425900.0,       # Total en kilogramos
    "count_activities": 24,          # Número de actividades
    "by_scope": {1: 123.45, 2: 67.89, 3: 234.56},  # Por scope
    "by_category": {"mobile_combustion": 45.67, ...}  # Por categoría
}
```

##### **Ejemplo**

```python
from calculators.core import get_total_emissions

# Obtener estadísticas completas
stats = get_total_emissions(results)

print(f"🌍 Huella de Carbono Total: {stats['total_tonnes_co2e']:.2f} tCO2e")
print(f"📊 Actividades calculadas: {stats['count_activities']}")
print(f"📈 Por Scope:")
for scope, tonnes in stats['by_scope'].items():
    pct = (tonnes / stats['total_tonnes_co2e']) * 100
    print(f"   Scope {scope}: {tonnes:.2f} tCO2e ({pct:.1f}%)")
# Output:
# 🌍 Huella de Carbono Total: 425.90 tCO2e
# 📊 Actividades calculadas: 24
# 📈 Por Scope:
#    Scope 1: 123.45 tCO2e (29.0%)
#    Scope 2: 67.89 tCO2e (15.9%)
#    Scope 3: 234.56 tCO2e (55.1%)
```

---

## 📦 Módulo: models

### `models.emissions`

Modelos de datos principales del sistema.

---

#### `ActivityRecord`

Representa una actividad con consumo de recursos.

```python
@dataclass
class ActivityRecord:
    entity_id: str
    scope: int
    category: str
    activity_value: float
    activity_unit: str
    geography: Optional[str] = "UK"
    year: Optional[int] = 2025
    month: Optional[int] = None
    ghg_factor: Optional[float] = None
    fuel_type: Optional[str] = None
    vehicle_type: Optional[str] = None
```

##### **Atributos**

| Atributo | Tipo | Requerido | Default | Descripción |
|----------|------|-----------|---------|-------------|
| `entity_id` | `str` | ✅ Sí | - | Identificador único de la entidad (empresa, departamento, etc.) |
| `scope` | `int` | ✅ Sí | - | Alcance GHG Protocol: 1, 2 o 3 |
| `category` | `str` | ✅ Sí | - | Categoría de emisión (ej: `mobile_combustion`) |
| `activity_value` | `float` | ✅ Sí | - | Valor numérico del consumo (ej: 1000 litros) |
| `activity_unit` | `str` | ✅ Sí | - | Unidad de medida (ej: `litres`, `kWh`, `km`) |
| `geography` | `str` | ❌ No | `"UK"` | Código de país (UK, US, ES, etc.) |
| `year` | `int` | ❌ No | `2025` | Año fiscal de la actividad |
| `month` | `int` | ❌ No | `None` | Mes (1-12) para análisis temporal |
| `ghg_factor` | `float` | ❌ No | `None` | Factor personalizado (sobrescribe búsqueda) |
| `fuel_type` | `str` | ❌ No | `None` | Tipo de combustible (Diesel, Petrol, etc.) |
| `vehicle_type` | `str` | ❌ No | `None` | Tipo de vehículo (Car, Van, HGV, etc.) |

##### **Métodos**

```python
def to_dict() -> Dict[str, Any]
```
Convierte el registro a diccionario.

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'ActivityRecord'
```
Crea un `ActivityRecord` desde un diccionario.

```python
@classmethod
def from_csv_row(cls, row: pd.Series) -> 'ActivityRecord'
```
Crea un `ActivityRecord` desde una fila de pandas DataFrame.

##### **Ejemplo**

```python
from models.emissions import ActivityRecord

# Crear desde constructor
activity = ActivityRecord(
    entity_id="Oficina_Central",
    scope=2,
    category="purchased_electricity",
    activity_value=5000,
    activity_unit="kWh",
    geography="UK",
    year=2025,
    month=6
)

# Crear desde diccionario
data = {
    "entity_id": "Flota_Vehiculos",
    "scope": 1,
    "category": "mobile_combustion",
    "activity_value": 2000,
    "activity_unit": "litres",
    "fuel_type": "Diesel"
}
activity2 = ActivityRecord.from_dict(data)

# Convertir a diccionario
print(activity.to_dict())
# Output:
# {
#     "entity_id": "Oficina_Central",
#     "scope": 2,
#     "category": "purchased_electricity",
#     "activity_value": 5000.0,
#     "activity_unit": "kWh",
#     ...
# }
```

##### **Categorías Válidas**

**Scope 1** (8 categorías):
- `mobile_combustion`
- `stationary_combustion`
- `process_emissions`
- `fugitive_emissions`
- `refrigerants`
- `agricultural_emissions`
- `land_use_change`
- `other_scope1`

**Scope 2** (2 categorías):
- `purchased_electricity`
- `purchased_heat_steam`

**Scope 3** (15 categorías):
- `purchased_goods`
- `capital_goods`
- `upstream_energy`
- `upstream_transport`
- `waste_generated`
- `business_travel`
- `employee_commuting`
- `leased_assets_upstream`
- `downstream_transport`
- `product_processing`
- `product_use`
- `end_of_life`
- `leased_assets_downstream`
- `franchises`
- `other_scope3`

---

#### `EmissionFactor`

Representa un factor de emisión de base de datos.

```python
@dataclass
class EmissionFactor:
    source: str
    gas: str
    value: float
    unit: str
    year: int
    geography: Optional[str] = None
    scope: Optional[int] = None
    category: Optional[str] = None
    notes: Optional[str] = None
```

##### **Atributos**

| Atributo | Tipo | Requerido | Default | Descripción |
|----------|------|-----------|---------|-------------|
| `source` | `str` | ✅ Sí | - | Fuente del factor (UK2025, IPCC2006, EPA2024) |
| `gas` | `str` | ✅ Sí | - | Gas o mezcla (CO2, CH4, N2O, CO2e) |
| `value` | `float` | ✅ Sí | - | Valor numérico del factor |
| `unit` | `str` | ✅ Sí | - | Unidad del factor (kg CO2e / litres, etc.) |
| `year` | `int` | ✅ Sí | - | Año de publicación del factor |
| `geography` | `str` | ❌ No | `None` | Región geográfica aplicable |
| `scope` | `int` | ❌ No | `None` | Scope GHG Protocol (1, 2, 3) |
| `category` | `str` | ❌ No | `None` | Categoría GHG Protocol |
| `notes` | `str` | ❌ No | `None` | Notas adicionales o descripción |

##### **Ejemplo**

```python
from models.emissions import EmissionFactor

# Factor de electricidad UK 2025
factor_electricity = EmissionFactor(
    source="UK2025",
    gas="CO2e",
    value=0.213,  # kg CO2e / kWh
    unit="kWh",
    year=2025,
    geography="UK",
    scope=2,
    category="purchased_electricity",
    notes="UK grid electricity, 2025 average"
)

# Factor de diesel
factor_diesel = EmissionFactor(
    source="UK2025",
    gas="CO2e",
    value=2.68442,  # kg CO2e / litre
    unit="litres",
    year=2025,
    geography="UK",
    scope=1,
    category="mobile_combustion",
    notes="Diesel (average biofuel blend)"
)
```

---

#### `EmissionResult`

Resultado del cálculo de emisión para una actividad.

```python
@dataclass
class EmissionResult:
    activity_record: ActivityRecord
    emission_factor: EmissionFactor
    emission_kgCO2e: float
    emission_tCO2e: float
    calculation_timestamp: datetime
    category_label: str
    scope_label: str
```

##### **Atributos**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `activity_record` | `ActivityRecord` | Actividad original |
| `emission_factor` | `EmissionFactor` | Factor aplicado |
| `emission_kgCO2e` | `float` | Emisión en kg CO₂e |
| `emission_tCO2e` | `float` | Emisión en toneladas CO₂e |
| `calculation_timestamp` | `datetime` | Timestamp del cálculo |
| `category_label` | `str` | Etiqueta legible de la categoría |
| `scope_label` | `str` | Etiqueta legible del scope |

##### **Propiedades Calculadas**

```python
@property
def tonnes_per_unit(self) -> float
    """Intensidad de emisión (tCO2e / unidad de actividad)"""
    
@property
def kg_co2(self) -> float
    """Componente CO2 (si está disponible en el factor)"""
    
@property
def kg_ch4(self) -> float
    """Componente CH4 (si está disponible en el factor)"""
    
@property
def kg_n2o(self) -> float
    """Componente N2O (si está disponible en el factor)"""
```

##### **Métodos**

```python
def to_dict() -> Dict[str, Any]
    """Convierte resultado a diccionario"""
    
def to_dataframe() -> pd.DataFrame
    """Convierte resultado a DataFrame de 1 fila"""
```

##### **Ejemplo**

```python
from calculators.core import compute_emission

# Calcular emisión
result = compute_emission(activity, factor)

# Acceder a atributos
print(f"Emisión: {result.emission_tCO2e:.4f} tCO2e")
print(f"Categoría: {result.category_label}")
print(f"Scope: {result.scope_label}")
print(f"Timestamp: {result.calculation_timestamp}")

# Intensidad de emisión
intensity = result.tonnes_per_unit
print(f"Intensidad: {intensity:.6f} tCO2e/unidad")

# Exportar a dict
result_dict = result.to_dict()

# Exportar a DataFrame
df = result.to_dataframe()
print(df.columns)
# Output:
# ['entity_id', 'scope', 'category', 'activity_value', 
#  'activity_unit', 'emission_kgCO2e', 'emission_tCO2e', ...]
```

---

## 🛠️ Módulo: utils

### `utils.factors`

Funciones para carga y búsqueda de factores de emisión.

---

#### `load_uk_gov_factors()`

Carga factores de emisión del UK Government GHG Conversion Factors.

```python
def load_uk_gov_factors(
    file_path: str,
    year: int = 2025
) -> pd.DataFrame
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `file_path` | `str` | ✅ Sí | - | Ruta al archivo Excel de factores UK Gov |
| `year` | `int` | ❌ No | `2025` | Año de los factores (2024, 2025, etc.) |

##### **Retorna**

`pd.DataFrame` - DataFrame con factores normalizados.

**Columnas del DataFrame**:
- `Sheet`: Nombre de la hoja de origen
- `Level 1`, `Level 2`, `Level 3`: Jerarquía de categorías
- `Unit`: Unidad del factor
- `GHG`: Gas de efecto invernadero
- `kg CO2e`: Valor del factor en kg CO2e
- `kg CO2`, `kg CH4`, `kg N2O`: Componentes individuales (si aplica)
- `Description`: Descripción completa del factor

##### **Ejemplo**

```python
from utils.factors import load_uk_gov_factors

# Cargar factores UK Gov 2025
factors_df = load_uk_gov_factors(
    file_path="data/ghg-conversion-factors-2025-condensed-set.xlsx",
    year=2025
)

print(f"Total de factores cargados: {len(factors_df)}")
# Output: Total de factores cargados: 521

# Ver muestra
print(factors_df[['Sheet', 'Level 1', 'Unit', 'kg CO2e']].head(10))
# Output:
#          Sheet              Level 1     Unit  kg CO2e
# 0        Fuels  Diesel (average...)  litres  2.68442
# 1        Fuels  Petrol (average...)  litres  2.31279
# 2        Fuels  Natural gas (100%)      kWh  0.18316
# ...
```

##### **Fuentes Soportadas**

| Fuente | Año | Factores | Geográfico |
|--------|-----|----------|-----------|
| **UK Government** | 2025 | 521 | UK |
| UK Government | 2024 | 498 | UK |
| IPCC AR5 | 2014 | 245 | Global |
| EPA eGRID | 2024 | 183 | US |

##### **Hojas Procesadas** (UK Gov 2025)

- Fuels
- Bioenergy
- Refrigerant & other
- Passenger vehicles
- UK electricity
- Transmission and distribution
- Water supply
- Water treatment
- Material use
- Waste disposal
- Business travel - air
- Business travel - sea
- Business travel - land
- Freighting goods
- Hotel stay

##### **Caché**

⚡ Función cacheada con `@functools.lru_cache(maxsize=1)`:
- Primera llamada: ~2.5 segundos
- Llamadas subsecuentes: <0.01 segundos (cache hit)

---

#### `find_factor()`

Busca el factor de emisión más apropiado para una actividad.

```python
def find_factor(
    factors_df: pd.DataFrame,
    category: str,
    unit: str,
    geography: Optional[str] = "UK",
    scope: Optional[int] = None,
    fuel_type: Optional[str] = None,
    vehicle_type: Optional[str] = None,
    fallback_global: bool = True
) -> Optional[Tuple[float, str, Dict[str, Any]]]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `factors_df` | `pd.DataFrame` | ✅ Sí | - | DataFrame de factores (de `load_uk_gov_factors`) |
| `category` | `str` | ✅ Sí | - | Categoría GHG Protocol |
| `unit` | `str` | ✅ Sí | - | Unidad de la actividad |
| `geography` | `str` | ❌ No | `"UK"` | Código de país |
| `scope` | `int` | ❌ No | `None` | Scope (1, 2, 3) para filtro adicional |
| `fuel_type` | `str` | ❌ No | `None` | Tipo de combustible (Diesel, Petrol, etc.) |
| `vehicle_type` | `str` | ❌ No | `None` | Tipo de vehículo (Car, Van, etc.) |
| `fallback_global` | `bool` | ❌ No | `True` | Si no se encuentra factor regional, usar global |

##### **Retorna**

`Optional[Tuple[float, str, Dict[str, Any]]]` o `None` si no se encuentra.

**Tupla retornada**:
```python
(
    2.68442,  # float: valor del factor (kg CO2e)
    "UK2025",  # str: fuente del factor
    {  # dict: metadata
        "unit": "litres",
        "year": 2025,
        "geography": "UK",
        "full_description": "Diesel (average biofuel blend)",
        "sheet": "Fuels",
        "level_1": "Diesel",
        "level_2": "average biofuel blend",
        "level_3": None
    }
)
```

##### **Ejemplo Básico**

```python
from utils.factors import load_uk_gov_factors, find_factor

# Cargar factores
factors_df = load_uk_gov_factors("data/ghg-factors-2025.xlsx")

# Buscar factor para diesel
result = find_factor(
    factors_df,
    category="mobile_combustion",
    unit="litres",
    geography="UK",
    fuel_type="Diesel"
)

if result:
    value, source, metadata = result
    print(f"Factor encontrado: {value} kg CO2e / {metadata['unit']}")
    print(f"Fuente: {source}")
    print(f"Descripción: {metadata['full_description']}")
# Output:
# Factor encontrado: 2.68442 kg CO2e / litres
# Fuente: UK2025
# Descripción: Diesel (average biofuel blend)
else:
    print("No se encontró factor para esta actividad")
```

##### **Ejemplo con Fallback**

```python
# Buscar factor para España (no disponible en UK Gov)
result = find_factor(
    factors_df,
    category="purchased_electricity",
    unit="kWh",
    geography="ES",  # España
    fallback_global=True  # Usar factor global si no hay regional
)

if result:
    value, source, metadata = result
    print(f"Usando factor global: {value} kg CO2e / kWh")
    print(f"Geografía original solicitada: ES")
    print(f"Geografía del factor: {metadata['geography']}")  # "Global" o "UK"
```

##### **Lógica de Búsqueda**

1. **Búsqueda exacta**: categoría + unit + geography + fuel_type + vehicle_type
2. **Búsqueda sin vehículo**: categoría + unit + geography + fuel_type
3. **Búsqueda sin combustible**: categoría + unit + geography
4. **Búsqueda global** (si `fallback_global=True`): categoría + unit + geography="Global"
5. **Búsqueda genérica**: solo categoría + unit

##### **Casos de Uso Común**

**1. Combustión móvil (vehículos)**
```python
find_factor(
    factors_df,
    category="mobile_combustion",
    unit="km",
    geography="UK",
    fuel_type="Diesel",
    vehicle_type="Car"
)
```

**2. Electricidad**
```python
find_factor(
    factors_df,
    category="purchased_electricity",
    unit="kWh",
    geography="UK",
    scope=2
)
```

**3. Vuelos de negocios**
```python
find_factor(
    factors_df,
    category="business_travel",
    unit="passenger.km",
    geography="UK",
    vehicle_type="Domestic flight"
)
```

---

### `utils.data_validator`

Funciones para validación de datos de actividad.

---

#### `validate_activity_data()`

Valida un DataFrame de actividades contra reglas GHG Protocol.

```python
def validate_activity_data(
    df: pd.DataFrame,
    strict: bool = False
) -> Tuple[List[ActivityRecord], ValidationReport]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `df` | `pd.DataFrame` | ✅ Sí | - | DataFrame con datos de actividad |
| `strict` | `bool` | ❌ No | `False` | Modo estricto (falla si hay advertencias) |

##### **Retorna**

`Tuple[List[ActivityRecord], ValidationReport]`:
- `List[ActivityRecord]`: Lista de registros válidos parseados
- `ValidationReport`: Objeto con reporte de validación

##### **Validaciones Aplicadas**

| Validación | Tipo | Descripción |
|-----------|------|-------------|
| **Columnas requeridas** | Error | `entity_id`, `scope`, `category`, `activity_value`, `activity_unit` |
| **Scope válido** | Error | Debe ser 1, 2 o 3 |
| **Categoría válida** | Error | Debe estar en lista de 23 categorías GHG Protocol |
| **Valor numérico** | Error | `activity_value` debe ser > 0 |
| **Unidad válida** | Advertencia | Unidad debe estar en lista soportada |
| **Geografía válida** | Advertencia | Código de país debe ser ISO 3166-1 |
| **Año válido** | Advertencia | Año debe estar entre 2000 y 2030 |
| **Duplicados** | Advertencia | Filas completamente duplicadas |

##### **Ejemplo Básico**

```python
import pandas as pd
from utils.data_validator import validate_activity_data

# Cargar datos
df = pd.read_csv("data/mis_actividades.csv")

# Validar
valid_activities, report = validate_activity_data(df, strict=False)

# Revisar reporte
print(f"Total filas: {report.total_rows}")
print(f"Filas válidas: {report.valid_rows}")
print(f"Filas inválidas: {report.invalid_rows}")
print(f"Tasa de éxito: {report.success_rate:.1f}%")

# Mostrar errores
if report.errors:
    print("\nErrores encontrados:")
    for error in report.errors:
        print(f"  Fila {error.row}: {error.message}")

# Proceder solo si hay datos válidos
if valid_activities:
    print(f"\n✅ {len(valid_activities)} actividades listas para cálculo")
else:
    print("\n❌ No hay actividades válidas, revisa los errores")
```

##### **Ejemplo con Manejo de Errores**

```python
try:
    valid_activities, report = validate_activity_data(df, strict=True)
    
    if report.success_rate < 80:
        raise ValueError(
            f"Tasa de validación muy baja: {report.success_rate:.1f}%. "
            f"Se requiere al menos 80%."
        )
    
    # Continuar con cálculos
    for activity in valid_activities:
        result = compute_emission(activity, factor)
        
except ValueError as e:
    print(f"Error de validación: {e}")
    # Exportar reporte de errores
    errors_df = report.to_dataframe()
    errors_df.to_csv("errores_validacion.csv", index=False)
```

---

#### `get_data_quality_summary()`

Genera un resumen de calidad de datos.

```python
def get_data_quality_summary(
    df: pd.DataFrame
) -> Dict[str, Any]
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `df` | `pd.DataFrame` | ✅ Sí | DataFrame de actividades |

##### **Retorna**

`Dict[str, Any]` - Diccionario con métricas de calidad:

```python
{
    "total_rows": 100,
    "total_columns": 12,
    "missing_values": 5,
    "duplicate_rows": 2,
    "unique_entities": 8,
    "scopes_distribution": {1: 45, 2: 30, 3: 25},
    "categories_count": 12,
    "date_range": ("2024-01-01", "2024-12-31"),
    "quality_score": 0.92  # 0-1 (1 = perfect)
}
```

##### **Ejemplo**

```python
from utils.data_validator import get_data_quality_summary

# Obtener resumen de calidad
summary = get_data_quality_summary(df)

# Mostrar métricas clave
print(f"📊 Resumen de Datos:")
print(f"  Total filas: {summary['total_rows']}")
print(f"  Entidades únicas: {summary['unique_entities']}")
print(f"  Valores faltantes: {summary['missing_values']}")
print(f"  Duplicados: {summary['duplicate_rows']}")
print(f"  Score de calidad: {summary['quality_score']:.0%}")

# Distribución por scope
print("\n📈 Distribución por Scope:")
for scope, count in summary['scopes_distribution'].items():
    pct = (count / summary['total_rows']) * 100
    print(f"  Scope {scope}: {count} ({pct:.1f}%)")
```

---

### `utils.report_generator`

Funciones para generación de reportes.

---

#### `generate_excel_report()`

Genera un reporte Excel completo de la huella de carbono.

```python
def generate_excel_report(
    results: List[EmissionResult],
    output_path: str,
    include_charts: bool = True,
    company_name: Optional[str] = None,
    reporting_period: Optional[str] = None
) -> str
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `results` | `List[EmissionResult]` | ✅ Sí | - | Lista de resultados de emisiones |
| `output_path` | `str` | ✅ Sí | - | Ruta donde guardar el archivo Excel |
| `include_charts` | `bool` | ❌ No | `True` | Incluir gráficos en el reporte |
| `company_name` | `str` | ❌ No | `None` | Nombre de la empresa (para el reporte) |
| `reporting_period` | `str` | ❌ No | `None` | Periodo de reporte (ej: "2024") |

##### **Retorna**

`str` - Ruta completa del archivo generado.

##### **Estructura del Reporte Excel**

El archivo generado contiene **5 hojas**:

1. **Summary** (Resumen Ejecutivo)
   - Huella total
   - Distribución por Scope (tabla + gráfico de pastel)
   - Top 5 categorías
   - Métricas clave

2. **By Scope** (Desglose por Alcance)
   - Tabla detallada de emisiones por Scope 1, 2, 3
   - Subtotales y porcentajes
   - Gráfico de barras

3. **By Category** (Desglose por Categoría)
   - Todas las categorías con emisiones
   - Ordenado de mayor a menor
   - Gráfico de barras horizontales

4. **Detailed** (Datos Detallados)
   - Una fila por actividad calculada
   - Todas las columnas: entity, scope, category, value, unit, emission, factor, etc.
   - Formato de tabla con filtros

5. **Metadata** (Información del Reporte)
   - Fecha de generación
   - Versión del software
   - Número total de actividades
   - Período de reporte
   - Empresa

##### **Ejemplo Básico**

```python
from utils.report_generator import generate_excel_report
from calculators.core import compute_emission

# Calcular emisiones
results = [compute_emission(act, factor) for act in activities]

# Generar reporte
file_path = generate_excel_report(
    results,
    output_path="reports/huella_carbono_2024.xlsx",
    include_charts=True,
    company_name="Mi Empresa S.A.",
    reporting_period="Año Fiscal 2024"
)

print(f"✅ Reporte generado: {file_path}")
# Output:
# ✅ Reporte generado: reports/huella_carbono_2024.xlsx
```

##### **Ejemplo Avanzado con Formato**

```python
from datetime import datetime

# Información contextual
company_name = "Empresa XYZ"
year = datetime.now().year
period = f"Enero - Diciembre {year}"

# Generar reporte
file_path = generate_excel_report(
    results,
    output_path=f"reports/{company_name.replace(' ', '_')}_GHG_{year}.xlsx",
    include_charts=True,
    company_name=company_name,
    reporting_period=period
)

# Abrir automáticamente (Windows)
import os
os.startfile(file_path)  # Abre Excel con el reporte
```

---

#### `generate_word_report()`

Genera un reporte en formato Word/PDF con narrativa.

```python
def generate_word_report(
    results: List[EmissionResult],
    output_path: str,
    template_path: Optional[str] = None,
    company_name: Optional[str] = None,
    reporting_period: Optional[str] = None,
    include_recommendations: bool = True
) -> str
```

##### **Parámetros**

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `results` | `List[EmissionResult]` | ✅ Sí | - | Lista de resultados de emisiones |
| `output_path` | `str` | ✅ Sí | - | Ruta donde guardar el archivo |
| `template_path` | `str` | ❌ No | `None` | Plantilla Word personalizada |
| `company_name` | `str` | ❌ No | `None` | Nombre de la empresa |
| `reporting_period` | `str` | ❌ No | `None` | Período de reporte |
| `include_recommendations` | `bool` | ❌ No | `True` | Incluir recomendaciones de reducción |

##### **Retorna**

`str` - Ruta completa del archivo generado.

##### **Secciones del Reporte**

1. **Portada**
   - Logo (si está en template)
   - Nombre de la empresa
   - Título: "Reporte de Huella de Carbono"
   - Período de reporte
   - Fecha de generación

2. **Resumen Ejecutivo**
   - Huella total en tCO2e
   - Distribución por Scope (tabla y gráfico)
   - Principales hallazgos

3. **Metodología**
   - Estándar GHG Protocol
   - Factores de emisión utilizados (UK Gov 2025)
   - Alcances incluidos

4. **Resultados Detallados**
   - Scope 1: Emisiones directas
   - Scope 2: Emisiones indirectas por energía
   - Scope 3: Otras emisiones indirectas
   - Tablas y gráficos por categoría

5. **Análisis y Tendencias**
   - Comparación con períodos anteriores (si aplica)
   - Hotspots (puntos críticos)
   - Oportunidades de reducción

6. **Recomendaciones** (opcional)
   - Top 3-5 recomendaciones priorizadas
   - Estimación de potencial de reducción
   - Plan de acción sugerido

7. **Anexos**
   - Datos detallados (tabla completa)
   - Glosario de términos
   - Referencias

##### **Ejemplo**

```python
from utils.report_generator import generate_word_report

# Generar reporte Word
word_path = generate_word_report(
    results,
    output_path="reports/reporte_ejecutivo_2024.docx",
    company_name="Mi Empresa S.A.",
    reporting_period="Año 2024",
    include_recommendations=True
)

print(f"✅ Reporte Word generado: {word_path}")

# Convertir a PDF (requiere python-docx-pdf)
try:
    from docx2pdf import convert
    pdf_path = word_path.replace(".docx", ".pdf")
    convert(word_path, pdf_path)
    print(f"✅ Reporte PDF generado: {pdf_path}")
except ImportError:
    print("⚠️ Instala docx2pdf para generar PDF: pip install docx2pdf")
```

---

## 💡 Ejemplos de Uso

### **Ejemplo Completo: Flujo de Principio a Fin**

```python
import pandas as pd
from utils.factors import load_uk_gov_factors, find_factor
from utils.data_validator import validate_activity_data
from calculators.core import compute_emission, get_total_emissions
from utils.report_generator import generate_excel_report

# PASO 1: Cargar factores de emisión
print("📁 Cargando factores de emisión...")
factors_df = load_uk_gov_factors(
    "data/ghg-conversion-factors-2025-condensed-set.xlsx"
)
print(f"✅ {len(factors_df)} factores cargados")

# PASO 2: Cargar datos de actividad
print("\n📊 Cargando datos de actividad...")
activity_df = pd.read_csv("data/mis_actividades.csv")
print(f"✅ {len(activity_df)} filas cargadas")

# PASO 3: Validar datos
print("\n🔍 Validando datos...")
valid_activities, report = validate_activity_data(activity_df)
print(f"✅ Validación completada:")
print(f"   - Tasa de éxito: {report.success_rate:.1f}%")
print(f"   - Actividades válidas: {len(valid_activities)}")

if report.errors:
    print(f"⚠️ {len(report.errors)} errores encontrados")
    for error in report.errors[:5]:  # Mostrar primeros 5
        print(f"   - Fila {error.row}: {error.message}")

# PASO 4: Calcular emisiones
print("\n🧮 Calculando emisiones...")
results = []

for activity in valid_activities:
    # Buscar factor
    factor_result = find_factor(
        factors_df,
        activity.category,
        activity.activity_unit,
        geography=activity.geography,
        scope=activity.scope
    )
    
    if factor_result:
        factor_value, factor_source, metadata = factor_result
        
        # Crear EmissionFactor
        from models.emissions import EmissionFactor
        ef = EmissionFactor(
            source=factor_source,
            gas="CO2e",
            value=factor_value,
            unit=metadata['unit'],
            year=metadata['year'],
            geography=metadata.get('geography'),
            scope=activity.scope,
            category=activity.category
        )
        
        # Calcular
        result = compute_emission(activity, ef)
        results.append(result)

print(f"✅ {len(results)} emisiones calculadas")

# PASO 5: Obtener totales
print("\n📈 Resultados:")
totals = get_total_emissions(results)

print(f"🌍 Huella de Carbono Total: {totals['total_tonnes_co2e']:.2f} tCO2e")
print(f"\n📊 Por Scope:")
for scope, tonnes in totals['by_scope'].items():
    pct = (tonnes / totals['total_tonnes_co2e']) * 100
    print(f"   Scope {scope}: {tonnes:.2f} tCO2e ({pct:.1f}%)")

# Top 3 categorías
sorted_cats = sorted(
    totals['by_category'].items(),
    key=lambda x: x[1],
    reverse=True
)[:3]

print(f"\n🔥 Top 3 Categorías:")
for cat, tonnes in sorted_cats:
    pct = (tonnes / totals['total_tonnes_co2e']) * 100
    print(f"   {cat}: {tonnes:.2f} tCO2e ({pct:.1f}%)")

# PASO 6: Generar reporte
print("\n📄 Generando reporte Excel...")
report_path = generate_excel_report(
    results,
    output_path="reports/huella_carbono.xlsx",
    company_name="Mi Empresa",
    reporting_period="2024"
)
print(f"✅ Reporte guardado: {report_path}")
```

**Output esperado**:
```
📁 Cargando factores de emisión...
✅ 521 factores cargados

📊 Cargando datos de actividad...
✅ 24 filas cargadas

🔍 Validando datos...
✅ Validación completada:
   - Tasa de éxito: 100.0%
   - Actividades válidas: 24

🧮 Calculando emisiones...
✅ 24 emisiones calculadas

📈 Resultados:
🌍 Huella de Carbono Total: 24.46 tCO2e

📊 Por Scope:
   Scope 1: 8.52 tCO2e (34.8%)
   Scope 2: 10.65 tCO2e (43.5%)
   Scope 3: 5.29 tCO2e (21.6%)

🔥 Top 3 Categorías:
   purchased_electricity: 10.65 tCO2e (43.5%)
   mobile_combustion: 8.52 tCO2e (34.8%)
   business_travel: 5.29 tCO2e (21.6%)

📄 Generando reporte Excel...
✅ Reporte guardado: reports/huella_carbono.xlsx
```

---

## 📐 Tipos de Datos

### **Unidades Soportadas**

#### **Masa**
- `kg` - Kilogramos
- `tonnes` - Toneladas métricas (1000 kg)
- `lbs` - Libras
- `g` - Gramos

#### **Volumen**
- `litres` - Litros
- `m3` - Metros cúbicos
- `gallons` - Galones
- `ft3` - Pies cúbicos

#### **Energía**
- `kWh` - Kilovatios-hora
- `MWh` - Megavatios-hora
- `GWh` - Gigavatios-hora
- `GJ` - Gigajulios
- `MJ` - Megajulios
- `therm` - Termas

#### **Distancia**
- `km` - Kilómetros
- `miles` - Millas
- `passenger.km` - Pasajero-kilómetro
- `tonne.km` - Tonelada-kilómetro

#### **Dinero**
- `GBP` - Libras esterlinas
- `USD` - Dólares estadounidenses
- `EUR` - Euros

---

### **Geografías Soportadas**

| Código | País/Región |
|--------|-------------|
| `UK` | Reino Unido |
| `US` | Estados Unidos |
| `ES` | España |
| `FR` | Francia |
| `DE` | Alemania |
| `IT` | Italia |
| `BR` | Brasil |
| `MX` | México |
| `CN` | China |
| `IN` | India |
| `AU` | Australia |
| `Global` | Factor global/promedio |

---

## ⚠️ Manejo de Errores

### **Excepciones Comunes**

#### **UnitConversionError**
```python
from utils.unit_converter import UnitConversionError

try:
    result = compute_emission(activity, factor, auto_convert_units=False)
except UnitConversionError as e:
    print(f"Error de conversión: {e}")
    print("Solución: Activar auto_convert_units=True o verificar unidades")
```

#### **FactorNotFoundError**
```python
from utils.factors import FactorNotFoundError

try:
    factor_result = find_factor(factors_df, "invalid_category", "liters")
except FactorNotFoundError as e:
    print(f"Factor no encontrado: {e}")
    print("Solución: Verificar categoría, unidad o usar factor personalizado")
```

#### **ValidationError**
```python
from utils.data_validator import ValidationError

try:
    valid_activities, report = validate_activity_data(df, strict=True)
except ValidationError as e:
    print(f"Error de validación: {e}")
    print("Errores:")
    for error in e.errors:
        print(f"  Fila {error.row}: {error.message}")
```

---

## 📞 Soporte

### **Documentación Adicional**
- [USER_GUIDE.md](USER_GUIDE.md) - Guía de usuario completa
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Guía para desarrolladores
- [DOCKER_TESTING_GUIDE.md](DOCKER_TESTING_GUIDE.md) - Guía de Docker

### **Referencias Externas**
- [GHG Protocol](https://ghgprotocol.org/) - Estándar oficial
- [UK Gov GHG Factors](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting) - Factores de emisión
- [IPCC AR5](https://www.ipcc.ch/report/ar5/) - Valores GWP

---

**Versión**: 1.0  
**Última actualización**: 8 de octubre de 2025  
**Autor**: Carbon GHG Calculator Team  
**Licencia**: MIT
