"""
Motor de cálculo de emisiones GHG Protocol.
Implementa la fórmula base: E = AD × EF
Soporta conversión de unidades y GWP para conversión a CO2e.
"""
from typing import List, Optional, Dict
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult, GWP_AR5
from utils.unit_converter import convert_unit, are_units_compatible
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def compute_emission(
    activity: ActivityRecord, 
    ef: EmissionFactor,
    auto_convert_units: bool = True
) -> EmissionResult:
    """
    Calcula emisiones usando la fórmula: Emisiones = Dato de Actividad × Factor de Emisión.
    
    Args:
        activity: Registro de actividad validado
        ef: Factor de emisión aplicable
        auto_convert_units: Si True, intenta convertir unidades automáticamente
        
    Returns:
        Resultado de emisión con trazabilidad completa
        
    Raises:
        ValueError: Si las unidades son incompatibles y no se puede convertir
        
    Formula:
        E_CO2e = AD × EF × GWP
        
        Donde:
        - E_CO2e: Emisiones en kg CO2 equivalente
        - AD: Dato de actividad (activity_value)
        - EF: Factor de emisión (ef.value)
        - GWP: Global Warming Potential (para convertir otros gases a CO2e)
        
    Referencias:
        - IPCC 2006 Guidelines, Volume 1, Chapter 2
        - https://www.ipcc-nggip.iges.or.jp/support/Primer_2006GLs.pdf
    """
    conversion_notes = []
    
    # Paso 1: Verificar y convertir unidades si es necesario
    activity_value = activity.activity_value
    
    # Extraer unidad del factor de emisión (formato típico: "kg CO2e / kWh")
    ef_activity_unit = extract_activity_unit_from_ef(ef.unit)
    
    if activity.activity_unit.lower() != ef_activity_unit.lower():
        if auto_convert_units and are_units_compatible(activity.activity_unit, ef_activity_unit):
            converted_value = convert_unit(activity_value, activity.activity_unit, ef_activity_unit)
            if converted_value is not None:
                conversion_notes.append(
                    f"Conversión de unidades: {activity_value} {activity.activity_unit} "
                    f"→ {converted_value:.4f} {ef_activity_unit}"
                )
                activity_value = converted_value
                logger.info(f"Unidades convertidas: {activity.activity_unit} → {ef_activity_unit}")
            else:
                raise ValueError(
                    f"No se pudo convertir {activity.activity_unit} a {ef_activity_unit}"
                )
        else:
            logger.warning(
                f"Unidades no coinciden: actividad={activity.activity_unit}, factor={ef_activity_unit}. "
                f"Usando valor directo."
            )
            conversion_notes.append(
                f"⚠️ ADVERTENCIA: Unidades no coinciden ({activity.activity_unit} vs {ef_activity_unit}). "
                f"Resultado puede ser incorrecto."
            )
    
    # Paso 2: Calcular emisión base (E = AD × EF)
    emission_kg = activity_value * ef.value
    
    # Paso 3: Aplicar GWP si el gas no es CO2e
    gwp_factor = 1.0
    if ef.gas.upper() != 'CO2E':
        gwp_factor = GWP_AR5.get(ef.gas.upper(), 1.0)
        if gwp_factor != 1.0:
            emission_kg *= gwp_factor
            conversion_notes.append(
                f"Conversión GWP (AR5): {ef.gas} × {gwp_factor} → CO2e"
            )
            logger.info(f"GWP aplicado para {ef.gas}: factor={gwp_factor}")
    
    # Paso 4: Convertir a toneladas
    emission_tonnes = emission_kg / 1000.0
    
    # Paso 5: Construir fórmula descriptiva
    formula = f"E = {activity_value:.2f} {ef_activity_unit} × {ef.value} kg CO2e/{ef_activity_unit}"
    if gwp_factor != 1.0:
        formula += f" × {gwp_factor} (GWP)"
    formula += f" = {emission_kg:.2f} kg CO2e"
    
    # Paso 6: Crear resultado con trazabilidad completa
    result = EmissionResult(
        activity_record=activity,
        emission_factor=ef,
        emission_kgCO2e=emission_kg,
        emission_tCO2e=emission_tonnes,
        calculation_date=datetime.now(),
        calculation_formula=formula,
        conversion_notes="; ".join(conversion_notes) if conversion_notes else None,
        quality_flag="OK" if not conversion_notes else "WARNING"
    )
    
    logger.info(
        f"✓ Emisión calculada: {emission_kg:.2f} kg CO2e | "
        f"Entidad: {activity.entity_id} | Scope {activity.scope} | {activity.category}"
    )
    
    return result


