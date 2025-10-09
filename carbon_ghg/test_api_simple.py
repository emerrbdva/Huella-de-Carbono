"""Simple test to verify API works with real data"""
from fastapi.testclient import TestClient
import sys
sys.path.append('.')

from api.main import app

client = TestClient(app)

# Test 1: Health check
print("=" * 60)
print("TEST 1: Health Check")
print("=" * 60)
response = client.get("/api/v1/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test 2: List categories
print("=" * 60)
print("TEST 2: List Categories")
print("=" * 60)
response = client.get("/api/v1/categories")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Total factors: {data.get('total_factors')}")
print(f"Sheets: {data.get('sheets', [])[:3]}")
print(f"Activities: {data.get('activities', [])[:3]}")
print(f"Units: {data.get('units', [])[:5]}")
print()

# Test 3: List factors
print("=" * 60)
print("TEST 3: List Factors (first 5)")
print("=" * 60)
response = client.get("/api/v1/factors?limit=5")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Total: {data.get('total_factors')}")
if 'factors' in data and len(data['factors']) > 0:
    print(f"First factor: {data['factors'][0]}")
print()

# Test 4: Calculate emission
print("=" * 60)
print("TEST 4: Calculate Emission - Gaseous fuels/litres")
print("=" * 60)
payload = {
    "activities": [
        {
            "entity_id": "test-001",
            "scope": 1,
            "category": "Gaseous fuels",  # Real category from UK Gov data
            "activity_value": 100.0,
            "activity_unit": "litres",  # Real unit from UK Gov data
            "geography": "UK",
            "year": 2025
        }
    ]
}
response = client.post("/api/v1/calculate", json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Total emissions (kg): {data.get('total_emissions_kg')}")
    if 'results' in data and len(data['results']) > 0:
        print(f"First result: {data['results'][0]}")
else:
    print(f"Error: {response.json()}")
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
