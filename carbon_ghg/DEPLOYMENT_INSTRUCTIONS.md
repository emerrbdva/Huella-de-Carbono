# 🚀 INSTRUCCIONES DE DEPLOYMENT - PASO A PASO

**Fecha**: 8 de octubre de 2025  
**Objetivo**: Desplegar Carbon GHG Calculator en Streamlit Cloud (GRATIS)  
**Tiempo total**: 15-20 minutos

---

## ✅ Estado Actual del Proyecto

- ✅ Git inicializado
- ✅ Primer commit creado (92 archivos, 32,761 líneas)
- ✅ Código 95% completo y production-ready
- ✅ Archivos de configuración listos (.streamlit/config.toml, .gitignore)
- ⏳ Pendiente: Subir a GitHub y desplegar

---

## 📝 PASO 1: Crear Repositorio en GitHub (5 min)

### 1.1 Ir a GitHub

Abre tu navegador y ve a: **https://github.com/new**

(Si no tienes cuenta, créala gratis en https://github.com/join)

### 1.2 Configurar el repositorio

Completa el formulario:

- **Repository name**: `carbon-ghg-calculator`
- **Description**: `🌱 Carbon Footprint Calculator - GHG Protocol Compliant (Scope 1, 2, 3)`
- **Visibility**: 
  - ✅ **Public** (requerido para Streamlit Cloud Free)
  - ❌ Private (requiere plan de pago)
- **Initialize this repository**:
  - ❌ NO marcar "Add a README file" (ya lo tenemos)
  - ❌ NO agregar .gitignore (ya lo tenemos)
  - ❌ NO elegir licencia (ya tenemos LICENSE)

### 1.3 Crear repositorio

Click en **"Create repository"** (botón verde)

Verás una página con instrucciones. **Copia la URL del repositorio**, se verá así:

```
https://github.com/TU-USUARIO/carbon-ghg-calculator.git
```

---

## 📤 PASO 2: Subir Código a GitHub (3 min)

### 2.1 Abrir PowerShell/Terminal

Ya deberías estar en: `c:\Python\Huella de Carbono\carbon_ghg`

Si no, ejecuta:

```powershell
cd "c:\Python\Huella de Carbono\carbon_ghg"
```

### 2.2 Configurar Git (solo primera vez)

```powershell
# Reemplaza con tu información
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 2.3 Conectar con GitHub

```powershell
# Reemplaza TU-USUARIO con tu username de GitHub
git remote add origin https://github.com/TU-USUARIO/carbon-ghg-calculator.git
```

### 2.4 Verificar la conexión

```powershell
git remote -v
```

Deberías ver:

```
origin  https://github.com/TU-USUARIO/carbon-ghg-calculator.git (fetch)
origin  https://github.com/TU-USUARIO/carbon-ghg-calculator.git (push)
```

### 2.5 Subir el código

```powershell
git branch -M main
git push -u origin main
```

Te pedirá autenticación:
- **Username**: Tu username de GitHub
- **Password**: Tu Personal Access Token (NO tu password de GitHub)

#### ¿Cómo crear un Personal Access Token?

Si no tienes token:

1. Ve a https://github.com/settings/tokens/new
2. **Note**: "Streamlit Deployment"
3. **Expiration**: 90 days (o No expiration)
4. **Scopes**: Marca ✅ `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **COPIA EL TOKEN** (solo se muestra una vez)
7. Úsalo como password en `git push`

### 2.6 Verificar en GitHub

Abre tu navegador en:

```
https://github.com/TU-USUARIO/carbon-ghg-calculator
```

Deberías ver todos tus archivos! 🎉

---

## 🚀 PASO 3: Desplegar en Streamlit Cloud (7 min)

### 3.1 Crear cuenta en Streamlit Cloud

1. Ve a **https://share.streamlit.io/**
2. Click en **"Sign up"**
3. Elige **"Continue with GitHub"** (más fácil)
4. Autoriza Streamlit a acceder a tus repositorios públicos

### 3.2 Crear nueva app

1. Click en **"New app"** (botón azul, arriba a la derecha)
2. Verás un formulario con 3 secciones:

#### Sección 1: Repository

- **Repository**: Selecciona `TU-USUARIO/carbon-ghg-calculator`
- **Branch**: `main`
- **Main file path**: `app/streamlit_app.py`

#### Sección 2: App URL (opcional)

- **Customize app URL**: `carbon-ghg-calculator`
  
  Tu URL será: `https://carbon-ghg-calculator.streamlit.app`

#### Sección 3: Advanced settings (opcional)

Por ahora déjalo en default:
- Python version: 3.10 (auto-detectado)

### 3.3 Desplegar

Click en **"Deploy!"** (botón azul)

Verás un log en tiempo real:

```
🚀 Starting deployment...
📦 Installing system packages...
🐍 Installing Python 3.10...
📚 Installing dependencies from requirements.txt...
   ✓ pandas>=2.0.0
   ✓ streamlit>=1.28.0
   ✓ plotly>=5.17.0
   ✓ openpyxl>=3.1.0
   ✓ python-docx>=1.1.0
   ... (más dependencias)
🎉 App is running!
```

**Tiempo de deployment**: 3-5 minutos

### 3.4 ¡Listo! 🎊

Tu app está desplegada en:

```
https://carbon-ghg-calculator.streamlit.app
```

O la URL que elegiste. **¡Ábrela y pruébala!**

---

## 🧪 PASO 4: Verificar que Funciona (2 min)

### 4.1 Probar carga de datos

1. Abre la app en tu navegador
2. Descarga el archivo de ejemplo: `data/sample_activities.csv`
3. En la app, ve a la sección **"📤 Cargar Datos"**
4. Sube el archivo CSV

### 4.2 Verificar cálculos

Deberías ver:

- ✅ Dashboard con total de emisiones
- ✅ Sankey diagram
- ✅ Treemap
- ✅ Gráficos de barras
- ✅ Tabla detallada

### 4.3 Probar exportación

1. Scroll hasta **"📊 Exportar Reportes"**
2. Click en **"Generar Reporte Excel"**
3. Descarga el archivo .xlsx
4. Ábrelo en Excel

**Si todo funciona, ¡felicidades! 🎉**

---

## 🔄 PASO 5: Configurar Auto-Deploy (ya está listo!)

Cada vez que hagas cambios en el código:

```powershell
# 1. Hacer cambios en archivos
# 2. Commit
git add .
git commit -m "Descripción de cambios"

# 3. Push a GitHub
git push

# 4. Streamlit Cloud auto-detecta y re-deploya en 2-3 min
```

**No necesitas hacer nada más!** El CI/CD es automático.

---

## 📊 PASO 6: Monitorear la App

### Ver logs

1. Dashboard de Streamlit Cloud: https://share.streamlit.io/
2. Click en tu app
3. Click en **"⋮"** → **"Manage app"**
4. Tab **"Logs"**

### Ver analytics

1. En "Manage app", tab **"Analytics"**
2. Verás:
   - 👥 Visitantes únicos
   - 📊 Sesiones
   - 🌍 Países de origen
   - ⏱️ Tiempo de uso

---

## ✅ CHECKLIST FINAL

Antes de compartir tu app:

- [ ] ✅ App abre sin errores
- [ ] ✅ Puedes subir CSV de ejemplo
- [ ] ✅ Se calculan emisiones correctamente
- [ ] ✅ Visualizaciones se generan (Sankey, Treemap)
- [ ] ✅ Puedes exportar reportes Excel/Word
- [ ] ✅ No hay errores en logs de Streamlit Cloud
- [ ] ✅ README.md tiene link a la app desplegada

---

## 🎯 URLs Importantes

Guarda estos links:

- **Tu app desplegada**: https://carbon-ghg-calculator.streamlit.app
- **Repositorio GitHub**: https://github.com/TU-USUARIO/carbon-ghg-calculator
- **Dashboard Streamlit**: https://share.streamlit.io/
- **Documentación**: Ver carpeta `docs/` en GitHub

---

## 🐛 Troubleshooting Rápido

### ❌ "git push" falla con error de autenticación

**Solución**: Crear Personal Access Token

1. https://github.com/settings/tokens/new
2. Scopes: `repo`
3. Usar token como password

### ❌ App no inicia en Streamlit Cloud

**Revisar**:

1. Logs en "Manage app" → "Logs"
2. Verificar que `requirements.txt` tiene todas las dependencias
3. Verificar rutas de archivos (usar rutas relativas)

### ❌ "Module not found" en Streamlit Cloud

**Solución**: Agregar dependencia en `requirements.txt`

```powershell
echo "nombre-paquete>=version" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### ❌ "File not found" en Streamlit Cloud

**Verificar rutas**:

```python
# ❌ MAL: Ruta absoluta
df = pd.read_excel("C:/Users/Desktop/data.xlsx")

# ✅ BIEN: Ruta relativa
import os
BASE_DIR = os.path.dirname(__file__)
df = pd.read_excel(os.path.join(BASE_DIR, "../data/ghg-factors.xlsx"))
```

---

## 📱 Compartir tu App

### Link directo

```
🌱 Carbon GHG Calculator
https://carbon-ghg-calculator.streamlit.app

Calcula la huella de carbono de tu organización 
siguiendo el estándar GHG Protocol (Scope 1, 2, 3).
100% gratis y open source!
```

### QR Code

Genera un QR code de tu URL:
- https://www.qr-code-generator.com/

### Redes sociales

**Twitter/X**:
```
🚀 Acabo de lanzar Carbon GHG Calculator!
🌱 Calcula emisiones según GHG Protocol
📊 Visualizaciones interactivas
📄 Reportes profesionales
💯 100% GRATIS

Pruébalo: https://carbon-ghg-calculator.streamlit.app
#sustainability #GHGProtocol #climateaction
```

**LinkedIn**:
```
Orgulloso de compartir mi proyecto: Carbon GHG Calculator

Una aplicación web profesional para calcular la huella de carbono 
de organizaciones, siguiendo los estándares del GHG Protocol.

✅ Scope 1, 2 y 3
✅ 521 factores de emisión UK Gov 2025
✅ Visualizaciones interactivas
✅ Reportes Excel/Word
✅ 100% gratis y open source

Pruébalo: https://carbon-ghg-calculator.streamlit.app
Código: https://github.com/TU-USUARIO/carbon-ghg-calculator

#Sustainability #ClimateAction #OpenSource #Python
```

---

## 🎉 ¡FELICIDADES!

Has completado el deployment de tu aplicación profesional de cálculo de huella de carbono.

**Lo que has logrado**:
- ✅ Código en GitHub (version control)
- ✅ App desplegada en producción (gratis)
- ✅ CI/CD automático configurado
- ✅ Aplicación accesible desde cualquier parte del mundo
- ✅ Monitoreo y analytics incluidos

**Próximos pasos sugeridos**:
1. Compartir con usuarios beta
2. Recolectar feedback
3. Iterar y mejorar
4. Agregar nuevas features
5. Escribir artículo/blog sobre el proyecto

---

**¿Preguntas?**
- 📖 Documentación: `docs/` en GitHub
- 🐛 Issues: https://github.com/TU-USUARIO/carbon-ghg-calculator/issues
- 💬 Discussions: https://github.com/TU-USUARIO/carbon-ghg-calculator/discussions

**Made with ❤️ using Python & Streamlit**
