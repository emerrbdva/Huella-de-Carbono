"""
Modelos Pydantic para validación de datos de emisiones GHG Protocol.
Implementa esquemas robustos con validación de tipos y catálogos controlados.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime

# Catálogos controlados según GHG Protocol
SCOPE_1_CATEGORIES = [
    "stationary_combustion", "mobile_combustion", 
    "process_emissions", "fugitive_emissions"
]

SCOPE_2_CATEGORIES = [
    "purchased_electricity", "purchased_heat", 
    "purchased_steam", "purchased_cooling"
]

SCOPE_3_CATEGORIES = [
    "purchased_goods_services", "capital_goods", "fuel_energy_activities",
    "upstream_transportation", "waste_generated", "business_travel",
    "employee_commuting", "upstream_leased_assets", "downstream_transportation",
    "processing_sold_products", "use_sold_products", "end_of_life_sold_products",
    "downstream_leased_assets", "franchises", "investments"
]

GHG_GASES = ["CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6", "NF3", "CO2e", "CO2-e"]

# GWP values (AR5, 100-year horizon)
GWP_AR5 = {
    "CO2": 1,
    "CH4": 28,
    "N2O": 265,
    "SF6": 23500,
    "NF3": 16100,
    "CO2e": 1,
    "CO2-e": 1
}


class ActivityRecord(BaseModel):
    """
    Registro de actividad que genera emisiones.
    Validación estricta según GHG Protocol.
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    
    entity_id: str = Field(..., description="ID único de la entidad emisora")
    scope: Literal[1, 2, 3] = Field(..., description="Alcance GHG Protocol (1, 2 o 3)")
    category: str = Field(..., description="Categoría de emisión específica")
    subcategory: Optional[str] = Field(None, description="Subcategoría opcional")
    activity_value: float = Field(..., ge=0, description="Valor del dato de actividad")
    activity_unit: str = Field(..., description="Unidad del dato de actividad")
    geography: Optional[str] = Field(None, description="País o región (ISO 3166-1 alpha-3)")
    year: Optional[int] = Field(None, ge=1990, le=2100, description="Año del dato")
    month: Optional[int] = Field(None, ge=1, le=12, description="Mes opcional")
    facility: Optional[str] = Field(None, description="Instalación o sitio específico")
    description: Optional[str] = Field(None, description="Descripción adicional")
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str, info) -> str:
        """Valida que la categoría sea apropiada para el scope."""
        scope = info.data.get('scope')
        v_lower = v.lower().replace(' ', '_').replace('-', '_')
        
        if scope == 1 and v_lower not in SCOPE_1_CATEGORIES:
            # Intenta mapeo flexible
            if any(cat in v_lower for cat in ['combustion', 'fuel', 'diesel', 'gasoline', 'natural_gas']):
                return "mobile_combustion" if 'mobile' in v_lower or 'vehicle' in v_lower else "stationary_combustion"
            elif any(cat in v_lower for cat in ['process', 'industrial']):
                return "process_emissions"
            elif any(cat in v_lower for cat in ['fugitive', 'leak', 'refrigerant']):
                return "fugitive_emissions"
        elif scope == 2 and v_lower not in SCOPE_2_CATEGORIES:
            if 'electric' in v_lower:
                return "purchased_electricity"
            elif 'heat' in v_lower:
                return "purchased_heat"
            elif 'steam' in v_lower:
                return "purchased_steam"
            elif 'cool' in v_lower:
                return "purchased_cooling"
        elif scope == 3 and v_lower not in SCOPE_3_CATEGORIES:
            # Mapeo inteligente para Scope 3
            if any(cat in v_lower for cat in ['travel', 'flight', 'hotel']):
                return "business_travel"
            elif any(cat in v_lower for cat in ['commut', 'employee']):
                return "employee_commuting"
            elif any(cat in v_lower for cat in ['waste', 'disposal']):
                return "waste_generated"
            elif any(cat in v_lower for cat in ['transport', 'shipping', 'logistics']):
                return "upstream_transportation"
        
        return v


class EmissionFactor(BaseModel):
    """
    Factor de emisión con trazabilidad completa.
    Formula: Emisiones = Dato de Actividad × Factor de Emisión
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    
    source: Literal["IPCC2006", "IPCC2019", "UK2024", "UK2025", "EPA2024", "EPA2025", "CUSTOM", "TEST", "DEMO"] = Field(
        ..., description="Fuente del factor de emisión"
    )
    source_version: Optional[str] = Field(None, description="Versión específica del dataset")
    gas: str = Field(..., description="Gas de efecto invernadero")
    value: float = Field(..., gt=0, description="Valor numérico del factor")
    unit: str = Field(..., description="Unidad del factor (ej: kg CO2e / kWh)")
    year: int = Field(..., ge=1990, le=2100, description="Año de vigencia del factor")
    geography: Optional[str] = Field(None, description="Geografía aplicable")
    scope: Optional[int] = Field(None, ge=1, le=3, description="Scope GHG asociado")
    category: Optional[str] = Field(None, description="Categoría de actividad")
    notes: Optional[str] = Field(None, description="Notas adicionales o supuestos")
    url: Optional[str] = Field(None, description="URL de la fuente original")
    
    @field_validator('gas')
    @classmethod
    def validate_gas(cls, v: str) -> str:
        """Valida que el gas sea reconocido."""
        v_upper = v.upper()
        # Permitir variantes de CO2e
        if v_upper in ['CO2E', 'CO2-E', 'CO2EQ', 'CO2 EQ']:
            return 'CO2e'
        if v_upper not in GHG_GASES and not v_upper.startswith('HFC') and not v_upper.startswith('PFC'):
            raise ValueError(f"Gas '{v}' no reconocido. Use: {', '.join(GHG_GASES)}")
        return v_upper


class EmissionResult(BaseModel):
    """
    Resultado del cálculo de emisiones con trazabilidad completa.
    """
    activity_record: ActivityRecord
    emission_factor: EmissionFactor
    emission_kgCO2e: float = Field(..., description="Emisión total en kg CO2e")
    emission_tCO2e: float = Field(..., description="Emisión total en toneladas CO2e")
    calculation_date: datetime = Field(default_factory=datetime.now)
    calculation_formula: str = Field(
        default="E = AD × EF",
        description="Fórmula utilizada"
    )
    conversion_notes: Optional[str] = Field(None, description="Notas sobre conversiones aplicadas")
    quality_flag: Optional[str] = Field(None, description="Bandera de calidad del dato")
    
    @property
    def scope_label(self) -> str:
        return f"Scope {self.activity_record.scope}"
    
    @property
    def category_label(self) -> str:
        return self.activity_record.category.replace('_', ' ').title()


class ValidationError(BaseModel):
    """
    Error de validación de datos con contexto completo.
    """
    row_number: int
    field: str
    error_message: str
    invalid_value: Optional[str] = None
    suggestion: Optional[str] = None