def extract_activity_unit_from_ef(ef_unit_string: str) -> str:
    """
    Extrae la unidad de actividad de una cadena de unidad de factor de emisión.
    
    Args:
        ef_unit_string: Cadena como "kg CO2e / kWh" o "kg CO2e per tonne"
        
    Returns:
        Unidad de actividad extraída (ej: "kWh", "tonne")
        
    Example:
        >>> extract_activity_unit_from_ef("kg CO2e / kWh")
        'kWh'
        >>> extract_activity_unit_from_ef("kg CO2e per passenger.km")
        'passenger.km'
    """
    separators = [' / ', ' per ', '/', 'per']
    
    for sep in separators:
        if sep in ef_unit_string:
            parts = ef_unit_string.split(sep)
            if len(parts) >= 2:
                return parts[-1].strip()
    
    # Si no se encuentra separador, devolver la cadena completa
    logger.warning(f"No se pudo extraer unidad de actividad de '{ef_unit_string}', usando cadena completa")
    return ef_unit_string.strip()


def compute_batch_emissions(
    activities: List[ActivityRecord],
    emission_factors: List[EmissionFactor],
    factor_matching_func=None
) -> List[EmissionResult]:
    """
    Calcula emisiones para un lote de actividades.
    
    Args:
        activities: Lista de registros de actividad
        emission_factors: Lista de factores de emisión disponibles
        factor_matching_func: Función opcional para emparejar actividades con factores
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        # Si hay función de emparejamiento personalizada, usarla
        if factor_matching_func:
            matched_ef = factor_matching_func(activity, emission_factors)
        else:
            # Emparejamiento simple por categoría
            matched_ef = next(
                (ef for ef in emission_factors if ef.category == activity.category),
                None
            )
        
        if matched_ef:
            try:
                result = compute_emission(activity, matched_ef)
                results.append(result)
            except Exception as e:
                logger.error(f"Error calculando emisión para {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor de emisión para actividad: {activity.category}")
    
    return results


def aggregate_emissions_by_scope(results: List[EmissionResult]) -> Dict[int, float]:
    """
    Agrega emisiones por Scope (1, 2, 3).
    
    Args:
        results: Lista de resultados de emisión
        
    Returns:
        Diccionario {scope: total_tCO2e}
    """
    aggregation = {1: 0.0, 2: 0.0, 3: 0.0}
    
    for result in results:
        scope = result.activity_record.scope
        aggregation[scope] += result.emission_tCO2e
    
    return aggregation


def aggregate_emissions_by_category(results: List[EmissionResult]) -> Dict[str, float]:
    """
    Agrega emisiones por categoría.
    
    Args:
        results: Lista de resultados de emisión
        
    Returns:
        Diccionario {category: total_tCO2e}
    """
    aggregation = {}
    
    for result in results:
        category = result.activity_record.category
        if category not in aggregation:
            aggregation[category] = 0.0
        aggregation[category] += result.emission_tCO2e
    
    return aggregation


def aggregate_emissions_by_entity(results: List[EmissionResult]) -> Dict[str, float]:
    """
    Agrega emisiones por entidad.
    
    Args:
        results: Lista de resultados de emisión
        
    Returns:
        Diccionario {entity_id: total_tCO2e}
    """
    aggregation = {}
    
    for result in results:
        entity = result.activity_record.entity_id
        if entity not in aggregation:
            aggregation[entity] = 0.0
        aggregation[entity] += result.emission_tCO2e
    
    return aggregation


def get_total_emissions(results: List[EmissionResult]) -> Dict[str, float]:
    """
    Calcula totales generales de emisiones.
    
    Args:
        results: Lista de resultados de emisión
        
    Returns:
        Diccionario con totales en diferentes unidades
    """
    total_kg = sum(r.emission_kgCO2e for r in results)
    total_tonnes = sum(r.emission_tCO2e for r in results)
    
    return {
        'total_kg_co2e': total_kg,
        'total_tonnes_co2e': total_tonnes,
        'total_metric_tons_co2e': total_tonnes,  # Alias
        'count_activities': len(results)
    }
