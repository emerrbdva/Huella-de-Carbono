# 📥 Guía de Descargas - Sistema de Huella de Carbono

## 🎯 Formatos de Descarga Disponibles

El sistema ofrece **4 formatos** de descarga de resultados:

### 1. 📊 **Excel (.xlsx)** - Reporte Completo Profesional

**Contenido:**
- **Hoja 1 - Resumen Ejecutivo:**
  - Header con formato profesional (azul oscuro)
  - Metadata (fecha, metodología, fuente de factores)
  - Total de emisiones destacado
  - Tabla de distribución por Scope con porcentajes
  - Formato con colores corporativos

- **Hoja 2 - Resultados Detallados:**
  - Todas las actividades calculadas
  - Columnas: Entidad, Scope, Categoría, Actividad, Unidad, Factor, Emisión
  - Headers con fondo azul y texto blanco
  - Columnas auto-ajustadas

- **Hoja 3 - Totales por Categoría:**
  - Ranking de categorías por emisión
  - Ordenado de mayor a menor
  - Formato tabla con headers

**Características:**
- ✅ Múltiples hojas organizadas
- ✅ Formato profesional con colores
- ✅ Listo para presentaciones
- ✅ Compatible con Excel 2010+

**Cómo usar:**
1. Ir a tab "Resultados"
2. Hacer scroll hasta "Descargar Resultados"
3. Click en botón "📊 Excel"
4. Se descarga: `reporte_YYYYMMDD_HHMMSS.xlsx`

---

### 2. 📝 **Word (.docx)** - Reporte APA 7 Profesional

**Contenido:**

**Portada:**
- Título centrado: "Reporte de Huella de Carbono"
- Subtítulo: "Cálculo de Emisiones de Gases de Efecto Invernadero"
- Metadata: Fecha, metodología, fuente de factores

**Resumen Ejecutivo:**
- Explicación de la metodología GHG Protocol
- Total de emisiones en texto narrativo
- Distribución por alcances

**Resultados Generales:**
- Tabla profesional con totales por Scope
- Columnas: Alcance | Emisiones (tCO₂e) | Porcentaje
- Total general destacado en negrita

**Metodología:**
- Ecuación fundamental: **E = AD × EF × GWP**
- Explicación de cada variable
- Referencia a IPCC AR5

**Referencias (Formato APA 7):**
- GHG Protocol Corporate Standard (WBCSD/WRI, 2004)
- UK Government Conversion Factors 2025
- IPCC AR5 (2014)

**Características:**
- ✅ Formato APA 7ª edición
- ✅ Listo para entregar como reporte oficial
- ✅ Compatible con Word 2010+
- ✅ Estructura académica/profesional

**Cómo usar:**
1. Ir a tab "Resultados"
2. Click en botón "📝 Word"
3. Se descarga: `reporte_APA7_YYYYMMDD.docx`

---

### 3. 📥 **CSV (.csv)** - Datos Crudos para Análisis

**Contenido:**
- Todos los resultados en formato tabla simple
- Columnas separadas por comas
- Compatible con Excel, Python, R, SPSS

**Columnas incluidas:**
```
Entidad, Scope, Categoría, Actividad_Valor, Actividad_Unidad,
Factor_Valor, Factor_Unidad, Emisión_kgCO2e, Emisión_tCO2e,
Fuente_Factor, Fórmula_Cálculo
```

**Características:**
- ✅ Formato universal
- ✅ Ideal para análisis estadístico
- ✅ Importable a cualquier software
- ✅ UTF-8 encoding

**Cómo usar:**
1. Ir a tab "Resultados"
2. Click en botón "📥 CSV"
3. Se descarga: `huella_carbono_YYYYMMDD_HHMMSS.csv`

---

### 4. 📄 **TXT (.txt)** - Resumen Ejecutivo Simple

