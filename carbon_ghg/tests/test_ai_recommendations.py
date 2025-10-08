"""
Pruebas unitarias para módulo utils.ai_recommendations
Ejecutar: pytest tests/test_ai_recommendations.py -v
"""
import pytest
from utils.ai_recommendations import (
    AIRecommendationEngine,
    Recommendation
)


class TestRecommendation:
    """Pruebas para dataclass Recommendation."""
    
    def test_create_recommendation(self):
        """Debe crear una recomendación válida."""
        rec = Recommendation(
            priority=1,
            category="Scope 2 - Electricidad",
            title="Transición a Energía Renovable",
            description="Cambiar a fuentes renovables",
            impact_potential="Alto",
            implementation_difficulty="Media",
            estimated_reduction_pct=50.0,
            actions=["Contratar PPA", "Instalar paneles solares"],
            timeframe="Mediano plazo (6-18 meses)",
            cost_range="$$"
        )
        
        assert rec.priority == 1
        assert rec.category == "Scope 2 - Electricidad"
        assert rec.estimated_reduction_pct == 50.0
        assert len(rec.actions) == 2


class TestSectorBenchmarks:
    """Pruebas para benchmarks sectoriales."""
    
    @pytest.fixture
    def engine(self):
        """Instancia del engine."""
        return AIRecommendationEngine()
    
    def test_benchmark_structure(self, engine):
        """Debe contener benchmarks para sectores clave."""
        assert 'services' in engine.SECTOR_BENCHMARKS
        assert 'manufacturing' in engine.SECTOR_BENCHMARKS
        assert 'transport' in engine.SECTOR_BENCHMARKS
        assert 'retail' in engine.SECTOR_BENCHMARKS
        assert 'technology' in engine.SECTOR_BENCHMARKS
        assert 'default' in engine.SECTOR_BENCHMARKS
    
    def test_benchmark_values_positive(self, engine):
        """Todos los benchmarks deben ser positivos."""
        for sector, value in engine.SECTOR_BENCHMARKS.items():
            assert value > 0
    
    def test_benchmark_reasonable_ranges(self, engine):
        """Los benchmarks deben estar en rangos razonables."""
        for sector, value in engine.SECTOR_BENCHMARKS.items():
            assert 500 <= value <= 20000  # kg CO2e/empleado/año


