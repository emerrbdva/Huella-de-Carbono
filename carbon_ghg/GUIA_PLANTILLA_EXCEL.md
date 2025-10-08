# 📊 GUÍA DE USO - PLANTILLA EXCEL HUELLA DE CARBONO

## 🎯 Introducción

Este documento explica cómo utilizar la **PLANTILLA_HUELLA_CARBONO.xlsx** para cargar datos de actividades y calcular las emisiones de gases de efecto invernadero (GEI) según el **GHG Protocol**.

---

## 📁 Archivo Generado

**Ubicación**: `data/PLANTILLA_HUELLA_CARBONO.xlsx`

**Hojas incluidas**:
1. **INSTRUCCIONES** - Guía completa de uso
2. **DATOS** - Plantilla vacía para completar ✏️
3. **EJEMPLOS** - 5 ejemplos de actividades
4. **CATEGORÍAS** - Catálogo completo por Scope
5. **UNIDADES** - Unidades de medida soportadas
6. **PAÍSES** - Códigos ISO-3 principales

---

## 🚀 Inicio Rápido (3 pasos)

### 1. Abrir la plantilla
```
📂 carbon_ghg/data/PLANTILLA_HUELLA_CARBONO.xlsx
```

### 2. Completar la hoja "DATOS"
- Ver ejemplos en la hoja "EJEMPLOS"
- Consultar catálogos en hojas "CATEGORÍAS", "UNIDADES", "PAÍSES"

### 3. Cargar en la aplicación
```bash
streamlit run app/streamlit_app.py
```
Ir a la pestaña **"📊 Datos"** → **"Cargar CSV/Excel"**

---

## 📋 CAMPOS DE LA PLANTILLA

### ✅ Campos OBLIGATORIOS (*)

#### 1. `entity_id` *
**Descripción**: Identificador único de la entidad emisora

**Formato**: Texto alfanumérico

**Ejemplos**:
- `FACTORY001` - Fábrica principal
- `OFFICE_HQ` - Oficinas centrales
- `WAREHOUSE_NORTH` - Almacén norte
- `VEHICLE_FLEET` - Flota de vehículos
- `DATACENTER_01` - Centro de datos

**Recomendaciones**:
- Use nombres consistentes y descriptivos
- Evite caracteres especiales (solo letras, números, guiones)
- Mantenga una nomenclatura estándar en toda su organización

---

#### 2. `scope` *
**Descripción**: Alcance GHG Protocol (1, 2 o 3)

**Valores permitidos**: `1`, `2`, `3`

**Significado**:

| Scope | Tipo | Descripción | Ejemplos |
|-------|------|-------------|----------|
| **1** | Directo | Emisiones de fuentes controladas por la organización | Combustión de combustibles, vehículos propios, fugas de refrigerantes |
| **2** | Indirecto (Energía) | Emisiones por compra de energía | Electricidad, calor, vapor comprados |
| **3** | Indirecto (Cadena) | Otras emisiones indirectas en la cadena de valor | Viajes, residuos, transporte, productos/servicios |

**Ejemplo de uso**:
```
Actividad: Diesel en vehículos propios → scope = 1
Actividad: Electricidad comprada → scope = 2
Actividad: Viajes de negocios → scope = 3
```

---

#### 3. `category` *
**Descripción**: Categoría de emisión según el alcance

**Valores por Scope**:

##### 📍 SCOPE 1 (4 categorías)
- `stationary_combustion` - Combustión estacionaria (calderas, generadores)
- `mobile_combustion` - Combustión móvil (vehículos, maquinaria)
- `process_emissions` - Emisiones de procesos industriales
- `fugitive_emissions` - Emisiones fugitivas (fugas de refrigerantes)

##### ⚡ SCOPE 2 (4 categorías)
- `purchased_electricity` - Electricidad comprada
- `purchased_heat` - Calor comprado
- `purchased_steam` - Vapor comprado
- `purchased_cooling` - Refrigeración comprada

