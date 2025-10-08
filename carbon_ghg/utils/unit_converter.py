"""
Sistema de conversión de unidades para datos de actividad.
Soporta unidades energéticas, masa, volumen, distancia.
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Factores de conversión a unidades base
ENERGY_CONVERSIONS = {
    # Base: MJ (Megajoules)
    'mj': 1.0,
    'gj': 1000.0,
    'tj': 1_000_000.0,
    'kwh': 3.6,
    'mwh': 3600.0,
    'gwh': 3_600_000.0,
    'btu': 0.001055,
    'mmbtu': 1055.0,
    'therm': 105.5,
}

MASS_CONVERSIONS = {
    # Base: kg (kilogramos)
    'kg': 1.0,
    'g': 0.001,
    'mg': 0.000001,
    'tonne': 1000.0,
    'tonnes': 1000.0,
    'ton': 1000.0,
    'metric_ton': 1000.0,
    'lb': 0.453592,
    'lbs': 0.453592,
    'pound': 0.453592,
    'oz': 0.0283495,
}

VOLUME_CONVERSIONS = {
    # Base: liters
    'liter': 1.0,
    'liters': 1.0,
    'l': 1.0,
    'ml': 0.001,
    'gallon': 3.78541,
    'gallons': 3.78541,
    'gal': 3.78541,
    'imperial_gallon': 4.54609,
    'm3': 1000.0,
    'm³': 1000.0,
    'cubic_meter': 1000.0,
    'ft3': 28.3168,
}

DISTANCE_CONVERSIONS = {
    # Base: km (kilómetros)
    'km': 1.0,
    'kilometer': 1.0,
    'kilometers': 1.0,
    'm': 0.001,
    'meter': 0.001,
    'meters': 0.001,
    'mile': 1.60934,
    'miles': 1.60934,
    'mi': 1.60934,
    'nautical_mile': 1.852,
    'nm': 1.852,
    'ft': 0.0003048,
    'feet': 0.0003048,
}

# Mapeo de categorías de unidades
UNIT_CATEGORIES = {
    **{k: 'energy' for k in ENERGY_CONVERSIONS.keys()},
    **{k: 'mass' for k in MASS_CONVERSIONS.keys()},
    **{k: 'volume' for k in VOLUME_CONVERSIONS.keys()},
    **{k: 'distance' for k in DISTANCE_CONVERSIONS.keys()},
}


def normalize_unit_name(unit: str) -> str:
    """
    Normaliza el nombre de una unidad eliminando espacios y caracteres especiales.
    
    Args:
        unit: Nombre de la unidad
        
    Returns:
        Nombre normalizado
    """
    return unit.strip().lower().replace(' ', '_').replace('-', '_').replace('.', '_')


def get_unit_category(unit: str) -> Optional[str]:
    """
    Determina la categoría de una unidad (energy, mass, volume, distance).
    
    Args:
        unit: Nombre de la unidad
        
    Returns:
        Categoría de la unidad o None si no se reconoce
    """
    normalized = normalize_unit_name(unit)
    return UNIT_CATEGORIES.get(normalized)


def convert_unit(value: float, from_unit: str, to_unit: str) -> Optional[float]:
    """
    Convierte un valor de una unidad a otra.
    
    Args:
        value: Valor a convertir
        from_unit: Unidad origen
        to_unit: Unidad destino
        
    Returns:
        Valor convertido o None si la conversión no es posible
        
    Example:
        >>> convert_unit(100, 'kWh', 'MJ')
        360.0
        >>> convert_unit(5, 'ton', 'kg')
        5000.0
    """
    from_normalized = normalize_unit_name(from_unit)
    to_normalized = normalize_unit_name(to_unit)
    
    # Si son la misma unidad, no convertir
    if from_normalized == to_normalized:
        return value
    
    # Determinar categoría
    from_category = get_unit_category(from_unit)
    to_category = get_unit_category(to_unit)
    
    if not from_category or not to_category:
        logger.warning(f"No se pudo determinar categoría para '{from_unit}' o '{to_unit}'")
        return None
    
    if from_category != to_category:
        logger.error(f"No se puede convertir entre categorías diferentes: {from_category} -> {to_category}")
        return None
    
    # Obtener tabla de conversión apropiada
    conversion_table = {
        'energy': ENERGY_CONVERSIONS,
        'mass': MASS_CONVERSIONS,
        'volume': VOLUME_CONVERSIONS,
        'distance': DISTANCE_CONVERSIONS,
    }.get(from_category)
    
    if not conversion_table:
        return None
    
    # Convertir a unidad base y luego a unidad destino
    try:
        from_factor = conversion_table[from_normalized]
        to_factor = conversion_table[to_normalized]
        
        # Valor en unidad base
        base_value = value * from_factor
        # Valor en unidad destino
        converted_value = base_value / to_factor
        
        logger.debug(f"Converted {value} {from_unit} -> {converted_value} {to_unit}")
        return converted_value
    
    except KeyError as e:
        logger.error(f"Unidad no reconocida en tabla de conversión: {e}")
        return None
    except ZeroDivisionError:
        logger.error(f"Factor de conversión cero para '{to_unit}'")
        return None


def are_units_compatible(unit1: str, unit2: str) -> bool:
    """
    Verifica si dos unidades son compatibles (misma categoría).
    
    Args:
        unit1: Primera unidad
        unit2: Segunda unidad
        
    Returns:
        True si son compatibles, False en caso contrario
    """
    cat1 = get_unit_category(unit1)
    cat2 = get_unit_category(unit2)
    
    if not cat1 or not cat2:
        return False
    
    return cat1 == cat2


def get_conversion_factor(from_unit: str, to_unit: str) -> Optional[float]:
    """
    Obtiene el factor de conversión directo entre dos unidades.
    
    Args:
        from_unit: Unidad origen
        to_unit: Unidad destino
        
    Returns:
        Factor de conversión (multiplicador) o None
        
    Example:
        >>> get_conversion_factor('kg', 'tonne')
        0.001
    """
    if convert_unit(1.0, from_unit, to_unit) is not None:
        return convert_unit(1.0, from_unit, to_unit)
    return None
