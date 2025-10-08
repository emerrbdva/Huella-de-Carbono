"""
Ejemplo de uso programático del sistema de cálculo de huella de carbono.
Este script muestra cómo usar las librerías sin la interfaz Streamlit.

Ejecutar: python examples/usage_example.py
"""
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime

# Imports del proyecto
from models.emissions import ActivityRecord, EmissionFactor
from utils.data_validator import validate_activity_data
from utils.factors import load_uk_gov_factors, find_factor
from calculators.core import (
    compute_emission,
    aggregate_emissions_by_scope,
    aggregate_emissions_by_category,
    get_total_emissions
)
from calculators.scope1 import calculate_scope1_total
from calculators.scope2 import calculate_scope2_total


def ejemplo_basico():
    """Ejemplo básico de cálculo manual."""
    print("\n" + "="*60)
    print("📌 EJEMPLO 1: Cálculo Básico Manual")
    print("="*60)
    
    # Crear actividad manualmente
    activity = ActivityRecord(
        entity_id="mi_empresa",
        scope=1,
        category="diesel",
        activity_value=1000,
        activity_unit="liters",
        geography="GBR",
        year=2024,
        description="Consumo mensual de diesel en generador"
    )
    
    # Crear factor de emisión manualmente
    # Valor típico de diesel: 2.68 kg CO2e / liter (UK Gov 2025)
    ef = EmissionFactor(
        source="UK2025",
        gas="CO2e",
        value=2.68,
        unit="kg CO2e / liter",
        year=2025,
        scope=1,
        category="diesel",
        geography="GBR"
    )
    
    # Calcular emisión
    result = compute_emission(activity, ef)
    
    # Mostrar resultados
    print(f"\n✅ Resultado:")
    print(f"  Entidad: {result.activity_record.entity_id}")
    print(f"  Scope: {result.activity_record.scope}")
    print(f"  Actividad: {result.activity_record.activity_value} {result.activity_record.activity_unit}")
    print(f"  Factor: {result.emission_factor.value} {result.emission_factor.unit}")
    print(f"  Emisión: {result.emission_kgCO2e:,.2f} kg CO₂e")
    print(f"  Emisión: {result.emission_tCO2e:,.4f} tCO₂e")
    print(f"  Fórmula: {result.calculation_formula}")
    
    return result


