"""
Calculadora para emisiones Scope 3 - Otras emisiones indirectas de la cadena de valor.
15 categorías según GHG Protocol.

Referencias:
- GHG Protocol Corporate Value Chain (Scope 3) Standard
- https://ghgprotocol.org/standards/scope-3-standard
"""
from typing import List, Dict, Optional
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult
from calculators.core import compute_emission
import logging

logger = logging.getLogger(__name__)

# 15 Categorías de Scope 3 según GHG Protocol
SCOPE_3_CATEGORY_DESCRIPTIONS = {
    1: {
        'name': 'purchased_goods_services',
        'title': 'Bienes y Servicios Comprados',
        'description': 'Extracción, producción y transporte de bienes y servicios comprados',
        'type': 'upstream'
    },
    2: {
        'name': 'capital_goods',
        'title': 'Bienes de Capital',
        'description': 'Extracción, producción y transporte de bienes de capital',
        'type': 'upstream'
    },
    3: {
        'name': 'fuel_energy_activities',
        'title': 'Actividades Relacionadas con Combustible y Energía',
        'description': 'Extracción, producción y transporte de combustibles y energía no incluidos en Scope 1 y 2',
        'type': 'upstream'
    },
    4: {
        'name': 'upstream_transportation',
        'title': 'Transporte y Distribución Upstream',
        'description': 'Transporte de bienes comprados y otros servicios de transporte',
        'type': 'upstream'
    },
    5: {
        'name': 'waste_generated',
        'title': 'Residuos Generados en Operaciones',
        'description': 'Eliminación y tratamiento de residuos generados en operaciones propias',
        'type': 'upstream'
    },
    6: {
        'name': 'business_travel',
        'title': 'Viajes de Negocio',
        'description': 'Transporte de empleados para actividades relacionadas con el negocio',
        'type': 'upstream'
    },
    7: {
        'name': 'employee_commuting',
        'title': 'Desplazamientos de Empleados',
        'description': 'Transporte de empleados entre casa y trabajo',
        'type': 'upstream'
    },
    8: {
        'name': 'upstream_leased_assets',
        'title': 'Activos Arrendados Upstream',
        'description': 'Operación de activos arrendados por la empresa (no incluidos en Scope 1 y 2)',
        'type': 'upstream'
    },
    9: {
        'name': 'downstream_transportation',
        'title': 'Transporte y Distribución Downstream',
        'description': 'Transporte y distribución de productos vendidos',
        'type': 'downstream'
    },
    10: {
        'name': 'processing_sold_products',
        'title': 'Procesamiento de Productos Vendidos',
        'description': 'Procesamiento de productos intermedios vendidos por terceros',
        'type': 'downstream'
    },
    11: {
        'name': 'use_sold_products',
        'title': 'Uso de Productos Vendidos',
        'description': 'Uso final de productos vendidos por consumidores',
        'type': 'downstream'
    },
    12: {
        'name': 'end_of_life_sold_products',
        'title': 'Fin de Vida de Productos Vendidos',
        'description': 'Eliminación y tratamiento al final de vida de productos vendidos',
        'type': 'downstream'
    },
    13: {
        'name': 'downstream_leased_assets',
        'title': 'Activos Arrendados Downstream',
        'description': 'Operación de activos propiedad de la empresa pero arrendados a otros',
        'type': 'downstream'
    },
    14: {
        'name': 'franchises',
        'title': 'Franquicias',
        'description': 'Operación de franquicias',
        'type': 'downstream'
    },
    15: {
        'name': 'investments',
        'title': 'Inversiones',
        'description': 'Operación de inversiones (acciones, bonos, etc.)',
        'type': 'downstream'
    }
}


