"""
Script para marcar todos los AI tests como skip si Ollama no está disponible
"""
import re

# Leer el archivo
with open('tests/test_ai_assistant.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Agregar la función para verificar Ollama al inicio
ollama_check = '''"""
Pruebas unitarias para módulo utils.ai_assistant
Ejecutar: pytest tests/test_ai_assistant.py -v
"""
import pytest
import pandas as pd
import subprocess
from utils.ai_assistant import (
    SemanticFactorSearch,
    GHGCategoryMapper,
    CategorizationResult
)


def is_ollama_available():
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False


ollama_available = is_ollama_available()
skip_if_no_ollama = pytest.mark.skipif(
    not ollama_available,
    reason="Ollama not available - AI tests require Ollama"
)

'''

# Reemplazar el header
content = re.sub(
    r'^"""[\s\S]*?""".*?(?=class TestSemanticFactorSearch)',
    ollama_check,
    content,
    flags=re.MULTILINE
)

# Agregar decorator a todas las clases de tests
content = re.sub(
    r'(class Test\w+:)',
    r'@skip_if_no_ollama\n\1',
    content
)

# Guardar
with open('tests/test_ai_assistant.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AI tests marcados para skip si Ollama no disponible")
print("   - Agregado is_ollama_available() function")
print("   - Agregado @skip_if_no_ollama decorator a todas las clases")
