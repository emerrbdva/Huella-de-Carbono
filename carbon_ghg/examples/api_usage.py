"""
Ejemplos de uso de la API REST - Carbon GHG Calculator

Para ejecutar la API:
    uvicorn api.main:app --reload --port 8000

Documentación interactiva:
    http://localhost:8000/docs
"""

import requests
import json

# Base URL de la API
BASE_URL = "http://localhost:8000"


def example_1_health_check():
    """Example 1: Health check"""
    print("\n" + "="*60)
    print("Example 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/v1/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def example_2_calculate_single_emission():
    """Example 2: Calculate emission for single activity"""
    print("\n" + "="*60)
    print("Example 2: Calculate Single Emission")
    print("="*60)
    
    # Diesel fuel consumption
    payload = {
        "activities": [
            {
                "entity_id": "fleet-vehicle-001",
                "scope": 1,
                "category": "mobile_combustion",
                "activity_value": 500.0,
                "activity_unit": "liters",
                "geography": "GBR",
                "year": 2025
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success!")
        print(f"Total Emissions: {data['total_emissions_tonnes']:.2f} tonnes CO2e")
        print(f"Total Emissions: {data['total_emissions_kg']:.2f} kg CO2e")
        print(f"\nResults:")
        for result in data['results']:
            print(f"  - {result['entity_id']}: {result['emission_kg_co2e']:.2f} kg CO2e")
    else:
        print(f"❌ Error: {response.text}")


def example_3_calculate_multiple_emissions():
    """Example 3: Calculate emissions for multiple activities"""
    print("\n" + "="*60)
    print("Example 3: Calculate Multiple Emissions")
    print("="*60)
    
    payload = {
        "activities": [
            {
                "entity_id": "factory-diesel-001",
                "scope": 1,
                "category": "mobile_combustion",
                "activity_value": 1000.0,
                "activity_unit": "liters",
                "geography": "GBR",
                "year": 2025
            },
            {
                "entity_id": "office-electricity-001",
                "scope": 2,
                "category": "purchased_electricity",
                "activity_value": 10000.0,
                "activity_unit": "kWh",
                "geography": "GBR",
                "year": 2025
            },
            {
                "entity_id": "warehouse-gas-001",
                "scope": 1,
                "category": "stationary_combustion",
                "activity_value": 5000.0,
                "activity_unit": "kWh",
                "geography": "GBR",
                "year": 2025
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success!")
        print(f"Total Emissions: {data['total_emissions_tonnes']:.2f} tonnes CO2e")
        
        print(f"\nAggregation by Scope:")
        for scope, total in data['aggregation_by_scope'].items():
            print(f"  Scope {scope}: {total:.2f} tonnes CO2e")
        
        print(f"\nAggregation by Category:")
        for category, total in data['aggregation_by_category'].items():
            print(f"  {category}: {total:.2f} tonnes CO2e")
        
        print(f"\nIndividual Results:")
        for result in data['results']:
            print(f"  - {result['entity_id']}: {result['emission_kg_co2e']:.2f} kg CO2e")
    else:
        print(f"❌ Error: {response.text}")


def example_4_list_factors():
    """Example 4: List available emission factors"""
    print("\n" + "="*60)
    print("Example 4: List Emission Factors")
    print("="*60)
    
    # List factors for Scope 1, mobile combustion
    params = {
        "scope": 1,
        "category": "mobile",
        "limit": 10
    }
    
    response = requests.get(
        f"{BASE_URL}/api/v1/factors",
        params=params
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Found {data['total_factors']} factors")
        print(f"Filters applied: {data['filters_applied']}")
        
        print(f"\nFirst 5 factors:")
        for i, factor in enumerate(data['factors'][:5], 1):
            print(f"\n{i}. {factor.get('category', 'N/A')}")
            print(f"   Unit: {factor.get('unit', 'N/A')}")
            print(f"   Value: {factor.get('value', 'N/A')} kg CO2e")
            print(f"   Source: {factor.get('source', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")


def example_5_list_categories():
    """Example 5: List all categories by scope"""
    print("\n" + "="*60)
    print("Example 5: List Categories by Scope")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/v1/categories")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Total categories: {data['total_categories']}")
        
        for scope_key, categories in data['categories_by_scope'].items():
            print(f"\n{scope_key.upper()}:")
            for category in categories[:5]:  # Show first 5
                print(f"  - {category}")
            if len(categories) > 5:
                print(f"  ... and {len(categories) - 5} more")
    else:
        print(f"❌ Error: {response.text}")


def example_6_curl_commands():
    """Example 6: cURL commands for testing"""
    print("\n" + "="*60)
    print("Example 6: cURL Commands")
    print("="*60)
    
    print("\n1. Health Check:")
    print('curl -X GET "http://localhost:8000/api/v1/health"')
    
    print("\n2. Calculate Emission:")
    print('''curl -X POST "http://localhost:8000/api/v1/calculate" \\
  -H "Content-Type: application/json" \\
  -d '{
    "activities": [
      {
        "entity_id": "test-001",
        "scope": 1,
        "category": "mobile_combustion",
        "activity_value": 500,
        "activity_unit": "liters",
        "geography": "GBR",
        "year": 2025
      }
    ]
  }'
''')
    
    print("\n3. List Factors:")
    print('curl -X GET "http://localhost:8000/api/v1/factors?scope=1&limit=10"')
    
    print("\n4. List Categories:")
    print('curl -X GET "http://localhost:8000/api/v1/categories"')


def run_all_examples():
    """Run all examples"""
    try:
        example_1_health_check()
        example_2_calculate_single_emission()
        example_3_calculate_multiple_emissions()
        example_4_list_factors()
        example_5_list_categories()
        example_6_curl_commands()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running:")
        print("  uvicorn api.main:app --reload --port 8000")
        print("\n")
        example_6_curl_commands()


if __name__ == "__main__":
    print("🌍 Carbon GHG Calculator API - Examples")
    print("\n⚠️  Make sure the API is running first:")
    print("   uvicorn api.main:app --reload --port 8000")
    print("\nPress Enter to continue...")
    input()
    
    run_all_examples()
