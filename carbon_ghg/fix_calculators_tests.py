"""
Script para arreglar los tests de calculators para usar la estructura correcta de EmissionResult
"""
import re

# El problema es que los tests usan .total_co2e pero el modelo real tiene .emission_kgCO2e

test_file = "tests/test_calculators.py"

with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar todas las referencias a .total_co2e con .emission_kgCO2e
content = re.sub(r'\.total_co2e\b', '.emission_kgCO2e', content)
content = re.sub(r'total_co2e=', 'emission_kgCO2e=', content)

# Reemplazar también assertion patterns
content = re.sub(r'assert result\.emission_kgCO2e ==', 'assert result.emission_kgCO2e ==', content)

print(f"✅ Arreglando {test_file}...")
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Test file actualizado: {test_file}")
print("✨ Cambios realizados:")
print("   - .total_co2e → .emission_kgCO2e")
print("   - total_co2e= → emission_kgCO2e=")
