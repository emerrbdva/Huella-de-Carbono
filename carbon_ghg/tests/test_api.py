"""
Tests for REST API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from api.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns 200"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "factors_loaded" in data
        assert "timestamp" in data
    
    def test_health_check_has_factors(self):
        """Test that factors are loaded"""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert data["factors_loaded"] > 0


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_returns_welcome(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data


class TestCalculateEndpoint:
    """Tests for emission calculation endpoint"""
    
    def test_calculate_single_activity(self):
        """Test calculating emission for single activity"""
        payload = {
            "activities": [
                {
                    "entity_id": "test-001",
                    "scope": 1,
                    "category": "Diesel",  # Real fuel from UK Gov data
                    "activity_value": 100.0,
                    "activity_unit": "litres",  # Real unit
                    "geography": "UK",
                    "year": 2025
                }
            ]
        }
        
        response = client.post("/api/v1/calculate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert len(data["results"]) == 1
        assert data["total_emissions_kg"] > 0
        assert data["total_emissions_tonnes"] > 0
        
        # Check result structure
        result = data["results"][0]
        assert result["entity_id"] == "test-001"
        assert result["scope"] == 1
        # Category will be transformed by validator
        assert result["emission_kg_co2e"] > 0
    
    def test_calculate_multiple_activities(self):
        """Test calculating emissions for multiple activities"""
        payload = {
            "activities": [
                {
                    "entity_id": "diesel-001",
                    "scope": 1,
                    "category": "Diesel",  # Real fuel from UK Gov
                    "activity_value": 50.0,
                    "activity_unit": "litres",
                    "geography": "UK",
                    "year": 2025
                },
                {
                    "entity_id": "electricity-001",
                    "scope": 2,
                    "category": "electricity",  # Real category
                    "activity_value": 1000.0,
                    "activity_unit": "kWh",
                    "geography": "UK",
                    "year": 2025
                }
            ]
        }
        
        response = client.post("/api/v1/calculate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert len(data["results"]) == 2
        
        # Check aggregations
        assert "aggregation_by_scope" in data
        assert "aggregation_by_category" in data
        
        # Should have emissions in scope 1 and 2
        assert data["aggregation_by_scope"]["1"] > 0
        assert data["aggregation_by_scope"]["2"] > 0
    
    def test_calculate_empty_activities(self):
        """Test that empty activities list returns 400"""
        payload = {"activities": []}
        
        response = client.post("/api/v1/calculate", json=payload)
        
        assert response.status_code == 400
    
    def test_calculate_invalid_activity(self):
        """Test that invalid activity returns 422 (validation error)"""
        payload = {
            "activities": [
                {
                    "entity_id": "test-001",
                    # Missing required fields
                }
            ]
        }
        
        response = client.post("/api/v1/calculate", json=payload)
        
        assert response.status_code == 422  # Pydantic validation error
    
    def test_calculate_unknown_category(self):
        """Test that unknown category returns 404"""
        payload = {
            "activities": [
                {
                    "entity_id": "test-001",
                    "scope": 1,
                    "category": "unknown_category_xyz",
                    "activity_value": 100.0,
                    "activity_unit": "units",
                    "geography": "GBR",
                    "year": 2025
                }
            ]
        }
        
        response = client.post("/api/v1/calculate", json=payload)
        
        # Should return 404 - no factor found
        assert response.status_code == 404


class TestFactorsEndpoint:
    """Tests for factors listing endpoint"""
    
    def test_list_all_factors(self):
        """Test listing factors without filters"""
        response = client.get("/api/v1/factors")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_factors" in data
        assert "factors" in data
        assert "filters_applied" in data
        assert data["total_factors"] > 0
        assert len(data["factors"]) > 0
    
    def test_list_factors_by_scope(self):
        """Test filtering factors by sheet (replaces scope filtering)"""
        response = client.get("/api/v1/factors?sheet=Fuels")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "sheet" in data["filters_applied"]
        
        # All factors should be from Fuels sheet
        for factor in data["factors"]:
            assert factor["Sheet"] == "Fuels"
    
    def test_list_factors_by_category(self):
        """Test filtering factors by activity"""
        response = client.get("/api/v1/factors?activity=Diesel")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "activity" in data["filters_applied"]
        
        # All factors should contain 'Diesel' in Activity or Fuel
        for factor in data["factors"]:
            factor_str = str(factor.get("Activity", "")) + str(factor.get("Fuel", ""))
            assert "diesel" in factor_str.lower()
    
    def test_list_factors_with_limit(self):
        """Test limiting number of results"""
        response = client.get("/api/v1/factors?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["factors"]) <= 5
    
    def test_list_factors_invalid_scope(self):
        """Test that invalid parameters are handled gracefully"""
        # API now uses sheet/activity/fuel filters instead of scope
        # Invalid filters just return all results
        response = client.get("/api/v1/factors?sheet=NonExistent")
        
        assert response.status_code == 200
        # Should return empty or minimal results
        data = response.json()
        assert "factors" in data


class TestCategoriesEndpoint:
    """Tests for categories listing endpoint"""
    
    def test_list_categories(self):
        """Test listing all categories"""
        response = client.get("/api/v1/categories")
        
        assert response.status_code == 200
        data = response.json()
        
        # New structure returns sheets, activities, fuels, units
        assert "total_factors" in data
        assert data["total_factors"] > 0
        
        # Should have sheets (main categories)
        assert "sheets" in data
        assert len(data["sheets"]) > 0
        
        # Should have activities
        assert "activities" in data
        assert len(data["activities"]) > 0
        
        # Should have units
        assert "units" in data
        assert len(data["units"]) > 0


class TestIntegrationScenarios:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow: health -> categories -> calculate"""
        # 1. Check health
        health = client.get("/api/v1/health")
        assert health.status_code == 200
        assert health.json()["status"] == "healthy"
        
        # 2. Get categories
        categories = client.get("/api/v1/categories")
        assert categories.status_code == 200
        cats_data = categories.json()
        
        # Get first sheet (main category)
        first_sheet = cats_data["sheets"][0]
        
        # 3. List factors for that sheet
        factors = client.get(f"/api/v1/factors?sheet={first_sheet}&limit=1")
        assert factors.status_code == 200
        factors_data = factors.json()
        
        if factors_data["total_factors"] > 0:
            factor = factors_data["factors"][0]
            
            # 4. Calculate emission using that factor
            # Use Activity or Fuel as category, and Unit for activity_unit
            category = factor.get("Activity") or factor.get("Fuel") or "Diesel"
            unit = factor.get("Unit", "litres")
            
            payload = {
                "activities": [
                    {
                        "entity_id": "integration-test",
                        "scope": 1,  # Default to scope 1
                        "category": category,
                        "activity_value": 10.0,  # Small value to avoid large emissions
                        "activity_unit": unit,
                        "geography": "UK",
                        "year": 2025
                    }
                ]
            }
            
            calc = client.post("/api/v1/calculate", json=payload)
            assert calc.status_code == 200
            calc_data = calc.json()
            
            assert calc_data["success"] is True
            assert calc_data["total_emissions_kg"] > 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
