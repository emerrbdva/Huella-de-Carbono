# Contributing to Carbon GHG Calculator

¡Gracias por tu interés en contribuir a Carbon GHG Calculator! 🎉

Este documento proporciona pautas para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Pruebas](#pruebas)
- [Documentación](#documentación)
- [Reporte de Bugs](#reporte-de-bugs)
- [Sugerencias de Features](#sugerencias-de-features)

## 🤝 Código de Conducta

Este proyecto adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor reporta comportamientos inaceptables a [email].

### Nuestros Estándares

- Usar lenguaje acogedor e inclusivo
- Respetar puntos de vista y experiencias diferentes
- Aceptar crítica constructiva graciosamente
- Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

## 🚀 Cómo Contribuir

### 1. Fork el Repositorio

```bash
# Hacer fork en GitHub, luego clonar tu fork
git clone https://github.com/TU-USUARIO/carbon-ghg.git
cd carbon-ghg
```

### 2. Crear una Branch

```bash
# Crear branch desde main
git checkout -b feature/nombre-descriptivo

# Ejemplos de nombres de branch:
# feature/add-ipcc-2024-factors
# bugfix/fix-unit-conversion
# docs/update-readme
# test/add-calculator-tests
```

### 3. Hacer tus Cambios

- Escribe código limpio y bien documentado
- Sigue los estándares de código (ver abajo)
- Añade pruebas para nuevas funcionalidades
- Actualiza documentación si es necesario

### 4. Commit tus Cambios

```bash
# Staging
git add .

# Commit con mensaje descriptivo
git commit -m "feat: add IPCC 2024 emission factors"

# Formato de mensajes de commit:
# feat: nueva funcionalidad
# fix: corrección de bug
# docs: cambios en documentación
# test: añadir o modificar pruebas
# refactor: refactorización de código
# style: cambios de formato (no afectan lógica)
# chore: tareas de mantenimiento
```

### 5. Push y Pull Request

```bash
# Push a tu fork
git push origin feature/nombre-descriptivo

# Abrir Pull Request en GitHub
# Incluir:
# - Descripción clara de cambios
# - Issue relacionado (si aplica)
# - Screenshots (si es UI)
# - Tests que pasen
```

## 🔧 Proceso de Desarrollo

### Setup del Entorno

```powershell
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe

# 3. Instalar pre-commit hooks (si aplica)
pre-commit install
```

### Workflow de Desarrollo

1. **Actualizar tu fork**
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Desarrollar en branch**
   ```bash
   git checkout -b feature/mi-feature
   # Hacer cambios
   ```

3. **Ejecutar pruebas localmente**
   ```bash
   pytest tests/ -v
   ```

4. **Commit y push**
   ```bash
   git add .
   git commit -m "feat: mi nueva feature"
   git push origin feature/mi-feature
   ```

5. **Crear Pull Request** en GitHub

## 📝 Estándares de Código

### Python Style Guide

Seguimos **PEP 8** con algunas excepciones:

```python
# ✅ BIEN - Nombres descriptivos, docstrings
def calculate_emission_factor(
    activity_value: float,
    emission_factor: float,
    gwp: float = 1.0
) -> float:
    """
    Calculate CO2e emissions from activity data.
    
    Args:
        activity_value: Amount of activity
        emission_factor: EF value in kg CO2e
        gwp: Global Warming Potential (default 1.0)
    
    Returns:
        Total emissions in kg CO2e
    """
    return activity_value * emission_factor * gwp


# ❌ MAL - Sin tipos, sin docstring, nombre poco claro
def calc(a, b, c=1):
    return a * b * c
```

### Docstrings

Usamos **Google Style** para docstrings:

```python
def complex_function(param1: str, param2: int) -> dict:
    """
    Short description of function.
    
    Longer explanation if needed. Can span multiple
    lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Example:
        >>> result = complex_function("test", 5)
        >>> print(result)
        {'status': 'success'}
    """
    if param2 < 0:
        raise ValueError("param2 must be positive")
    return {'status': 'success', 'value': param2}
```

### Type Hints

Siempre usar type hints:

```python
from typing import List, Dict, Optional, Union

# ✅ BIEN
def process_emissions(
    activities: List[ActivityRecord],
    factors: Dict[str, float]
) -> Optional[EmissionResult]:
    ...

# ❌ MAL
def process_emissions(activities, factors):
    ...
```

### Imports

Ordenar imports en 3 bloques:

```python
# 1. Standard library
import os
import sys
from datetime import datetime
from typing import List, Dict

# 2. Third-party
import pandas as pd
import numpy as np
from pydantic import BaseModel

# 3. Local
from models.emissions import ActivityRecord
from utils.factors import load_uk_gov_factors
```

## 🧪 Pruebas

### Escribir Pruebas

Toda nueva funcionalidad debe incluir pruebas:

```python
# tests/test_nueva_funcionalidad.py
import pytest
from tu_modulo import tu_funcion

class TestNuevaFuncionalidad:
    """Pruebas para nueva funcionalidad."""
    
    def test_caso_basico(self):
        """Debe funcionar con caso básico."""
        result = tu_funcion(parametro="test")
        assert result == "expected"
    
    def test_caso_edge(self):
        """Debe manejar casos límite."""
        result = tu_funcion(parametro="")
        assert result is None
    
    def test_error_handling(self):
        """Debe lanzar error apropiado."""
        with pytest.raises(ValueError):
            tu_funcion(parametro=None)
```

### Ejecutar Pruebas

```powershell
# Todas las pruebas
pytest tests/ -v

# Prueba específica
pytest tests/test_calculators.py::TestComputeEmission::test_basic_calculation -v

# Con coverage
pytest tests/ -v --cov=models --cov=calculators

# Solo pruebas rápidas (excluir slow)
pytest tests/ -v -m "not slow"
```

### Coverage Mínimo

- **Nuevo código**: 80% coverage mínimo
- **Funciones críticas**: 100% coverage (calculators, validators)
- **UI/Streamlit**: No obligatorio

## 📚 Documentación

### Actualizar Documentación

Si tu cambio afecta el uso del sistema, actualiza:

1. **README.md** - Cambios en features principales
2. **Docstrings** - Funciones/clases modificadas
3. **DOCKER_GUIDE.md** - Cambios en despliegue
4. **Examples** - Añadir ejemplos si es aplicable

### Ejemplo de Documentación

```python
# utils/nueva_utilidad.py

"""
Módulo de utilidad para [propósito].

Este módulo proporciona funciones para [describir qué hace].

Example:
    >>> from utils.nueva_utilidad import funcion_principal
    >>> result = funcion_principal(param="valor")
    >>> print(result)
    'valor procesado'

Note:
    Esta utilidad requiere [dependencia] instalada.

References:
    - [Link a documentación externa]
    - [Paper científico relevante]
"""

def funcion_principal(param: str) -> str:
    """Procesa el parámetro y retorna resultado."""
    ...
```

## 🐛 Reporte de Bugs

### Crear un Issue

Cuando encuentres un bug, crea un issue con:

1. **Título claro**: "Bug: [descripción breve]"
2. **Descripción**: Qué esperabas vs qué obtuviste
3. **Pasos para reproducir**:
   ```
   1. Ir a '...'
   2. Click en '...'
   3. Ver error
   ```
4. **Entorno**:
   - OS: Windows 10
   - Python: 3.12.7
   - Versión del proyecto: 1.0.0
5. **Screenshots** (si aplica)
6. **Logs de error**:
   ```
   Traceback (most recent call last):
     ...
   ```

### Plantilla de Issue

```markdown
## Descripción del Bug
[Descripción clara y concisa]

## Pasos para Reproducir
1. ...
2. ...
3. ...

## Comportamiento Esperado
[Qué debería pasar]

## Comportamiento Actual
[Qué pasó realmente]

## Entorno
- OS: [Windows/Linux/Mac]
- Python: [versión]
- Proyecto: [versión]

## Información Adicional
[Screenshots, logs, contexto adicional]
```

## 💡 Sugerencias de Features

### Proponer una Nueva Feature

1. **Verificar** que no exista un issue similar
2. **Crear issue** con etiqueta `feature request`
3. **Describir**:
   - Problema que resuelve
   - Solución propuesta
   - Alternativas consideradas
   - Impacto en usuarios existentes

### Plantilla de Feature Request

```markdown
## Problema
[Descripción del problema o necesidad]

## Solución Propuesta
[Cómo resolverías este problema]

## Alternativas Consideradas
[Otras soluciones que consideraste]

## Información Adicional
[Contexto, links, referencias]

## Impacto
- [ ] Breaking change
- [ ] Backward compatible
- [ ] Requiere migración de datos
- [ ] Requiere nuevas dependencias
```

## 🏆 Reconocimientos

Contribuciones destacadas serán reconocidas en:
- Archivo `CONTRIBUTORS.md`
- Release notes
- README principal

## 📞 Contacto

¿Preguntas? Contáctanos:
- **Email**: [email]
- **Discord**: [link]
- **GitHub Discussions**: [link]

---

¡Gracias por hacer Carbon GHG Calculator mejor! 🌱