**Contenido:**
```
RESUMEN EJECUTIVO - HUELLA DE CARBONO
Fecha: 2025-10-08 13:55:50
Metodología: GHG Protocol

TOTALES:
- Emisiones Totales: 513.09 tCO₂e
- Actividades Calculadas: 24

POR ALCANCE:
- Scope 1: 172.53 tCO₂e (33.6%)
- Scope 2: 285.00 tCO₂e (55.5%)
- Scope 3: 55.56 tCO₂e (10.8%)

Fuente de Factores: UK Gov 2025
```

**Características:**
- ✅ Formato simple y legible
- ✅ Ideal para emails rápidos
- ✅ Compatible con cualquier editor de texto
- ✅ Copiar/pegar fácil

**Cómo usar:**
1. Ir a tab "Resultados"
2. Click en botón "📄 TXT"
3. Se descarga: `resumen_YYYYMMDD.txt`

---

## 🔧 Instalación de Dependencias

Si algún botón está deshabilitado, instala las dependencias:

### Para Excel:
```bash
pip install openpyxl
```

### Para Word:
```bash
pip install python-docx
```

### Todas las dependencias:
```bash
cd "c:\Python\Huella de Carbono\carbon_ghg"
pip install -r requirements.txt
```

---

## 📊 Comparación de Formatos

| Formato | Uso Recomendado | Ventajas |
|---------|----------------|----------|
| **Excel** | Presentaciones ejecutivas | Múltiples hojas, formato profesional, gráficos |
| **Word** | Reportes oficiales | APA 7, referencias, texto narrativo |
| **CSV** | Análisis de datos | Compatible universal, fácil procesamiento |
| **TXT** | Resúmenes rápidos | Simple, ligero, fácil de compartir |

---

## 💡 Consejos de Uso

### Excel:
- ✅ Úsalo para presentar resultados a stakeholders
- ✅ Las hojas están listas para crear gráficos adicionales
- ✅ Puedes agregar tu logo en la hoja de resumen

### Word:
- ✅ Perfecto para cumplir con requisitos académicos/corporativos
- ✅ Las referencias están en formato APA 7
- ✅ Puedes agregar más secciones manteniendo el formato

### CSV:
- ✅ Importa a Python para análisis avanzados
- ✅ Usa en Excel para tablas dinámicas
- ✅ Combina con otros datos fácilmente

### TXT:
- ✅ Copia/pega en emails
- ✅ Incluye en documentos más grandes
- ✅ Versión rápida para revisiones

---

## 🚀 Flujo de Trabajo Recomendado

1. **Durante el análisis:** Usa CSV para procesar datos
2. **Para reportes internos:** Usa Excel con múltiples hojas
3. **Para reportes oficiales:** Usa Word en formato APA 7
4. **Para comunicaciones rápidas:** Usa TXT

---

## 🎨 Personalización

### Excel:
Los colores corporativos se pueden cambiar en `utils/report_generator.py`:
```python
# Cambiar colores del header
ws_summary['A1'].fill = PatternFill(
    start_color="1F4E78",  # <- Tu color corporativo aquí
    end_color="1F4E78",
    fill_type="solid"
)
```

### Word:
El formato APA 7 se puede extender agregando secciones en `generate_word_report()`.

---

## ❓ Solución de Problemas

### "Botón Excel/Word deshabilitado"
**Solución:** Instala las dependencias faltantes
```bash
pip install openpyxl python-docx
```

### "Error al generar reporte"
**Solución:** Verifica que los cálculos estén completos en el tab "Cálculo"

### "Archivo no se descarga"
**Solución:** 
- Verifica que tu navegador permita descargas
- Revisa la carpeta de descargas del navegador
- Intenta con otro navegador

---

## 📚 Referencias Técnicas

- **openpyxl:** Manipulación de archivos Excel (.xlsx)
- **python-docx:** Generación de documentos Word (.docx)
- **pandas:** Manejo de datos y exportación CSV
- **Streamlit:** Framework web y download buttons

---

¿Necesitas un formato adicional (PDF, JSON, HTML)? ¡Contáctanos!
