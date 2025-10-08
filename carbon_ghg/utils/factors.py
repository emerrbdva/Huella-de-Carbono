"""
Utilidades para carga y búsqueda de factores de emisión.
Soporta múltiples fuentes: UK Gov, EPA, IPCC, EFDB.
"""
import pandas as pd
from typing import Optional, Tuple, Dict, List
import logging
import functools

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def load_uk_gov_factors(file_path: str, year: int = 2025) -> pd.DataFrame:
    """
    Carga los factores de emisión del UK Government GHG Conversion Factors.
    
    OPTIMIZACIÓN: Función cacheada con @lru_cache para evitar recargas.
    El cache se mantiene durante toda la sesión de la aplicación.
    
    Args:
        file_path: Ruta al archivo Excel de factores UK Gov
        year: Año de los factores (2024, 2025, etc.)
    
    Returns:
        DataFrame con factores normalizados
        
    Referencias:
        - https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting
        - Dataset 2025: https://assets.publishing.service.gov.uk/media/6846a4f55e92539572806125/ghg-conversion-factors-2025-full-set.xlsx
    """
    try:
        xls = pd.ExcelFile(file_path)
        logger.info(f"Hojas disponibles en el archivo: {xls.sheet_names}")
        
        # Hojas principales a procesar (UK Gov 2025 structure)
        sheets_to_process = [
            'Fuels', 'Bioenergy', 'Refrigerant & other', 
            'Passenger vehicles', 'UK electricity', 
            'Transmission and distribution',
            'Water supply', 'Water treatment',
            'Material use', 'Waste disposal',
            'Business travel- air', 'Business travel- sea', 'Business travel- land',
            'Freighting goods', 'Hotel stay'
        ]
        
        all_factors_dfs = []
        
        for sheet_name in sheets_to_process:
            if sheet_name not in xls.sheet_names:
                logger.warning(f"Hoja '{sheet_name}' no encontrada, saltando...")
                continue
            
            try:
                # UK Gov usa filas de encabezado variable
                # Buscar la fila que contiene 'kg CO2e' para determinar el header
                df_preview = pd.read_excel(xls, sheet_name=sheet_name, header=None, nrows=35)
                header_row = None
                for idx in range(len(df_preview)):
                    row_str = ' '.join(str(x) for x in df_preview.iloc[idx].values if pd.notna(x))
                    # Buscar específicamente la fila con 'kg CO2e' (no el título general)
                    if 'kg CO2e' in row_str and ('Unit' in row_str or 'unit' in row_str.lower()):
                        header_row = idx
                        logger.debug(f"Encontrado header en fila {idx} para '{sheet_name}'")
                        break
                
                if header_row is None:
                    logger.warning(f"No se encontró fila de encabezado en '{sheet_name}', saltando...")
                    continue
                
                # Leer con el header correcto
                df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=header_row)
                
                # Intentar identificar columnas clave
                # Normalizar nombres de columnas
                df_sheet.columns = df_sheet.columns.str.strip()
                
                logger.info(f"Procesando hoja '{sheet_name}' con {len(df_sheet)} filas")
                logger.debug(f"Columnas: {df_sheet.columns.tolist()}")
                
                # Buscar columna de CO2e (puede variar el nombre exacto)
                co2e_cols = [col for col in df_sheet.columns 
                            if 'co2' in str(col).lower().replace(' ', '')]
                
                if not co2e_cols:
                    logger.warning(f"No se encontró columna CO2e en '{sheet_name}', saltando...")
                    continue
                
                # Preferir columna exacta 'kg CO2e' si existe
                co2e_col = 'kg CO2e' if 'kg CO2e' in df_sheet.columns else co2e_cols[0]
                
                # Identificar columnas descriptivas (formato 2025 condensed set)
                desc_cols = ['Activity', 'Fuel', 'GHG Protocol scope', 'Level 1', 'Level 2', 'Level 3', 'Level 4']
                available_desc_cols = [col for col in desc_cols if col in df_sheet.columns]
                
                # Buscar columna de unidades
                unit_col = 'Unit' if 'Unit' in df_sheet.columns else next((col for col in df_sheet.columns if 'unit' in col.lower()), None)
                
                if not unit_col:
                    logger.warning(f"No se encontró columna de unidades en '{sheet_name}'")
                    # Continuar sin columna de unidades
                
                # Seleccionar columnas relevantes
                cols_to_keep = available_desc_cols + [co2e_col]
                if unit_col and unit_col in df_sheet.columns:
                    cols_to_keep.append(unit_col)
                cols_to_keep = [col for col in cols_to_keep if col in df_sheet.columns]
                
                df_subset = df_sheet[cols_to_keep].copy()
                
                # Renombrar para estandarizar
                rename_map = {co2e_col: 'kgCO2e'}
                if unit_col in df_subset.columns:
                    rename_map[unit_col] = 'Unit'
                df_subset.rename(columns=rename_map, inplace=True)
                
                # Agregar metadatos
                df_subset['Source'] = f'UK{year}'
                df_subset['Sheet'] = sheet_name
                df_subset['Year'] = year
                
                # Limpiar valores
                df_subset['kgCO2e'] = pd.to_numeric(df_subset['kgCO2e'], errors='coerce')
                df_subset.dropna(subset=['kgCO2e'], inplace=True)
                
                # Forward fill para columnas jerárquicas
                for col in available_desc_cols:
                    if col in df_subset.columns:
                        df_subset[col] = df_subset[col].ffill()
                
                all_factors_dfs.append(df_subset)
                logger.info(f"✓ Procesados {len(df_subset)} factores de '{sheet_name}'")
                
            except Exception as e:
                logger.error(f"Error procesando hoja '{sheet_name}': {e}")
                continue
        
        if not all_factors_dfs:
            raise ValueError("No se pudo procesar ninguna hoja del archivo de factores UK Gov")
        
        # Concatenar todos los DataFrames
        df_all = pd.concat(all_factors_dfs, ignore_index=True)
        logger.info(f"✓ Total de factores cargados: {len(df_all)}")
        
        return df_all
    
    except Exception as e:
        logger.error(f"Error al cargar factores UK Gov: {e}")
        raise


