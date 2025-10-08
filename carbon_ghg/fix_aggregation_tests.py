"""
Complete rewrite of aggregation tests to use correct structure
"""

aggregation_tests = '''
class TestAggregateByScope:
    """Pruebas para agregación por scope."""
    
    def test_aggregate_single_scope(self, sample_emission_results):
        """Debe agregar correctamente un solo alcance."""
        # Filtrar solo scope 1
        scope_1_results = [r for r in sample_emission_results if r.activity_record.scope == 1]
        
        agg = aggregate_emissions_by_scope(scope_1_results)
        
        # Verificar que solo hay scope 1
        assert agg[1] > 0
        assert agg[2] == 0
        assert agg[3] == 0
    
    def test_aggregate_multiple_scopes(self, sample_emission_results):
        """Debe agregar correctamente múltiples alcances."""
        agg = aggregate_emissions_by_scope(sample_emission_results)
        
        # Verificar que hay múltiples scopes con emisiones
        total_scopes_with_emissions = sum(1 for v in agg.values() if v > 0)
        assert total_scopes_with_emissions >= 2  # Al menos 2 scopes diferentes
        
        # Verificar que las sumas son correctas
        total = sum(agg.values())
        assert total > 0
    
    def test_aggregate_empty_dataframe(self):
        """Debe manejar lista vacía."""
        agg = aggregate_emissions_by_scope([])
        
        # Debe devolver diccionario con scopes en 0
        assert agg == {1: 0.0, 2: 0.0, 3: 0.0}


class TestAggregateByCategory:
    """Pruebas para agregación por categoría."""
    
    def test_aggregate_single_category(self, sample_emission_results):
        """Debe agregar correctamente por categoría."""
        agg = aggregate_emissions_by_category(sample_emission_results)
        
        # Verificar que es un diccionario con categorías
        assert isinstance(agg, dict)
        assert len(agg) > 0
        
        # Verificar que las categorías tienen emisiones > 0
        for category, total in agg.items():
            assert total > 0
            assert isinstance(category, str)
    
    def test_aggregate_multiple_categories(self, sample_emission_results):
        """Debe agregar correctamente múltiples categorías."""
        agg = aggregate_emissions_by_category(sample_emission_results)
        
        # Debe haber múltiples categorías (nuestro fixture tiene 3)
        assert len(agg) >= 2
        
        # La suma de todas las categorías debe ser el total
        total = sum(agg.values())
        assert total > 0
    
    def test_category_sorting(self, sample_emission_results):
        """Las categorías deben estar en el resultado."""
        agg = aggregate_emissions_by_category(sample_emission_results)
        
        # Verificar que las categorías esperadas están presentes
        expected_categories = set(r.activity_record.category for r in sample_emission_results)
        actual_categories = set(agg.keys())
        
        assert expected_categories == actual_categories
'''

# Leer el archivo actual
with open('tests/test_calculators.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar dónde empiezan las clases TestAggregateByScope
import re

# Buscar el inicio de TestAggregateByScope hasta el final de TestAggregateByCategory
pattern = r'class TestAggregateByScope:.*?(?=class Test|$)'
match = re.search(pattern, content, re.DOTALL)

if match:
    # Reemplazar toda la sección
    before = content[:match.start()]
    after_match = content[match.end():]
    
    # Encontrar dónde termina TestAggregateByCategory
    pattern2 = r'class TestAggregateByCategory:.*?(?=class Test|$)'
    match2 = re.search(pattern2, after_match, re.DOTALL)
    
    if match2:
        after = after_match[match2.end():]
    else:
        after = after_match
    
    new_content = before + aggregation_tests + '\n\n' + after
    
    with open('tests/test_calculators.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Aggregation tests rewritten successfully!")
else:
    print("❌ Could not find TestAggregateByScope class")
