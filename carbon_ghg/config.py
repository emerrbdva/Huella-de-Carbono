"""
Configuración global del sistema de cálculo de huella de carbono.
"""
import os
from pathlib import Path

# ===== RUTAS DEL PROYECTO =====
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
REPORTS_DIR = PROJECT_ROOT / 'reports'
TESTS_DIR = PROJECT_ROOT / 'tests'

# Crear directorios si no existen
REPORTS_DIR.mkdir(exist_ok=True)

# ===== CONFIGURACIÓN DE FACTORES DE EMISIÓN =====
EMISSION_FACTOR_SOURCES = {
    'UK_GOV_2025': {
        'name': 'UK Government GHG Conversion Factors 2025',
        'url': 'https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting',
        'download_url': 'https://assets.publishing.service.gov.uk/media/6846a4f55e92539572806125/ghg-conversion-factors-2025-full-set.xlsx',
        'year': 2025,
        'priority': 1
    },
    'UK_GOV_2024': {
        'name': 'UK Government GHG Conversion Factors 2024',
        'year': 2024,
        'priority': 2
    },
    'IPCC_2019': {
        'name': 'IPCC 2019 Refinement',
        'url': 'https://www.ipcc-nggip.iges.or.jp/public/2019rf/index.html',
        'year': 2019,
        'priority': 3
    },
    'IPCC_2006': {
        'name': 'IPCC 2006 Guidelines',
        'url': 'https://www.ipcc-nggip.iges.or.jp/public/2006gl/index.html',
        'year': 2006,
        'priority': 4
    },
    'EPA_2024': {
        'name': 'EPA Emission Factors Hub 2024',
        'url': 'https://www.epa.gov/climateleadership/ghg-emission-factors-hub',
        'year': 2024,
        'priority': 5
    }
}

# ===== GWP (Global Warming Potential) =====
# AR5 (IPCC Fifth Assessment Report) - 100 year horizon
GWP_AR5_100YR = {
    'CO2': 1,
    'CH4': 28,
    'N2O': 265,
    'SF6': 23500,
    'NF3': 16100,
    'HFC-134a': 1300,
    'HFC-32': 677,
    'HFC-125': 3170,
    'HFC-143a': 4800,
    'HFC-152a': 138,
    'HFC-227ea': 3350,
    'HFC-23': 12400,
    'CF4': 6630,
    'C2F6': 11100,
    'C3F8': 8900,
}

# AR6 (IPCC Sixth Assessment Report) - 100 year horizon
GWP_AR6_100YR = {
    'CO2': 1,
    'CH4': 27.9,
    'N2O': 273,
    'SF6': 25200,
    'NF3': 17400,
}

# Configuración activa
ACTIVE_GWP = GWP_AR5_100YR  # Cambiar a GWP_AR6_100YR si se prefiere AR6

# ===== SCOPE CATEGORIES (GHG Protocol) =====
SCOPE_1_CATEGORIES = {
    'stationary_combustion': 'Combustión estacionaria (calderas, hornos, generadores)',
    'mobile_combustion': 'Combustión móvil (vehículos, equipos móviles)',
    'process_emissions': 'Emisiones de proceso industrial',
    'fugitive_emissions': 'Emisiones fugitivas (refrigerantes, fugas)'
}

SCOPE_2_CATEGORIES = {
    'purchased_electricity': 'Electricidad comprada',
    'purchased_heat': 'Calor comprado',
    'purchased_steam': 'Vapor comprado',
    'purchased_cooling': 'Refrigeración comprada'
}

SCOPE_3_CATEGORIES = {
    1: 'purchased_goods_services',
    2: 'capital_goods',
    3: 'fuel_energy_activities',
    4: 'upstream_transportation',
    5: 'waste_generated',
    6: 'business_travel',
    7: 'employee_commuting',
    8: 'upstream_leased_assets',
    9: 'downstream_transportation',
    10: 'processing_sold_products',
    11: 'use_sold_products',
    12: 'end_of_life_sold_products',
    13: 'downstream_leased_assets',
    14: 'franchises',
    15: 'investments'
}

# ===== UNIDADES SOPORTADAS =====
SUPPORTED_UNITS = {
    'energy': ['kWh', 'MWh', 'GWh', 'MJ', 'GJ', 'TJ', 'BTU', 'MMBTU', 'therm'],
    'mass': ['kg', 'g', 'mg', 'tonne', 'ton', 'lb', 'lbs', 'oz'],
    'volume': ['liter', 'liters', 'l', 'L', 'ml', 'gallon', 'gal', 'm3', 'm³'],
    'distance': ['km', 'kilometer', 'm', 'meter', 'mile', 'mi', 'ft', 'nautical_mile'],
    'composite': ['passenger.km', 'tonne.km', 'vehicle.km']
}