def find_factor(
    factors_df: pd.DataFrame, 
    category: str, 
    activity_unit: str,
    geography: Optional[str] = None,
    scope: Optional[int] = None
) -> Optional[Tuple[float, str, Dict]]:
    """
    Busca un factor de emisión apropiado en el DataFrame.
    
    Args:
        factors_df: DataFrame con factores de emisión
        category: Categoría de actividad (ej: "diesel", "electricity")
        activity_unit: Unidad del dato de actividad
        geography: Geografía opcional para filtrar
        scope: Scope opcional para filtrar
    
    Returns:
        Tupla (valor_factor, descripción_fuente, metadata_dict) o None
    """
    if factors_df is None or factors_df.empty:
        logger.warning("DataFrame de factores vacío o None")
        return None
    
    search_term = category.lower().strip()
    unit_term = activity_unit.lower().strip()
    
    # Columnas descriptivas a buscar
    description_cols = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Column Text', 'Sheet']
    available_desc_cols = [col for col in description_cols if col in factors_df.columns]
    
    # Filtrar por scope si está disponible
    df_search = factors_df.copy()
    if scope and 'GHG Protocol scope' in df_search.columns:
        scope_filter = df_search['GHG Protocol scope'].astype(str).str.contains(str(scope), na=False)
        if scope_filter.any():
            df_search = df_search[scope_filter]
    
    # Búsqueda por categoría
    matches = pd.DataFrame()
    for col in available_desc_cols:
        if col not in df_search.columns:
            continue
        try:
            col_matches = df_search[df_search[col].astype(str).str.lower().str.contains(search_term, na=False, regex=False)]
            if not col_matches.empty:
                matches = pd.concat([matches, col_matches]).drop_duplicates()
        except Exception as e:
            logger.debug(f"Error buscando en columna {col}: {e}")
            continue
    
    if matches.empty:
        logger.warning(f"No se encontraron coincidencias para categoría '{category}'")
        return None
    
    # Filtrar por unidad si está disponible
    if 'Unit' in matches.columns:
        unit_matches = matches[matches['Unit'].astype(str).str.lower().str.contains(unit_term, na=False, regex=False)]
        if not unit_matches.empty:
            matches = unit_matches
        else:
            logger.warning(f"No se encontró coincidencia exacta de unidad '{activity_unit}', usando primera coincidencia")
    
    # Tomar el primer resultado
    best_match = matches.iloc[0]
    factor_value = float(best_match['kgCO2e'])
    
    # Construir descripción de fuente
    source_parts = []
    for col in ['Source', 'Sheet', 'Level 1', 'Level 2']:
        if col in best_match and pd.notna(best_match[col]):
            source_parts.append(str(best_match[col]))
    source_desc = " - ".join(source_parts[:3])  # Limitar longitud
    
    # Metadata adicional
    metadata = {
        'unit': best_match.get('Unit', activity_unit),
        'source': best_match.get('Source', 'UK'),
        'year': best_match.get('Year', 2025),
        'scope': best_match.get('GHG Protocol scope', scope),
        'full_description': ' > '.join([str(best_match.get(col, '')) for col in available_desc_cols if col in best_match and pd.notna(best_match[col])])
    }
    
    logger.info(f"✓ Factor encontrado: {factor_value} kg CO2e/{metadata['unit']} - {source_desc}")
    
    return factor_value, source_desc, metadata


def normalize_unit(unit: str) -> str:
    """
    Normaliza unidades a formato estándar.
    
    Args:
        unit: Unidad a normalizar
    
    Returns:
        Unidad normalizada
    """
    unit_map = {
        'kwh': 'kWh',
        'mwh': 'MWh',
        'kwh': 'kWh',
        'litre': 'liters',
        'liter': 'liters',
        'l': 'liters',
        'kg': 'kg',
        'tonne': 'tonnes',
        'ton': 'tonnes',
        't': 'tonnes',
        'km': 'km',
        'mile': 'miles',
        'm3': 'm³',
        'gj': 'GJ',
        'passenger.km': 'passenger-km',
        'tonne.km': 'tonne-km'
    }
    
    normalized = unit.lower().strip().replace(' ', '')
    return unit_map.get(normalized, unit)
