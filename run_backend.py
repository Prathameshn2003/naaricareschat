#!/usr/bin/env python3
"""
NaariCare ML Backend - Clean Startup Script
Suppresses warnings and starts the server
"""

import os
import sys
import warnings

# Set environment variables FIRST
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Suppress all warnings
warnings.filterwarnings('ignore')
import logging
logging.basicConfig(level=logging.ERROR)

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Now import everything else
from main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting NaariCare ML Backend...")
    print("📍 Server: http://127.0.0.1:8001")
    print("⚠️  Warnings suppressed for clean output\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="error",  # Only show errors, not info logs
    )
