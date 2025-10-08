"""
Pruebas simplificadas para módulos de IA.
Ejecutar: pytest tests/test_ai_simplified.py -v
"""
import pytest
import pandas as pd
from utils.ai_assistant import (
    SemanticFactorSearch,
    GHGCategoryMapper,
    CategorizationResult,
    FactorMatch
)
from utils.ai_recommendations import (
    AIRecommendationEngine,
    Recommendation
)


class TestGHGCategoryMapperSimplified:
    """Pruebas simplificadas para GHGCategoryMapper."""
    
    def test_initialization(self):
        """Debe inicializar correctamente."""
        mapper = GHGCategoryMapper()
        assert mapper is not None
        assert hasattr(mapper, 'model')
        assert hasattr(mapper, 'api_url')
        assert hasattr(mapper, 'context')
    
    def test_context_has_scopes(self):
        """Contexto debe mencionar los 3 Scopes."""
        mapper = GHGCategoryMapper()
        context = mapper.context
        
        assert 'Scope 1' in context
        assert 'Scope 2' in context
        assert 'Scope 3' in context
    
    def test_context_has_categories(self):
        """Contexto debe mencionar categorías principales."""
        mapper = GHGCategoryMapper()
        context = mapper.context
        
        # Verificar algunas categorías clave
        assert 'stationary_combustion' in context
        assert 'mobile_combustion' in context
        assert 'purchased_electricity' in context


class TestSemanticFactorSearchSimplified:
    """Pruebas simplificadas para SemanticFactorSearch."""
    
    @pytest.fixture
    def sample_factors(self):
        """Factores de ejemplo."""
        return pd.DataFrame([
            {
                'Activity': 'Liquid fuels',
                'Fuel': 'Diesel',
                'kgCO2e': 2.68,
                'Unit': 'litres',
                'Sheet': 'Fuels',
                'Source': 'UK Gov 2025',
                'Year': 2025
            },
            {
                'Activity': 'Gaseous fuels',
                'Fuel': 'Natural gas',
                'kgCO2e': 0.18385,
                'Unit': 'kWh',
                'Sheet': 'Fuels',
                'Source': 'UK Gov 2025',
                'Year': 2025
            },
            {
                'Activity': 'Electricity',
                'Fuel': 'UK electricity',
                'kgCO2e': 0.21233,
                'Unit': 'kWh',
                'Sheet': 'Electricity',
                'Source': 'UK Gov 2025',
                'Year': 2025
            }
        ])
    
    def test_initialization(self, sample_factors):
        """Debe inicializar correctamente."""
        searcher = SemanticFactorSearch(sample_factors)
        assert searcher is not None
        assert len(searcher.search_index) == 3
    
    def test_search_returns_results(self, sample_factors):
        """Búsqueda debe retornar resultados."""
        searcher = SemanticFactorSearch(sample_factors)
        results = searcher.search("diesel", top_k=3)
        
        assert isinstance(results, list)
        # Debe encontrar al menos algo
        if len(results) > 0:
            assert isinstance(results[0], FactorMatch)
            assert hasattr(results[0], 'factor_name')
            assert hasattr(results[0], 'value')
            assert hasattr(results[0], 'unit')
    
    def test_search_diesel(self, sample_factors):
        """Búsqueda de diesel debe funcionar."""
        searcher = SemanticFactorSearch(sample_factors)
        results = searcher.search("diesel", top_k=3)
        
        # Debe encontrar diesel
        assert len(results) > 0
        # El mejor resultado debe tener relación con diesel
        assert 'diesel' in results[0].factor_name.lower() or results[0].match_score > 0.5
    
    def test_search_cache_works(self, sample_factors):
        """Cache debe funcionar."""
        searcher = SemanticFactorSearch(sample_factors)
        
        # Primera búsqueda
        results1 = searcher.search("diesel", top_k=3)
        
        # Segunda búsqueda (debería venir del cache)
        results2 = searcher.search("diesel", top_k=3)
        
        # Deben ser idénticos
        assert len(results1) == len(results2)
        if len(results1) > 0:
            assert results1[0].factor_name == results2[0].factor_name


