"""
Validador robusto de datos de actividad usando Pydantic.
Genera reportes de calidad de datos y maneja errores de forma granular.
"""
import pandas as pd
from typing import List, Tuple, Dict
from pydantic import ValidationError as PydanticValidationError
from models.emissions import ActivityRecord, ValidationError
import logging

logger = logging.getLogger(__name__)


class DataQualityReport:
    """
    Reporte de calidad de datos con estadísticas y errores detallados.
    """
    
    def __init__(self):
        self.total_rows: int = 0
        self.valid_rows: int = 0
        self.invalid_rows: int = 0
        self.errors: List[ValidationError] = []
        self.warnings: List[str] = []
        self.valid_records: List[ActivityRecord] = []
        
    @property
    def success_rate(self) -> float:
        """Porcentaje de filas válidas."""
        if self.total_rows == 0:
            return 0.0
        return (self.valid_rows / self.total_rows) * 100
    
    def add_error(self, row_num: int, field: str, message: str, value: str = None, suggestion: str = None):
        """Agrega un error de validación."""
        self.errors.append(ValidationError(
            row_number=row_num,
            field=field,
            error_message=message,
            invalid_value=value,
            suggestion=suggestion
        ))
        
    def add_warning(self, message: str):
        """Agrega una advertencia."""
        self.warnings.append(message)
        
    def to_dict(self) -> Dict:
        """Convierte el reporte a diccionario."""
        return {
            'total_rows': self.total_rows,
            'valid_rows': self.valid_rows,
            'invalid_rows': self.invalid_rows,
            'success_rate': round(self.success_rate, 2),
            'errors': [
                {
                    'row': e.row_number,
                    'field': e.field,
                    'message': e.error_message,
                    'value': e.invalid_value,
                    'suggestion': e.suggestion
                }
                for e in self.errors
            ],
            'warnings': self.warnings
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convierte errores a DataFrame para visualización."""
        if not self.errors:
            return pd.DataFrame()
        
        return pd.DataFrame([
            {
                'Fila': e.row_number,
                'Campo': e.field,
                'Error': e.error_message,
                'Valor Inválido': e.invalid_value,
                'Sugerencia': e.suggestion
            }
            for e in self.errors
        ])
    
    def __str__(self) -> str:
        return (
            f"📊 Reporte de Calidad de Datos\n"
            f"{'='*50}\n"
            f"Total de filas: {self.total_rows}\n"
            f"Filas válidas: {self.valid_rows} ({self.success_rate:.1f}%)\n"
            f"Filas inválidas: {self.invalid_rows}\n"
            f"Errores: {len(self.errors)}\n"
            f"Advertencias: {len(self.warnings)}\n"
        )


def validate_activity_data(df: pd.DataFrame, strict: bool = False) -> Tuple[List[ActivityRecord], DataQualityReport]:
    """
    Valida un DataFrame de datos de actividad usando esquemas Pydantic.
    
    Args:
        df: DataFrame con datos de actividad
        strict: Si es True, rechaza filas con cualquier error; si es False, intenta corregir
        
    Returns:
        Tupla (lista de registros válidos, reporte de calidad)
        
    Example:
        >>> df = pd.read_csv('activities.csv')
        >>> valid_records, report = validate_activity_data(df)
        >>> print(report)
    """
    report = DataQualityReport()
    report.total_rows = len(df)
    
    # Columnas requeridas
    required_cols = ['entity_id', 'scope', 'category', 'activity_value', 'activity_unit']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        report.add_error(
            row_num=0,
            field='columns',
            message=f"Columnas requeridas faltantes: {', '.join(missing_cols)}",
            suggestion=f"Agrega las columnas: {', '.join(missing_cols)}"
        )
        report.invalid_rows = report.total_rows
        return [], report
    
    # Validar fila por fila
    for idx, row in df.iterrows():
        row_num = idx + 2  # +2 porque Excel/CSV inicia en 1 y tiene encabezado
        
        try:
            # Convertir fila a diccionario, manejando NaN
            row_dict = row.to_dict()
            
            # Limpiar valores NaN/None en campos opcionales
            for key, value in row_dict.items():
                if pd.isna(value):
                    row_dict[key] = None
            
            # Validar con Pydantic
            activity_record = ActivityRecord(**row_dict)
            report.valid_records.append(activity_record)
            report.valid_rows += 1
            
        except PydanticValidationError as e:
            report.invalid_rows += 1
            
            # Extraer errores individuales de Pydantic
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                msg = error['msg']
                error_type = error['type']
                
                # Intentar obtener valor inválido
                invalid_value = str(row_dict.get(field, 'N/A'))
                
                # Generar sugerencias según tipo de error
                suggestion = generate_suggestion(field, error_type, invalid_value)
                
                report.add_error(
                    row_num=row_num,
                    field=str(field),
                    message=msg,
                    value=invalid_value,
                    suggestion=suggestion
                )
            
            logger.debug(f"Fila {row_num} inválida: {e}")
            
        except Exception as e:
            report.invalid_rows += 1
            report.add_error(
                row_num=row_num,
                field='general',
                message=f"Error inesperado: {str(e)}",
                suggestion="Revisa el formato de los datos en esta fila"
            )
            logger.error(f"Error inesperado en fila {row_num}: {e}")
    
    # Advertencias generales
    if report.invalid_rows > 0:
        report.add_warning(
            f"{report.invalid_rows} filas contienen errores y serán excluidas del cálculo"
        )
    
    if report.success_rate < 80:
        report.add_warning(
            f"Tasa de éxito baja ({report.success_rate:.1f}%). Revisa la estructura de tu archivo"
        )
    
    logger.info(f"Validación completada: {report.valid_rows}/{report.total_rows} filas válidas")
    
    return report.valid_records, report


def generate_suggestion(field: str, error_type: str, value: str) -> str:
    """
    Genera sugerencias de corrección según el tipo de error.
    
    Args:
        field: Campo con error
        error_type: Tipo de error de Pydantic
        value: Valor inválido
        
    Returns:
        Texto con sugerencia de corrección
    """
    suggestions = {
        'scope': {
            'default': 'El scope debe ser 1, 2 o 3 según GHG Protocol',
            'greater_than_equal': 'Usa valores 1, 2 o 3',
            'less_than_equal': 'Usa valores 1, 2 o 3',
        },
        'activity_value': {
            'default': 'El valor de actividad debe ser un número positivo',
            'greater_than_equal': 'El valor debe ser mayor o igual a 0',
            'float_parsing': 'Ingresa un número válido (ej: 100.5)',
        },
        'year': {
            'default': 'El año debe estar entre 1990 y 2100',
            'greater_than_equal': 'Usa un año mayor o igual a 1990',
            'less_than_equal': 'Usa un año menor o igual a 2100',
        },
        'month': {
            'default': 'El mes debe estar entre 1 y 12',
            'greater_than_equal': 'Usa un valor entre 1 y 12',
            'less_than_equal': 'Usa un valor entre 1 y 12',
        }
    }
    
    field_suggestions = suggestions.get(field, {})
    return field_suggestions.get(error_type, field_suggestions.get('default', 'Revisa el formato de este campo'))


def get_data_quality_summary(df: pd.DataFrame) -> Dict:
    """
    Genera un resumen rápido de calidad de datos sin validación completa.
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        Diccionario con estadísticas de calidad
    """
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': df.columns.tolist(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.astype(str).to_dict(),
    }
    
    # Calcular porcentaje de completitud por columna
    summary['completeness'] = {
        col: round((1 - df[col].isnull().sum() / len(df)) * 100, 1)
        for col in df.columns
    }
    
    return summary
