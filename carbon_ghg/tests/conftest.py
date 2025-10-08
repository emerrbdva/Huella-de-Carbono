"""
Pytest fixtures and configuration for Carbon GHG Calculator tests.

This module provides reusable test fixtures that match the current
Pydantic models structure.
"""

import pytest
import pandas as pd
from datetime import datetime
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult


@pytest.fixture
def sample_activity():
    """Create a valid ActivityRecord for testing"""
    return ActivityRecord(
        entity_id="test-factory-1",
        scope=1,
        category="mobile_combustion",
        activity_value=1000.0,
        activity_unit="liters",
        geography="GBR",
        year=2025,
        date=datetime(2025, 1, 15)
    )


@pytest.fixture
def sample_diesel_activity():
    """Create a diesel activity record"""
    return ActivityRecord(
        entity_id="fleet-vehicle-01",
        scope=1,
        category="mobile_combustion",
        activity_value=500.0,
        activity_unit="liters",
        geography="GBR",
        year=2025,
        date=datetime(2025, 2, 1)
    )


@pytest.fixture
def sample_electricity_activity():
    """Create an electricity activity record"""
    return ActivityRecord(
        entity_id="office-building-01",
        scope=2,
        category="electricity_grid",
        activity_value=10000.0,
        activity_unit="kWh",
        geography="GBR",
        year=2025,
        date=datetime(2025, 3, 1)
    )


@pytest.fixture
def sample_factor():
    """Create a valid EmissionFactor for testing"""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68442,
        unit="kg CO2e / liters",
        year=2025,
        geography="GBR",
        scope=1,
        category="mobile_combustion"
    )


@pytest.fixture
def sample_diesel_factor():
    """Create a diesel emission factor"""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68442,
        unit="kg CO2e / liters",
        year=2025,
        geography="GBR",
        scope=1,
        category="mobile_combustion"
    )


@pytest.fixture
def sample_electricity_factor():
    """Create an electricity emission factor"""
    return EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=0.17704,
        unit="kg CO2e / kWh",
        year=2025,
        geography="GBR",
        scope=2,
        category="purchased_electricity"
    )


@pytest.fixture
def sample_result(sample_activity, sample_diesel_factor):
    """Create a valid EmissionResult for testing"""
    return EmissionResult(
        activity_record=sample_activity,
        emission_factor=sample_diesel_factor,
        emission_kgCO2e=2684.42,
        emission_tCO2e=2.68442,
        calculation_formula="E = AD × EF"
    )


@pytest.fixture
def sample_emission_results():
    """Create a list of EmissionResult objects for aggregation tests"""
    # Create activity records
    activity1 = ActivityRecord(
        entity_id="factory-1",
        scope=1,
        category="mobile_combustion",
        activity_value=1000.0,
        activity_unit="liters",
        geography="GBR",
        year=2025
    )
    activity2 = ActivityRecord(
        entity_id="office-1",
        scope=2,
        category="purchased_electricity",
        activity_value=10000.0,
        activity_unit="kWh",
        geography="GBR",
        year=2025
    )
    activity3 = ActivityRecord(
        entity_id="warehouse-1",
        scope=1,
        category="stationary_combustion",
        activity_value=500.0,
        activity_unit="kWh",
        geography="GBR",
        year=2025
    )
    
    # Create emission factors
    factor1 = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68442,
        unit="kg CO2e / liters",
        year=2025,
        geography="GBR",
        scope=1,
        category="mobile_combustion"
    )
    factor2 = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=0.17704,
        unit="kg CO2e / kWh",
        year=2025,
        geography="GBR",
        scope=2,
        category="purchased_electricity"
    )
    factor3 = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=0.21,
        unit="kg CO2e / kWh",
        year=2025,
        geography="GBR",
        scope=1,
        category="stationary_combustion"
    )
    
    return [
        EmissionResult(
            activity_record=activity1,
            emission_factor=factor1,
            emission_kgCO2e=2684.42,
            emission_tCO2e=2.68442
        ),
        EmissionResult(
            activity_record=activity2,
            emission_factor=factor2,
            emission_kgCO2e=1770.4,
            emission_tCO2e=1.7704
        ),
        EmissionResult(
            activity_record=activity3,
            emission_factor=factor3,
            emission_kgCO2e=105.0,
            emission_tCO2e=0.105
        )
    ]


@pytest.fixture
def sample_factors_dataframe():
    """Create a sample factors DataFrame for testing"""
    return pd.DataFrame([
        {
            "category": "mobile_combustion",
            "unit": "liters",
            "co2_factor": 2.68442,
            "ch4_factor": 0.00015,
            "n2o_factor": 0.0001,
            "co2e_factor": 2.68442,
            "source": "UK Gov 2025 - Diesel",
            "geography": "GBR",
            "scope": 1
        },
        {
            "category": "electricity_grid",
            "unit": "kWh",
            "co2_factor": 0.17,
            "ch4_factor": 0.0,
            "n2o_factor": 0.0,
            "co2e_factor": 0.17704,
            "source": "UK Gov 2025 - Grid",
            "geography": "GBR",
            "scope": 2
        },
        {
            "category": "mobile_combustion",
            "unit": "km",
            "co2_factor": 0.15,
            "ch4_factor": 0.00001,
            "n2o_factor": 0.000005,
            "co2e_factor": 0.15234,
            "source": "UK Gov 2025 - Petrol Car",
            "geography": "GBR",
            "scope": 1
        }
    ])


# Pytest configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "ai: mark test as requiring AI/Ollama (deselect with '-m \"not ai\"')"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
