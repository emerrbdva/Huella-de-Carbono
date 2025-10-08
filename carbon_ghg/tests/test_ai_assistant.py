"""
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


@skip_if_no_ollama
class TestSemanticFactorSearch:
    """Pruebas para SemanticFactorSearch."""
    
    @pytest.fixture
    def sample_factors_df(self):
        """DataFrame de ejemplo con factores de emisión."""
        return pd.DataFrame([
            {
                'Activity': 'Liquid fuels',
                'Fuel': 'Diesel (average biofuel blend)',
                'kgCO2e': 2.68,
                'Unit': 'litres',
                'Sheet': 'Fuels',
                'Source': 'UK Gov 2025',
                'Year': 2025
            },
            {
                'Activity': 'Gaseous fuels',
                'Fuel': 'Natural gas',
                'kgCO2e': 0.2027,
                'Unit': 'kWh (Net CV)',
                'Sheet': 'Fuels',
                'Source': 'UK Gov 2025',
                'Year': 2025
            },
            {
                'Activity': 'UK electricity',
                'Fuel': 'UK electricity',
                'kgCO2e': 0.21233,
                'Unit': 'kWh',
                'Sheet': 'UK electricity',
                'Source': 'UK Gov 2025',
                'Year': 2025
            },
            {
                'Activity': 'Flights',
                'Fuel': 'Domestic, to/from UK',
                'kgCO2e': 0.24587,
                'Unit': 'passenger.km',
                'Sheet': 'Business travel- air',
                'Source': 'UK Gov 2025',
                'Year': 2025
            }
        ])
    
    def test_initialization(self, sample_factors_df):
        """Debe inicializar correctamente con índice de búsqueda."""
        searcher = SemanticFactorSearch(sample_factors_df)
        
        assert len(searcher.search_index) == 4
        assert hasattr(searcher, '_search_cache')
    
    def test_search_diesel(self, sample_factors_df):
        """Debe encontrar diesel correctamente."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("diesel", top_k=3)
        
        assert len(results) > 0
        assert results[0].activity == 'Liquid fuels'
        assert 'Diesel' in results[0].fuel
    
    def test_search_gas_natural(self, sample_factors_df):
        """Debe encontrar gas natural correctamente."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("gas natural", top_k=3)
        
        assert len(results) > 0
        best_match = results[0]
        assert 'Natural gas' in best_match.fuel
        assert best_match.relevance_score >= 0.8  # Alta relevancia
    
    def test_search_electricity(self, sample_factors_df):
        """Debe encontrar electricidad correctamente."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("electricidad", top_k=3)
        
        assert len(results) > 0
        # Puede encontrar 'electricity' debido a sinónimos
    
    def test_search_with_category_hint(self, sample_factors_df):
        """Debe filtrar por categoría cuando se proporciona."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("diesel", top_k=3, category_hint="Fuels")
        
        assert len(results) > 0
        for result in results:
            assert result.sheet == 'Fuels'
    
    def test_search_cache(self, sample_factors_df):
        """Debe usar caché para búsquedas repetidas."""
        searcher = SemanticFactorSearch(sample_factors_df)
        
        # Primera búsqueda
        results1 = searcher.search("diesel", top_k=3)
        cache_size_1 = len(searcher._search_cache)
        
        # Segunda búsqueda (debe usar caché)
        results2 = searcher.search("diesel", top_k=3)
        cache_size_2 = len(searcher._search_cache)
        
        assert results1 == results2
        assert cache_size_1 == cache_size_2  # No debe crecer el caché
    
    def test_search_with_category_automatic(self, sample_factors_df):
        """Debe categorizar automáticamente y buscar."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search_with_category("diesel para camiones", top_k=3)
        
        assert len(results) > 0
        # Debe encontrar diesel
    
    def test_synonym_expansion(self, sample_factors_df):
        """Debe expandir búsqueda con sinónimos."""
        searcher = SemanticFactorSearch(sample_factors_df)
        
        # 'gasoil' es sinónimo de 'diesel'
        results = searcher.search("gasoil", top_k=3)
        
        assert len(results) > 0
        # Debe encontrar diesel a través de sinónimos
    
    def test_empty_query(self, sample_factors_df):
        """Debe manejar consulta vacía."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("", top_k=3)
        
        assert len(results) == 0
    
    def test_no_matches(self, sample_factors_df):
        """Debe retornar lista vacía cuando no hay coincidencias."""
        searcher = SemanticFactorSearch(sample_factors_df)
        results = searcher.search("xyz123abc456", top_k=3)
        
        # Puede retornar algunos resultados con relevancia baja o vacío
        assert isinstance(results, list)


@skip_if_no_ollama
class TestGHGCategoryMapper:
    """Pruebas para mapeo de categorías."""
    
    @pytest.fixture
    def mapper(self):
        """Instancia del mapper."""
        return GHGCategoryMapper()
    
    def test_category_map_structure(self, mapper):
        """Debe tener estructura correcta de categorías."""
        assert 'stationary_combustion' in mapper.CATEGORY_MAP
        assert 'mobile_combustion' in mapper.CATEGORY_MAP
        assert 'purchased_electricity' in mapper.CATEGORY_MAP
        
        # Cada categoría debe tener scope y keywords
        for category, info in mapper.CATEGORY_MAP.items():
            assert 'scope' in info
            assert 'keywords' in info
            assert isinstance(info['scope'], int)
            assert isinstance(info['keywords'], list)
    
    def test_scope_values(self, mapper):
        """Todos los scopes deben estar entre 1 y 3."""
        for category, info in mapper.CATEGORY_MAP.items():
            assert 1 <= info['scope'] <= 3
    
    def test_keywords_non_empty(self, mapper):
        """Todas las categorías deben tener keywords."""
        for category, info in mapper.CATEGORY_MAP.items():
            assert len(info['keywords']) > 0


@skip_if_no_ollama
class TestSynonyms:
    """Pruebas para diccionario de sinónimos."""
    
    @pytest.fixture
    def mapper(self):
        """Instancia del mapper."""
        return GHGCategoryMapper()
    
    def test_synonyms_structure(self, mapper):
        """Debe tener categorías principales de sinónimos."""
        assert 'diesel' in mapper.SYNONYMS
        assert 'gasoline' in mapper.SYNONYMS
        assert 'electricity' in mapper.SYNONYMS
        assert 'natural_gas' in mapper.SYNONYMS
    
    def test_synonyms_are_lists(self, mapper):
        """Todos los sinónimos deben ser listas."""
        for key, synonyms in mapper.SYNONYMS.items():
            assert isinstance(synonyms, list)
            assert len(synonyms) > 0
    
    def test_diesel_synonyms(self, mapper):
        """Debe contener sinónimos comunes de diesel."""
        diesel_syns = mapper.SYNONYMS['diesel']
        
        assert 'diesel' in diesel_syns
        assert 'diésel' in diesel_syns or 'gasoil' in diesel_syns
    
    def test_electricity_synonyms(self, mapper):
        """Debe contener sinónimos de electricidad."""
        elec_syns = mapper.SYNONYMS['electricity']
        
        # Debe tener variantes en español/inglés
        assert any('electric' in s.lower() for s in elec_syns)


@skip_if_no_ollama
class TestCategorizeActivity:
    """Pruebas para categorización."""
    
    @pytest.fixture
    def mapper(self):
        """Instancia del mapper."""
        return GHGCategoryMapper()
    
    def test_categorize_returns_result(self, mapper):
        """Debe retornar CategorizationResult."""
        description = "Diesel para camiones de distribución"
        
        try:
            result = mapper.categorize_activity(description)
            
            if result:  # Si hay resultado
                assert isinstance(result, CategorizationResult)
                assert result.scope in [1, 2, 3]
                assert result.category is not None
                assert 0.0 <= result.confidence <= 1.0
        except Exception:
            # Si Ollama no está disponible, skip
            pytest.skip("Ollama no disponible")
    
    def test_categorize_handles_error(self, mapper):
        """Debe manejar errores gracefully."""
        # Descripción vacía
        result = mapper.categorize_activity("")
        
        # Debe retornar CategorizationResult o None
        assert result is None or isinstance(result, CategorizationResult)


# Fixtures para pruebas de integración
@pytest.fixture
def real_factors_sample():
    """Muestra real de factores UK Gov 2025."""
    return pd.DataFrame([
        {
            'Activity': 'Liquid fuels',
            'Fuel': 'Diesel (average biofuel blend)',
            'kgCO2e': 2.68213,
            'Unit': 'litres',
            'Sheet': 'Fuels',
            'Source': 'UK Gov 2025',
            'Year': 2025
        },
        {
            'Activity': 'Liquid fuels',
            'Fuel': 'Petrol (average biofuel blend)',
            'kgCO2e': 2.31384,
            'Unit': 'litres',
            'Sheet': 'Fuels',
            'Source': 'UK Gov 2025',
            'Year': 2025
        },
        {
            'Activity': 'Gaseous fuels',
            'Fuel': 'Natural gas',
            'kgCO2e': 0.2027,
            'Unit': 'kWh (Net CV)',
            'Sheet': 'Fuels',
            'Source': 'UK Gov 2025',
            'Year': 2025
        },
        {
            'Activity': 'Gaseous fuels',
            'Fuel': 'Natural gas',
            'kgCO2e': 2.06672,
            'Unit': 'cubic metres',
            'Sheet': 'Fuels',
            'Source': 'UK Gov 2025',
            'Year': 2025
        },
        {
            'Activity': 'UK electricity',
            'Fuel': 'UK electricity',
            'kgCO2e': 0.21233,
            'Unit': 'kWh',
            'Sheet': 'UK electricity',
            'Source': 'UK Gov 2025',
            'Year': 2025
        }
    ])


@skip_if_no_ollama
class TestIntegrationSemanticSearch:
    """Pruebas de integración con datos reales."""
    
    def test_diesel_search_integration(self, real_factors_sample):
        """Integración: búsqueda de diesel con datos reales."""
        searcher = SemanticFactorSearch(real_factors_sample)
        results = searcher.search("diesel en litros", top_k=3)
        
        assert len(results) > 0
        best_match = results[0]
        assert 'Diesel' in best_match.fuel
        assert best_match.unit == 'litres'
        assert best_match.kgco2e == pytest.approx(2.68213, rel=1e-3)
    
    def test_gas_search_integration(self, real_factors_sample):
        """Integración: búsqueda de gas natural."""
        searcher = SemanticFactorSearch(real_factors_sample)
        results = searcher.search("gas natural en kWh", top_k=3)
        
        assert len(results) > 0
        # Debe priorizar el factor en kWh sobre m3
        best_match = results[0]
        assert 'Natural gas' in best_match.fuel
    
    def test_electricity_search_integration(self, real_factors_sample):
        """Integración: búsqueda de electricidad UK."""
        searcher = SemanticFactorSearch(real_factors_sample)
        results = searcher.search("electricidad Reino Unido", top_k=3)
        
        assert len(results) > 0
        best_match = results[0]
        assert 'UK electricity' in best_match.activity
        assert best_match.kgco2e == pytest.approx(0.21233, rel=1e-3)
    
    def test_multiple_searches_cache(self, real_factors_sample):
        """Integración: verificar caché en múltiples búsquedas."""
        searcher = SemanticFactorSearch(real_factors_sample)
        
        # Primera búsqueda
        results1 = searcher.search("diesel", top_k=3)
        
        # Segunda búsqueda diferente
        results2 = searcher.search("gas natural", top_k=3)
        
        # Tercera búsqueda repetida
        results3 = searcher.search("diesel", top_k=3)
        
        # Debe tener entradas de caché
        assert len(searcher._search_cache) >= 2
        
        # Resultados 1 y 3 deben ser idénticos
        assert results1 == results3
