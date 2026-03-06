#!/usr/bin/env python3
"""Test script to verify ML API endpoints"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_root():
    """Test the root endpoint"""
    print("Testing GET /")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_pcos():
    """Test PCOS prediction endpoint"""
    print("Testing POST /ml-predict with PCOS model")
    payload = {
        "model_type": "pcos",
        "input_data": {
            "age": 28,
            "weight": 65,
            "bmi": 24,
            "cycleRegular": True,
            "cycleLength": 28,
            "weightGain": False,
            "hairGrowth": False,
            "skinDarkening": False,
            "hairLoss": False,
            "pimples": False,
            "fastFood": False,
            "regularExercise": True,
            "follicleLeft": 5,
            "follicleRight": 6,
            "endometrium": 8
        }
    }
    try:
        response = requests.post(f"{BASE_URL}/ml-predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_menopause():
    """Test Menopause prediction endpoint"""
    print("Testing POST /ml-predict with Menopause model")
    payload = {
        "model_type": "menopause",
        "input_data": {
            "age": 45,
            "estrogenLevel": 50,
            "fshLevel": 30,
            "yearsSinceLastPeriod": 0,
            "irregularPeriods": True,
            "missedPeriods": False,
            "hotFlashes": False,
            "nightSweats": False,
            "sleepProblems": False,
            "vaginalDryness": False,
            "jointPain": False
        }
    }
    try:
        response = requests.post(f"{BASE_URL}/ml-predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_cycle():
    """Test Cycle prediction endpoint"""
    print("Testing POST /ml-predict with Cycle model")
    payload = {
        "model_type": "cycle",
        "input_data": {
            "prev1": 28,
            "prev2": 29,
            "prev3": 27,
            "lastPeriodStart": "2026-03-01T00:00:00.000Z"
        }
    }
    try:
        response = requests.post(f"{BASE_URL}/ml-predict", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("NaariCare ML Backend API Test Suite")
    print("=" * 60 + "\n")

    results = {
        "Root": test_root(),
        "PCOS": test_pcos(),
        "Menopause": test_menopause(),
        "Cycle": test_cycle()
    }

    print("=" * 60)
    print("Test Results Summary:")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    print("=" * 60)
    print(f"Overall: {sum(results.values())}/{len(results)} tests passed")
