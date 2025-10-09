"""
Carbon GHG Calculator - REST API
FastAPI implementation for emission calculations

Endpoints:
- POST /api/v1/calculate - Calculate emissions
- GET /api/v1/factors - List available factors
- GET /api/v1/health - Health check
- GET /docs - Interactive API documentation (Swagger UI)
- GET /redoc - Alternative API documentation

Author: Carbon GHG Team
Version: 1.0.0
License: MIT
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import pandas as pd
import logging

# Import project modules
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from calculators.core import compute_emission, aggregate_emissions_by_scope, aggregate_emissions_by_category
from utils.factors import load_uk_gov_factors, find_factor
from models.emissions import ActivityRecord, EmissionFactor, EmissionResult

# Setup logger
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Carbon GHG Calculator API",
    description="REST API for calculating greenhouse gas emissions according to GHG Protocol",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Carbon GHG Team",
        "url": "https://github.com/YOUR-USERNAME/carbon-ghg-calculator",
        "email": "your-email@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Add CORS middleware (permite requests desde cualquier origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load emission factors at startup
print("🔄 Loading emission factors...")
try:
    factors_df = load_uk_gov_factors("data/ghg-conversion-factors-2025-condensed-set.xlsx")
    print(f"✅ Loaded {len(factors_df)} emission factors")
except Exception as e:
    print(f"❌ Error loading factors: {e}")
    factors_df = pd.DataFrame()


# ==================== Pydantic Models ====================

class ActivityRequestAPI(BaseModel):
    """Activity request for API - No validation transformations"""
    entity_id: str = Field(..., description="Unique identifier for this activity")
    scope: int = Field(..., ge=1, le=3, description="GHG Protocol scope (1, 2, or 3)")
    category: str = Field(..., description="Activity category (e.g., 'Gaseous fuels', 'Diesel')")
    activity_value: float = Field(..., gt=0, description="Quantity of activity")
    activity_unit: str = Field(..., description="Unit of measurement (e.g., 'litres', 'kWh')")
    geography: Optional[str] = Field(None, description="Geography code (e.g., 'UK', 'USA')")
    year: Optional[int] = Field(2025, ge=1990, le=2100, description="Year of activity")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month of activity")
    facility: Optional[str] = Field(None, description="Facility or site")
    description: Optional[str] = Field(None, description="Additional description")

class CalculateRequest(BaseModel):
    """Request body for emission calculation"""
    activities: List[ActivityRequestAPI] = Field(
        ...,
        description="List of activities to calculate emissions for",
        example=[
            {
                "entity_id": "factory-001",
                "scope": 1,
                "category": "mobile_combustion",
                "activity_value": 1000.0,
                "activity_unit": "liters",
                "geography": "GBR",
                "year": 2025
            }
        ]
    )

class EmissionResultAPI(BaseModel):
    """Simplified emission result for API response"""
    entity_id: str
    scope: int
    category: str
    activity_value: float
    activity_unit: str
    emission_kg_co2e: float
    emission_tonnes_co2e: float
    factor_source: str
    calculation_date: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "entity_id": "factory-001",
                "scope": 1,
                "category": "mobile_combustion",
                "activity_value": 1000.0,
                "activity_unit": "liters",
                "emission_kg_co2e": 2684.42,
                "emission_tonnes_co2e": 2.68442,
                "factor_source": "UK Gov 2025",
                "calculation_date": "2025-10-08T10:30:00"
            }
        }

class CalculateResponse(BaseModel):
    """Response body for emission calculation"""
    success: bool = True
    results: List[EmissionResultAPI]
    total_emissions_kg: float
    total_emissions_tonnes: float
    aggregation_by_scope: Dict[int, float]
    aggregation_by_category: Dict[str, float]
    calculation_timestamp: datetime = Field(default_factory=datetime.now)

class FactorQueryResponse(BaseModel):
    """Response for factor queries"""
    total_factors: int
    factors: List[Dict]
    filters_applied: Dict[str, str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "1.0.0"
    factors_loaded: int
    timestamp: datetime = Field(default_factory=datetime.now)


# ==================== Helper Functions ====================

def emission_result_to_api(result: EmissionResult) -> EmissionResultAPI:
    """Convert EmissionResult to API-friendly format"""
    return EmissionResultAPI(
        entity_id=result.activity_record.entity_id,
        scope=result.activity_record.scope,
        category=result.activity_record.category,
        activity_value=result.activity_record.activity_value,
        activity_unit=result.activity_record.activity_unit,
        emission_kg_co2e=result.emission_kgCO2e,
        emission_tonnes_co2e=result.emission_tCO2e,
        factor_source=result.emission_factor.source,
        calculation_date=result.calculation_date
    )

def find_matching_factor_for_api(activity: ActivityRecord, factors_df: pd.DataFrame) -> Optional[EmissionFactor]:
    """
    Find matching emission factor for an activity using the simplified DataFrame structure.
    
    DataFrame columns: Activity, Fuel, kgCO2e, Unit, Source, Sheet, Year
    """
    # Start with all factors
    filtered = factors_df.copy()
    
    search_term = activity.category.lower().strip()
    unit_term = activity.activity_unit.lower().strip()
    
    # Search in Activity, Fuel, and Sheet columns
    matches = pd.DataFrame()
    
    for col in ['Activity', 'Fuel', 'Sheet']:
        if col in filtered.columns:
            try:
                col_matches = filtered[
                    filtered[col].astype(str).str.lower().str.contains(search_term, na=False, regex=False)
                ]
                if not col_matches.empty:
                    matches = pd.concat([matches, col_matches]).drop_duplicates()
            except:
                continue
    
    if matches.empty:
        logger.warning(f"No matches found for category '{activity.category}'")
        return None
    
    # Filter by unit
    if 'Unit' in matches.columns:
        # Try exact match first
        unit_exact = matches[matches['Unit'].str.lower() == unit_term]
        if not unit_exact.empty:
            matches = unit_exact
        else:
            # Try partial match
            unit_partial = matches[
                matches['Unit'].astype(str).str.lower().str.contains(unit_term, na=False, regex=False)
            ]
            if not unit_partial.empty:
                matches = unit_partial
    
    # Filter by year if available
    if 'Year' in matches.columns and activity.year:
        year_matches = matches[matches['Year'] == activity.year]
        if not year_matches.empty:
            matches = year_matches
    
    if matches.empty:
        logger.warning(f"No matches found after filtering by unit '{activity.activity_unit}'")
        return None
    
    # Take first match
    row = matches.iloc[0]
    
    # Build source description for notes field
    source_parts = []
    for col in ['Source', 'Sheet', 'Activity', 'Fuel']:
        if col in row.index and pd.notna(row[col]):
            source_parts.append(str(row[col]))
    source_desc = " - ".join(source_parts[:3])
    
    logger.info(f"✓ Factor found: {row['kgCO2e']} kg CO2e/{row['Unit']} - {source_desc}")
    
    return EmissionFactor(
        source="UK2025",  # Valid literal value
        source_version=str(row.get('Sheet', '')),  # Store sheet name here
        gas='CO2e',
        value=float(row['kgCO2e']),
        unit=f"kg CO2e per {row['Unit']}",
        year=int(row.get('Year', activity.year)),
        geography=activity.geography or 'UK',
        scope=activity.scope,
        category=str(row.get('Sheet', activity.category)),
        notes=source_desc  # Full description in notes
    )


# ==================== API Endpoints ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - Welcome message"""
    return {
        "message": "Welcome to Carbon GHG Calculator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns API status and basic metrics
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        factors_loaded=len(factors_df),
        timestamp=datetime.now()
    )

