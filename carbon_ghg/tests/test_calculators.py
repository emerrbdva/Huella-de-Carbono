"""
Pruebas unitarias para módulo calculators.core
Ejecutar: pytest tests/test_calculators.py -v
"""
import pytest
import pandas as pd
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult
from calculators.core import (
    compute_emission,
    aggregate_emissions_by_scope,
    aggregate_emissions_by_category
)


class TestComputeEmission:
    """Pruebas para función compute_emission."""
    
    def test_basic_emission_calculation(self):
        """Debe calcular emisiones correctamente."""
        activity = ActivityRecord(
            entity_id="TEST001",
            scope=1,
            category="mobile_combustion",
            activity_value=1000.0,
            activity_unit="liters",
            geography="GBR",
            year=2025
        )
        
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=2.68,
            unit="kg CO2e / liter",
            year=2025,
            scope=1
        )
        
        result = compute_emission(activity, factor)
        
        assert isinstance(result, EmissionResult)
        assert result.co2e_kg == pytest.approx(2680.0, rel=1e-2)
        assert result.entity_id == "TEST001"
        assert result.scope == 1
    
    def test_small_value_calculation(self):
        """Debe manejar valores pequeños correctamente."""
        activity = ActivityRecord(
            entity_id="TEST002",
            scope=2,
            category="purchased_electricity",
            activity_value=10.5,
            activity_unit="kWh",
            geography="USA",
            year=2025
        )
        
        factor = EmissionFactor(
            source="EPA2025",
            gas="CO2e",
            value=0.42,
            unit="kg CO2e / kWh",
            year=2025,
            scope=2
        )
        
        result = compute_emission(activity, factor)
        
        assert result.co2e_kg == pytest.approx(4.41, rel=1e-2)
    
    def test_large_value_calculation(self):
        """Debe manejar valores grandes correctamente."""
        activity = ActivityRecord(
            entity_id="TEST003",
            scope=1,
            category="stationary_combustion",
            activity_value=50000.0,
            activity_unit="m3",
            geography="GBR",
            year=2025
        )
        
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=2.03,
            unit="kg CO2e / m3",
            year=2025,
            scope=1
        )
        
        result = compute_emission(activity, factor)
        
        assert result.co2e_kg == pytest.approx(101500.0, rel=1e-2)
    
    def test_decimal_precision(self):
        """Debe mantener precisión decimal adecuada."""
        activity = ActivityRecord(
            entity_id="TEST004",
            scope=3,
            category="business_travel",
            activity_value=123.456,
            activity_unit="km",
            geography="Global",
            year=2025
        )
        
        factor = EmissionFactor(
            source="DEFRA2025",
            gas="CO2e",
            value=0.12345,
            unit="kg CO2e / km",
            year=2025,
            scope=3
        )
        
        result = compute_emission(activity, factor)
        
        # 123.456 * 0.12345 = 15.241632
        assert result.co2e_kg == pytest.approx(15.241632, rel=1e-4)


