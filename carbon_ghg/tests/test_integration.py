"""
Pruebas de integración simplificadas para verificar funcionalidad básica
Ejecutar: pytest tests/test_integration.py -v
"""
import pytest
import pandas as pd
from models.emissions import ActivityRecord, EmissionFactor
from calculators.core import compute_emission


class TestBasicIntegration:
    """Pruebas básicas de integración."""
    
    def test_diesel_calculation(self):
        """Debe calcular emisiones de diesel correctamente."""
        activity = ActivityRecord(
            entity_id="FLEET001",
            scope=1,
            category="mobile_combustion",
            activity_value=1000.0,
            activity_unit="litres",
            geography="GBR",
            year=2025
        )
        
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=2.68,
            unit="kg CO2e / litre",
            year=2025
        )
        
        result = compute_emission(activity, factor)
        
        assert result.emission_kgCO2e == pytest.approx(2680.0, rel=1e-2)
        assert result.emission_tCO2e == pytest.approx(2.68, rel=1e-2)
    
    def test_electricity_calculation(self):
        """Debe calcular emisiones de electricidad correctamente."""
        activity = ActivityRecord(
            entity_id="OFFICE001",
            scope=2,
            category="purchased_electricity",
            activity_value=5000.0,
            activity_unit="kWh",
            geography="GBR",
            year=2025
        )
        
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=0.21233,
            unit="kg CO2e / kWh",
            year=2025
        )
        
        result = compute_emission(activity, factor)
        
        assert result.emission_kgCO2e == pytest.approx(1061.65, rel=1e-2)
    
    def test_activity_record_validation(self):
        """Debe validar correctamente los datos de actividad."""
        # Scope válido
        activity = ActivityRecord(
            entity_id="TEST001",
            scope=1,
            category="mobile_combustion",
            activity_value=100.0,
            activity_unit="liters",
            year=2025
        )
        assert activity.scope == 1
        
        # Scope inválido debe fallar
        with pytest.raises(ValueError):
            ActivityRecord(
                entity_id="TEST002",
                scope=5,  # Inválido
                category="test",
                activity_value=100.0,
                activity_unit="liters",
                year=2025
            )
    
    def test_emission_factor_validation(self):
        """Debe validar correctamente los factores de emisión."""
        # Factor válido
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=2.5,
            unit="kg CO2e / liter",
            year=2025
        )
        assert factor.value > 0
        
        # Valor cero o negativo debe fallar
        with pytest.raises(ValueError):
            EmissionFactor(
                source="TEST",
                gas="CO2",
                value=0,  # Inválido
                unit="kg/liter",
                year=2025
            )
    
    def test_result_properties(self):
        """Debe tener propiedades de resultado correctas."""
        activity = ActivityRecord(
            entity_id="TEST001",
            scope=2,
            category="purchased_electricity",
            activity_value=100.0,
            activity_unit="kWh",
            year=2025
        )
        
        factor = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=0.2,
            unit="kg CO2e / kWh",
            year=2025
        )
        
        result = compute_emission(activity, factor)
        
        assert result.scope_label == "Scope 2"
        assert "Purchased Electricity" in result.category_label


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
