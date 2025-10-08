"""
Calculadora para emisiones Scope 1 - Emisiones directas.
Categorías: combustión estacionaria, combustión móvil, emisiones de proceso, fugitivas.

Referencias:
- GHG Protocol Corporate Standard, Chapter 4
- https://ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf
"""
from typing import List, Dict
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult
from calculators.core import compute_emission
import logging

logger = logging.getLogger(__name__)

# Categorías de Scope 1 según GHG Protocol
STATIONARY_COMBUSTION_FUELS = [
    'natural_gas', 'coal', 'diesel', 'fuel_oil', 'propane', 'butane', 
    'lpg', 'biomass', 'waste', 'other_petroleum_products'
]

MOBILE_COMBUSTION_FUELS = [
    'gasoline', 'diesel', 'lpg', 'cng', 'lng', 'aviation_gasoline',
    'jet_fuel', 'marine_fuel', 'biofuels'
]

PROCESS_EMISSION_TYPES = [
    'cement_production', 'lime_production', 'glass_production',
    'ammonia_production', 'iron_steel', 'aluminum_production',
    'chemical_reactions', 'carbonate_use'
]

FUGITIVE_EMISSION_SOURCES = [
    'refrigerants', 'air_conditioning', 'fire_suppression',
    'natural_gas_leakage', 'oil_gas_equipment', 'coal_mining',
    'wastewater_treatment'
]


def calculate_stationary_combustion(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de combustión estacionaria (calderas, generadores, hornos).
    
    Formula típica:
        E_CO2 = Fuel_consumed × EF_fuel × Oxidation_factor
        
    Args:
        activities: Actividades de combustión estacionaria
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        # Buscar factor apropiado
        matching_factor = find_best_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Combustión estacionaria calculada: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en combustión estacionaria {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para combustión estacionaria: {activity.category}")
    
    return results


def calculate_mobile_combustion(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de combustión móvil (vehículos, equipos móviles).
    
    Métodos:
    1. Fuel-based (litros/galones de combustible)
    2. Distance-based (km recorridos × factor por tipo de vehículo)
    3. Spend-based (gasto monetario × factor económico)
    
    Args:
        activities: Actividades de transporte/movilidad
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Combustión móvil calculada: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en combustión móvil {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para combustión móvil: {activity.category}")
    
    return results


def calculate_process_emissions(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de procesos industriales (reacciones químicas, producción).
    
    Ejemplos:
    - Producción de cemento: calcinación de carbonato de calcio
    - Producción de ácido nítrico: emisiones de N2O
    - Producción de aluminio: emisiones de PFC
    
    Args:
        activities: Actividades de proceso industrial
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Proceso industrial calculado: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en proceso industrial {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para proceso: {activity.category}")
    
    return results


def calculate_fugitive_emissions(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones fugitivas (fugas de refrigerantes, CH4 de sistemas, etc.).
    
    Fuentes comunes:
    - Equipos de refrigeración y aire acondicionado (HFCs, CFCs)
    - Sistemas de extinción de incendios (HFCs, PFCs)
    - Fugas de gas natural en tuberías
    - Emisiones de minas de carbón
    
    Args:
        activities: Actividades con emisiones fugitivas
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Emisión fugitiva calculada: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en emisión fugitiva {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para fugitiva: {activity.category}")
    
    return results


def calculate_scope1_total(activities: List[ActivityRecord], factors: List[EmissionFactor]) -> Dict:
    """
    Calcula todas las emisiones de Scope 1 por categoría.
    
    Args:
        activities: Todas las actividades de Scope 1
        factors: Factores de emisión disponibles
        
    Returns:
        Diccionario con resultados por categoría y total
    """
    # Filtrar solo actividades de Scope 1
    scope1_activities = [a for a in activities if a.scope == 1]
    
    # Separar por categoría
    stationary = [a for a in scope1_activities if 'stationary' in a.category.lower() or 'combustion' in a.category.lower()]
    mobile = [a for a in scope1_activities if 'mobile' in a.category.lower() or 'vehicle' in a.category.lower() or 'transport' in a.category.lower()]
    process = [a for a in scope1_activities if 'process' in a.category.lower()]
    fugitive = [a for a in scope1_activities if 'fugitive' in a.category.lower() or 'refrigerant' in a.category.lower()]
    
    # Calcular cada categoría
    stationary_results = calculate_stationary_combustion(stationary, factors) if stationary else []
    mobile_results = calculate_mobile_combustion(mobile, factors) if mobile else []
    process_results = calculate_process_emissions(process, factors) if process else []
    fugitive_results = calculate_fugitive_emissions(fugitive, factors) if fugitive else []
    
    # Consolidar
    all_results = stationary_results + mobile_results + process_results + fugitive_results
    
    total_tco2e = sum(r.emission_tCO2e for r in all_results)
    
    return {
        'scope': 1,
        'categories': {
            'stationary_combustion': {
                'count': len(stationary_results),
                'total_tCO2e': sum(r.emission_tCO2e for r in stationary_results)
            },
            'mobile_combustion': {
                'count': len(mobile_results),
                'total_tCO2e': sum(r.emission_tCO2e for r in mobile_results)
            },
            'process_emissions': {
                'count': len(process_results),
                'total_tCO2e': sum(r.emission_tCO2e for r in process_results)
            },
            'fugitive_emissions': {
                'count': len(fugitive_results),
                'total_tCO2e': sum(r.emission_tCO2e for r in fugitive_results)
            }
        },
        'total_tCO2e': total_tco2e,
        'total_activities': len(all_results),
        'results': all_results
    }


def find_best_factor(activity: ActivityRecord, factors: List[EmissionFactor]) -> EmissionFactor:
    """
    Encuentra el mejor factor de emisión para una actividad dada.
    
    Prioridad de búsqueda:
    1. Coincidencia exacta de categoría y geografía
    2. Coincidencia de categoría
    3. Coincidencia parcial por palabras clave
    
    Args:
        activity: Actividad a emparejar
        factors: Lista de factores disponibles
        
    Returns:
        Factor de emisión más apropiado o None
    """
    # Búsqueda exacta
    for factor in factors:
        if (factor.category and factor.category.lower() == activity.category.lower() and
            factor.geography and factor.geography == activity.geography):
            return factor
    
    # Búsqueda por categoría sin geografía
    for factor in factors:
        if factor.category and factor.category.lower() == activity.category.lower():
            return factor
    
    # Búsqueda parcial por palabras clave
    category_keywords = activity.category.lower().split('_')
    for factor in factors:
        if factor.category:
            factor_keywords = factor.category.lower().split('_')
            if any(kw in factor_keywords for kw in category_keywords):
                return factor
    
    return None