class TestAggregateByScope:
    """Pruebas para agregación por alcance."""
    
    def test_aggregate_single_scope(self):
        """Debe agregar correctamente un solo alcance."""
        results = [
            EmissionResult(
                entity_id="E001",
                scope=1,
                category="mobile",
                co2e_kg=1000.0,
                activity_value=100,
                activity_unit="liters",
                emission_factor_value=10,
                emission_factor_unit="kg/liter",
                year=2025
            ),
            EmissionResult(
                entity_id="E002",
                scope=1,
                category="stationary",
                co2e_kg=2000.0,
                activity_value=200,
                activity_unit="m3",
                emission_factor_value=10,
                emission_factor_unit="kg/m3",
                year=2025
            )
        ]
        
        df = pd.DataFrame([r.dict() for r in results])
        agg = aggregate_emissions_by_scope(df)
        
        assert len(agg) == 1
        assert agg.iloc[0]['scope'] == 1
        assert agg.iloc[0]['total_co2e_kg'] == pytest.approx(3000.0)
    
    def test_aggregate_multiple_scopes(self):
        """Debe agregar correctamente múltiples alcances."""
        results = [
            EmissionResult(
                entity_id="E001",
                scope=1,
                category="mobile",
                co2e_kg=1000.0,
                activity_value=100,
                activity_unit="liters",
                emission_factor_value=10,
                emission_factor_unit="kg/liter",
                year=2025
            ),
            EmissionResult(
                entity_id="E002",
                scope=2,
                category="electricity",
                co2e_kg=2000.0,
                activity_value=200,
                activity_unit="kWh",
                emission_factor_value=10,
                emission_factor_unit="kg/kWh",
                year=2025
            ),
            EmissionResult(
                entity_id="E003",
                scope=3,
                category="travel",
                co2e_kg=3000.0,
                activity_value=300,
                activity_unit="km",
                emission_factor_value=10,
                emission_factor_unit="kg/km",
                year=2025
            )
        ]
        
        df = pd.DataFrame([r.dict() for r in results])
        agg = aggregate_emissions_by_scope(df)
        
        assert len(agg) == 3
        assert agg['total_co2e_kg'].sum() == pytest.approx(6000.0)
    
    def test_aggregate_empty_dataframe(self):
        """Debe manejar DataFrame vacío."""
        df = pd.DataFrame(columns=['scope', 'co2e_kg'])
        agg = aggregate_emissions_by_scope(df)
        
        assert len(agg) == 0


class TestAggregateByCategory:
    """Pruebas para agregación por categoría."""
    
    def test_aggregate_single_category(self):
        """Debe agregar correctamente una sola categoría."""
        results = [
            EmissionResult(
                entity_id="E001",
                scope=1,
                category="mobile_combustion",
                co2e_kg=500.0,
                activity_value=100,
                activity_unit="liters",
                emission_factor_value=5,
                emission_factor_unit="kg/liter",
                year=2025
            ),
            EmissionResult(
                entity_id="E002",
                scope=1,
                category="mobile_combustion",
                co2e_kg=800.0,
                activity_value=160,
                activity_unit="liters",
                emission_factor_value=5,
                emission_factor_unit="kg/liter",
                year=2025
            )
        ]
        
        df = pd.DataFrame([r.dict() for r in results])
        agg = aggregate_emissions_by_category(df)
        
        assert len(agg) == 1
        assert agg.iloc[0]['category'] == 'mobile_combustion'
        assert agg.iloc[0]['total_co2e_kg'] == pytest.approx(1300.0)
    
    def test_aggregate_multiple_categories(self):
        """Debe agregar correctamente múltiples categorías."""
        results = [
            EmissionResult(
                entity_id="E001",
                scope=1,
                category="mobile_combustion",
                co2e_kg=1000.0,
                activity_value=100,
                activity_unit="liters",
                emission_factor_value=10,
                emission_factor_unit="kg/liter",
                year=2025
            ),
            EmissionResult(
                entity_id="E002",
                scope=1,
                category="stationary_combustion",
                co2e_kg=2000.0,
                activity_value=200,
                activity_unit="m3",
                emission_factor_value=10,
                emission_factor_unit="kg/m3",
                year=2025
            ),
            EmissionResult(
                entity_id="E003",
                scope=2,
                category="purchased_electricity",
                co2e_kg=1500.0,
                activity_value=150,
                activity_unit="kWh",
                emission_factor_value=10,
                emission_factor_unit="kg/kWh",
                year=2025
            )
        ]
        
        df = pd.DataFrame([r.dict() for r in results])
        agg = aggregate_emissions_by_category(df)
        
        assert len(agg) == 3
        assert agg['total_co2e_kg'].sum() == pytest.approx(4500.0)
    
    def test_category_sorting(self):
        """Debe ordenar categorías por emisiones (descendente)."""
        results = [
            EmissionResult(
                entity_id="E001",
                scope=1,
                category="cat_low",
                co2e_kg=500.0,
                activity_value=100,
                activity_unit="units",
                emission_factor_value=5,
                emission_factor_unit="kg/unit",
                year=2025
            ),
            EmissionResult(
                entity_id="E002",
                scope=1,
                category="cat_high",
                co2e_kg=3000.0,
                activity_value=300,
                activity_unit="units",
                emission_factor_value=10,
                emission_factor_unit="kg/unit",
                year=2025
            ),
            EmissionResult(
                entity_id="E003",
                scope=1,
                category="cat_medium",
                co2e_kg=1500.0,
                activity_value=150,
                activity_unit="units",
                emission_factor_value=10,
                emission_factor_unit="kg/unit",
                year=2025
            )
        ]
        
        df = pd.DataFrame([r.dict() for r in results])
        agg = aggregate_emissions_by_category(df)
        
        # Debe estar ordenado descendente
        assert agg.iloc[0]['category'] == 'cat_high'
        assert agg.iloc[1]['category'] == 'cat_medium'
        assert agg.iloc[2]['category'] == 'cat_low'


