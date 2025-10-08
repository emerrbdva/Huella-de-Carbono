"""
Calculadora para emisiones Scope 2 - Emisiones indirectas de energía comprada.
Categorías: electricidad, calor, vapor, refrigeración.

Referencias:
- GHG Protocol Scope 2 Guidance
- https://ghgprotocol.org/scope-2-guidance
"""
from typing import List, Dict, Optional
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult
from calculators.core import compute_emission
import logging

logger = logging.getLogger(__name__)

# Métodos de cálculo según GHG Protocol Scope 2 Guidance
CALCULATION_METHODS = {
    'location_based': 'Basado en factores promedio de la red eléctrica regional',
    'market_based': 'Basado en contratos específicos de compra de energía (PPAs, RECs)'
}


def calculate_purchased_electricity(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor],
    method: str = 'location_based'
) -> List[EmissionResult]:
    """
    Calcula emisiones de electricidad comprada.
    
    Métodos según GHG Protocol Scope 2:
    1. Location-based: usa grid average emission factor (factor promedio de red)
    2. Market-based: usa factores específicos de contratos o certificados
    
    Formula:
        E = Electricity_consumed (kWh) × EF_grid (kg CO2e/kWh)
        
    Args:
        activities: Actividades de consumo eléctrico
        factors: Factores de emisión de red eléctrica por región
        method: 'location_based' o 'market_based'
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        # Buscar factor apropiado por geografía
        matching_factor = find_electricity_factor(activity, factors, method)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                
                # Agregar nota sobre método usado
                if result.conversion_notes:
                    result.conversion_notes += f"; Método Scope 2: {method}"
                else:
                    result.conversion_notes = f"Método Scope 2: {method}"
                
                results.append(result)
                logger.info(
                    f"Electricidad calculada ({method}): {result.emission_tCO2e:.3f} tCO2e | "
                    f"{activity.geography or 'No geography'}"
                )
            except Exception as e:
                logger.error(f"Error calculando electricidad {activity.entity_id}: {e}")
        else:
            logger.warning(
                f"No se encontró factor de electricidad para {activity.geography or 'sin geografía'} "
                f"con método {method}"
            )
    
    return results


def calculate_purchased_heat_steam(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de calor/vapor comprado (district heating, steam).
    
    Formula:
        E = Heat_consumed (GJ) × EF_heat (kg CO2e/GJ)
        
    Args:
        activities: Actividades de consumo de calor/vapor
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope2_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Calor/vapor calculado: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error calculando calor/vapor {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para calor/vapor: {activity.category}")
    
    return results


def calculate_purchased_cooling(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de refrigeración comprada (district cooling).
    
    Formula:
        E = Cooling_consumed (kWh or GJ) × EF_cooling (kg CO2e/kWh)
        
    Args:
        activities: Actividades de consumo de refrigeración
        factors: Factores de emisión aplicables
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope2_factor(activity, factors)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Refrigeración calculada: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error calculando refrigeración {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para refrigeración: {activity.category}")
    
    return results


def calculate_scope2_total(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor],
    include_market_based: bool = False
) -> Dict:
    """
    Calcula todas las emisiones de Scope 2.
    
    Según GHG Protocol, las empresas deben reportar:
    - Location-based (obligatorio)
    - Market-based (opcional pero recomendado)
    
    Args:
        activities: Todas las actividades de Scope 2
        factors: Factores de emisión disponibles
        include_market_based: Si True, calcula ambos métodos
        
    Returns:
        Diccionario con resultados por categoría y método
    """
    scope2_activities = [a for a in activities if a.scope == 2]
    
    # Separar por categoría
    electricity = [a for a in scope2_activities if 'electric' in a.category.lower()]
    heat_steam = [a for a in scope2_activities if 'heat' in a.category.lower() or 'steam' in a.category.lower()]
    cooling = [a for a in scope2_activities if 'cool' in a.category.lower()]
    
    # Location-based (obligatorio)
    electricity_lb = calculate_purchased_electricity(electricity, factors, 'location_based')
    heat_steam_results = calculate_purchased_heat_steam(heat_steam, factors)
    cooling_results = calculate_purchased_cooling(cooling, factors)
    
    location_based_results = electricity_lb + heat_steam_results + cooling_results
    location_based_total = sum(r.emission_tCO2e for r in location_based_results)
    
    result = {
        'scope': 2,
        'location_based': {
            'categories': {
                'purchased_electricity': {
                    'count': len(electricity_lb),
                    'total_tCO2e': sum(r.emission_tCO2e for r in electricity_lb)
                },
                'purchased_heat_steam': {
                    'count': len(heat_steam_results),
                    'total_tCO2e': sum(r.emission_tCO2e for r in heat_steam_results)
                },
                'purchased_cooling': {
                    'count': len(cooling_results),
                    'total_tCO2e': sum(r.emission_tCO2e for r in cooling_results)
                }
            },
            'total_tCO2e': location_based_total,
            'total_activities': len(location_based_results),
            'results': location_based_results
        }
    }
    
    # Market-based (opcional)
    if include_market_based:
        electricity_mb = calculate_purchased_electricity(electricity, factors, 'market_based')
        market_based_results = electricity_mb + heat_steam_results + cooling_results
        market_based_total = sum(r.emission_tCO2e for r in market_based_results)
        
        result['market_based'] = {
            'total_tCO2e': market_based_total,
            'total_activities': len(market_based_results),
            'results': market_based_results,
            'note': 'Requiere factores específicos de contratos de energía (PPAs, RECs)'
        }
    
    return result


def find_electricity_factor(
    activity: ActivityRecord,
    factors: List[EmissionFactor],
    method: str = 'location_based'
) -> Optional[EmissionFactor]:
    """
    Encuentra el factor de electricidad apropiado por geografía y método.
    
    Args:
        activity: Actividad de consumo eléctrico
        factors: Lista de factores disponibles
        method: 'location_based' o 'market_based'
        
    Returns:
        Factor de emisión más apropiado
    """
    geography = activity.geography
    
    # Filtrar factores de electricidad
    electricity_factors = [
        f for f in factors
        if f.scope == 2 and 'electric' in (f.category or '').lower()
    ]
    
    if not electricity_factors:
        return None
    
    # Búsqueda por geografía exacta
    if geography:
        for factor in electricity_factors:
            if factor.geography and factor.geography.upper() == geography.upper():
                return factor
    
    # Si no hay geografía o no se encuentra, usar primer factor disponible
    return electricity_factors[0] if electricity_factors else None


def find_best_scope2_factor(
    activity: ActivityRecord,
    factors: List[EmissionFactor]
) -> Optional[EmissionFactor]:
    """
    Encuentra el mejor factor de Scope 2 para cualquier categoría.
    
    Args:
        activity: Actividad de Scope 2
        factors: Lista de factores disponibles
        
    Returns:
        Factor de emisión más apropiado
    """
    # Filtrar por Scope 2
    scope2_factors = [f for f in factors if f.scope == 2]
    
    # Búsqueda por categoría y geografía
    for factor in scope2_factors:
        if (factor.category and factor.category.lower() in activity.category.lower() and
            factor.geography and factor.geography == activity.geography):
            return factor
    
    # Búsqueda solo por categoría
    for factor in scope2_factors:
        if factor.category and factor.category.lower() in activity.category.lower():
            return factor
    
    # Búsqueda genérica
    category_keywords = activity.category.lower().split('_')
    for factor in scope2_factors:
        if factor.category:
            if any(kw in factor.category.lower() for kw in category_keywords):
                return factor
    
    return None