##### 🌐 SCOPE 3 (15 categorías)
- `purchased_goods_services` - Bienes y servicios adquiridos
- `capital_goods` - Bienes de capital
- `fuel_energy_activities` - Actividades relacionadas con energía
- `upstream_transportation` - Transporte y distribución (aguas arriba)
- `waste_generated` - Residuos generados
- `business_travel` - Viajes de negocios
- `employee_commuting` - Desplazamientos de empleados
- `upstream_leased_assets` - Activos arrendados (aguas arriba)
- `downstream_transportation` - Transporte y distribución (aguas abajo)
- `processing_sold_products` - Procesamiento de productos vendidos
- `use_sold_products` - Uso de productos vendidos
- `end_of_life_sold_products` - Fin de vida de productos vendidos
- `downstream_leased_assets` - Activos arrendados (aguas abajo)
- `franchises` - Franquicias
- `investments` - Inversiones

**Validación**: La categoría debe ser compatible con el Scope indicado.

---

#### 4. `activity_value` *
**Descripción**: Valor numérico de la actividad

**Formato**: Número positivo (puede incluir decimales)

**Ejemplos**:
- `1000` - Mil litros
- `50000.5` - Cincuenta mil quinientos kWh
- `2.5` - Dos toneladas y media

**Validaciones**:
- ✅ Debe ser un número
- ✅ Debe ser mayor que 0
- ❌ No se permiten valores negativos
- ❌ No se permite texto

---

#### 5. `activity_unit` *
**Descripción**: Unidad de medida de la actividad

**Unidades más comunes**:

| Categoría | Unidades | Uso típico |
|-----------|----------|------------|
| **Combustibles líquidos** | `litres` | Diesel, gasolina, fuel oil |
| **Combustibles gaseosos** | `m³` | Gas natural |
| **Electricidad** | `kWh`, `MWh` | Consumo eléctrico |
| **Masa** | `kg`, `tonnes` | Residuos, refrigerantes |
| **Distancia** | `km` | Viajes, transporte |
| **Transporte pasajeros** | `passenger.km` | Vuelos, trenes |
| **Transporte carga** | `tonne.km` | Flete, logística |
| **Monetarias** | `USD`, `EUR`, `GBP` | Bienes/servicios adquiridos |

**Validación**: Debe coincidir con las unidades disponibles en los factores de emisión.

---

### 🔶 Campos OPCIONALES

#### 6. `subcategory`
**Descripción**: Subcategoría para mayor detalle

**Ejemplos**:
- Scope 1, mobile_combustion → `diesel`, `petrol`, `cng`
- Scope 1, stationary_combustion → `natural_gas`, `lpg`, `coal`
- Scope 3, business_travel → `flights`, `rental_cars`, `taxis`
- Scope 3, waste_generated → `landfill`, `recycling`, `incineration`

**Uso**: Permite mayor granularidad en el análisis de resultados.

---

#### 7. `geography`
**Descripción**: Código ISO-3 del país donde ocurre la actividad

**Formato**: Código de 3 letras (mayúsculas)

**Códigos principales**:
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

**Uso**: Los factores de emisión pueden variar por país (especialmente electricidad).

---

#### 8. `year`
**Descripción**: Año de la actividad

**Formato**: Número de 4 dígitos

**Rango válido**: 1990 - 2100

**Ejemplo**: `2025`, `2024`, `2023`

**Uso**: Permite análisis temporal y comparación entre años.

---

#### 9. `month`
**Descripción**: Mes de la actividad

**Formato**: Número del 1 al 12

**Ejemplo**: `1` (enero), `6` (junio), `12` (diciembre)

**Uso**: Análisis de estacionalidad y tendencias mensuales.

---

#### 10. `facility`
**Descripción**: Nombre de la instalación o sitio

**Formato**: Texto libre

**Ejemplos**:
- `Plant_North`
- `Headquarters_Madrid`
- `Warehouse_London`
- `Factory_Shanghai`

**Uso**: Comparación entre instalaciones, análisis por sitio.

---

#### 11. `description`
**Descripción**: Descripción adicional de la actividad

**Formato**: Texto libre

**Ejemplos**:
- `Diesel para vehículos de la flota corporativa`
- `Consumo eléctrico mensual de oficinas`
- `Vuelos internacionales del equipo ejecutivo`
- `Gas natural para calefacción del edificio`

**Uso**: Trazabilidad, auditoría, documentación.

---

## 💡 EJEMPLOS COMPLETOS

### Ejemplo 1: Vehículos de la empresa (Scope 1)
```
entity_id: FACTORY001
scope: 1
category: mobile_combustion
subcategory: diesel
activity_value: 1000
activity_unit: litres
geography: GBR
year: 2025
month: 1
facility: Plant_North
description: Diesel para vehículos de la flota corporativa
```