@app.post("/api/v1/calculate", response_model=CalculateResponse, tags=["Calculations"])
async def calculate_emissions(request: CalculateRequest):
    """
    Calculate GHG emissions for a list of activities
    
    - **activities**: List of activity records with entity_id, scope, category, value, unit, etc.
    
    Returns:
    - Individual emission results
    - Total emissions (kg and tonnes)
    - Aggregations by scope and category
    """
    if not request.activities:
        raise HTTPException(status_code=400, detail="No activities provided")
    
    if factors_df.empty:
        raise HTTPException(status_code=503, detail="Emission factors not loaded")
    
    results = []
    api_results = []
    
    for activity_api in request.activities:
        # Create a search activity with original category (no validation transformation)
        search_activity = ActivityRecord(
            entity_id=activity_api.entity_id,
            scope=activity_api.scope,
            category="temp",  # Use temp to avoid validation
            activity_value=activity_api.activity_value,
            activity_unit=activity_api.activity_unit,
            geography=activity_api.geography,
            year=activity_api.year or 2025
        )
        # Override category with original value for search
        search_activity.__dict__['category'] = activity_api.category
        
        # Find matching emission factor using original category
        factor = find_matching_factor_for_api(search_activity, factors_df)
        
        if not factor:
            raise HTTPException(
                status_code=404,
                detail=f"No emission factor found for activity: {activity_api.category}, {activity_api.activity_unit}, scope {activity_api.scope}"
            )
        
        # Calculate emission using properly validated ActivityRecord
        try:
            # Create activity for calculation (will go through validation)
            calc_activity = ActivityRecord(
                entity_id=activity_api.entity_id,
                scope=activity_api.scope,
                category=activity_api.category,  # Will be validated/transformed
                activity_value=activity_api.activity_value,
                activity_unit=activity_api.activity_unit,
                geography=activity_api.geography,
                year=activity_api.year
            )
            
            result = compute_emission(calc_activity, factor)
            results.append(result)
            api_results.append(emission_result_to_api(result))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating emission for {activity_api.entity_id}: {str(e)}"
            )
    
    # Calculate aggregations
    agg_scope = aggregate_emissions_by_scope(results)
    agg_category = aggregate_emissions_by_category(results)
    
    # Calculate totals
    total_kg = sum(r.emission_kgCO2e for r in results)
    total_tonnes = total_kg / 1000.0
    
    return CalculateResponse(
        success=True,
        results=api_results,
        total_emissions_kg=total_kg,
        total_emissions_tonnes=total_tonnes,
        aggregation_by_scope=agg_scope,
        aggregation_by_category=agg_category,
        calculation_timestamp=datetime.now()
    )

