# 🚀 CÓMO USAR LA PLANTILLA EXCEL - 3 PASOS

## ✨ NUEVA FUNCIONALIDAD AGREGADA

Ahora puedes cargar tus datos de huella de carbono usando una **plantilla Excel profesional** con guías integradas.

---

## 📋 PASO 1: ABRIR LA PLANTILLA

### Ubicación:
```
📂 carbon_ghg/data/PLANTILLA_HUELLA_CARBONO.xlsx
```

### Doble clic para abrir en:
- ✅ Microsoft Excel
- ✅ Google Sheets (subir archivo)
- ✅ LibreOffice Calc
- ✅ Apple Numbers

---

## 📖 PASO 2: COMPLETAR LOS DATOS

### 2.1 Leer las instrucciones
- Ir a hoja **"INSTRUCCIONES"**
- Leer guía completa (5 minutos)

### 2.2 Ver ejemplos
- Ir a hoja **"EJEMPLOS"**
- Ver 5 actividades completas
- Copiar estructura para tus datos

### 2.3 Consultar catálogos
- Hoja **"CATEGORÍAS"**: 23 categorías por Scope
- Hoja **"UNIDADES"**: 12 unidades soportadas
- Hoja **"PAÍSES"**: Códigos ISO-3

### 2.4 Completar tus datos
- Ir a hoja **"DATOS"**
- **Empezar en FILA 3** (después de headers y descripciones)
- Completar campos obligatorios (*):

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **entity_id*** | ID de la entidad | FACTORY001 |
| **scope*** | Alcance (1, 2 o 3) | 1 |
| **category*** | Ver hoja CATEGORÍAS | mobile_combustion |
| **activity_value*** | Número positivo | 1000 |
| **activity_unit*** | Ver hoja UNIDADES | litres |

**Opcional**: subcategory, geography, year, month, facility, description

### Ejemplo de fila completa:
```
FACTORY001 | 1 | mobile_combustion | diesel | 1000 | litres | GBR | 2025 | 1 | Plant_Main | Diesel para flota
```

---

## 🚀 PASO 3: CARGAR EN LA APLICACIÓN

### 3.1 Guardar archivo
```
💾 Archivo → Guardar como
📁 Ubicación: Tus documentos
📋 Nombre: mis_actividades_2025.xlsx
```

### 3.2 Iniciar aplicación
```powershell
# Terminal
cd "c:\Python\Huella de Carbono\carbon_ghg"
streamlit run app/streamlit_app.py
```

### 3.3 Cargar archivo
1. Abrir navegador: http://localhost:8501
2. Ir a Tab **"📊 Datos"**
3. Sección **"Cargar CSV/Excel"**
4. Clic **"Browse files"**
5. Seleccionar: `mis_actividades_2025.xlsx`
6. ✅ El sistema valida automáticamente

### 3.4 Ver resultados
- ✅ Tab **"📈 Resultados"**: Cálculos por Scope
- ✅ Tab **"📊 Visualización"**: Gráficos interactivos
- ✅ Tab **"🔍 Análisis"**: Recomendaciones de IA
- ✅ Descargar reportes: CSV, Excel, Markdown

---

## 💡 EJEMPLO RÁPIDO

### Para calcular 1000 litros de diesel:

**En Excel (hoja DATOS, fila 3)**:
```
entity_id:      FLEET001
scope:          1
category:       mobile_combustion
activity_value: 1000
activity_unit:  litres
```

**Resultado en la app**:
```
Scope 1: 2,680 kg CO2e (2.68 toneladas)
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Si necesitas más ayuda:

### Guías disponibles:
- 📖 **GUIA_PLANTILLA_EXCEL.md** (guía completa, 650 líneas)
- 🎨 **PLANTILLA_VISUAL.md** (visualización detallada, 730 líneas)
- 📋 **data/README_PLANTILLA.md** (inicio rápido, 160 líneas)
- 📊 **Hoja "INSTRUCCIONES"** del Excel (45 filas integradas)

### Otros recursos:
- **README_COMPLETE.md**: Guía del proyecto completo
- **GUIA_ASISTENTE_IA.md**: Features de IA
- **examples/usage_example.py**: Código de ejemplo

---

## ✅ VALIDACIONES AUTOMÁTICAS

Al cargar el archivo, el sistema verifica:

✅ Campos obligatorios presentes  
✅ Scope es 1, 2 o 3  
✅ Categoría compatible con Scope  
✅ Valores numéricos positivos  
✅ Unidades reconocidas  

**Si hay errores**: El sistema te indicará qué corregir

---

## 🔧 REGENERAR PLANTILLA

Si necesitas una plantilla nueva:

```bash
cd "c:\Python\Huella de Carbono\carbon_ghg"
python create_template_excel.py
```

Genera automáticamente:
- ✅ 6 hojas con contenido
- ✅ Formato profesional con colores
- ✅ Ejemplos y catálogos
- ✅ Headers congelados

---

## 🎯 RESUMEN VISUAL

```
┌─────────────────────────────────────────┐
│  1. ABRIR PLANTILLA                     │
│     📂 data/PLANTILLA_HUELLA_CARBONO... │
│                                         │
│  2. COMPLETAR DATOS                     │
│     📝 Hoja "DATOS" fila 3+             │
│     ✏️ Campos obligatorios (*)          │
│                                         │
│  3. CARGAR EN APP                       │
│     🚀 streamlit run app/streamlit_app  │
│     📊 Tab "Datos" → Upload file        │
│                                         │
│  ✅ VER RESULTADOS                      │
│     📈 Cálculos automáticos             │
│     📊 Visualizaciones                  │
│     💡 Recomendaciones IA               │
└─────────────────────────────────────────┘
```

---

## ⚡ TIEMPO ESTIMADO

```
Primera vez (con lectura):
├── Leer instrucciones:    5 min
├── Ver ejemplos:          2 min
├── Completar 10 activs:  10 min
├── Cargar en app:         2 min
└── TOTAL:                19 min

Usos siguientes:
├── Completar 10 activs:   5 min
├── Cargar en app:         1 min
└── TOTAL:                 6 min
```

---

## 🌟 CARACTERÍSTICAS

✅ **6 hojas**: Instrucciones, Datos, Ejemplos, Categorías, Unidades, Países  
✅ **11 columnas**: 5 obligatorias, 6 opcionales  
✅ **23 categorías**: GHG Protocol completo  
✅ **Formato profesional**: Colores, bordes, headers congelados  
✅ **Validación automática**: Al cargar en la app  
✅ **Compatible**: Excel, Google Sheets, LibreOffice  

---

## 🎊 ¡LISTO!

Ya puedes empezar a medir tu huella de carbono de forma profesional.

**Próximo paso**:
```
📂 Abrir: data/PLANTILLA_HUELLA_CARBONO.xlsx
```

---

**¿Preguntas?** Ver `GUIA_PLANTILLA_EXCEL.md` para guía completa.

**¡Tu huella de carbono en minutos, no semanas!** 🌍💚

*Versión 1.0.0 | Octubre 2025 | GHG Protocol Compliant*
