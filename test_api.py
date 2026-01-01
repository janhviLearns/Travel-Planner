#!/usr/bin/env python
"""
Simple test script for the Travel Planner API.
Run this after starting the server to verify everything works.
"""
import httpx
import json
import time
import sys


def test_api():
    """Test the Travel Planner API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Multi-Source Travel Planner API\n")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = httpx.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   ⚠️  Make sure the server is running: python main.py")
        return False
    
    # Test 2: Trip endpoint with popular city
    print("\n2. Testing trip endpoint (Paris, 3 days)...")
    try:
        start = time.time()
        response = httpx.get(
            f"{base_url}/trip",
            params={"city": "Paris", "days": 3},
            timeout=30.0
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Trip endpoint passed ({elapsed:.2f}s)")
            print(f"   City: {data['city']}")
            print(f"   Country: {data['country']}")
            print(f"   Coordinates: {data['coordinates']}")
            print(f"   Weather days: {len(data['weather_forecast'])}")
            print(f"   Attractions: {len(data['top_attractions'])}")
            print(f"   Cached: {data['cached']}")
            
            # Pretty print first weather day
            if data['weather_forecast']:
                weather = data['weather_forecast'][0]
                print(f"\n   📅 First day weather:")
                print(f"      Date: {weather['date']}")
                print(f"      Temp: {weather['temp_min']}°C - {weather['temp_max']}°C")
                print(f"      Description: {weather['description']}")
            
            # Show first attraction
            if data['top_attractions']:
                attr = data['top_attractions'][0]
                print(f"\n   🏛️  Top attraction:")
                print(f"      Name: {attr['name']}")
                print(f"      Category: {attr['category']}")
                print(f"      Distance: {attr['distance']} km")
        else:
            print(f"   ❌ Trip endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   ⚠️  Check your API keys in .env file")
        return False
    
    # Test 3: Cache test (same request)
    print("\n3. Testing cache (same request)...")
    try:
        start = time.time()
        response = httpx.get(
            f"{base_url}/trip",
            params={"city": "Paris", "days": 3},
            timeout=30.0
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if data['cached']:
                print(f"   ✅ Cache working! ({elapsed:.2f}s - much faster)")
            else:
                print(f"   ⚠️  Response not cached (Redis might not be running)")
        else:
            print(f"   ❌ Cache test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Different city
    print("\n4. Testing with different city (Tokyo, 2 days)...")
    try:
        start = time.time()
        response = httpx.get(
            f"{base_url}/trip",
            params={"city": "Tokyo", "days": 2},
            timeout=30.0
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Different city works ({elapsed:.2f}s)")
            print(f"   City: {data['city']}, Country: {data['country']}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Invalid city (error handling)
    print("\n5. Testing error handling (invalid city)...")
    try:
        response = httpx.get(
            f"{base_url}/trip",
            params={"city": "InvalidCityXYZ123", "days": 3},
            timeout=30.0
        )
        
        if response.status_code == 404:
            print(f"   ✅ Error handling works (404 for invalid city)")
            print(f"   Error message: {response.json().get('error', 'N/A')}")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Testing complete!\n")
    return True


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)