# ===== LOGGING =====
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ===== VALIDACIÓN =====
VALIDATION_CONFIG = {
    'strict_mode': False,  # Si True, rechaza filas con cualquier error
    'allow_missing_geography': True,
    'allow_missing_year': True,
    'default_year': 2024,
    'min_activity_value': 0,
    'max_activity_value': 1e12  # 1 trillion
}

# ===== REPORTES =====
REPORT_CONFIG = {
    'default_format': 'CSV',  # CSV, PDF, DOCX
    'apa_version': 7,
    'include_charts': True,
    'include_methodology': True,
    'include_assumptions': True,
    'language': 'es'  # es, en
}

# ===== STREAMLIT UI =====
STREAMLIT_CONFIG = {
    'page_title': 'Calculadora Huella de Carbono - GHG Protocol',
    'page_icon': '🌱',
    'layout': 'wide',
    'theme': {
        'primaryColor': '#2E7D32',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730',
        'font': 'sans serif'
    }
}

# ===== OLLAMA (IA LOCAL) =====
OLLAMA_CONFIG = {
    'enabled': False,  # Cambiar a True si Ollama está instalado
    'model': 'llama3',  # llama3, mistral, codellama, etc.
    'api_url': 'http://localhost:11434',
    'temperature': 0.3,
    'max_tokens': 2048
}

# ===== REFERENCIAS BIBLIOGRÁFICAS (APA 7) =====
REFERENCES_APA7 = [
    "IPCC. (2006). 2006 IPCC Guidelines for National Greenhouse Gas Inventories. IGES. https://www.ipcc-nggip.iges.or.jp/public/2006gl/",
    
    "IPCC. (2019). 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories. IGES. https://www.ipcc.ch/report/2019-refinement-to-the-2006-ipcc-guidelines-for-national-greenhouse-gas-inventories/",
    
    "UK Government. (2025). Government conversion factors for company reporting of greenhouse gas emissions. Department for Energy Security and Net Zero. https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting",
    
    "World Resources Institute & World Business Council for Sustainable Development. (2004). The Greenhouse Gas Protocol: A Corporate Accounting and Reporting Standard (Revised Edition). WRI. https://ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf",
    
    "World Resources Institute & World Business Council for Sustainable Development. (2011). Corporate Value Chain (Scope 3) Accounting and Reporting Standard. WRI. https://ghgprotocol.org/standards/scope-3-standard",
    
    "World Resources Institute & World Business Council for Sustainable Development. (2015). GHG Protocol Scope 2 Guidance. WRI. https://ghgprotocol.org/scope-2-guidance",
    
    "U.S. Environmental Protection Agency. (2024). Emission Factors Hub. EPA. https://www.epa.gov/climateleadership/ghg-emission-factors-hub"
]

# ===== AYUDA Y DOCUMENTACIÓN =====
HELP_TEXT = {
    'scope_1': """
    **Scope 1 - Emisiones Directas:**
    
    Emisiones de fuentes que son propiedad o están controladas por la organización:
    - Combustión estacionaria: calderas, hornos, generadores
    - Combustión móvil: vehículos de empresa, equipos móviles
    - Proceso: reacciones químicas, producción
    - Fugitivas: refrigerantes, fugas de gas natural, CH₄
    """,
    
    'scope_2': """
    **Scope 2 - Emisiones Indirectas de Energía:**
    
    Emisiones de la generación de energía comprada:
    - Electricidad comprada
    - Calor/vapor comprado
    - Refrigeración comprada
    
    Métodos de cálculo:
    - Location-based (obligatorio): factor promedio de red
    - Market-based (opcional): contratos específicos, RECs
    """,
    
    'scope_3': """
    **Scope 3 - Otras Emisiones Indirectas:**
    
    Emisiones de la cadena de valor (15 categorías):
    
    **Upstream:**
    1. Bienes y servicios comprados
    2. Bienes de capital
    3. Combustibles y energía
    4. Transporte upstream
    5. Residuos
    6. Viajes de negocio
    7. Desplazamientos empleados
    8. Activos arrendados upstream
    
    **Downstream:**
    9. Transporte downstream
    10. Procesamiento de productos
    11. Uso de productos
    12. Fin de vida de productos
    13. Activos arrendados downstream
    14. Franquicias
    15. Inversiones
    """
}