class TestAIRecommendationEngine:
    """Pruebas para motor de recomendaciones."""
    
    @pytest.fixture
    def engine(self):
        """Instancia del motor de recomendaciones."""
        return AIRecommendationEngine()
    
    def test_initialization(self, engine):
        """Debe inicializar correctamente."""
        assert isinstance(engine, AIRecommendationEngine)
    
    def test_analyze_high_scope2(self, engine):
        """Debe recomendar energía renovable para Scope 2 alto."""
        emissions_by_scope = {
            1: 1000.0,
            2: 5000.0,  # 71% del total
            3: 1000.0
        }
        
        emissions_by_category = {
            'purchased_electricity': 5000.0,
            'mobile_combustion': 1000.0,
            'business_travel': 1000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=7000.0,
            sector='services',
            num_employees=50
        )
        
        # Debe haber recomendación de energía renovable (prioridad 1)
        renewable_rec = [r for r in recommendations if 'Renovable' in r.title]
        assert len(renewable_rec) > 0
        assert renewable_rec[0].priority == 1
    
    def test_analyze_high_scope1(self, engine):
        """Debe recomendar optimización para Scope 1 alto."""
        emissions_by_scope = {
            1: 4000.0,  # 67% del total
            2: 1000.0,
            3: 1000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 3000.0,
            'stationary_combustion': 1000.0,
            'purchased_electricity': 1000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=6000.0,
            sector='transport',
            num_employees=100
        )
        
        # Debe haber recomendación de optimización (prioridad 1)
        assert len(recommendations) > 0
        high_priority = [r for r in recommendations if r.priority == 1]
        assert len(high_priority) > 0
    
    def test_analyze_mobile_combustion(self, engine):
        """Debe recomendar electrificación para combustión móvil."""
        emissions_by_scope = {
            1: 3000.0,
            2: 1500.0,
            3: 500.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 3000.0,  # Principal categoría
            'purchased_electricity': 1500.0,
            'business_travel': 500.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=5000.0,
            sector='default',
            num_employees=25
        )
        
        # Debe haber recomendación de electrificación
        electric_rec = [r for r in recommendations if 'Electrificación' in r.title or 'Flota' in r.title]
        assert len(electric_rec) > 0
    
    def test_analyze_business_travel(self, engine):
        """Debe recomendar política de viajes para travel alto."""
        emissions_by_scope = {
            1: 500.0,
            2: 1000.0,
            3: 3000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 500.0,
            'purchased_electricity': 1000.0,
            'business_travel': 3000.0  # Principal categoría
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=4500.0,
            sector='services',
            num_employees=30
        )
        
        # Debe haber recomendación de viajes sostenibles
        travel_rec = [r for r in recommendations if 'Viaje' in r.title or 'Travel' in r.category]
        assert len(travel_rec) > 0
    
    def test_benchmark_comparison_above(self, engine):
        """Debe detectar emisiones por encima del benchmark."""
        # services benchmark = 2500 kg/empleado/año
        # 50 empleados * 2500 = 125,000 kg
        # Probamos con 150,000 kg (+20%)
        
        emissions_by_scope = {
            1: 50000.0,
            2: 80000.0,
            3: 20000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 50000.0,
            'purchased_electricity': 80000.0,
            'business_travel': 20000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=150000.0,
            sector='services',
            num_employees=50
        )
        
        # Debe haber recomendación de reducción urgente
        urgent_rec = [r for r in recommendations if 'Urgente' in r.title or r.priority == 1]
        assert len(urgent_rec) > 0
    
    def test_benchmark_comparison_below(self, engine):
        """Debe reconocer emisiones por debajo del benchmark."""
        # services benchmark = 2500 kg/empleado/año
        # 50 empleados * 2500 = 125,000 kg
        # Probamos con 80,000 kg (-36%, debajo de -20%)
        
        emissions_by_scope = {
            1: 30000.0,
            2: 40000.0,
            3: 10000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 30000.0,
            'purchased_electricity': 40000.0,
            'business_travel': 10000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=80000.0,
            sector='services',
            num_employees=50
        )
        
        # Debe haber recomendación de liderazgo (prioridad 3)
        leadership_rec = [r for r in recommendations if 'Liderazgo' in r.title]
        assert len(leadership_rec) > 0
        assert leadership_rec[0].priority == 3
    
    def test_general_recommendations(self, engine):
        """Debe incluir recomendaciones generales siempre."""
        emissions_by_scope = {
            1: 1000.0,
            2: 1000.0,
            3: 1000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 1000.0,
            'purchased_electricity': 1000.0,
            'business_travel': 1000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=3000.0,
            sector='default',
            num_employees=10
        )
        
        # Debe haber al menos 2 recomendaciones generales
        general_rec = [r for r in recommendations if r.priority == 3]
        assert len(general_rec) >= 2
    
    def test_priority_sorting(self, engine):
        """Las recomendaciones deben estar ordenadas por prioridad."""
        emissions_by_scope = {
            1: 2000.0,
            2: 4000.0,
            3: 1000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 2000.0,
            'purchased_electricity': 4000.0,
            'business_travel': 1000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=7000.0,
            sector='manufacturing',
            num_employees=75
        )
        
        # Verificar que están ordenadas: prioridad 1, luego 2, luego 3
        priorities = [r.priority for r in recommendations]
        assert priorities == sorted(priorities)
    
    def test_reduction_percentages_valid(self, engine):
        """Todos los porcentajes de reducción deben ser válidos."""
        emissions_by_scope = {
            1: 1500.0,
            2: 2500.0,
            3: 1000.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 1500.0,
            'purchased_electricity': 2500.0,
            'business_travel': 1000.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=5000.0,
            sector='retail',
            num_employees=40
        )
        
        for rec in recommendations:
            assert 0 <= rec.estimated_reduction_pct <= 100
    
    def test_summary_report_generation(self, engine):
        """Debe generar reporte resumen en Markdown."""
        emissions_by_scope = {
            1: 1000.0,
            2: 2000.0,
            3: 500.0
        }
        
        emissions_by_category = {
            'mobile_combustion': 1000.0,
            'purchased_electricity': 2000.0,
            'business_travel': 500.0
        }
        
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope=emissions_by_scope,
            emissions_by_category=emissions_by_category,
            total_emissions=3500.0,
            sector='technology',
            num_employees=20
        )
        
        report = engine.generate_summary_report(recommendations)
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert '# Reporte de Recomendaciones' in report or 'Recomendaciones' in report
        assert 'Total de recomendaciones' in report or str(len(recommendations)) in report