def ejemplo_desde_csv():
    """Ejemplo cargando datos desde CSV."""
    print("\n" + "="*60)
    print("📌 EJEMPLO 2: Carga desde CSV con Validación")
    print("="*60)
    
    # Cargar CSV
    csv_path = Path(__file__).parent.parent / 'data' / 'sample_activities.csv'
    print(f"\n📂 Cargando datos desde: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"✓ {len(df)} filas cargadas")
    
    # Validar datos
    print("\n🔍 Validando datos...")
    valid_activities, report = validate_activity_data(df)
    
    print(f"\n📊 Reporte de Validación:")
    print(f"  Total filas: {report.total_rows}")
    print(f"  Filas válidas: {report.valid_rows} ({report.success_rate:.1f}%)")
    print(f"  Filas inválidas: {report.invalid_rows}")
    print(f"  Errores: {len(report.errors)}")
    
    if report.errors:
        print("\n⚠️ Errores encontrados:")
        for error in report.errors[:3]:  # Mostrar primeros 3
            print(f"  - Fila {error.row_number}, campo '{error.field}': {error.error_message}")
    
    # Mostrar primeras actividades válidas
    print(f"\n✅ Primeras 3 actividades válidas:")
    for i, act in enumerate(valid_activities[:3], 1):
        print(f"  {i}. {act.entity_id} | Scope {act.scope} | {act.category} | "
              f"{act.activity_value} {act.activity_unit}")
    
    return valid_activities


def ejemplo_con_factores_reales():
    """Ejemplo usando factores de emisión reales del archivo UK Gov."""
    print("\n" + "="*60)
    print("📌 EJEMPLO 3: Cálculo con Factores Reales UK Gov 2025")
    print("="*60)
    
    # Cargar factores
    factors_path = Path(__file__).parent.parent / 'data' / 'ghg-conversion-factors-2025-condensed-set.xlsx'
    
    if not factors_path.exists():
        print(f"⚠️ Archivo de factores no encontrado: {factors_path}")
        print("   Descarga desde: https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting")
        return None
    
    print(f"\n📂 Cargando factores desde: {factors_path.name}")
    factors_df = load_uk_gov_factors(str(factors_path), year=2025)
    print(f"✓ {len(factors_df)} factores cargados")
    
    # Crear actividad de ejemplo
    activity = ActivityRecord(
        entity_id="oficina_central",
        scope=2,
        category="electricity",
        activity_value=10000,
        activity_unit="kWh",
        geography="GBR",
        year=2024
    )
    
    print(f"\n🔍 Buscando factor para: {activity.category} ({activity.activity_unit})")
    
    # Buscar factor apropiado
    factor_result = find_factor(
        factors_df,
        activity.category,
        activity.activity_unit,
        geography=activity.geography,
        scope=activity.scope
    )
    
    if factor_result:
        factor_value, factor_source, metadata = factor_result
        print(f"✓ Factor encontrado: {factor_value} kg CO₂e/{metadata['unit']}")
        print(f"  Fuente: {factor_source}")
        
        # Crear EmissionFactor
        ef = EmissionFactor(
            source="UK2025",
            gas="CO2e",
            value=factor_value,
            unit=metadata['unit'],
            year=metadata['year'],
            geography=metadata.get('geography'),
            scope=activity.scope,
            category=activity.category
        )
        
        # Calcular
        result = compute_emission(activity, ef)
        
        print(f"\n✅ Resultado:")
        print(f"  Consumo: {activity.activity_value:,} kWh")
        print(f"  Emisión: {result.emission_kgCO2e:,.2f} kg CO₂e")
        print(f"  Emisión: {result.emission_tCO2e:,.4f} tCO₂e")
        
        return result
    else:
        print("❌ No se encontró factor de emisión apropiado")
        return None


def ejemplo_calculo_completo():
    """Ejemplo de cálculo completo con múltiples actividades y agregaciones."""
    print("\n" + "="*60)
    print("📌 EJEMPLO 4: Cálculo Completo con Agregaciones")
    print("="*60)
    
    # Cargar datos
    csv_path = Path(__file__).parent.parent / 'data' / 'sample_activities.csv'
    df = pd.read_csv(csv_path)
    
    # Validar
    valid_activities, report = validate_activity_data(df)
    print(f"\n✓ {len(valid_activities)} actividades válidas para calcular")
    
    # Simular factores (en producción, cargar desde archivo real)
    # Para este ejemplo, usamos factores aproximados
    factor_defaults = {
        1: 2.5,   # Scope 1: ~2.5 kg CO2e por unidad
        2: 0.5,   # Scope 2: ~0.5 kg CO2e/kWh (electricidad)
        3: 0.2    # Scope 3: variable según categoría
    }
    
    results = []
    
    print("\n🧮 Calculando emisiones...")
    for activity in valid_activities:
        # Crear factor genérico para demostración
        factor_value = factor_defaults.get(activity.scope, 1.0)
        
        ef = EmissionFactor(
            source="DEMO",
            gas="CO2e",
            value=factor_value,
            unit=f"kg CO2e / {activity.activity_unit}",
            year=2024,
            scope=activity.scope,
            category=activity.category
        )
        
        result = compute_emission(activity, ef)
        results.append(result)
    
    print(f"✓ {len(results)} emisiones calculadas")
    
    # Agregaciones
    print("\n📊 Agregaciones:")
    
    # Por scope
    scope_totals = aggregate_emissions_by_scope(results)
    print("\n  Por Scope:")
    for scope, total in scope_totals.items():
        if total > 0:
            print(f"    Scope {scope}: {total:,.3f} tCO₂e")
    
    # Por categoría (top 5)
    category_totals = aggregate_emissions_by_category(results)
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    print("\n  Top 5 Categorías:")
    for i, (category, total) in enumerate(sorted_categories[:5], 1):
        print(f"    {i}. {category}: {total:,.3f} tCO₂e")
    
    # Total general
    totals = get_total_emissions(results)
    print(f"\n🌍 TOTAL GENERAL: {totals['total_tonnes_co2e']:,.3f} tCO₂e")
    print(f"   ({totals['total_kg_co2e']:,.0f} kg CO₂e)")
    
    return results


def ejemplo_exportacion():
    """Ejemplo de exportación de resultados."""
    print("\n" + "="*60)
    print("📌 EJEMPLO 5: Exportación de Resultados")
    print("="*60)
    
    # Cargar datos y calcular (versión simplificada)
    csv_path = Path(__file__).parent.parent / 'data' / 'sample_activities.csv'
    df = pd.read_csv(csv_path)
    valid_activities, _ = validate_activity_data(df)
    
    # Calcular resultados (usando factor demo)
    results = []
    for activity in valid_activities[:5]:  # Solo primeras 5 para ejemplo
        ef = EmissionFactor(
            source="DEMO", gas="CO2e", value=1.0,
            unit=f"kg CO2e / {activity.activity_unit}",
            year=2024, scope=activity.scope
        )
        result = compute_emission(activity, ef)
        results.append(result)
    
    # Crear DataFrame de resultados
    results_data = []
    for r in results:
        results_data.append({
            'Fecha_Calculo': r.calculation_date.strftime('%Y-%m-%d'),
            'Entidad': r.activity_record.entity_id,
            'Scope': r.activity_record.scope,
            'Categoría': r.category_label,
            'Actividad_Valor': r.activity_record.activity_value,
            'Actividad_Unidad': r.activity_record.activity_unit,
            'Factor_Valor': r.emission_factor.value,
            'Factor_Unidad': r.emission_factor.unit,
            'Emisión_kgCO2e': round(r.emission_kgCO2e, 2),
            'Emisión_tCO2e': round(r.emission_tCO2e, 4),
            'Fuente_Factor': r.emission_factor.source
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Guardar CSV
    output_path = Path(__file__).parent.parent / 'reports' / f'resultados_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    output_path.parent.mkdir(exist_ok=True)
    results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Resultados exportados a:")
    print(f"   {output_path}")
    print(f"\n📊 Primeras filas del archivo:")
    print(results_df.head().to_string())
    
    return output_path


def main():
    """Ejecutar todos los ejemplos."""
    # Configurar encoding para Windows
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*70)
    print("🌱 EJEMPLOS DE USO - CALCULADORA HUELLA DE CARBONO")
    print("="*70)
    print("Sistema profesional basado en GHG Protocol")
    print("="*70)
    
    try:
        # Ejemplo 1: Básico
        ejemplo_basico()
        
        # Ejemplo 2: Desde CSV
        ejemplo_desde_csv()
        
        # Ejemplo 3: Con factores reales
        ejemplo_con_factores_reales()
        
        # Ejemplo 4: Cálculo completo
        ejemplo_calculo_completo()
        
        # Ejemplo 5: Exportación
        ejemplo_exportacion()
        
        print("\n" + "="*70)
        print("✅ Todos los ejemplos ejecutados exitosamente")
        print("="*70)
        print("\n💡 Próximos pasos:")
        print("  1. Revisa los archivos exportados en /reports")
        print("  2. Adapta estos ejemplos a tus necesidades")
        print("  3. Lee README.md para más detalles")
        print("  4. Ejecuta la app web: streamlit run app/streamlit_app.py")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error al ejecutar ejemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