class TestAIRecommendationEngineSimplified:
    """Pruebas simplificadas para AIRecommendationEngine."""
    
    def test_initialization(self):
        """Debe inicializar correctamente."""
        engine = AIRecommendationEngine()
        assert engine is not None
        assert hasattr(engine, 'SECTOR_BENCHMARKS')
    
    def test_sector_benchmarks_exist(self):
        """Debe tener benchmarks sectoriales."""
        engine = AIRecommendationEngine()
        
        assert 'services' in engine.SECTOR_BENCHMARKS
        assert 'manufacturing' in engine.SECTOR_BENCHMARKS
        assert 'default' in engine.SECTOR_BENCHMARKS
        
        # Valores deben ser positivos
        for sector, value in engine.SECTOR_BENCHMARKS.items():
            assert value > 0
    
    def test_analyze_and_recommend_basic(self):
        """Debe generar recomendaciones básicas."""
        engine = AIRecommendationEngine()
        
        emissions_by_scope = {
            1: 1000.0,  # Scope 1
            2: 5000.0,  # Scope 2 (alto)
            3: 500.0    # Scope 3
        }
        
        emissions_by_category = {
            'mobile_combustion': 1000.0,
            'purchased_electricity': 5000.0,
            'business_travel': 500.0
        }
        
        total = 6500.0
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope,
            emissions_by_category,
            total,
            sector='services',
            num_employees=50
        )
        
        # Debe retornar lista de recomendaciones
        assert isinstance(recommendations, list)
        
        # Si hay recomendaciones, deben tener estructura correcta
        if len(recommendations) > 0:
            rec = recommendations[0]
            assert isinstance(rec, Recommendation)
            assert hasattr(rec, 'priority')
            assert hasattr(rec, 'title')
            assert hasattr(rec, 'description')
    
    def test_recommendations_are_prioritized(self):
        """Recomendaciones deben estar priorizadas."""
        engine = AIRecommendationEngine()
        
        emissions_by_scope = {1: 100.0, 2: 8000.0, 3: 200.0}
        emissions_by_category = {'purchased_electricity': 8000.0, 'mobile_combustion': 100.0}
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope,
            emissions_by_category,
            8300.0
        )
        
        # Debe haber al menos una recomendación
        assert len(recommendations) > 0
        
        # Primera recomendación debe ser alta prioridad (1 o 2)
        assert recommendations[0].priority in [1, 2]
    
    def test_high_scope2_gets_recommendations(self):
        """Scope 2 alto debe generar recomendaciones de electricidad."""
        engine = AIRecommendationEngine()
        
        emissions_by_scope = {1: 100.0, 2: 9000.0, 3: 100.0}
        emissions_by_category = {'purchased_electricity': 9000.0}
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope,
            emissions_by_category,
            9200.0
        )
        
        # Debe generar recomendaciones
        assert len(recommendations) > 0
        
        # Alguna recomendación debe mencionar electricidad o Scope 2
        has_electricity_rec = any(
            'electric' in rec.category.lower() or 'scope 2' in rec.category.lower()
            for rec in recommendations
        )
        assert has_electricity_rec


class TestRecommendationDataclass:
    """Pruebas para dataclass Recommendation."""
    
    def test_create_recommendation(self):
        """Debe crear recomendación válida."""
        rec = Recommendation(
            priority=1,
            category="Scope 2",
            title="Test",
            description="Test description",
            impact_potential="Alto",
            implementation_difficulty="Media",
            estimated_reduction_pct=30.0,
            actions=["Action 1"],
            timeframe="Corto plazo",
            cost_range="$$"
        )
        
        assert rec.priority == 1
        assert rec.category == "Scope 2"
        assert rec.estimated_reduction_pct == 30.0


class TestIntegrationAI:
    """Pruebas de integración simplificadas."""
    
    def test_search_and_recommend_workflow(self):
        """Workflow completo: buscar factor + generar recomendaciones."""
        # 1. Crear searcher
        factors_df = pd.DataFrame([
            {
                'Activity': 'Liquid fuels',
                'Fuel': 'Diesel',
                'kgCO2e': 2.68,
                'Unit': 'litres',
                'Sheet': 'Fuels',
                'Source': 'UK Gov 2025',
                'Year': 2025
            }
        ])
        
        searcher = SemanticFactorSearch(factors_df)
        
        # 2. Buscar diesel
        results = searcher.search("diesel fuel", top_k=1)
        
        # 3. Crear engine de recomendaciones
        engine = AIRecommendationEngine()
        
        # 4. Generar recomendaciones
        emissions_by_scope = {1: 2680.0, 2: 0.0, 3: 0.0}
        emissions_by_category = {'mobile_combustion': 2680.0}
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope,
            emissions_by_category,
            2680.0
        )
        
        # Verificar workflow completo
        assert len(results) > 0
        assert len(recommendations) > 0
        
        # Recomendación debe ser sobre Scope 1 o mobile
        assert any(
            'scope 1' in rec.category.lower() or 'mobile' in rec.category.lower()
            for rec in recommendations
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
