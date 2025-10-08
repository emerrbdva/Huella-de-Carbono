# 📦 INSTRUCCIONES DE INSTALACIÓN

## Sistema Completo de Cálculo de Huella de Carbono - GHG Protocol

---

## 🔧 Instalación Paso a Paso

### **Paso 1: Verificar Python**

Asegúrate de tener Python 3.9 o superior instalado:

```powershell
python --version
```

Si no tienes Python instalado, descárgalo de: https://www.python.org/downloads/

---

### **Paso 2: Crear Entorno Virtual (Recomendado)**

En PowerShell, desde la carpeta del proyecto:

```powershell
# Navegar a la carpeta del proyecto
cd "c:\Python\Huella de Carbono\carbon_ghg"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

**Nota**: Si hay error de ejecución de scripts, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### **Paso 3: Instalar Dependencias**

Con el entorno virtual activado:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará:
- ✅ pandas, numpy (procesamiento de datos)
- ✅ pydantic (validación)
- ✅ streamlit (interfaz web)
- ✅ plotly, matplotlib (visualizaciones)
- ✅ openpyxl, xlrd (Excel)
- ✅ python-docx, fpdf2 (reportes)
- ✅ jinja2, pyyaml (utilidades)
- ✅ pint (conversión de unidades)
- ✅ langchain* (IA local, opcional)

*langchain requiere Ollama instalado para funcionar

---

### **Paso 4: Verificar Instalación**

Ejecuta las pruebas básicas:

```powershell
python tests/test_basic.py
```

**Resultado esperado:**
```
============================================================
🧪 EJECUTANDO PRUEBAS DEL SISTEMA
============================================================

🧪 Probando modelos Pydantic...
✓ ActivityRecord creado: test_entity - Scope 1
✓ EmissionFactor creado: 2.68 kg CO2e / liter
✅ Modelos Pydantic: PASÓ

🧮 Probando cálculo de emisiones...
✓ Cálculo completado:
  - Actividad: 100 liters
  - Factor: 2.68 kg CO2e / liter
  - Emisión: 268.00 kg CO2e
  - Emisión: 0.2680 tCO2e
✅ Cálculo de Emisiones: PASÓ

[... más tests ...]

============================================================
📊 RESULTADOS: 6 pruebas pasaron, 0 fallaron
============================================================

🎉 ¡Todas las pruebas pasaron exitosamente!
```

---

### **Paso 5: Descargar Factores de Emisión**

Descarga el archivo de factores UK Government 2025:

**Opción A - Archivo Condensado (Recomendado para empezar):**
```
Ya incluido en: data/ghg-conversion-factors-2025-condensed-set.xlsx
```

**Opción B - Archivo Completo (Más completo):**
1. Visita: https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting
2. Descarga: "GHG conversion factors 2025 - full set"
3. Guarda en: `data/ghg-conversion-factors-2025-full-set.xlsx`

---

### **Paso 6: Ejecutar Aplicación**

Con el entorno virtual activado:

```powershell
streamlit run app/streamlit_app.py
```

La aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

---

## 🚀 Primer Uso

### 1. Cargar Factores de Emisión
- En la barra lateral, sección "Paso 1"
- Click en "Browse files"
- Selecciona `data/ghg-conversion-factors-2025-condensed-set.xlsx`
- Espera confirmación: "✅ XXX factores cargados"

### 2. Cargar Datos de Actividad
- Barra lateral, sección "Paso 2"
- Click en "Browse files"
- Selecciona `data/sample_activities.csv`
- Espera confirmación: "✅ 24 filas cargadas"

### 3. Validar Datos
- Ve a pestaña "🔍 Validación"
- Click en "🔍 Validar Datos"
- Revisa el reporte de calidad

### 4. Calcular Emisiones
- Ve a pestaña "🧮 Cálculo"
- Click en "🚀 Calcular Huella de Carbono"
- Espera el progreso de cálculo

### 5. Ver Resultados
- Ve a pestaña "📈 Resultados"
- Explora gráficos y tablas
- Descarga resultados

---

## 📁 Estructura de Archivos

```
carbon_ghg/
├── app/
│   └── streamlit_app.py          # Aplicación web principal
├── calculators/
│   ├── core.py                    # Motor de cálculo
│   ├── scope1.py                  # Scope 1 (directas)
│   └── scope2.py                  # Scope 2 (energía)
├── data/
│   ├── ghg-conversion-factors-2025-condensed-set.xlsx  # Factores UK Gov
│   └── sample_activities.csv      # Datos de ejemplo
├── models/
│   └── emissions.py               # Modelos de datos
├── utils/
│   ├── factors.py                 # Carga de factores
│   ├── unit_converter.py          # Conversión de unidades
│   └── data_validator.py          # Validación
├── tests/
│   └── test_basic.py              # Pruebas básicas
├── reports/                        # Reportes generados
├── venv/                          # Entorno virtual (creado)
├── config.py                      # Configuración
├── requirements.txt               # Dependencias
├── README.md                      # Documentación completa
├── QUICKSTART.md                  # Guía rápida
├── MEJORAS.md                     # Resumen de mejoras
└── INSTALL.md                     # Este archivo
```

---

## 🔧 Solución de Problemas

### Error: "streamlit: command not found"
**Causa**: Entorno virtual no activado o streamlit no instalado

**Solución**:
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Reinstalar streamlit
pip install streamlit
```

