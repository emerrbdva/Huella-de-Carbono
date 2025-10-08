"""
Script para arreglar tests de calculators - acceso a propiedades anidadas
"""
import re

test_file = "tests/test_calculators.py"

with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar acceso a propiedades del activity_record
replacements = [
    (r'result\.entity_id', 'result.activity_record.entity_id'),
    (r'result\.scope', 'result.activity_record.scope'),
    (r'result\.category', 'result.activity_record.category'),
    (r'result\.activity_value', 'result.activity_record.activity_value'),
    (r'result\.activity_unit', 'result.activity_record.activity_unit'),
    (r'result\.year', 'result.activity_record.year'),
    (r'result\.geography', 'result.activity_record.geography'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

print(f"✅ Arreglando {test_file}...")
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Test file actualizado: {test_file}")
print("✨ Cambios realizados:")
for pattern, replacement in replacements:
    count = len(re.findall(pattern, content))
    if count > 0:
        print(f"   - {pattern} → {replacement} ({count} veces)")