**Resultado esperado**: ~2,680 kg CO2e (usando factor UK 2.68 kg CO2e/litre)

---

### Ejemplo 2: Consumo eléctrico (Scope 2)
```
entity_id: FACTORY001
scope: 2
category: purchased_electricity
subcategory: 
activity_value: 50000
activity_unit: kWh
geography: GBR
year: 2025
month: 1
facility: Plant_North
description: Consumo eléctrico mensual de planta de producción
```

**Resultado esperado**: ~10,617 kg CO2e (usando factor UK ~0.21233 kg CO2e/kWh)

---

### Ejemplo 3: Viajes de negocios (Scope 3)
```
entity_id: OFFICE_HQ
scope: 3
category: business_travel
subcategory: flights
activity_value: 8500
activity_unit: km
geography: USA
year: 2025
month: 1
facility: Headquarters
description: Vuelos corporativos del personal ejecutivo
```

---

### Ejemplo 4: Calefacción con gas natural (Scope 1)
```
entity_id: WAREHOUSE_A
scope: 1
category: stationary_combustion
subcategory: natural_gas
activity_value: 5000
activity_unit: m³
geography: ESP
year: 2025
month: 1
facility: Warehouse_Madrid
description: Gas natural para calefacción del almacén
```

---

### Ejemplo 5: Residuos generados (Scope 3)
```
entity_id: WAREHOUSE_A
scope: 3
category: waste_generated
subcategory: landfill
activity_value: 2500
activity_unit: kg
geography: ESP
year: 2025
month: 1
facility: Warehouse_Madrid
description: Residuos industriales enviados a vertedero
```

---

## ✅ VALIDACIONES AUTOMÁTICAS

El sistema realiza las siguientes validaciones al cargar el archivo:

### 1. Validación de Scope
- ✅ Scope debe ser 1, 2 o 3
- ❌ Scope 4 o 0 → Error

### 2. Validación de Categoría
- ✅ Categorías Scope 1 solo con Scope 1
- ✅ Categorías Scope 2 solo con Scope 2
- ✅ Categorías Scope 3 solo con Scope 3
- ❌ Mezclar categorías → Error

### 3. Validación de Valores
- ✅ activity_value > 0
- ❌ Valores negativos o cero → Error
- ❌ Texto en lugar de número → Error

### 4. Validación de Unidades
- ✅ Unidades compatibles con factores de emisión
- ⚠️ Unidades no estándar → Advertencia (el sistema intentará convertir)

### 5. Validación de Fechas
- ✅ year entre 1990-2100
- ✅ month entre 1-12
- ❌ Valores fuera de rango → Error

---

## 🔄 PROCESO DE CARGA

### Paso 1: Preparar datos
1. Abrir `PLANTILLA_HUELLA_CARBONO.xlsx`
2. Ir a la hoja **"DATOS"**
3. Completar las filas con sus actividades (empezar en fila 3, después de las descripciones)

### Paso 2: Guardar archivo
- **Formato recomendado**: `.xlsx` (Excel)
- **Formato alternativo**: `.csv` (CSV UTF-8)
- **Ubicación**: Cualquiera (lo seleccionará en la app)

### Paso 3: Cargar en aplicación
1. Ejecutar: `streamlit run app/streamlit_app.py`
2. Ir a pestaña **"📊 Datos"**
3. Clic en **"Browse files"** o arrastrar archivo
4. El sistema validará y procesará automáticamente

### Paso 4: Usar IA (opcional)
Si algunas actividades no tienen `category` asignada:
- El sistema puede **categorizarlas automáticamente** con IA
- Usar la descripción en lenguaje natural
- Precisión: 85-90%

### Paso 5: Ver resultados
- Pestaña **"📈 Resultados"**: Cálculos y totales
- Pestaña **"📊 Visualización"**: Gráficos interactivos
- Pestaña **"🔍 Análisis"**: Recomendaciones de reducción

---

## 🎯 MEJORES PRÁCTICAS

### 1. Nomenclatura consistente
```
✅ BUENO: FACTORY_01, FACTORY_02, FACTORY_03
❌ MALO: Fábrica 1, factory-2, PLANT3
```