def calculate_business_travel(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de viajes de negocio (Categoría 6).
    
    Métodos:
    1. Distance-based: km × factor por modo de transporte
    2. Spend-based: gasto $ × factor económico
    3. Fuel-based: combustible usado × factor
    
    Args:
        activities: Actividades de viajes de negocio
        factors: Factores de emisión por modo de transporte
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope3_factor(activity, factors, category_num=6)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Viaje de negocio calculado: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en viaje de negocio {activity.entity_id}: {e}")
        else:
            logger.warning(f"No se encontró factor para viaje: {activity.category}")
    
    return results


def calculate_employee_commuting(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de desplazamientos de empleados (Categoría 7).
    
    Formula típica:
        E = Employees × Avg_distance × Days × EF_transport_mode
        
    Args:
        activities: Actividades de desplazamientos
        factors: Factores por modo de transporte
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope3_factor(activity, factors, category_num=7)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Desplazamiento empleados calculado: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en desplazamiento {activity.entity_id}: {e}")
    
    return results


def calculate_purchased_goods_services(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de bienes y servicios comprados (Categoría 1).
    
    Métodos:
    1. Supplier-specific: datos directos de proveedores
    2. Hybrid: combinación de métodos
    3. Average-data: factores promedio por industria
    4. Spend-based: gasto $ × factor económico
    
    Args:
        activities: Actividades de compras
        factors: Factores de emisión por tipo de bien/servicio
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope3_factor(activity, factors, category_num=1)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Bienes/servicios comprados: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en compras {activity.entity_id}: {e}")
    
    return results


def calculate_waste_generated(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de residuos generados (Categoría 5).
    
    Formula:
        E = Waste_amount × EF_disposal_method
        
    Métodos de disposición:
    - Landfill (vertedero)
    - Incineration (incineración)
    - Recycling (reciclaje)
    - Composting (compostaje)
    
    Args:
        activities: Actividades de generación de residuos
        factors: Factores por tipo de residuo y método de disposición
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope3_factor(activity, factors, category_num=5)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Residuos calculados: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en residuos {activity.entity_id}: {e}")
    
    return results


def calculate_upstream_transportation(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> List[EmissionResult]:
    """
    Calcula emisiones de transporte upstream (Categoría 4).
    
    Formula:
        E = Distance × Weight × EF_transport_mode
        (en tonne-km × factor)
        
    Args:
        activities: Actividades de transporte de materias primas
        factors: Factores por modo de transporte
        
    Returns:
        Lista de resultados de emisión
    """
    results = []
    
    for activity in activities:
        matching_factor = find_best_scope3_factor(activity, factors, category_num=4)
        
        if matching_factor:
            try:
                result = compute_emission(activity, matching_factor)
                results.append(result)
                logger.info(f"Transporte upstream: {result.emission_tCO2e:.3f} tCO2e")
            except Exception as e:
                logger.error(f"Error en transporte upstream {activity.entity_id}: {e}")
    
    return results


def calculate_scope3_total(
    activities: List[ActivityRecord],
    factors: List[EmissionFactor]
) -> Dict:
    """
    Calcula todas las emisiones de Scope 3 por categoría.
    
    Args:
        activities: Todas las actividades de Scope 3
        factors: Factores de emisión disponibles
        
    Returns:
        Diccionario con resultados por categoría y total
    """
    # Filtrar solo Scope 3
    scope3_activities = [a for a in activities if a.scope == 3]
    
    # Separar por categoría
    categories = {
        6: [],  # business_travel
        7: [],  # employee_commuting
        1: [],  # purchased_goods_services
        5: [],  # waste_generated
        4: [],  # upstream_transportation
    }
    
    for activity in scope3_activities:
        cat_name = activity.category.lower()
        if 'travel' in cat_name or 'flight' in cat_name:
            categories[6].append(activity)
        elif 'commut' in cat_name or 'employee' in cat_name:
            categories[7].append(activity)
        elif 'waste' in cat_name or 'disposal' in cat_name:
            categories[5].append(activity)
        elif 'transport' in cat_name or 'freight' in cat_name:
            categories[4].append(activity)
        elif 'goods' in cat_name or 'service' in cat_name or 'purchas' in cat_name:
            categories[1].append(activity)
    
    # Calcular cada categoría
    all_results = []
    category_results = {}
    
    if categories[6]:
        results_6 = calculate_business_travel(categories[6], factors)
        all_results.extend(results_6)
        category_results[6] = {
            'name': 'business_travel',
            'count': len(results_6),
            'total_tCO2e': sum(r.emission_tCO2e for r in results_6)
        }
    
    if categories[7]:
        results_7 = calculate_employee_commuting(categories[7], factors)
        all_results.extend(results_7)
        category_results[7] = {
            'name': 'employee_commuting',
            'count': len(results_7),
            'total_tCO2e': sum(r.emission_tCO2e for r in results_7)
        }
    
    if categories[5]:
        results_5 = calculate_waste_generated(categories[5], factors)
        all_results.extend(results_5)
        category_results[5] = {
            'name': 'waste_generated',
            'count': len(results_5),
            'total_tCO2e': sum(r.emission_tCO2e for r in results_5)
        }
    
    if categories[4]:
        results_4 = calculate_upstream_transportation(categories[4], factors)
        all_results.extend(results_4)
        category_results[4] = {
            'name': 'upstream_transportation',
            'count': len(results_4),
            'total_tCO2e': sum(r.emission_tCO2e for r in results_4)
        }
    
    if categories[1]:
        results_1 = calculate_purchased_goods_services(categories[1], factors)
        all_results.extend(results_1)
        category_results[1] = {
            'name': 'purchased_goods_services',
            'count': len(results_1),
            'total_tCO2e': sum(r.emission_tCO2e for r in results_1)
        }
    
    total_tco2e = sum(r.emission_tCO2e for r in all_results)
    
    return {
        'scope': 3,
        'categories': category_results,
        'total_tCO2e': total_tco2e,
        'total_activities': len(all_results),
        'results': all_results,
        'note': 'Scope 3 incluye 15 categorías. Solo se calcularon las categorías con datos disponibles.'
    }


def find_best_scope3_factor(
    activity: ActivityRecord,
    factors: List[EmissionFactor],
    category_num: Optional[int] = None
) -> Optional[EmissionFactor]:
    """
    Encuentra el mejor factor de Scope 3 para una actividad.
    
    Args:
        activity: Actividad de Scope 3
        factors: Lista de factores disponibles
        category_num: Número de categoría Scope 3 (1-15)
        
    Returns:
        Factor de emisión más apropiado
    """
    # Filtrar por Scope 3
    scope3_factors = [f for f in factors if f.scope == 3]
    
    # Si se especifica categoría, filtrar
    if category_num and category_num in SCOPE_3_CATEGORY_DESCRIPTIONS:
        category_name = SCOPE_3_CATEGORY_DESCRIPTIONS[category_num]['name']
        category_factors = [
            f for f in scope3_factors
            if f.category and category_name in f.category.lower()
        ]
        if category_factors:
            scope3_factors = category_factors
    
    # Búsqueda por categoría y geografía
    for factor in scope3_factors:
        if (factor.category and factor.category.lower() in activity.category.lower() and
            factor.geography and factor.geography == activity.geography):
            return factor
    
    # Búsqueda solo por categoría
    for factor in scope3_factors:
        if factor.category and factor.category.lower() in activity.category.lower():
            return factor
    
    # Búsqueda parcial
    activity_keywords = activity.category.lower().split('_')
    for factor in scope3_factors:
        if factor.category:
            if any(kw in factor.category.lower() for kw in activity_keywords):
                return factor
    
    return None


def get_scope3_category_info(category_num: int) -> Dict:
    """
    Obtiene información detallada de una categoría de Scope 3.
    
    Args:
        category_num: Número de categoría (1-15)
        
    Returns:
        Diccionario con información de la categoría
    """
    return SCOPE_3_CATEGORY_DESCRIPTIONS.get(category_num, {})


def list_all_scope3_categories() -> Dict[int, Dict]:
    """
    Lista todas las 15 categorías de Scope 3.
    
    Returns:
        Diccionario con todas las categorías
    """
    return SCOPE_3_CATEGORY_DESCRIPTIONS
