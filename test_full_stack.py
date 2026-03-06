#!/usr/bin/env python3
"""
NaariCare Full Stack Functionality Test
Tests both backend API and frontend integration
"""

import requests
import json
import time
from datetime import datetime

def test_backend_api():
    """Test backend ML API endpoints"""
    print("🔍 Testing Backend API...")

    base_url = "http://127.0.0.1:8001"

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        print("✅ Root endpoint: PASSED")
    except Exception as e:
        print(f"❌ Root endpoint: FAILED - {e}")
        return False

    # Test PCOS prediction
    try:
        pcos_data = {
            "age": 25,
            "height": 165,
            "weight": 60,
            "bmi": 22.0,
            "cycleRegular": True,
            "cycleLength": 28,
            "weightGain": False,
            "hairGrowth": False,
            "skinDarkening": False,
            "hairLoss": False,
            "pimples": False,
            "fastFood": False,
            "regularExercise": True,
            "follicleLeft": 8,
            "follicleRight": 7,
            "endometrium": 8.5,
            "lh": 5.2,
            "fsh": 6.1,
            "testosterone": 0.5,
            "insulin": 8.5
        }

        response = requests.post(
            f"{base_url}/ml-predict",
            json={"model_type": "pcos", "input_data": pcos_data}
        )
        assert response.status_code == 200
        result = response.json()
        assert "prediction" in result
        print("✅ PCOS prediction: PASSED")
    except Exception as e:
        print(f"❌ PCOS prediction: FAILED - {e}")
        return False

    # Test Cycle prediction
    try:
        cycle_data = {
            "lastPeriodStart": datetime.now().isoformat(),
            "averageCycleLength": 28,
            "cycleVariability": 2,
            "symptoms": ["cramps", "mood_changes"],
            "flowIntensity": "medium",
            "stressLevel": 3,
            "sleepHours": 7,
            "exerciseFrequency": 3
        }

        response = requests.post(
            f"{base_url}/ml-predict",
            json={"model_type": "cycle", "input_data": cycle_data}
        )
        assert response.status_code == 200
        result = response.json()
        assert "prediction" in result
        print("✅ Cycle prediction: PASSED")
    except Exception as e:
        print(f"❌ Cycle prediction: FAILED - {e}")
        return False

    # Test Menopause prediction (should fallback)
    try:
        menopause_data = {
            "age": 45,
            "estrogenLevel": 25.0,
            "fshLevel": 35.0,
            "yearsSinceLastPeriod": 0,
            "irregularPeriods": True,
            "missedPeriods": False,
            "hotFlashes": True,
            "nightSweats": False,
            "sleepProblems": True,
            "vaginalDryness": False,
            "jointPain": False
        }

        response = requests.post(
            f"{base_url}/ml-predict",
            json={"model_type": "menopause", "input_data": menopause_data}
        )
        assert response.status_code == 200
        result = response.json()
        assert result.get("fallback") == True  # Should use fallback
        print("✅ Menopause prediction (fallback): PASSED")
    except Exception as e:
        print(f"❌ Menopause prediction: FAILED - {e}")
        return False

    return True

def test_frontend_connectivity():
    """Test frontend can load and connect to backend"""
    print("\n🔍 Testing Frontend Connectivity...")

    # Test development server
    try:
        response = requests.get("http://localhost:8081", timeout=10)
        assert response.status_code == 200
        assert "NaariCare" in response.text or "html" in response.text.lower()
        print("✅ Frontend dev server: PASSED")
    except Exception as e:
        print(f"❌ Frontend dev server: FAILED - {e}")
        return False

    # Test production build
    try:
        response = requests.get("http://localhost:4173", timeout=10)
        assert response.status_code == 200
        assert "NaariCare" in response.text or "html" in response.text.lower()
        print("✅ Frontend prod build: PASSED")
    except Exception as e:
        print(f"❌ Frontend prod build: FAILED - {e}")
        return False

    return True

def test_pwa_features():
    """Test PWA manifest and service worker"""
    print("\n🔍 Testing PWA Features...")

    base_url = "http://localhost:4173"

    # Test manifest
    try:
        response = requests.get(f"{base_url}/manifest.webmanifest")
        assert response.status_code == 200
        manifest = response.json()
        assert manifest["name"] == "NaariCare - Women's Health Assistant"
        assert manifest["short_name"] == "NaariCare"
        print("✅ PWA Manifest: PASSED")
    except Exception as e:
        print(f"❌ PWA Manifest: FAILED - {e}")
        return False

    # Test service worker
    try:
        response = requests.get(f"{base_url}/sw.js")
        assert response.status_code == 200
        assert "workbox" in response.text.lower()
        print("✅ Service Worker: PASSED")
    except Exception as e:
        print(f"❌ Service Worker: FAILED - {e}")
        return False

    # Test PWA icons
    try:
        response = requests.get(f"{base_url}/pwa-192x192.png")
        assert response.status_code == 200
        print("✅ PWA Icons: PASSED")
    except Exception as e:
        print(f"❌ PWA Icons: FAILED - {e}")
        return False

    return True

def test_supabase_integration():
    """Test Supabase configuration"""
    print("\n🔍 Testing Supabase Integration...")

    # Check environment variables are loaded
    import os
    env_file = "c:\\Users\\prath\\OneDrive\\ドキュメント\\NaariCare App\\.env"

    try:
        with open(env_file, 'r') as f:
            content = f.read()
            assert "VITE_SUPABASE_URL" in content
            assert "VITE_SUPABASE_PUBLISHABLE_KEY" in content
            print("✅ Supabase config: PASSED")
    except Exception as e:
        print(f"❌ Supabase config: FAILED - {e}")
        return False

    return True

def main():
    """Run all functionality tests"""
    print("🚀 NaariCare Full Stack Functionality Test")
    print("=" * 50)

    all_passed = True

    # Test backend
    if not test_backend_api():
        all_passed = False

    # Test frontend
    if not test_frontend_connectivity():
        all_passed = False

    # Test PWA features
    if not test_pwa_features():
        all_passed = False

    # Test Supabase
    if not test_supabase_integration():
        all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! NaariCare is fully functional!")
        print("\n📱 Ready for deployment:")
        print("   • Backend: http://127.0.0.1:8001")
        print("   • Frontend Dev: http://localhost:8081")
        print("   • Frontend Prod: http://localhost:4173")
        print("   • PWA: Installable on mobile devices")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")

    return all_passed

if __name__ == "__main__":
    main()