---

### Error: "No module named 'pandas'"
**Causa**: Dependencias no instaladas

**Solución**:
```powershell
pip install -r requirements.txt
```

---

### Error: "Permission denied" al activar entorno virtual
**Causa**: Política de ejecución de PowerShell

**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Error al cargar archivo Excel
**Causa**: Librería openpyxl no instalada

**Solución**:
```powershell
pip install openpyxl
```

---

### Warning de deprecación de pandas
**Causa**: Uso de método deprecated `fillna(method='ffill')`

**Solución**: Ya corregido en el código con `.ffill()`

---

## 🔄 Actualizar el Proyecto

Si ya tenías una versión anterior instalada:

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Verificar actualización
python tests/test_basic.py
```

---

## 🧹 Desinstalación

Para eliminar completamente el proyecto:

```powershell
# Desactivar entorno virtual
deactivate

# Eliminar carpeta del entorno virtual
Remove-Item -Recurse -Force venv

# (Opcional) Eliminar toda la carpeta del proyecto
Remove-Item -Recurse -Force "c:\Python\Huella de Carbono\carbon_ghg"
```

---

## 📚 Recursos Adicionales

### Documentación del Proyecto
- **README.md**: Documentación completa del sistema
- **QUICKSTART.md**: Guía de inicio rápido (5 minutos)
- **MEJORAS.md**: Resumen de mejoras implementadas
- **config.py**: Configuración y referencias

### Documentación Externa
- **Streamlit**: https://docs.streamlit.io/
- **Pydantic**: https://docs.pydantic.dev/
- **Pandas**: https://pandas.pydata.org/docs/
- **Plotly**: https://plotly.com/python/

### Referencias GHG Protocol
- **Corporate Standard**: https://ghgprotocol.org/corporate-standard
- **Scope 2 Guidance**: https://ghgprotocol.org/scope-2-guidance
- **Scope 3 Standard**: https://ghgprotocol.org/standards/scope-3-standard

### Factores de Emisión
- **UK Gov**: https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting
- **IPCC EFDB**: https://www.ipcc-nggip.iges.or.jp/EFDB/main.php
- **EPA Hub**: https://www.epa.gov/climateleadership/ghg-emission-factors-hub

---

## ✅ Checklist de Instalación

Marca cada paso a medida que lo completes:

- [ ] Python 3.9+ instalado y verificado
- [ ] Entorno virtual creado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Pruebas básicas ejecutadas (`python tests/test_basic.py`)
- [ ] Factores de emisión descargados
- [ ] Aplicación ejecutada (`streamlit run app/streamlit_app.py`)
- [ ] Datos de ejemplo cargados y calculados
- [ ] Resultados visualizados y descargados

---

## 🎯 Próximos Pasos

Una vez instalado:

1. **Lee la guía rápida**: `QUICKSTART.md`
2. **Experimenta con datos de ejemplo**: `data/sample_activities.csv`
3. **Prepara tus propios datos** siguiendo el formato
4. **Explora la documentación completa**: `README.md`
5. **Personaliza la configuración**: `config.py`

---

## 🆘 Soporte

Si tienes problemas:

1. Verifica que completaste todos los pasos del checklist
2. Lee la sección de solución de problemas arriba
3. Revisa los logs en la terminal
4. Ejecuta las pruebas: `python tests/test_basic.py`
5. Consulta la documentación: `README.md`

---

**¡Instalación completada! 🎉**

Ahora puedes comenzar a calcular tu huella de carbono de manera profesional siguiendo los estándares del GHG Protocol.

**Versión**: 1.0.0  
**Fecha**: Octubre 2025