@app.get("/api/v1/factors", response_model=FactorQueryResponse, tags=["Factors"])
async def list_factors(
    sheet: Optional[str] = Query(None, description="Sheet name (e.g., Fuels, Passenger vehicles)"),
    activity: Optional[str] = Query(None, description="Activity type"),
    fuel: Optional[str] = Query(None, description="Fuel type"),
    unit: Optional[str] = Query(None, description="Unit of measurement"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of factors to return")
):
    """
    List available emission factors
    
    Real DataFrame columns: Activity, Fuel, kgCO2e, Unit, Source, Sheet, Year
    
    - **sheet**: Filter by sheet name (data source category)
    - **activity**: Filter by activity type
    - **fuel**: Filter by fuel type
    - **unit**: Filter by unit of measurement
    - **limit**: Maximum results to return (default: 100, max: 1000)
    
    Returns list of matching emission factors with their details
    """
    if factors_df.empty:
        raise HTTPException(status_code=503, detail="Emission factors not loaded")
    
    filtered = factors_df.copy()
    filters_applied = {}
    
    # Apply filters based on real columns
    if sheet:
        if 'Sheet' in filtered.columns:
            filtered = filtered[filtered['Sheet'].str.contains(sheet, case=False, na=False)]
            filters_applied['sheet'] = sheet
    
    if activity:
        if 'Activity' in filtered.columns:
            filtered = filtered[filtered['Activity'].str.contains(activity, case=False, na=False)]
            filters_applied['activity'] = activity
    
    if fuel:
        if 'Fuel' in filtered.columns:
            filtered = filtered[filtered['Fuel'].str.contains(fuel, case=False, na=False)]
            filters_applied['fuel'] = fuel
    
    if unit:
        if 'Unit' in filtered.columns:
            filtered = filtered[filtered['Unit'].str.contains(unit, case=False, na=False)]
            filters_applied['unit'] = unit
    
    # Limit results
    filtered = filtered.head(limit)
    
    # Convert to list of dicts
    factors_list = filtered.to_dict('records')
    
    return FactorQueryResponse(
        total_factors=len(filtered),
        factors=factors_list,
        filters_applied=filters_applied
    )

@app.get("/api/v1/categories", tags=["Reference Data"])
async def list_categories():
    """
    List all available emission categories (sheets and activities)
    
    Real DataFrame columns: Activity, Fuel, kgCO2e, Unit, Source, Sheet, Year
    
    Returns categorized list of sheets and activities
    """
    if factors_df.empty:
        raise HTTPException(status_code=503, detail="Emission factors not loaded")
    
    result = {}
    
    # Get unique sheets
    if 'Sheet' in factors_df.columns:
        sheets = sorted(factors_df['Sheet'].dropna().unique().tolist())
        result["sheets"] = sheets
    
    # Get unique activities
    if 'Activity' in factors_df.columns:
        activities = sorted(factors_df['Activity'].dropna().unique().tolist())
        result["activities"] = activities
    
    # Get unique fuels
    if 'Fuel' in factors_df.columns:
        fuels = sorted(factors_df['Fuel'].dropna().unique().tolist())
        result["fuels"] = fuels
    
    # Get unique units
    if 'Unit' in factors_df.columns:
        units = sorted(factors_df['Unit'].dropna().unique().tolist())
        result["units"] = units
    
    result["total_factors"] = len(factors_df)
    
    return result


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Execute on API startup"""
    print("🚀 Carbon GHG Calculator API starting...")
    print(f"📊 Loaded {len(factors_df)} emission factors")
    print("✅ API ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Execute on API shutdown"""
    print("👋 Carbon GHG Calculator API shutting down...")


# ==================== Main (for local testing) ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🌍 Carbon GHG Calculator API")
    print("=" * 60)
    print("📚 Documentation: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("🏥 Health check: http://localhost:8000/api/v1/health")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
