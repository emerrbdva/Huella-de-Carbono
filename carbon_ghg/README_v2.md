# 🌍 Sistema Profesional de Huella de Carbono v2.0

**Sistema completo para calcular, analizar y reportar emisiones de GEI según GHG Protocol**  
**100% gratuito, local y open source** 💚

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-red.svg)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/Tests-6%2F6%20Passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-100%25-success.svg)]()

---

## 🎉 ¿Qué hay de nuevo en v2.0? ⭐

### Visualizaciones Avanzadas (NUEVO):
- 🌊 **Diagrama Sankey**: Flujo visual de emisiones
- 🗺️ **Treemap Interactivo**: Mapa jerárquico con drill-down
- 📅 **Evolución Temporal**: Gráficos de tendencias mes a mes
- 💳 **Métricas Cards**: KPIs destacados en tiempo real

### Mejoras Core:
- ✅ 521 factores UK Gov 2025 (vs 0 en v1.0)
- ✅ 4 formatos de reporte (Excel, Word, CSV, TXT)
- ✅ Validación automática con sugerencias inteligentes
- ✅ Tests automatizados (6/6 passing)

---

## ✨ Características Principales

### 🧮 **Cálculo GHG Protocol Completo**
| Scope | Descripción | Categorías |
|-------|-------------|------------|
| **1** | Emisiones directas | Combustión estacionaria/móvil, Procesos, Fugitivas |
| **2** | Electricidad comprada | Location-based, Market-based |
| **3** | Cadena de valor | 15 categorías upstream/downstream |

**Fórmula**: `E = AD × EF × GWP`  
**Trazabilidad**: Completa (fuente, año, versión, calidad)

### 📊 **6 Visualizaciones Profesionales**
1. 🥧 Gráfico de torta - Distribución por Scope
2. 📊 Barras horizontales - Ranking de categorías
3. 🌊 **Sankey** - Flujo Scope → Categoría → Entidad
4. 🗺️ **Treemap** - Jerarquía interactiva
5. 📅 **Líneas temporales** - Evolución mes a mes
6. 💳 Métricas - Totales, promedios, tendencias

### 📁 **521 Factores de Emisión**
- **UK Government 2025**: 15 hojas (Fuels, Electricity, Transport, Waste, etc.)
- **IPCC 2019**: Valores de referencia globales
- **EPA 2024**: Factores USA complementarios
- **Búsqueda inteligente**: Por categoría, geografía, año

### 📄 **4 Formatos de Reporte**
| Formato | Características | Uso |
|---------|----------------|-----|
| 📊 **Excel** | 3 hojas (Resumen, Detalle, Categorías) | Análisis ejecutivo |
| 📝 **Word** | Formato APA 7 con referencias | Informes académicos |
| 📥 **CSV** | Datos crudos tabulares | Análisis adicional |
| 📄 **TXT** | Resumen ejecutivo simple | Comunicación rápida |

### 🔍 **Validación Automática**
```
✅ Validación de campos (tipo, rango, formato)
✅ Detección de errores con sugerencias
✅ Quality score automático (0-100%)
✅ Reporte de completitud por campo
```

---

## 🚀 Quick Start (5 minutos)

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/carbon_ghg.git
cd carbon_ghg

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar aplicación

```bash
# Iniciar Streamlit
streamlit run app/streamlit_app.py

# Abre navegador en: http://localhost:8501
```

### 3. Probar con datos de ejemplo

```bash
# En la interfaz Streamlit:
1. Tab "📊 Datos" → Cargar CSV
2. Selecciona: data/sample_activities_temporal.csv
3. Tab "✅ Validación" → Ver reporte de calidad
4. Tab "🧮 Cálculo" → Click "Calcular Emisiones"
5. Tab "📊 Resultados" → Explorar visualizaciones
```

---

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| [GUIA_VISUALIZACIONES.md](GUIA_VISUALIZACIONES.md) | Cómo usar Sankey, Treemap, Temporal |
| [PLAN_5_DIAS_SIN_COSTOS.md](PLAN_5_DIAS_SIN_COSTOS.md) | Roadmap de implementación |
| [ARQUITECTURA_AVANZADA.md](ARQUITECTURA_AVANZADA.md) | Arquitectura técnica detallada |
| [RESUMEN_QUICK_WINS.md](RESUMEN_QUICK_WINS.md) | Resumen ejecutivo mejoras v2.0 |
| [DESCARGAS.md](DESCARGAS.md) | Guía de formatos de reporte |

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
python tests/test_basic.py

# Resultado esperado:
# ✅ test_models: OK
# ✅ test_calculation: OK
# ✅ test_unit_conversion: OK
# ✅ test_validation: OK
# ✅ test_gwp: OK
# ✅ test_aggregation: OK
# 📊 RESULTADOS: 6 pruebas pasaron, 0 fallaron
```

---

## 📊 Ejemplo de Uso Programático

```python
from models.emissions import ActivityRecord, EmissionFactor
from calculators.core import compute_emission

# Definir actividad
activity = ActivityRecord(
    entity_id="factory_A",
    scope=1,
    category="mobile_combustion",
    activity_value=1000,  # litros
    activity_unit="liters",
    geography="GBR",
    year=2024
)

# Factor de emisión
factor = EmissionFactor(
    source="UK Gov 2025",
    gas="CO2e",
    value=2.68,  # kg CO2e/liter
    unit="kg CO2e per liter",
    year=2025
)

# Calcular
result = compute_emission(activity, factor)

