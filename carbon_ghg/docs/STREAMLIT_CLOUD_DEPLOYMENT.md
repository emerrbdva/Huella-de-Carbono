# 🚀 Guía de Deployment - Streamlit Cloud (GRATIS)

**Tiempo estimado**: 10-15 minutos  
**Costo**: $0 (Plan Free Forever)  
**Dificultad**: ⭐ Muy fácil (sin conocimientos técnicos)

---

## 📋 Requisitos Previos

✅ Cuenta de GitHub (gratis): https://github.com/join  
✅ Cuenta de Streamlit Cloud (gratis): https://share.streamlit.io/  
✅ Código del proyecto subido a GitHub  

---

## 🎯 Paso a Paso

### **Paso 1: Preparar el Repositorio en GitHub** (5 min)

#### 1.1 Verificar que tienes Git instalado

```powershell
git --version
```

Si no tienes Git, descárgalo de: https://git-scm.com/downloads

#### 1.2 Inicializar Git en el proyecto (si no lo has hecho)

```powershell
cd "c:\Python\Huella de Carbono\carbon_ghg"
git init
```

#### 1.3 Configurar Git (primera vez)

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

#### 1.4 Agregar todos los archivos

```powershell
git add .
```

#### 1.5 Crear el primer commit

```powershell
git commit -m "Initial commit - Carbon GHG Calculator v1.0"
```

#### 1.6 Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `carbon-ghg-calculator`
3. Descripción: `🌱 Carbon Footprint Calculator - GHG Protocol Compliant`
4. Visibilidad: **Public** (necesario para plan Free de Streamlit)
5. NO inicialices con README (ya lo tenemos)
6. Click en **"Create repository"**

#### 1.7 Conectar tu repositorio local con GitHub

```powershell
# Reemplaza "TU-USUARIO" con tu username de GitHub
git remote add origin https://github.com/TU-USUARIO/carbon-ghg-calculator.git
git branch -M main
git push -u origin main
```

**¡Listo!** Tu código ya está en GitHub 🎉

---

### **Paso 2: Deploy en Streamlit Cloud** (5 min)

#### 2.1 Crear cuenta en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Click en **"Sign up"**
3. Usa **"Continue with GitHub"** (más fácil)
4. Autoriza Streamlit Cloud a acceder a tus repositorios

#### 2.2 Crear nueva app

1. Click en **"New app"** (botón azul arriba a la derecha)
2. Completa los campos:

   - **Repository**: `TU-USUARIO/carbon-ghg-calculator`
   - **Branch**: `main`
   - **Main file path**: `app/streamlit_app.py`
   - **App URL** (opcional): `carbon-ghg-calculator` (personaliza tu URL)

3. Click en **"Deploy!"**

#### 2.3 Esperar el deployment (3-5 min)

Verás un log de instalación:

```
Installing Python dependencies...
✓ pandas>=2.0.0
✓ streamlit>=1.28.0
✓ plotly>=5.17.0
...
App is running!
```

**¡Felicidades! 🎉** Tu app está desplegada en:
```
https://TU-USUARIO-carbon-ghg-calculator-app-streamlit-app-xxxxx.streamlit.app
```

O en tu URL personalizada:
```
https://carbon-ghg-calculator.streamlit.app
```

---

## 🔧 Configuración Adicional (Opcional)

### Secrets Management (para variables sensibles)

Si tu app necesita API keys o secrets:

1. En el dashboard de Streamlit Cloud, click en tu app
2. Click en **"⋮"** (tres puntos) → **"Settings"**
3. Sección **"Secrets"**
4. Agrega tus secrets en formato TOML:

```toml
# .streamlit/secrets.toml
[database]
host = "localhost"
user = "admin"
password = "tu-password-seguro"

[api]
openai_api_key = "sk-..."
```

5. En tu código, accede con:

```python
import streamlit as st

db_host = st.secrets["database"]["host"]
api_key = st.secrets["api"]["openai_api_key"]
```

### Custom Domain (Solo en plan Premium)

El plan Free incluye:
- ✅ 1 app pública
- ✅ Unlimited viewers
- ✅ Auto-deploy on GitHub push
- ✅ HTTPS incluido
- ❌ Custom domain (requiere Team plan $250/mo)

Para custom domain en FREE:
- Usa la URL de Streamlit: `https://share.streamlit.io/tu-usuario/repo/main/app.py`

---

## 🔄 Auto-Deploy (CI/CD Automático)

**¡Ya está configurado!** Cada vez que hagas `git push`:

```powershell
# 1. Hacer cambios en el código
# 2. Commit
git add .
git commit -m "Fix: Mejorar visualización Sankey"

# 3. Push a GitHub
git push

# 4. Streamlit Cloud auto-detecta y re-deploya en 2-3 min
```

Verás el re-deploy en el dashboard de Streamlit Cloud.

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real

1. Dashboard de Streamlit Cloud
2. Click en tu app
3. Click en **"Manage app"**
4. Tab **"Logs"**