class TestEdgeCases:
    """Pruebas de casos límite."""
    
    @pytest.fixture
    def engine(self):
        return AIRecommendationEngine()
    
    def test_zero_emissions(self, engine):
        """Debe manejar emisiones cero."""
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope={1: 0, 2: 0, 3: 0},
            emissions_by_category={},
            total_emissions=0,
            sector='default',
            num_employees=1
        )
        
        # Debe retornar al menos recomendaciones generales
        assert len(recommendations) >= 1
    
    def test_no_employees(self, engine):
        """Debe manejar cero empleados (o None)."""
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope={1: 1000, 2: 1000, 3: 1000},
            emissions_by_category={'mobile_combustion': 3000},
            total_emissions=3000,
            sector='default',
            num_employees=None
        )
        
        # Debe funcionar sin comparación con benchmark
        assert len(recommendations) >= 1
    
    def test_very_high_emissions(self, engine):
        """Debe manejar emisiones muy altas."""
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope={1: 1000000, 2: 2000000, 3: 500000},
            emissions_by_category={'mobile_combustion': 1000000, 'purchased_electricity': 2000000},
            total_emissions=3500000,
            sector='manufacturing',
            num_employees=500
        )
        
        assert len(recommendations) > 0
        # Debe haber recomendaciones de alta prioridad
        high_priority = [r for r in recommendations if r.priority == 1]
        assert len(high_priority) > 0
    
    def test_unknown_sector(self, engine):
        """Debe usar benchmark default para sector desconocido."""
        recommendations = engine.analyze_and_recommend(
            emissions_by_scope={1: 1000, 2: 1000, 3: 1000},
            emissions_by_category={'mobile_combustion': 3000},
            total_emissions=3000,
            sector='unknown_sector_xyz',
            num_employees=10
        )
        
        # Debe funcionar con benchmark default
        assert len(recommendations) > 0


# Fixtures para pruebas de integración
@pytest.fixture
def realistic_emissions_services():
    """Emisiones realistas de empresa de servicios."""
    return {
        'emissions_by_scope': {
            1: 3400.0,  # Flota de vehículos
            2: 8500.0,  # Electricidad oficinas
            3: 2100.0   # Viajes de negocios
        },
        'emissions_by_category': {
            'mobile_combustion': 3400.0,
            'purchased_electricity': 8500.0,
            'business_travel': 2100.0
        },
        'total_emissions': 14000.0,
        'sector': 'services',
        'num_employees': 50
    }


@pytest.fixture
def realistic_emissions_manufacturing():
    """Emisiones realistas de empresa manufacturera."""
    return {
        'emissions_by_scope': {
            1: 120000.0,  # Combustión directa
            2: 180000.0,  # Electricidad planta
            3: 50000.0    # Cadena de suministro
        },
        'emissions_by_category': {
            'stationary_combustion': 80000.0,
            'mobile_combustion': 40000.0,
            'purchased_electricity': 180000.0,
            'upstream_transport': 30000.0,
            'waste_disposal': 20000.0
        },
        'total_emissions': 350000.0,
        'sector': 'manufacturing',
        'num_employees': 200
    }


class TestRealisticScenarios:
    """Pruebas con escenarios realistas."""
    
    def test_services_company(self, realistic_emissions_services):
        """Debe analizar correctamente empresa de servicios."""
        engine = AIRecommendationEngine()
        recommendations = engine.analyze_and_recommend(**realistic_emissions_services)
        
        assert len(recommendations) >= 5
        
        # Debe recomendar energía renovable (Scope 2 alto: 61%)
        renewable_rec = [r for r in recommendations if 'Renovable' in r.title]
        assert len(renewable_rec) > 0
        
        # Debe haber mix de prioridades
        priorities = set(r.priority for r in recommendations)
        assert len(priorities) >= 2
    
    def test_manufacturing_company(self, realistic_emissions_manufacturing):
        """Debe analizar correctamente empresa manufacturera."""
        engine = AIRecommendationEngine()
        recommendations = engine.analyze_and_recommend(**realistic_emissions_manufacturing)
        
        assert len(recommendations) >= 5
        
        # Scope 2 es 51% del total, debe recomendar energía renovable
        renewable_rec = [r for r in recommendations if 'Renovable' in r.title]
        assert len(renewable_rec) > 0
        
        # Total es 350k con 200 empleados = 1750 kg/empleado/año
        # Manufacturing benchmark = 8000, está bien debajo (-78%)
        # Debe haber recomendación de liderazgo
        leadership_rec = [r for r in recommendations if 'Liderazgo' in r.title]
        assert len(leadership_rec) > 0
