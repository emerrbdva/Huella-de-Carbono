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
        assert result.emission_kgCO2e == pytest.approx(2680.0, rel=1e-2)
        assert result.activity_record.entity_id == "TEST001"
        assert result.activity_record.scope == 1
    
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
        
        assert result.emission_kgCO2e == pytest.approx(4.41, rel=1e-2)
    
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
        
        assert result.emission_kgCO2e == pytest.approx(101500.0, rel=1e-2)
    
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
            source="TEST",
            gas="CO2e",
            value=0.12345,
            unit="kg CO2e / km",
            year=2025,
            geography="Global",
            scope=3,
            category="business_travel"
        )
        
        result = compute_emission(activity, factor)
        
        # 123.456 * 0.12345 = 15.241632
        assert result.emission_kgCO2e == pytest.approx(15.241632, rel=1e-4)



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


class TestIntegrationCalculations:
    """Pruebas de integración completas."""
    
    def test_diesel_fleet_calculation(self, sample_diesel_activity, sample_diesel_factor):
        """Debe calcular emisiones de flota diesel correctamente."""
        result = compute_emission(sample_diesel_activity, sample_diesel_factor)
        
        assert result.emission_kgCO2e > 0
        assert result.activity_record.scope == 1
        assert result.activity_record.category == "mobile_combustion"
    
    def test_electricity_office_calculation(self, sample_electricity_activity, sample_electricity_factor):
        """Debe calcular emisiones de electricidad correctamente."""
        result = compute_emission(sample_electricity_activity, sample_electricity_factor)
        
        assert result.emission_kgCO2e > 0
        assert result.activity_record.scope == 2
        assert result.activity_record.category in ["purchased_electricity", "electricity_grid"]
    
    def test_full_workflow(self, sample_diesel_activity, sample_diesel_factor,
                          sample_electricity_activity, sample_electricity_factor):
        """Debe ejecutar flujo completo: calcular + agregar."""
        # Calcular emisiones
        result1 = compute_emission(sample_diesel_activity, sample_diesel_factor)
        result2 = compute_emission(sample_electricity_activity, sample_electricity_factor)
        
        results = [result1, result2]
        
        # Agregar por alcance
        by_scope = aggregate_emissions_by_scope(results)
        assert by_scope[1] > 0  # Scope 1 (diesel)
        assert by_scope[2] > 0  # Scope 2 (electricity)
        
        # Agregar por categoría
        by_category = aggregate_emissions_by_category(results)
        assert len(by_category) >= 2  # Al menos 2 categorías
        
        # Verificar totales
        total_emissions = sum(r.emission_tCO2e for r in results)
        assert total_emissions > 0