Verás:
```
2025-10-08 10:30:15 INFO: App started
2025-10-08 10:30:20 INFO: Loading emission factors...
2025-10-08 10:30:22 INFO: Factors loaded successfully (521 factors)
```

### Métricas de uso

En **"Analytics"** verás:
- 👥 Número de visitantes
- 📊 Sesiones activas
- 🌍 Geolocalización de usuarios
- ⏱️ Tiempo promedio de uso

---

## 🐛 Troubleshooting

### ❌ Error: "No module named 'xxx'"

**Solución**: Agregar dependencia en `requirements.txt`

```bash
# Agregar la línea faltante en requirements.txt
echo "xxx>=1.0.0" >> requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### ❌ Error: "File not found"

**Solución**: Verificar rutas relativas

```python
# ❌ MAL: Ruta absoluta
df = pd.read_excel("C:/Users/Desktop/data.xlsx")

# ✅ BIEN: Ruta relativa
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(BASE_DIR, "../data/ghg-factors.xlsx"))
```

### ❌ Error: "Memory limit exceeded"

**Plan Free límites**:
- RAM: 1 GB
- CPU: Shared
- Storage: 1 GB

**Solución**: Optimizar carga de datos

```python
# ✅ Usar cache para no recargar en cada interacción
@st.cache_data(ttl=3600)
def load_factors():
    return pd.read_excel("data/ghg-factors.xlsx")

# ✅ Cargar solo columnas necesarias
df = pd.read_excel("data.xlsx", usecols=["col1", "col2"])

# ✅ Usar chunks para archivos grandes
for chunk in pd.read_csv("large_file.csv", chunksize=1000):
    process(chunk)
```

### ❌ App muy lenta

**Solución**: Verificar cache

```python
# Asegúrate de que estas funciones estén cacheadas
@st.cache_data(ttl=3600)
def load_uk_gov_factors(file_path):
    # ...

@st.cache_data(ttl=600)
def compute_all_emissions(activities, factors):
    # ...
```

---

## 📈 Plan Free vs Premium

| Feature | Free | Community ($0) | Teams ($250/mo) |
|---------|------|----------------|-----------------|
| **Apps públicas** | 1 | Unlimited | Unlimited |
| **Apps privadas** | 0 | Unlimited | Unlimited |
| **Viewers** | Unlimited | Unlimited | Unlimited |
| **RAM** | 1 GB | 1 GB | 2-8 GB |
| **Storage** | 1 GB | 1 GB | 10 GB |
| **Auto-deploy** | ✅ | ✅ | ✅ |
| **HTTPS** | ✅ | ✅ | ✅ |
| **Custom domain** | ❌ | ❌ | ✅ |
| **Password protect** | ❌ | ✅ | ✅ |
| **SSO** | ❌ | ❌ | ✅ |
| **Support** | Community | Community | Priority |

**Nuestra app**: Plan **Free** es suficiente (app pública, <1GB RAM)

---

## ✅ Checklist Final

Antes de compartir tu app:

- [ ] ✅ App funciona correctamente en local (`streamlit run app/streamlit_app.py`)
- [ ] ✅ Todos los archivos necesarios están en GitHub
- [ ] ✅ `requirements.txt` tiene todas las dependencias
- [ ] ✅ `.gitignore` excluye archivos sensibles
- [ ] ✅ `README.md` actualizado con link a la app
- [ ] ✅ Data files incluidos en el repo (ej: `data/ghg-factors.xlsx`)
- [ ] ✅ Cache configurado para performance
- [ ] ✅ No hay API keys hardcodeadas (usar secrets)

---

## 🎉 ¡App Desplegada!

Tu aplicación ya está disponible públicamente:

**URL de tu app**:
```
https://share.streamlit.io/TU-USUARIO/carbon-ghg-calculator/main/app/streamlit_app.py
```

**Comparte con**:
- 📧 Email: Envía el link a colegas
- 🐦 Twitter: Tweet sobre tu proyecto
- 💼 LinkedIn: Comparte en tu red profesional
- 📊 Reportes: Incluye el link en documentos

---

## 🔗 Links Útiles

- 📖 [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- 💬 [Streamlit Community Forum](https://discuss.streamlit.io/)
- 🐛 [Report Issues](https://github.com/streamlit/streamlit/issues)
- 📺 [Streamlit YouTube](https://www.youtube.com/c/Streamlit)

---

## 📞 ¿Necesitas Ayuda?

- **Error técnico**: [Streamlit Forum](https://discuss.streamlit.io/)
- **Pregunta sobre la app**: [GitHub Issues](https://github.com/TU-USUARIO/carbon-ghg-calculator/issues)
- **Feature request**: [GitHub Discussions](https://github.com/TU-USUARIO/carbon-ghg-calculator/discussions)

---

**¡Felicidades por tu deployment! 🎊**

Ahora tienes una aplicación web profesional de cálculo de huella de carbono **100% gratis y accesible desde cualquier lugar del mundo**.

**Próximos pasos sugeridos**:
1. ✅ Compartir la app con usuarios beta
2. ✅ Recolectar feedback
3. ✅ Iterar y mejorar
4. ✅ ¡Celebrar! 🎉
