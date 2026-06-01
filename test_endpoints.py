#!/usr/bin/env python3
"""
Test script to verify all API endpoints work correctly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from main import app

def test_endpoints():
    client = TestClient(app)

    print("Testing API endpoints...")

    # Test health endpoint
    print("\n1. Testing /healthz endpoint...")
    response = client.get("/healthz")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(" Health check passed")
    else:
        print(" Health check failed")

    # Test root endpoint
    print("\n2. Testing / endpoint...")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(" Root endpoint passed")
    else:
        print(" Root endpoint failed")

    # Test events analytics endpoint
    print("\n3. Testing /api/events/ endpoint...")
    response = client.get("/api/events/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(" Events analytics endpoint passed")
        print(f"Response: {response.json()}")
    else:
        print(" Events analytics endpoint failed")

    # Test create event endpoint
    print("\n4. Testing POST /api/events/ endpoint...")
    event_data = {
        "page": "/test",
        "user_agent": "test-agent",
        "ip_address": "127.0.0.1",
        "referrer": "",
        "session_id": "test-session",
        "duration": 100,
        "description": "Test event"
    }
    response = client.post("/api/events/", json=event_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(" Create event endpoint passed")
        event_id = response.json().get('id')
        print(f"Created event with ID: {event_id}")
    else:
        print(" Create event endpoint failed")
        print(f"Response: {response.text}")
        event_id = None

    # Test get event endpoint
    if event_id:
        print(f"\n5. Testing GET /api/events/{event_id} endpoint...")
        response = client.get(f"/api/events/{event_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(" Get event endpoint passed")
        else:
            print(" Get event endpoint failed")

        # Test update event endpoint
        print(f"\n6. Testing PUT /api/events/{event_id} endpoint...")
        update_data = {
            "page": "/updated-test",
            "description": "Updated test event"
        }
        response = client.put(f"/api/events/{event_id}", json=update_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(" Update event endpoint passed")
        else:
            print(" Update event endpoint failed")
            print(f"Response: {response.text}")

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_endpoints()