### 2. Granularidad adecuada
```
✅ BUENO: Separar por tipo de combustible, instalación, mes
❌ MALO: Un solo registro "Toda la empresa, todo el año"
```

### 3. Documentación completa
```
✅ BUENO: Usar descripción para detalles importantes
❌ MALO: Dejar descripción vacía
```

### 4. Datos verificables
```
✅ BUENO: Datos basados en facturas, medidores, registros
❌ MALO: Estimaciones sin respaldo
```

### 5. Actualización periódica
```
✅ BUENO: Cargar datos mensuales de forma consistente
❌ MALO: Cargar todo al final del año sin trazabilidad
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "Scope inválido"
**Causa**: Scope no es 1, 2 o 3  
**Solución**: Verificar que la columna `scope` tenga solo los valores 1, 2 o 3

### Error: "Categoría incompatible con Scope"
**Causa**: Categoría Scope 1 con Scope 2, etc.  
**Solución**: Consultar hoja "CATEGORÍAS" para ver categorías válidas por Scope

### Error: "Valor de actividad inválido"
**Causa**: Texto o número negativo en `activity_value`  
**Solución**: Asegurar que sea un número positivo

### Advertencia: "Unidad no reconocida"
**Causa**: Unidad no estándar en `activity_unit`  
**Solución**: Consultar hoja "UNIDADES" para unidades soportadas

### Error: "No se encontró factor de emisión"
**Causa**: Combinación de categoría/unidad sin factor disponible  
**Solución**: 
- Usar búsqueda semántica en la app
- Cambiar unidad a una más estándar
- Consultar catálogo de factores UK Gov 2025

---

## 📊 CAPACIDADES DE LA PLANTILLA

### Escala
- ✅ **Actividades por archivo**: Hasta 10,000 recomendadas
- ✅ **Tamaño de archivo**: Hasta 10 MB
- ✅ **Número de instalaciones**: Ilimitado

### Flexibilidad
- ✅ Múltiples entidades en un solo archivo
- ✅ Múltiples períodos (meses/años)
- ✅ Múltiples geografías
- ✅ Todos los Scopes simultáneamente

### Integración
- ✅ Compatible con Excel, Google Sheets, LibreOffice
- ✅ Exportable a CSV para otros sistemas
- ✅ Importable desde sistemas ERP/contabilidad

---

## 🚀 PRÓXIMOS PASOS

1. ✅ **Completar plantilla** con datos de su organización
2. ✅ **Cargar en la app** Streamlit
3. ✅ **Revisar cálculos** automáticos
4. ✅ **Obtener recomendaciones** de IA para reducción
5. ✅ **Exportar reportes** CSV/Excel
6. ✅ **Monitorear progreso** mes a mes

---

## 📞 SOPORTE

### Documentación
- `README_COMPLETE.md` - Guía completa del proyecto
- `DOCKER_GUIDE.md` - Despliegue con Docker
- `GUIA_ASISTENTE_IA.md` - Features de IA
- `CONTRIBUTING.md` - Contribuir al proyecto

### Archivos de ejemplo
- `data/sample_activities.csv` - 24 actividades de ejemplo
- Hoja "EJEMPLOS" de la plantilla - 5 casos de uso

### Catálogos de referencia
- Hoja "CATEGORÍAS" - 23 categorías totales
- Hoja "UNIDADES" - 12 unidades principales
- Hoja "PAÍSES" - 12 códigos ISO-3

---

## 📈 MÉTRICAS DE USO

Una vez cargados los datos, obtendrá:

✅ **Cálculos automáticos**:
- Emisiones totales por Scope (kg CO2e y toneladas)
- Desglose por categoría
- Distribución por instalación
- Evolución temporal

✅ **Visualizaciones**:
- Gráfico de barras por Scope
- Distribución de categorías
- Tendencias temporales
- Comparación entre instalaciones

✅ **Recomendaciones de IA**:
- 9 patrones de reducción identificados
- Priorización por impacto
- Estimación de % reducción potencial
- Pasos de acción concretos

✅ **Reportes exportables**:
- CSV con resultados detallados
- Resumen ejecutivo en Markdown
- Datos listos para auditoría

---

**¡Listo para medir su huella de carbono!** 🌍💚

*Versión 1.0.0 | Fecha: Octubre 2025 | GHG Protocol Compliant*
