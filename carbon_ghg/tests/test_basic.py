"""
Script de prueba básico para verificar el funcionamiento del sistema.
Ejecutar: python tests/test_basic.py
"""
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from models.emissions import ActivityRecord, EmissionFactor, GWP_AR5
from calculators.core import compute_emission, aggregate_emissions_by_scope
from utils.data_validator import validate_activity_data
from utils.unit_converter import convert_unit, get_unit_category

def test_models():
    """Prueba modelos Pydantic."""
    print("\n🧪 Probando modelos Pydantic...")
    
    # Test ActivityRecord
    activity = ActivityRecord(
        entity_id="test_entity",
        scope=1,
        category="stationary_combustion",
        activity_value=1000,
        activity_unit="liters",
        geography="GBR",
        year=2024
    )
    print(f"✓ ActivityRecord creado: {activity.entity_id} - Scope {activity.scope}")
    
    # Test EmissionFactor
    ef = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68,
        unit="kg CO2e / liter",
        year=2025,
        scope=1
    )
    print(f"✓ EmissionFactor creado: {ef.value} {ef.unit}")
    
    return True


def test_calculation():
    """Prueba cálculo de emisiones."""
    print("\n🧮 Probando cálculo de emisiones...")
    
    activity = ActivityRecord(
        entity_id="factory_test",
        scope=1,
        category="diesel",
        activity_value=100,
        activity_unit="liters",
        year=2024
    )
    
    ef = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68,  # kg CO2e / liter (diesel típico)
        unit="kg CO2e / liter",
        year=2025,
        scope=1,
        category="diesel"
    )
    
    result = compute_emission(activity, ef)
    
    print(f"✓ Cálculo completado:")
    print(f"  - Actividad: {activity.activity_value} {activity.activity_unit}")
    print(f"  - Factor: {ef.value} {ef.unit}")
    print(f"  - Emisión: {result.emission_kgCO2e:.2f} kg CO2e")
    print(f"  - Emisión: {result.emission_tCO2e:.4f} tCO2e")
    print(f"  - Fórmula: {result.calculation_formula}")
    
    assert result.emission_kgCO2e == 268.0, "Error en cálculo de emisión"
    
    return True


def test_unit_conversion():
    """Prueba conversión de unidades."""
    print("\n🔄 Probando conversión de unidades...")
    
    # Energía
    kwh_to_mj = convert_unit(100, 'kWh', 'MJ')
    print(f"✓ 100 kWh = {kwh_to_mj} MJ")
    assert kwh_to_mj == 360.0, "Error en conversión kWh a MJ"
    
    # Masa
    kg_to_tonnes = convert_unit(5000, 'kg', 'tonnes')
    print(f"✓ 5000 kg = {kg_to_tonnes} tonnes")
    assert kg_to_tonnes == 5.0, "Error en conversión kg a tonnes"
    
    # Volumen
    liters_to_m3 = convert_unit(1000, 'liters', 'm3')
    print(f"✓ 1000 liters = {liters_to_m3} m³")
    assert liters_to_m3 == 1.0, "Error en conversión liters a m³"
    
    # Distancia
    miles_to_km = convert_unit(100, 'miles', 'km')
    print(f"✓ 100 miles = {miles_to_km:.2f} km")
    assert round(miles_to_km, 2) == 160.93, "Error en conversión miles a km"
    
    # Categoría de unidad
    cat_energy = get_unit_category('kWh')
    cat_mass = get_unit_category('kg')
    print(f"✓ Categoría kWh: {cat_energy}")
    print(f"✓ Categoría kg: {cat_mass}")
    
    return True


