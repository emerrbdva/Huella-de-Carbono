# 📊 GUÍA RÁPIDA: NUEVAS VISUALIZACIONES

## 🎉 Quick Wins Implementados (SIN COSTO)

Hemos agregado **3 visualizaciones profesionales** a la aplicación Streamlit para mejorar el análisis de la huella de carbono:

---

## 1️⃣ DIAGRAMA SANKEY - Flujo de Emisiones 🌊

### ¿Qué muestra?
Visualiza el **flujo de emisiones** desde los Scopes hasta las categorías y finalmente las entidades.

### ¿Cómo leerlo?
- **Nodos (recuadros)**: Representan Scopes, Categorías y Entidades
- **Flujos (conexiones)**: El grosor indica la magnitud de las emisiones
- **Colores**:
  - 🔴 **Rojo**: Scope 1 (emisiones directas)
  - 🟦 **Turquesa**: Scope 2 (electricidad)
  - 🟩 **Verde**: Scope 3 (cadena de valor)
  - 🟨 **Amarillo/Gris**: Entidades

### Ejemplo de interpretación:
```
Scope 1 ──────► mobile_combustion ──────► factory_A (grande)
         │                          └──► warehouse_C (pequeño)
         └──► stationary_combustion ──► office_B
```

**Lectura**: "Scope 1 tiene mayor contribución desde mobile_combustion, principalmente en factory_A"

---

## 2️⃣ TREEMAP INTERACTIVO - Mapa Jerárquico 🗺️

### ¿Qué muestra?
Distribución **jerárquica** de emisiones con capacidad de **drill-down**.

### ¿Cómo interactuar?
1. **Haz clic** en cualquier recuadro para hacer zoom
2. **Hover** para ver detalles (actividad, fuente, porcentaje)
3. **Click en fondo** para volver al nivel superior

### Jerarquía:
```
┌─────────────────────────────────────┐
│          Scope 1/2/3                │
│  ┌───────────────┐  ┌─────────────┐│
│  │  Categoría 1  │  │ Categoría 2 ││
│  │ ┌───┐  ┌────┐ │  │             ││
│  │ │Ent││Ent2│ │  │             ││
│  │ └───┘  └────┘ │  │             ││
│  └───────────────┘  └─────────────┘│
└─────────────────────────────────────┘
```

### Colores:
- 🔴 **Rojo intenso**: Emisiones ALTAS
- 🟡 **Amarillo**: Emisiones MEDIAS
- 🟢 **Verde**: Emisiones BAJAS

---

## 3️⃣ EVOLUCIÓN TEMPORAL - Análisis de Tendencias 📅

### ¿Qué muestra?
Cambios en emisiones **mes a mes** o **año a año**.

### Requisitos:
Tu archivo CSV debe tener columnas `year` y `month`:
```csv
entity_id,scope,category,activity_value,activity_unit,geography,year,month
factory_A,1,diesel,500,liters,GBR,2024,1
factory_A,1,diesel,480,liters,GBR,2024,2
factory_A,1,diesel,520,liters,GBR,2024,3
```

### Métricas automáticas:
- **Primer Periodo**: Emisiones iniciales
- **Último Periodo**: Emisiones recientes
- **Tendencia**: Cambio porcentual (📈 aumento / 📉 reducción)

### Ejemplo de análisis:
```
Enero:  100 tCO2e
Febrero: 95 tCO2e  → 📉 Reducción del 5%
Marzo:  110 tCO2e  → 📈 Aumento del 10%
```

---

## 🚀 CÓMO USAR LAS VISUALIZACIONES

### Paso 1: Cargar datos temporales
Usa el archivo de ejemplo `data/sample_activities_temporal.csv` que incluye 4 meses de datos:

```bash
# En Streamlit:
1. Tab "📊 Datos" → Cargar CSV
2. Selecciona: sample_activities_temporal.csv
3. Click "✅ Validar"
```

### Paso 2: Calcular emisiones
```bash
# En tab "🧮 Cálculo":
1. Click "⚡ Calcular Emisiones"
2. Espera barra de progreso
3. Ver confirmación de cálculo exitoso
```

### Paso 3: Explorar visualizaciones
```bash
# En tab "📊 Resultados":
1. Scroll hacia abajo para ver:
   - 🌊 Diagrama Sankey
   - 🗺️ Treemap Interactivo
   - 📅 Evolución Temporal
2. Interactúa con cada gráfico
3. Analiza las métricas automáticas
```

---

## 💡 CASOS DE USO

### Caso 1: Identificar hotspots
**Usa**: Treemap
- Click en cada Scope
- Identifica categorías con mayor impacto
- Prioriza acciones de reducción

### Caso 2: Análisis de flujo
**Usa**: Sankey
- Visualiza rutas de emisiones
- Identifica concentraciones
- Comunica a stakeholders

### Caso 3: Seguimiento de metas
**Usa**: Evolución Temporal
- Compara mes vs mes anterior
- Verifica si cumples objetivos de reducción
- Detecta anomalías (picos inesperados)

---

## 📈 PRÓXIMOS PASOS (100% GRATIS)

### Fase 2: IA con Ollama (Mañana)
- ✅ **Categorización automática**: "consumo de diesel" → Scope 1
- ✅ **Búsqueda semántica**: Encuentra factores con lenguaje natural
- ✅ **Recomendaciones**: Sugiere mejoras basadas en benchmarks

### Fase 3: Tests y Calidad (Día 3)
- ✅ **Coverage 95%**: Tests exhaustivos
- ✅ **Docker**: Containerización para deployment fácil

---

## 🎯 EJEMPLO COMPLETO DE WORKFLOW

```bash
# 1. Iniciar aplicación
streamlit run app/streamlit_app.py

# 2. Cargar datos de 4 meses
# Tab Datos → sample_activities_temporal.csv

# 3. Ver validación
# 100% datos válidos (32 actividades)

# 4. Calcular
# Tab Cálculo → "Calcular Emisiones"

# 5. Analizar resultados:

# Sankey:
# - Scope 2 es el mayor → Electricidad
# - factory_A domina en Scope 1

# Treemap:
# - Click en Scope 2 → Ver detalle
# - purchased_electricity es 60% del total

# Temporal:
# - Enero: 15.2 tCO2e
# - Abril: 13.8 tCO2e
# - Tendencia: 📉 Reducción 9.2%

# 6. Descargar reportes
# - Excel con 3 hojas
# - Word en formato APA 7
# - CSV para análisis adicional
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### "No hay suficientes datos para Sankey"
➡️ Asegúrate de haber calculado emisiones primero

### "Solo hay datos de un periodo" (Temporal)
➡️ Tu CSV necesita múltiples valores de `month` o `year`

### Treemap no muestra drill-down
➡️ Verifica que tienes datos en múltiples categorías y entidades

---

## 📚 RECURSOS ADICIONALES

- **Documentación Plotly**: https://plotly.com/python/
- **GHG Protocol**: https://ghgprotocol.org/
- **Sample Data**: `data/sample_activities_temporal.csv`

---

¿Listo para explorar? **Abre http://localhost:8501 en tu navegador** 🚀
