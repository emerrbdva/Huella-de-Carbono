"""
Configuración de APIs Gratuitas para Huella de Carbono Profesional
Sistema de integración 100% sin costos con APIs climáticas y de emisiones

Autor: Sistema Profesional de Huella de Carbono
Fecha: Octubre 2025
Versión: 2.0.0 Professional
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class APIProvider(Enum):
    """Proveedores de APIs gratuitas disponibles"""
    CLIMATE_TRACE = "climate_trace"
    OPEN_METEO = "open_meteo"
    CLIMATIQ_FREE = "climatiq_free"
    NOAA_CLIMATE = "noaa_climate"
    NASA_EARTH = "nasa_earth"
    EPA_GHUB = "epa_ghub"
    UK_GOV = "uk_gov"
    WORLD_BANK = "world_bank"
    OPEN_CEDA = "open_ceda"

@dataclass
class APIConfig:
    """Configuración de API gratuita"""
    name: str
    base_url: str
    cost: float  # Siempre 0.0 para APIs gratuitas
    api_key_required: bool
    rate_limit: str
    features: List[str]
    reliability: float  # 0.0 - 1.0
    coverage: str  # Global, Regional, Country-specific
    data_format: List[str]  # JSON, CSV, XML

# =====================================================
# CONFIGURACIÓN DE APIs GRATUITAS
# =====================================================

FREE_APIS_CONFIG = {
    APIProvider.CLIMATE_TRACE: APIConfig(
        name="Climate TRACE",
        base_url="https://climatetrace.org/api",
        cost=0.0,
        api_key_required=False,
        rate_limit="unlimited",
        features=[
            "satellite_emissions",
            "real_time_data",
            "sector_breakdown",
            "country_data",
            "facility_level"
        ],
        reliability=0.95,
        coverage="Global",
        data_format=["JSON", "CSV"]
    ),
    
    APIProvider.OPEN_METEO: APIConfig(
        name="Open-Meteo",
        base_url="https://api.open-meteo.com/v1",
        cost=0.0,
        api_key_required=False,
        rate_limit="10000_req/day",
        features=[
            "weather_current",
            "weather_forecast",
            "historical_weather",
            "climate_data",
            "air_quality"
        ],
        reliability=0.90,
        coverage="Global",
        data_format=["JSON"]
    ),
    
    APIProvider.CLIMATIQ_FREE: APIConfig(
        name="Climatiq Data Explorer",
        base_url="https://www.climatiq.io/data",
        cost=0.0,
        api_key_required=False,
        rate_limit="unlimited_browser",
        features=[
            "emission_factors",
            "global_coverage",
            "sector_specific",
            "ghg_protocol_aligned"
        ],
        reliability=0.98,
        coverage="Global",
        data_format=["JSON", "CSV"]
    ),
    
    APIProvider.NOAA_CLIMATE: APIConfig(
        name="NOAA Climate Data",
        base_url="https://www.ncdc.noaa.gov/cdo-web/api/v2",
        cost=0.0,
        api_key_required=True,  # Gratis pero requiere registro
        rate_limit="1000_req/day",
        features=[
            "historical_climate",
            "weather_stations",
            "precipitation",
            "temperature",
            "extreme_events"
        ],
        reliability=0.99,
        coverage="Global (USA focus)",
        data_format=["JSON", "CSV"]
    ),
    
    APIProvider.NASA_EARTH: APIConfig(
        name="NASA Earth Data",
        base_url="https://earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/earthdata-login",
        cost=0.0,
        api_key_required=True,  # Gratis pero requiere registro NASA
        rate_limit="unlimited_registered",
        features=[
            "satellite_imagery",
            "atmospheric_data",
            "land_use_change",
            "vegetation_indices",
            "carbon_cycle"
        ],
        reliability=0.99,
        coverage="Global",
        data_format=["NetCDF", "HDF", "JSON"]
    ),
    
    APIProvider.UK_GOV: APIConfig(
        name="UK Government GHG Factors",
        base_url="https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting",
        cost=0.0,
        api_key_required=False,
        rate_limit="unlimited",
        features=[
            "official_emission_factors",
            "ghg_protocol_compliant",
            "annual_updates",
            "scope_123_coverage"
        ],
        reliability=1.0,
        coverage="UK (Global applicable)",
        data_format=["XLSX", "CSV"]
    ),
    
    APIProvider.WORLD_BANK: APIConfig(
        name="World Bank Climate Data",
        base_url="https://datahelpdesk.worldbank.org/knowledgebase/articles/889392",
        cost=0.0,
        api_key_required=False,
        rate_limit="unlimited",
        features=[
            "country_emissions",
            "economic_indicators",
            "energy_statistics",
            "population_data"
        ],
        reliability=0.95,
        coverage="Global",
        data_format=["JSON", "XML", "CSV"]
    ),
    
    APIProvider.OPEN_CEDA: APIConfig(
        name="Open CEDA Global Database",
        base_url="https://www.ceda.ac.uk/",
        cost=0.0,
        api_key_required=True,  # Registro gratuito
        rate_limit="unlimited_registered",
        features=[
            "emission_factors_148_countries",
            "sector_specific",
            "time_series_data",
            "uncertainty_ranges"
        ],
        reliability=0.92,
        coverage="Global (148 countries)",
        data_format=["JSON", "CSV", "NetCDF"]
    )
}

# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================

def get_available_apis() -> List[APIProvider]:
    """Retorna lista de APIs disponibles"""
    return list(FREE_APIS_CONFIG.keys())

def get_api_config(provider: APIProvider) -> APIConfig:
    """Obtiene configuración de API específica"""
    return FREE_APIS_CONFIG.get(provider)

def get_apis_by_feature(feature: str) -> List[APIProvider]:
    """Obtiene APIs que soportan una característica específica"""
    matching_apis = []
    for provider, config in FREE_APIS_CONFIG.items():
        if feature in config.features:
            matching_apis.append(provider)
    return matching_apis

def get_high_reliability_apis(min_reliability: float = 0.95) -> List[APIProvider]:
    """Obtiene APIs con alta confiabilidad"""
    return [
        provider for provider, config in FREE_APIS_CONFIG.items() 
        if config.reliability >= min_reliability
    ]

# =====================================================
# CONFIGURACIÓN DE CLAVES API (GRATUITAS)
# =====================================================

class FreeAPIKeys:
    """Manejo de claves API gratuitas"""
    
    @staticmethod
    def get_noaa_key() -> Optional[str]:
        """Clave NOAA (gratis, requiere registro en: https://www.ncdc.noaa.gov/cdo-web/token)"""
        return os.getenv("NOAA_API_KEY", "")
    
    @staticmethod
    def get_nasa_key() -> Optional[str]:
        """Clave NASA EarthData (gratis, requiere registro en: https://earthdata.nasa.gov/)"""
        return os.getenv("NASA_EARTHDATA_KEY", "")
    
    @staticmethod
    def get_ceda_key() -> Optional[str]:
        """Clave CEDA (gratis, requiere registro en: https://www.ceda.ac.uk/)"""
        return os.getenv("CEDA_API_KEY", "")
    
    @staticmethod
    def setup_env_file():
        """Crea archivo .env con plantilla para claves gratuitas"""
        env_template = '''# ===========================================
# CLAVES API GRATUITAS - HUELLA DE CARBONO
# ===========================================
# Todas estas APIs son 100% gratuitas, solo requieren registro

# NOAA Climate Data (gratis): https://www.ncdc.noaa.gov/cdo-web/token
NOAA_API_KEY=tu_clave_noaa_aqui

# NASA EarthData (gratis): https://earthdata.nasa.gov/
NASA_EARTHDATA_KEY=tu_clave_nasa_aqui

# CEDA Archive (gratis): https://www.ceda.ac.uk/
CEDA_API_KEY=tu_clave_ceda_aqui

# ===========================================
# CONFIGURACIÓN ADICIONAL
# ===========================================
CACHE_ENABLED=true
DEBUG_MODE=false
LOG_LEVEL=INFO
'''
        
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.write(env_template)
            print("✅ Archivo .env creado con plantilla de claves gratuitas")
        else:
            print("ℹ️ Archivo .env ya existe")

if __name__ == "__main__":
    # Configuración inicial
    print("🚀 Configurando APIs gratuitas...")
    
    # Mostrar APIs disponibles
    print(f"\n📡 APIs disponibles: {len(get_available_apis())}")
    for provider in get_available_apis():
        config = get_api_config(provider)
        print(f"  • {config.name} - {config.coverage} - Confiabilidad: {config.reliability*100:.1f}%")
    
    # Crear archivo .env
    FreeAPIKeys.setup_env_file()
    
    print("\n✅ Configuración completa!")