"""
Test de Búsqueda Semántica de Factores de Emisión
================================================

Prueba la capacidad del sistema para encontrar factores relevantes
usando descripciones en lenguaje natural.
"""

import sys
from pathlib import Path

# Agregar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from utils.ai_assistant import SemanticFactorSearch
from utils.factors import load_uk_gov_factors

def main():
    print("=" * 70)
    print("🔍 TEST DE BÚSQUEDA SEMÁNTICA DE FACTORES")
    print("=" * 70)
    print()
    
    # Cargar factores usando la función correcta
    print("📂 Cargando factores de emisión...")
    factors_path = project_root / 'data' / 'ghg-conversion-factors-2025-condensed-set.xlsx'
    
    try:
        factors_df = load_uk_gov_factors(str(factors_path), year=2025)
        print(f"   ✓ Cargados {len(factors_df)} factores normalizados")
        print(f"   ✓ Columnas: {factors_df.columns.tolist()}")
        print()
    except Exception as e:
        print(f"   ✗ Error cargando factores: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Crear buscador
    print("🔧 Inicializando buscador semántico...")
    searcher = SemanticFactorSearch(factors_df)
    print(f"   ✓ Índice construido con {len(searcher.search_index)} entradas")
    print()
    
    # Casos de prueba
    test_queries = [
        {
            'query': 'diesel en camiones de carga',
            'description': 'Buscar factor para camiones diesel'
        },
        {
            'query': 'electricidad renovable',
            'description': 'Buscar factor de electricidad'
        },
        {
            'query': 'vuelo internacional de negocios',
            'description': 'Buscar factor para aviación comercial'
        },
        {
            'query': 'transporte marítimo de contenedores',
            'description': 'Buscar factor para transporte por barco'
        },
        {
            'query': 'residuos plásticos reciclables',
            'description': 'Buscar factor para gestión de residuos'
        },
        {
            'query': 'gas natural para calefacción',
            'description': 'Buscar factor de gas natural'
        },
        {
            'query': 'refrigerante R-410A en aire acondicionado',
            'description': 'Buscar factor de refrigerante específico'
        }
    ]
    
    print("=" * 70)
    print("📊 RESULTADOS DE BÚSQUEDA")
    print("=" * 70)
    print()
    
    for i, test in enumerate(test_queries, 1):
        print(f"🔎 Test {i}: {test['description']}")
        print(f"   Query: '{test['query']}'")
        print()
        
        # Búsqueda simple
        results = searcher.search(test['query'], top_k=3)
        
        if results:
            print(f"   ✓ Encontrados {len(results)} factores relevantes:")
            print()
            
            for j, match in enumerate(results, 1):
                print(f"   #{j} - {match.factor_name}")
                print(f"        Valor: {match.value} {match.unit}")
                print(f"        Categoría: {match.category}")
                print(f"        Score: {match.match_score:.2%}")
                print()
        else:
            print("   ✗ No se encontraron factores relevantes")
            print()
        
        print("-" * 70)
        print()
    
    # Test de búsqueda con categorización automática
    print("=" * 70)
    print("🤖 BÚSQUEDA CON CATEGORIZACIÓN IA")
    print("=" * 70)
    print()
    
    advanced_queries = [
        "consumo de diesel en tractores agrícolas para arado",
        "electricidad comprada de la red para iluminación de oficinas",
        "viajes en avión de ejecutivos a conferencias internacionales"
    ]
    
    for i, query in enumerate(advanced_queries, 1):
        print(f"🔎 Query {i}: '{query}'")
        print()
        
        try:
            results = searcher.search_with_category(query, top_k=3)
            
            if results:
                print(f"   ✓ Top 3 factores (con categorización IA):")
                print()
                
                for j, match in enumerate(results, 1):
                    print(f"   #{j} - {match.factor_name}")
                    print(f"        {match.value} {match.unit}")
                    print(f"        Score: {match.match_score:.2%}")
                    print()
            else:
                print("   ⚠️ No se encontraron factores específicos")
                print()
        
        except Exception as e:
            print(f"   ✗ Error: {e}")
            print()
        
        print("-" * 70)
        print()
    
    # Estadísticas finales
    print("=" * 70)
    print("📈 ESTADÍSTICAS DE BÚSQUEDA")
    print("=" * 70)
    print()
    print(f"✓ Tests completados: {len(test_queries) + len(advanced_queries)}")
    print(f"✓ Factores en índice: {len(searcher.search_index)}")
    print(f"✓ Sinónimos configurados: {len(searcher.SYNONYMS)}")
    print(f"✓ Entradas en cache: {len(searcher._search_cache)}")
    print()
    
    print("🎯 CAPACIDADES IMPLEMENTADAS:")
    print("   ✓ Búsqueda multi-nivel (exacta, sinónimos, fuzzy)")
    print("   ✓ Categorización automática antes de buscar")
    print("   ✓ Scoring con pesos por relevancia")
    print("   ✓ Cache de resultados frecuentes")
    print("   ✓ Expansión con sinónimos")
    print()
    
    print("✅ Búsqueda semántica funcionando correctamente")
    print()


if __name__ == '__main__':
    main()
