# 📚 USER GUIDE - Carbon GHG Calculator

**Versión**: 1.0  
**Fecha**: Octubre 8, 2025  
**Audiencia**: Usuarios finales (responsables de sostenibilidad, analistas ambientales)

---

## 📖 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Primeros Pasos](#primeros-pasos)
3. [Preparar tus Datos](#preparar-tus-datos)
4. [Cargar y Validar](#cargar-y-validar)
5. [Calcular Emisiones](#calcular-emisiones)
6. [Interpretar Resultados](#interpretar-resultados)
7. [Generar Reportes](#generar-reportes)
8. [Usar IA](#usar-ia)
9. [Análisis Temporal](#análisis-temporal)
10. [FAQ](#faq)

---

## 1. Introducción

### ¿Qué es Carbon GHG Calculator?

Carbon GHG Calculator es una herramienta profesional para medir tu **huella de carbono corporativa** siguiendo el estándar internacional **GHG Protocol**.

### ¿Por qué GHG Protocol?

El GHG Protocol es el estándar mundial para contabilizar emisiones de gases de efecto invernadero (GEI). Clasifica las emisiones en **3 Scopes**:

- **Scope 1**: Emisiones directas de fuentes que controlas (tus vehículos, calderas, procesos)
- **Scope 2**: Emisiones indirectas de energía comprada (electricidad, vapor, calor)
- **Scope 3**: Otras emisiones indirectas (viajes de negocios, transporte de productos, residuos)

### Características Principales

✅ **521 factores de emisión UK Gov 2025** (los más actualizados)  
✅ **Cálculos automáticos** con conversión de unidades  
✅ **Visualizaciones interactivas** (Sankey, Treemap, evolución temporal)  
✅ **Inteligencia Artificial** para categorización y recomendaciones  
✅ **Reportes exportables** en CSV y Excel  
✅ **100% gratuito** y open source  

---

## 2. Primeros Pasos

### Opción 1: Usar la Plantilla Excel (⚡ RECOMENDADO - 1 minuto)

**La forma más rápida de empezar**:

1. **Abre la plantilla**:
   ```
   📁 data/PLANTILLA_HUELLA_CARBONO.xlsx
   ```

2. **Lee las instrucciones**:
   - Hoja 1: "INSTRUCCIONES" tiene guía completa
   - Hoja 2: "DATOS" es donde completarás tu información
   - Hoja 3: "EJEMPLOS" muestra 5 actividades de referencia

3. **Completa tus datos** en la hoja "DATOS" (fila 3 en adelante)

4. **Guarda tu archivo** como `mis_emisiones_2025.xlsx`

5. **Carga en la app**:
   - Abre http://localhost:8501
   - Ve a pestaña "📊 Datos"
   - Click "Cargar desde archivo Excel"
   - Selecciona tu archivo
   - ¡Listo! 🎉

**Tiempo total**: ~5 minutos para tus primeras emisiones calculadas

### Opción 2: Usar archivo CSV

Si prefieres CSV:

1. Crea archivo con estas columnas (mínimas):
   ```csv
   entity_id,scope,category,activity_value,activity_unit
   FLEET001,1,mobile_combustion,1000,litres
   OFFICE_HQ,2,purchased_electricity,50000,kWh
   ```

2. Guarda como `mis_datos.csv`

3. Carga en pestaña "📊 Datos" → "Cargar desde CSV"

### Opción 3: Cargar datos de ejemplo

Para probar la herramienta:

1. En pestaña "📊 Datos"
2. Click en "Cargar datos de ejemplo"
3. Explora las funcionalidades con 24 actividades pre-cargadas

---

## 3. Preparar tus Datos

### 3.1 Campos Obligatorios

Para cada actividad que genere emisiones, necesitas:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **entity_id** | Identificador de la entidad (planta, oficina, flota) | `FACTORY_001` |
| **scope** | Scope GHG (1, 2 o 3) | `1` |
| **category** | Categoría de emisión | `mobile_combustion` |
| **activity_value** | Cantidad consumida | `1000` |
| **activity_unit** | Unidad de medida | `litres` |

### 3.2 Campos Opcionales (recomendados)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **subcategory** | Tipo específico de combustible/energía | `diesel` |
| **geography** | País (código ISO-3) | `GBR` |
| **year** | Año del dato | `2025` |
| **month** | Mes (1-12) | `1` |
| **facility** | Nombre de instalación | `Planta Norte` |
| **description** | Descripción libre | `Flota de distribución` |

### 3.3 Categorías Disponibles

#### Scope 1 (Emisiones Directas):
- `stationary_combustion` - Calderas, generadores fijos
- `mobile_combustion` - Vehículos propios
- `process_emissions` - Procesos industriales
- `fugitive_emissions` - Fugas de refrigerantes

#### Scope 2 (Energía Comprada):
- `purchased_electricity` - Electricidad de la red
- `purchased_heat` - Calor/vapor comprado
- `purchased_steam` - Vapor comprado
- `purchased_cooling` - Refrigeración comprada

#### Scope 3 (Otras Indirectas):
- `purchased_goods_services` - Materiales comprados
- `capital_goods` - Equipos, construcción
- `fuel_energy_activities` - Upstream de combustibles
- `upstream_transportation` - Transporte de insumos
- `waste_generated` - Residuos generados
- `business_travel` - Viajes de negocios
- `employee_commuting` - Traslados empleados
- `upstream_leased_assets` - Activos arrendados
- `downstream_transportation` - Distribución productos
- `processing_sold_products` - Procesamiento downstream
- `use_sold_products` - Uso por clientes
- `end_of_life_sold_products` - Disposición final
- `downstream_leased_assets` - Activos arrendados downstream
- `franchises` - Franquicias
- `investments` - Inversiones financieras

### 3.4 Unidades Soportadas

| Unidad | Descripción | Uso típico |
|--------|-------------|------------|
| `litres` | Litros | Combustibles líquidos |
| `m³` | Metros cúbicos | Gas natural |
| `kg` | Kilogramos | Sólidos, residuos |
| `tonnes` | Toneladas | Grandes cantidades |
| `kWh` | Kilovatios-hora | Electricidad, gas |
| `MWh` | Megavatios-hora | Grandes consumos |
| `km` | Kilómetros | Distancias (transporte propio) |
| `passenger.km` | Pasajero-kilómetro | Vuelos, transporte pasajeros |
| `tonne.km` | Tonelada-kilómetro | Transporte de carga |
| `USD` | Dólares | Compras (spend-based) |
| `EUR` | Euros | Compras (spend-based) |
| `GBP` | Libras | Compras (spend-based) |

### 3.5 Códigos de País (ISO-3)

| Código | País |
|--------|------|
| `GBR` | Reino Unido |
| `USA` | Estados Unidos |
| `ESP` | España |
| `FRA` | Francia |
| `DEU` | Alemania |
| `ITA` | Italia |
| `MEX` | México |
| `BRA` | Brasil |
| `CHN` | China |
| `IND` | India |
| `JPN` | Japón |
| `AUS` | Australia |

---

## 4. Cargar y Validar

### 4.1 Cargar Datos

**Desde Excel**:
1. Pestaña "📊 Datos"
2. Sección "Cargar datos desde archivo"
3. Botón "Cargar archivo Excel"
4. Seleccionar tu archivo `.xlsx`
5. Esperar mensaje: "✅ Archivo cargado: X actividades"

**Desde CSV**:
1. Pestaña "📊 Datos"
2. Botón "Cargar archivo CSV"
3. Seleccionar tu archivo `.csv`
4. Esperar confirmación

### 4.2 Validación Automática

La aplicación valida automáticamente:

✅ **Scope válido** (1, 2 o 3)  
✅ **Categoría válida** (23 categorías GHG Protocol)  
✅ **Valor positivo** (activity_value > 0)  
✅ **Unidad soportada** (12 unidades disponibles)  
✅ **Año válido** (1990-2100)  
✅ **Mes válido** (1-12 si se proporciona)  

### 4.3 Ver Errores

Si hay errores:

1. La app mostrará: "⚠️ X actividades con errores"
2. Expande "Ver errores" para detalles
3. Corrige en tu archivo fuente
4. Vuelve a cargar

**Errores comunes**:
```
❌ Scope inválido: debe ser 1, 2 o 3
   Fila 5: scope = "A" → Cambiar a 1, 2 o 3

❌ Activity value negativo
   Fila 12: activity_value = -500 → Cambiar a 500

❌ Unidad no soportada
   Fila 8: activity_unit = "galones" → Cambiar a "litres"
```

---

## 5. Calcular Emisiones

### 5.1 Cálculo Automático

Una vez cargados los datos válidos:

1. Pestaña "🔬 Cálculos"
2. Ver resumen automático:
   ```
   Total Emisiones: 45,892 kg CO2e (45.89 toneladas)
   
   Por Scope:
   - Scope 1: 12,340 kg CO2e (26.9%)
   - Scope 2: 28,150 kg CO2e (61.3%)
   - Scope 3:  5,402 kg CO2e (11.8%)
   ```

### 5.2 Entender el Cálculo

**Fórmula básica**:
```
Emisiones (kg CO2e) = Activity Data × Emission Factor
```

**Ejemplo**:
- **Activity Data**: 1,000 litros de diesel
- **Emission Factor**: 2.68 kg CO2e/litro (UK Gov 2025)
- **Resultado**: 1,000 × 2.68 = **2,680 kg CO2e**

### 5.3 GWP (Global Warming Potential)

Usamos valores de **IPCC AR5** para convertir todos los gases a CO2 equivalente:

| Gas | GWP AR5 | Significado |
|-----|---------|-------------|
| CO2 | 1 | Dióxido de carbono (referencia) |
| CH4 | 28 | Metano (28× más potente que CO2) |
| N2O | 265 | Óxido nitroso (265× más potente) |

**Ejemplo con mezcla de gases**:
```
1 kg CO2  = 1 kg CO2e
1 kg CH4  = 28 kg CO2e
1 kg N2O  = 265 kg CO2e
```

---

## 6. Interpretar Resultados

### 6.1 Pestaña "📊 Resumen"

**KPIs Principales**:
- **Total emisiones**: En kg CO2e y toneladas
- **Intensidad**: kg CO2e por empleado (si proporcionas # empleados)
- **Distribución por Scope**: % de cada Scope
- **Top 5 categorías**: Actividades con más emisiones

**Benchmarks**:
- Compara vs promedios sectoriales
- Verde = Por debajo del promedio ✅
- Amarillo = En promedio 🟡
- Rojo = Por encima del promedio ⚠️

### 6.2 Visualizaciones

#### 🌊 Diagrama Sankey
**¿Qué muestra?**
- Flujo de emisiones desde Scopes → Categorías → Subcategorías
- Ancho de líneas proporcional a emisiones
- Interactivo (hover para valores exactos)

**Cómo leer**:
- Línea gruesa = Fuente importante de emisiones
- Sigue el flujo para entender composición
- Identifica hotspots visuales

#### 🗺️ Treemap
**¿Qué muestra?**
- Jerarquía de emisiones en rectángulos
- Tamaño = Proporción de emisiones
- Color = Scope (1: rojo, 2: azul, 3: verde)

**Cómo leer**:
- Rectángulo grande = Categoría importante
- Click para drill-down
- Comparar tamaños relativos

#### 📈 Evolución Temporal
**¿Qué muestra?** (si tienes datos de múltiples meses/años)
- Tendencia de emisiones en el tiempo
- Por Scope o categoría
- Identificar estacionalidad o cambios

**Cómo leer**:
- Línea ascendente = Aumento de emisiones ⚠️
- Línea descendente = Reducción de emisiones ✅
- Picos = Meses/períodos atípicos

### 6.3 Tabla Detallada

En pestaña "📋 Detalles":
- **Todas las actividades** con su cálculo
- **Filtros** por Scope, categoría, entidad
- **Ordenar** por emisiones (mayor a menor)
- **Buscar** texto en descripciones

---

## 7. Generar Reportes

### 7.1 Tipos de Reporte

#### 📄 CSV Completo
- Todas las actividades calculadas
- Columnas: entity_id, scope, category, activity_value, unit, emissions_kgCO2e, factor_used, source
- **Uso**: Análisis en Excel, Power BI, Tableau

#### 📊 Excel Consolidado
- Múltiples hojas: Resumen, Por Scope, Por Categoría, Detalles
- Gráficos incluidos
- **Uso**: Presentaciones ejecutivas, reportes internos

#### 📈 PDF Ejecutivo (próximamente)
- Resumen visual de 1-2 páginas
- KPIs principales + gráficos
- **Uso**: Stakeholders, inversionistas

### 7.2 Generar Reporte

1. Pestaña "📥 Exportar"
2. Seleccionar formato (CSV o Excel)
3. Click "Generar Reporte"
4. Archivo descargado a carpeta `reports/`
5. Nombre automático: `carbon_footprint_YYYYMMDD_HHMMSS.{ext}`

**Ejemplo**:
```
reports/carbon_footprint_20251008_143052.xlsx
```

---

## 8. Usar IA

### 8.1 Categorización Automática

**¿Para qué?**
- Tienes descripciones en lenguaje natural
- No sabes la categoría GHG exacta
- Ahorrar tiempo en clasificación manual

**Cómo usar**:
1. Pestaña "🤖 Asistente IA"
2. Sección "Categorización Automática"
3. Escribe descripción: "Consumo de diesel en camiones de reparto"
4. Click "Categorizar"
5. Resultado:
   ```
   ✅ Scope: 1
   📂 Categoría: mobile_combustion
   ⚡ Subcategoría: diesel
   🎯 Confianza: 92%
   💡 Explicación: El diesel usado en vehículos propios (camiones de reparto) 
      son emisiones directas de fuentes móviles que controlas.
   ```

**Precisión**: 85-90% (validado con 100+ casos de prueba)

### 8.2 Búsqueda Semántica de Factores

**¿Para qué?**
- Encontrar el factor de emisión correcto entre 521 opciones
- Buscar en lenguaje natural (español o inglés)

**Cómo usar**:
1. Pestaña "🤖 Asistente IA"
2. Sección "Búsqueda de Factores"
3. Escribe: "transporte marítimo de contenedores"
4. Ver resultados ordenados por relevancia:
   ```
   🔍 Top 3 Factores:
   
   1. ⭐ 95% relevancia
      Sea freight - Container ship
      0.01113 kg CO2e/tonne.km
      
   2. ⭐ 88% relevancia
      Freight flights - Cargo
      1.58 kg CO2e/tonne.km
      
   3. ⭐ 75% relevancia
      Heavy Goods Vehicle (diesel) - 40+ tonnes
      0.62 kg CO2e/km
   ```

### 8.3 Recomendaciones Inteligentes

**¿Para qué?**
- Identificar oportunidades de reducción
- Priorizar acciones de mitigación
- Comparar con benchmarks

**Cómo usar**:
1. Pestaña "🤖 Recomendaciones"
2. Proporcionar:
   - Sector de tu empresa (ej: servicios, manufactura)
   - Número de empleados (opcional)
3. Ver recomendaciones priorizadas:

**Ejemplo de recomendación**:
```
🎯 PRIORIDAD 1: Transición a Energía Renovable

📂 Categoría: Scope 2 - Electricidad comprada
📊 Impacto: Alto (61.3% de tus emisiones)
⚙️ Dificultad: Media
📉 Reducción estimada: 40-60%

Acciones específicas:
1. Contratar PPA (Power Purchase Agreement) con renovables
2. Instalar paneles solares en techos (ROI: 5-7 años)
3. Comprar certificados de energía renovable (RECs)

⏱️ Plazo: Mediano (6-18 meses)
💰 Costo: $$ (inversión media)

💡 Beneficio adicional: Mejora en ratings ESG
```

---

## 9. Análisis Temporal

### 9.1 Requisitos

Para análisis temporal necesitas:
- Datos de al menos 2 períodos (meses o años)
- Columnas `year` y/o `month` completadas

### 9.2 Ver Tendencias

1. Pestaña "📈 Tendencias"
2. Seleccionar:
   - Granularidad: Mensual o Anual
   - Scope a visualizar: Todos, 1, 2 o 3
   - Categoría (opcional): mobile_combustion, purchased_electricity, etc.

3. Ver gráfico de línea temporal

### 9.3 Interpretación

**Ejemplo de análisis**:
```
Emisiones Scope 2 (Electricidad)
Enero 2024: 28,500 kg CO2e
Junio 2024:  24,200 kg CO2e (-15%)
Diciembre 2024: 22,100 kg CO2e (-22% vs Enero)

✅ Conclusión: Reducción sostenida, probablemente por:
   - Instalación de paneles solares (Mayo 2024)
   - Cambio a PPA renovable (Agosto 2024)
   - Eficiencia energética en equipos
```

### 9.4 Identificar Estacionalidad

**Patrón típico manufactura**:
- Verano (Jun-Ago): Mayor electricidad (aire acondicionado)
- Invierno (Dic-Feb): Mayor gas natural (calefacción)

**Acción**:
- Ajustar metas de reducción considerando estacionalidad
- Comparar año contra año (YoY) no mes a mes

---

## 10. FAQ

### P1: ¿Cuántas actividades puedo cargar?
**R**: Hasta 10,000 actividades en un solo archivo. Para más, contacta soporte.

### P2: ¿Qué hago si mi país no está en la lista?
**R**: Usa el código más cercano geográficamente. Los factores UK Gov son aplicables globalmente con ajustes menores.

### P3: ¿Puedo usar factores personalizados?
**R**: Sí (próximamente). Versión 1.1 permitirá subir factores propios o regionales.

### P4: ¿Los datos se guardan en la nube?
**R**: No. Todo se procesa localmente en tu computadora. Tus datos son 100% privados.

### P5: ¿Necesito internet para usar la IA?
**R**: No si usas Ollama local. Sí si usas API de OpenAI (próximamente).

### P6: ¿Cómo actualizo los factores de emisión?
**R**: UK Gov publica actualizaciones anuales (junio). Descarga nueva versión del Excel en `data/`.

### P7: ¿Puedo calcular Scope 3 completo?
**R**: Sí para categorías con factores disponibles. Scope 3 categorías 10-15 requieren datos específicos de productos.

### P8: ¿Es compatible con ISO 14064?
**R**: Sí. GHG Protocol es el estándar base de ISO 14064-1:2018.

### P9: ¿Puedo exportar para CDP o GRI?
**R**: Los reportes Excel tienen el formato base. Deberás agregar contexto narrativo según template CDP/GRI.

### P10: ¿Hay límite de usuarios?
**R**: No. Open source, uso ilimitado, sin costos de licencia.

---

## 📞 Soporte y Recursos

### Documentación Adicional:
- **GUIA_PLANTILLA_EXCEL.md**: Guía detallada de la plantilla
- **PLANTILLA_VISUAL.md**: Visualización de la plantilla
- **INICIO_RAPIDO_PLANTILLA.md**: Quick start en 3 pasos
- **DOCKER_GUIDE.md**: Guía de instalación con Docker
- **API.md**: Referencia para desarrolladores
- **CONTRIBUTING.md**: Guía para contribuir

### Comunidad:
- GitHub Issues: reportar bugs o sugerir features
- Discussions: preguntas y respuestas
- Examples: casos de uso reales

### Actualizaciones:
- Factores UK Gov: Junio de cada año
- Software: releases trimestrales
- Documentación: continua

---

## 🎯 Ejemplo Completo: Empresa de Servicios

### Escenario:
- **Empresa**: Consultoría con 50 empleados
- **Oficinas**: 1 edificio (no propio)
- **Transporte**: 3 vehículos de empresa + viajes aéreos

### Paso 1: Preparar datos en Excel

Abrir `data/PLANTILLA_HUELLA_CARBONO.xlsx`, hoja "DATOS":

| entity_id | scope | category | subcategory | activity_value | activity_unit | geography | year | month | facility | description |
|-----------|-------|----------|-------------|----------------|---------------|-----------|------|-------|----------|-------------|
| OFFICE_HQ | 2 | purchased_electricity | | 65000 | kWh | GBR | 2024 | 12 | Oficina Central | Consumo eléctrico |
| FLEET_001 | 1 | mobile_combustion | diesel | 3500 | litres | GBR | 2024 | 12 | Flota | 3 vehículos diésel |
| TRAVEL_AIR | 3 | business_travel | flights_domestic | 45000 | passenger.km | GBR | 2024 | 12 | Viajes | Vuelos nacionales |
| WASTE_001 | 3 | waste_generated | recycling | 850 | kg | GBR | 2024 | 12 | Oficina Central | Residuos reciclados |

### Paso 2: Cargar en app

1. Guardar Excel como `consultoría_dic2024.xlsx`
2. Streamlit → Pestaña "📊 Datos"
3. Cargar archivo
4. Ver: "✅ 4 actividades cargadas"

### Paso 3: Calcular

Pestaña "🔬 Cálculos":
```
Total Emisiones: 24,456 kg CO2e (24.46 toneladas)

Por Scope:
- Scope 1:  9,380 kg CO2e (38.4%) - Flota diesel
- Scope 2: 13,801 kg CO2e (56.4%) - Electricidad
- Scope 3:  1,275 kg CO2e  (5.2%) - Viajes + residuos

Intensidad: 489 kg CO2e/empleado
Benchmark servicios: 2,500 kg CO2e/empleado
✅ Desempeño: 80% por debajo del promedio sectorial
```

### Paso 4: Ver recomendaciones

Pestaña "🤖 Recomendaciones":

**Top 3 Recomendaciones**:

1. **🎯 PRIORIDAD 1: Transición a Electricidad Renovable**
   - Impacto: Alto (56.4% emisiones)
   - Reducción: 13.8 ton CO2e (-56%)
   - Acción: Contratar PPA 100% renovable
   - Costo: $$ (premium ~10-20%)

2. **🎯 PRIORIDAD 2: Electrificar Flota**
   - Impacto: Alto (38.4% emisiones)
   - Reducción: 9.4 ton CO2e (-38%)
   - Acción: Cambiar a vehículos eléctricos
   - Costo: $$$ (inversión alta, ROI 6-8 años)

3. **🎯 PRIORIDAD 3: Optimizar Viajes**
   - Impacto: Bajo (5.2% emisiones)
   - Reducción: 0.6 ton CO2e (-50% de viajes)
   - Acción: Política de videollamadas primero
   - Costo: $ (casi gratis)

**Total reducción potencial**: 23.8 ton CO2e (97% de emisiones actuales)

### Paso 5: Exportar reporte

1. Pestaña "📥 Exportar"
2. Formato: Excel
3. Descargar: `reports/carbon_footprint_20241208.xlsx`
4. Listo para presentar a gerencia ✅

---

## 🌟 Mejores Prácticas

### ✅ DO:
- Usa la plantilla Excel (ahorra tiempo)
- Completa campos opcionales (geography, year, month) para análisis detallado
- Revisa recomendaciones de IA (identifica quick wins)
- Exporta reportes mensualmente (tracking temporal)
- Compara vs benchmarks sectoriales

### ❌ DON'T:
- No mezcles unidades (usa conversión automática)
- No dejes filas vacías en Excel (se ignoran)
- No uses categorías inventadas (solo las 23 oficiales GHG Protocol)
- No ignores validaciones (corrige errores antes de calcular)

---

**Versión**: 1.0  
**Última actualización**: Octubre 8, 2025  
**Feedback**: GitHub Issues o discussions  
**Licencia**: MIT - Uso libre ✨