def test_validation():
    """Prueba validación de datos."""
    print("\n✅ Probando validación de datos...")
    
    # Datos válidos
    data_valid = {
        'entity_id': ['test1', 'test2'],
        'scope': [1, 2],
        'category': ['diesel', 'electricity'],
        'activity_value': [100, 5000],
        'activity_unit': ['liters', 'kWh'],
        'year': [2024, 2024]
    }
    df_valid = pd.DataFrame(data_valid)
    
    valid_records, report = validate_activity_data(df_valid)
    
    print(f"✓ Validación completada:")
    print(f"  - Total filas: {report.total_rows}")
    print(f"  - Filas válidas: {report.valid_rows}")
    print(f"  - Tasa de éxito: {report.success_rate:.1f}%")
    
    assert report.success_rate == 100.0, "Error en validación de datos válidos"
    
    # Datos inválidos
    data_invalid = {
        'entity_id': ['test3'],
        'scope': [5],  # Scope inválido
        'category': ['test'],
        'activity_value': [-100],  # Valor negativo
        'activity_unit': ['liters']
    }
    df_invalid = pd.DataFrame(data_invalid)
    
    invalid_records, report_invalid = validate_activity_data(df_invalid)
    
    print(f"\n✓ Validación de datos inválidos:")
    print(f"  - Errores detectados: {len(report_invalid.errors)}")
    
    assert len(report_invalid.errors) > 0, "Error: debería detectar errores"
    
    return True


def test_gwp():
    """Prueba valores GWP."""
    print("\n🌍 Probando GWP (Global Warming Potential)...")
    
    print(f"✓ GWP AR5 (100 años):")
    print(f"  - CO2: {GWP_AR5['CO2']}")
    print(f"  - CH4: {GWP_AR5['CH4']}")
    print(f"  - N2O: {GWP_AR5['N2O']}")
    print(f"  - SF6: {GWP_AR5['SF6']}")
    
    assert GWP_AR5['CH4'] == 28, "Error en GWP de CH4"
    assert GWP_AR5['N2O'] == 265, "Error en GWP de N2O"
    
    return True


def test_aggregation():
    """Prueba agregación de resultados."""
    print("\n📊 Probando agregación de resultados...")
    
    # Crear resultados de ejemplo
    from models.emissions import EmissionResult
    from datetime import datetime
    
    results = []
    for scope in [1, 1, 2, 3]:
        activity = ActivityRecord(
            entity_id=f"entity_{scope}",
            scope=scope,
            category=f"cat_{scope}",
            activity_value=100,
            activity_unit="kWh"
        )
        ef = EmissionFactor(
            source="TEST",
            gas="CO2e",
            value=0.5,
            unit="kg CO2e / kWh",
            year=2024,
            scope=scope
        )
        result = EmissionResult(
            activity_record=activity,
            emission_factor=ef,
            emission_kgCO2e=50,
            emission_tCO2e=0.05,
            calculation_date=datetime.now(),
            calculation_formula="E = 100 × 0.5"
        )
        results.append(result)
    
    # Agregar por scope
    scope_agg = aggregate_emissions_by_scope(results)
    
    print(f"✓ Agregación por Scope:")
    for scope, total in scope_agg.items():
        print(f"  - Scope {scope}: {total:.3f} tCO2e")
    
    assert scope_agg[1] == 0.1, "Error en agregación Scope 1"
    assert scope_agg[2] == 0.05, "Error en agregación Scope 2"
    assert scope_agg[3] == 0.05, "Error en agregación Scope 3"
    
    return True


def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("🧪 EJECUTANDO PRUEBAS DEL SISTEMA")
    print("=" * 60)
    
    tests = [
        ("Modelos Pydantic", test_models),
        ("Cálculo de Emisiones", test_calculation),
        ("Conversión de Unidades", test_unit_conversion),
        ("Validación de Datos", test_validation),
        ("GWP Values", test_gwp),
        ("Agregación", test_aggregation)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {name}: PASÓ")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name}: FALLÓ - {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed} pruebas pasaron, {failed} fallaron")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print(f"\n⚠️ {failed} prueba(s) fallaron. Revisa los errores arriba.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