# Fixtures
@pytest.fixture
def sample_activity_diesel():
    """Actividad de ejemplo: consumo diesel."""
    return ActivityRecord(
        entity_id="FLEET001",
        scope=1,
        category="mobile_combustion",
        activity_value=1000.0,
        activity_unit="liters",
        geography="GBR",
        year=2025,
        description="Diesel para flota de camiones"
    )


@pytest.fixture
def sample_factor_diesel():
    """Factor de emisión: diesel."""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68,
        unit="kg CO2e / liter",
        year=2025,
        scope=1,
        category="mobile_combustion"
    )


@pytest.fixture
def sample_activity_electricity():
    """Actividad de ejemplo: electricidad."""
    return ActivityRecord(
        entity_id="OFFICE001",
        scope=2,
        category="purchased_electricity",
        activity_value=5000.0,
        activity_unit="kWh",
        geography="GBR",
        year=2025,
        description="Electricidad oficina central"
    )


@pytest.fixture
def sample_factor_electricity():
    """Factor de emisión: electricidad UK."""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=0.21233,
        unit="kg CO2e / kWh",
        year=2025,
        scope=2,
        category="purchased_electricity"
    )


class TestIntegrationCalculations:
    """Pruebas de integración completas."""
    
    def test_diesel_fleet_calculation(self, sample_activity_diesel, sample_factor_diesel):
        """Debe calcular emisiones de flota diesel correctamente."""
        result = compute_emission(sample_activity_diesel, sample_factor_diesel)
        
        assert result.co2e_kg == pytest.approx(2680.0, rel=1e-2)
        assert result.scope == 1
        assert result.category == "mobile_combustion"
    
    def test_electricity_office_calculation(self, sample_activity_electricity, sample_factor_electricity):
        """Debe calcular emisiones de electricidad correctamente."""
        result = compute_emission(sample_activity_electricity, sample_factor_electricity)
        
        assert result.co2e_kg == pytest.approx(1061.65, rel=1e-2)
        assert result.scope == 2
        assert result.category == "purchased_electricity"
    
    def test_full_workflow(self, sample_activity_diesel, sample_factor_diesel,
                          sample_activity_electricity, sample_factor_electricity):
        """Debe ejecutar flujo completo: calcular + agregar."""
        # Calcular emisiones
        result1 = compute_emission(sample_activity_diesel, sample_factor_diesel)
        result2 = compute_emission(sample_activity_electricity, sample_factor_electricity)
        
        # Crear DataFrame
        df = pd.DataFrame([result1.dict(), result2.dict()])
        
        # Agregar por alcance
        by_scope = aggregate_emissions_by_scope(df)
        assert len(by_scope) == 2  # Scope 1 y 2
        
        # Agregar por categoría
        by_category = aggregate_emissions_by_category(df)
        assert len(by_category) == 2  # mobile_combustion y purchased_electricity
        
        # Verificar totales
        total_emissions = df['co2e_kg'].sum()
        assert total_emissions == pytest.approx(3741.65, rel=1e-2)
