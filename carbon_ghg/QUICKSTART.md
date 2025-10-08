# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a comenzar a usar la Calculadora de Huella de Carbono en menos de 5 minutos.

## ⚡ Instalación Rápida

### 1. Requisitos
- Python 3.9 o superior
- pip

### 2. Instalar Dependencias

```bash
cd carbon_ghg
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación

```bash
streamlit run app/streamlit_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📝 Primer Cálculo (3 Pasos)

### Paso 1: Descargar Factores de Emisión

**Opción A - UK Government Factors (Recomendado):**
1. Descarga el archivo condensado: [GHG Conversion Factors 2025](https://assets.publishing.service.gov.uk/media/6722566a3758e4604742aa1e/ghg-conversion-factors-2024-condensed_set__for_most_users__v1_1.xlsx)
2. O usa el archivo incluido: `data/ghg-conversion-factors-2025-condensed-set.xlsx`

**Opción B - Usar Dataset de Ejemplo:**
- Ya incluido en `data/ghg-conversion-factors-2025-condensed-set.xlsx`

### Paso 2: Preparar tus Datos de Actividad

Crea un archivo CSV o Excel con estas columnas:

| entity_id | scope | category | activity_value | activity_unit | geography | year |
|-----------|-------|----------|----------------|---------------|-----------|------|
| factory_A | 1 | diesel | 500 | liters | GBR | 2024 |
| factory_A | 2 | electricity | 25000 | kWh | GBR | 2024 |
| office_B | 3 | business_travel | 5000 | km | USA | 2024 |

**O usa el archivo de ejemplo incluido:**
- `data/sample_activities.csv`

**Columnas Requeridas:**
- `entity_id`: ID de tu entidad (ej: "factory_1", "office_main")
- `scope`: 1, 2 o 3 (Alcance GHG Protocol)
- `category`: Tipo de actividad (ej: "diesel", "electricity", "business_travel")
- `activity_value`: Cantidad (número)
- `activity_unit`: Unidad (ej: "liters", "kWh", "km")

**Columnas Opcionales:**
- `geography`: País (ISO 3166-1 alpha-3, ej: "GBR", "USA")
- `year`: Año del dato
- `month`: Mes (1-12)
- `facility`: Nombre de instalación
- `description`: Descripción adicional

### Paso 3: Calcular en la Aplicación

1. **Cargar Factores:**
   - En la barra lateral, sube el archivo de factores de emisión

2. **Cargar Datos:**
   - Sube tu archivo CSV/Excel con datos de actividad

3. **Validar:**
   - Ve a la pestaña "🔍 Validación"
   - Click en "🔍 Validar Datos"
   - Revisa el reporte de calidad

4. **Calcular:**
   - Ve a la pestaña "🧮 Cálculo"
   - Click en "🚀 Calcular Huella de Carbono"

5. **Ver Resultados:**
   - Ve a la pestaña "📈 Resultados"
   - Explora gráficos y tablas
   - Descarga resultados en CSV

## 📊 Ejemplo Completo (Línea de Comandos)

Si prefieres trabajar con código Python:

```python
import pandas as pd
from models.emissions import ActivityRecord, EmissionFactor
from calculators.core import compute_emission
from utils.data_validator import validate_activity_data

# 1. Cargar datos
df = pd.read_csv('data/sample_activities.csv')

# 2. Validar
valid_activities, report = validate_activity_data(df)
print(f"Actividades válidas: {len(valid_activities)}")

# 3. Calcular (ejemplo simple)
activity = valid_activities[0]
ef = EmissionFactor(
    source="UK2025",
    gas="CO2e",
    value=2.68,  # kg CO2e / liter (diesel)
    unit="kg CO2e / liter",
    year=2025,
    scope=1
)

result = compute_emission(activity, ef)
print(f"Emisión: {result.emission_tCO2e:.4f} tCO2e")
```

## 🧪 Verificar Instalación

Ejecuta las pruebas básicas:

```bash
python tests/test_basic.py
```

Si todas las pruebas pasan (✅), ¡estás listo!

## 🌍 Categorías Principales

### Scope 1 - Emisiones Directas
- `stationary_combustion`: Calderas, generadores (gas natural, diesel, carbón)
- `mobile_combustion`: Vehículos de empresa (gasolina, diesel)
- `process_emissions`: Procesos industriales
- `fugitive_emissions`: Fugas de refrigerantes, CH₄

### Scope 2 - Energía Comprada
- `purchased_electricity`: Consumo eléctrico
- `purchased_heat`: Calefacción/vapor comprado
- `purchased_steam`: Vapor industrial
- `purchased_cooling`: Refrigeración centralizada

### Scope 3 - Cadena de Valor (15 categorías)
- `business_travel`: Viajes de negocio
- `employee_commuting`: Desplazamientos empleados
- `purchased_goods_services`: Bienes/servicios comprados
- `waste_generated`: Residuos generados
- `upstream_transportation`: Transporte de materias primas
- ... y 10 categorías más

## 🔧 Unidades Soportadas

### Energía
`kWh`, `MWh`, `GWh`, `MJ`, `GJ`, `TJ`, `BTU`, `MMBTU`, `therm`

### Masa
`kg`, `g`, `tonne`, `ton`, `lb`, `lbs`

### Volumen
`liter`, `l`, `L`, `ml`, `gallon`, `gal`, `m3`, `m³`

### Distancia
`km`, `m`, `mile`, `mi`, `ft`

### Compuestas
`passenger.km`, `tonne.km`, `vehicle.km`

**¡El sistema convierte automáticamente entre unidades compatibles!**

## 💡 Tips y Mejores Prácticas

### ✅ DO - Hacer
- Usa categorías descriptivas ("diesel_vehicles", "natural_gas_heating")
- Incluye geografía para factores más precisos
- Valida datos antes de calcular
- Revisa el reporte de calidad de datos
- Descarga resultados regularmente

### ❌ DON'T - Evitar
- No uses valores negativos en `activity_value`
- No mezcles unidades sin verificar compatibilidad
- No uses scopes fuera del rango 1-3
- No omitas columnas requeridas

## 🆘 Problemas Comunes

### Error: "No se encontró factor de emisión"
**Solución:**
- Verifica que el archivo de factores esté cargado correctamente
- Asegúrate de que la categoría coincida con las disponibles
- Revisa que la unidad sea compatible
- Prueba con categorías más genéricas ("diesel" en lugar de "diesel_heavy_duty")

### Error: "Unidades no compatibles"
**Solución:**
- Verifica que las unidades sean del mismo tipo (energía con energía, masa con masa)
- Usa unidades estándar: `kWh`, `liters`, `kg`, `km`
- Revisa el log para ver qué unidad esperaba el factor

### Tasa de validación baja (<80%)
**Solución:**
- Revisa la pestaña de Validación para ver errores específicos
- Verifica que los scopes sean 1, 2 o 3
- Asegúrate de que `activity_value` sea positivo
- Completa campos requeridos (entity_id, scope, category, activity_value, activity_unit)

## 📚 Recursos Adicionales

### Documentación
- **README completo**: `README.md`
- **Configuración**: `config.py`
- **Ejemplos**: `data/sample_activities.csv`

### Referencias GHG Protocol
- [Corporate Standard](https://ghgprotocol.org/corporate-standard)
- [Scope 2 Guidance](https://ghgprotocol.org/scope-2-guidance)
- [Scope 3 Standard](https://ghgprotocol.org/standards/scope-3-standard)

### Factores de Emisión
- [UK Gov Factors](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting)
- [IPCC EFDB](https://www.ipcc-nggip.iges.or.jp/EFDB/main.php)
- [EPA Factors Hub](https://www.epa.gov/climateleadership/ghg-emission-factors-hub)

## 🎯 Próximos Pasos

1. **Experimenta con el archivo de ejemplo:**
   ```bash
   # Usa data/sample_activities.csv en la aplicación
   ```

2. **Prepara tus propios datos:**
   - Exporta desde Excel/Google Sheets
   - Asegúrate de incluir columnas requeridas
   - Valida antes de calcular

3. **Explora funcionalidades avanzadas:**
   - Conversión automática de unidades
   - Agregación por scope y categoría
   - Reportes descargables

4. **Integra con tus sistemas:**
   - Exporta desde tus sistemas de gestión
   - Automatiza cálculos mensuales
   - Genera reportes periódicos

---

**¿Necesitas ayuda?**
- Revisa `README.md` para documentación completa
- Consulta ejemplos en `data/`
- Ejecuta `python tests/test_basic.py` para verificar funcionamiento

**¡Comienza a calcular tu huella de carbono ahora! 🌱**
