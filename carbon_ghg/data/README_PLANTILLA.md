# 📊 PLANTILLA EXCEL - INICIO RÁPIDO

## ✅ Archivo Generado

**📁 Ubicación**: `data/PLANTILLA_HUELLA_CARBONO.xlsx`  
**📏 Tamaño**: ~12 KB  
**📅 Fecha**: Octubre 2025

---

## 🚀 INICIO RÁPIDO (3 PASOS)

### 1️⃣ Abrir la plantilla Excel
```
📂 carbon_ghg/data/PLANTILLA_HUELLA_CARBONO.xlsx
```

### 2️⃣ Completar la hoja "DATOS"
- **Fila 1**: Headers (no modificar)
- **Fila 2**: Descripciones (no modificar)
- **Fila 3+**: TUS DATOS AQUÍ ✏️

**Campos obligatorios** (columnas con *):
- `entity_id` - ID de la entidad (ej: FACTORY001)
- `scope` - Alcance GHG: 1, 2 o 3
- `category` - Ver hoja "CATEGORÍAS"
- `activity_value` - Número positivo
- `activity_unit` - Ver hoja "UNIDADES"

**Campos opcionales**:
- `subcategory`, `geography`, `year`, `month`, `facility`, `description`

### 3️⃣ Cargar en la aplicación
```bash
# Iniciar aplicación
streamlit run app/streamlit_app.py

# En el navegador:
# 1. Ir a pestaña "📊 Datos"
# 2. Cargar archivo Excel
# 3. Ver resultados automáticos
```

---

## 📚 HOJAS INCLUIDAS

### 🔷 INSTRUCCIONES
Guía completa de uso con:
- Descripción de todos los campos
- Alcances GHG Protocol
- Validaciones automáticas
- Proceso de carga paso a paso

### 🔶 DATOS (✏️ COMPLETAR AQUÍ)
Plantilla vacía con:
- 11 columnas (5 obligatorias, 6 opcionales)
- Fila 1: Nombres de columnas
- Fila 2: Descripciones de cada campo
- Fila 3+: Para tus actividades

### 🔷 EJEMPLOS
5 actividades de ejemplo:
1. Diesel vehículos (Scope 1)
2. Electricidad (Scope 2)
3. Viajes de negocios (Scope 3)
4. Gas natural calefacción (Scope 1)
5. Residuos (Scope 3)

### 🔶 CATEGORÍAS
Catálogo completo:
- **Scope 1**: 4 categorías
- **Scope 2**: 4 categorías
- **Scope 3**: 15 categorías
- **Total**: 23 categorías

### 🔷 UNIDADES
12 unidades soportadas:
- Combustibles: `litres`, `m³`
- Electricidad: `kWh`, `MWh`
- Masa: `kg`, `tonnes`
- Distancia: `km`, `passenger.km`, `tonne.km`
- Monetarias: `USD`, `EUR`, `GBP`

### 🔶 PAÍSES
Códigos ISO-3 principales:
- `GBR` - Reino Unido
- `USA` - Estados Unidos
- `ESP` - España
- `FRA` - Francia
- Y 8 más...

---

## 💡 EJEMPLO MÍNIMO

Para calcular emisiones de **1000 litros de diesel**:

| entity_id | scope | category | activity_value | activity_unit |
|-----------|-------|----------|----------------|---------------|
| FLEET001 | 1 | mobile_combustion | 1000 | litres |

**Resultado esperado**: ~2,680 kg CO2e

---

## 🎯 ALCANCES GHG PROTOCOL

| Scope | Tipo | Ejemplos |
|-------|------|----------|
| **1** | Emisiones DIRECTAS | Combustibles, vehículos propios, fugas |
| **2** | Energía COMPRADA | Electricidad, calor, vapor |
| **3** | CADENA DE VALOR | Viajes, residuos, transporte, productos |

---

## ✅ VALIDACIONES

El sistema valida automáticamente:
- ✓ Scope 1, 2 o 3
- ✓ Categoría compatible con el Scope
- ✓ Valores numéricos positivos
- ✓ Unidades compatibles con factores de emisión
- ✓ Fechas en rango válido

---

## 🔧 REGENERAR PLANTILLA

Si necesitas regenerar el archivo:

```bash
cd "c:\Python\Huella de Carbono\carbon_ghg"
python create_template_excel.py
```

El script genera:
- 6 hojas con formato profesional
- Colores y estilos aplicados
- Congelación de encabezados
- Anchos de columna optimizados

---

## 📖 DOCUMENTACIÓN COMPLETA

Para información detallada:
- **`GUIA_PLANTILLA_EXCEL.md`** - Guía completa (1,000+ líneas)
- **`README_COMPLETE.md`** - Documentación del proyecto
- **Hoja "INSTRUCCIONES"** del Excel

---

## 🎊 CARACTERÍSTICAS

✅ **Fácil de usar**: Solo llenar y cargar  
✅ **Validación automática**: Detecta errores al cargar  
✅ **Inteligente**: IA puede categorizar actividades  
✅ **Completo**: Todos los Scopes GHG Protocol  
✅ **Profesional**: Formato y colores aplicados  
✅ **Multiidioma**: Soporte español/inglés  

---

## 📊 CAPACIDAD

- **Actividades**: Hasta 10,000 por archivo
- **Tamaño**: Máximo recomendado 10 MB
- **Entidades**: Ilimitadas en un solo archivo
- **Períodos**: Múltiples meses/años simultáneos

---

## 🚀 PRÓXIMO PASO

1. ✅ **Abrir** `PLANTILLA_HUELLA_CARBONO.xlsx`
2. ✅ **Ver ejemplos** en hoja "EJEMPLOS"
3. ✅ **Completar** hoja "DATOS" con tus actividades
4. ✅ **Guardar** archivo
5. ✅ **Cargar** en la aplicación Streamlit
6. ✅ **Obtener** cálculos y recomendaciones automáticas

---

**¡Tu huella de carbono en minutos, no semanas!** 🌍💚

*GHG Protocol Compliant | UK Gov DEFRA 2025 Factors | 521 Factores de Emisión*