print(f"Emisión: {result.emission_tCO2e:.2f} tCO2e")
# Output: Emisión: 2.68 tCO2e
```

---

## 🏗️ Estructura del Proyecto

```
carbon_ghg/
├── app/
│   └── streamlit_app.py          # Interfaz web (5 tabs, 6 visualizaciones)
├── calculators/
│   ├── core.py                   # Motor de cálculo E = AD × EF × GWP
│   ├── scope1.py                 # Scope 1: 4 categorías
│   ├── scope2.py                 # Scope 2: location/market-based
│   └── scope3.py                 # Scope 3: 15 categorías
├── data/
│   ├── ghg-conversion-factors-2025-condensed-set.xlsx
│   ├── sample_activities.csv     # Ejemplo 1 mes (24 actividades)
│   └── sample_activities_temporal.csv  # Ejemplo 4 meses (32 actividades)
├── models/
│   └── emissions.py              # Pydantic schemas (ActivityRecord, etc.)
├── utils/
│   ├── factors.py                # Carga UK Gov (521 factores)
│   ├── unit_converter.py         # 40+ unidades soportadas
│   ├── data_validator.py         # Validación con quality score
│   └── report_generator.py       # Excel (3 hojas) + Word (APA 7)
├── tests/
│   └── test_basic.py             # 6 tests automatizados
├── examples/
│   └── usage_example.py          # Ejemplos sin UI (5 casos)
├── reports/                      # Reportes generados
├── docs/                         # Documentación adicional
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

---

## 🔧 Dependencias

```txt
# Core
python >= 3.9
pandas >= 2.0.0
pydantic >= 2.0.0

# Web UI
streamlit >= 1.28.0
plotly >= 5.17.0

# Reportes
openpyxl >= 3.1.0          # Excel
python-docx >= 1.1.0       # Word

# Conversión
pint >= 0.22               # Unidades

# Testing
pytest >= 7.4.0
pytest-cov >= 4.0.0
```

---

## 🎯 Roadmap

### ✅ Completado (v2.0):
- [x] Cálculo GHG Protocol completo
- [x] 521 factores UK Gov 2025
- [x] 6 visualizaciones profesionales
- [x] 4 formatos de reporte
- [x] Validación automática
- [x] Tests 6/6 passing

### ⏳ En progreso (v2.1):
- [ ] IA local con Ollama (categorización automática)
- [ ] Búsqueda semántica de factores
- [ ] Recomendaciones inteligentes
- [ ] Benchmarking sectorial

### 📅 Planificado (v3.0):
- [ ] API REST con FastAPI
- [ ] Multi-tenant + autenticación
- [ ] PostgreSQL + Redis
- [ ] Forecasting con Prophet/SARIMA
- [ ] Módulos sectoriales (agricultura, construcción, etc.)

Ver [PLAN_5_DIAS_SIN_COSTOS.md](PLAN_5_DIAS_SIN_COSTOS.md) para detalles completos.

---

## 💡 Casos de Uso

### 1. Empresa Manufacturera
```
Objetivo: Reducir Scope 2 (electricidad) en 30%
Proceso:
1. Cargar CSV con consumo mensual de electricidad
2. Validar datos (100% completitud)
3. Calcular baseline (Enero: 250 tCO2e)
4. Implementar medidas (paneles solares)
5. Comparar Feb-Abr (promedio: 175 tCO2e)
6. Resultado: 30% reducción alcanzado ✅
```

### 2. Municipalidad
```
Objetivo: Inventario GHG Protocol completo
Alcances:
- Scope 1: Flota municipal (vehículos, camiones)
- Scope 2: Alumbrado público + edificios
- Scope 3: Residuos, commuting empleados
Visualización: Sankey muestra que residuos son 40% Scope 3
Acción: Priorizar planta de reciclaje
```

### 3. Proyecto Construcción
```
Objetivo: Certificación LEED (reporte APA 7)
Pasos:
1. Registrar todas las actividades (combustibles, electricidad, materiales)
2. Calcular con factores UK Gov 2025
3. Generar reporte Word APA 7
4. Enviar a certificador ✅
```

---

## 🤝 Contribuciones

¡Contribuciones son bienvenidas!

```bash
# Fork el repositorio
# Crea una rama
git checkout -b feature/nueva-funcionalidad

# Haz tus cambios
# Ejecuta tests
python tests/test_basic.py

# Commit
git commit -m "feat: agregar nueva funcionalidad"

# Push
git push origin feature/nueva-funcionalidad

# Crea Pull Request
```

---

## 📜 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- **GHG Protocol**: Metodología estándar de cálculo
- **UK DEFRA**: Factores de emisión 2025
- **IPCC**: Valores GWP AR5
- **Streamlit**: Framework web open source
- **Plotly**: Visualizaciones interactivas
- **Pydantic**: Validación de datos

---

## 📞 Soporte

- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/carbon_ghg/issues)
- 📚 Docs: [Wiki](https://github.com/tu-usuario/carbon_ghg/wiki)
- 💬 Discusiones: [GitHub Discussions](https://github.com/tu-usuario/carbon_ghg/discussions)

---

## 🌟 ¿Te gusta el proyecto?

⭐ **Dale una estrella** en GitHub si te resultó útil!

---

**Versión**: 2.0.0  
**Última actualización**: 8 de Octubre, 2025  
**Autor**: [Tu nombre]

---

## 🚀 Comenzar Ahora

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Ejecutar
streamlit run app/streamlit_app.py

# 3. Abrir navegador
# http://localhost:8501

# 4. ¡Explorar! 🎉
```

---

**¿Listo para medir tu huella de carbono?** 🌍💚
