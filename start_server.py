#!/usr/bin/env python3
"""
Start the FinPulse FastAPI server for Power BI integration.

This script starts the API server that Power BI will connect to
for live data feeds.
"""

import uvicorn
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting FinPulse API server...")
    print("📊 Power BI can connect to: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n🔗 Key Power BI Endpoints:")
    print("   - Sentiment Summary: http://localhost:8000/sentiment/summary")
    print("   - Articles: http://localhost:8000/articles")
    print("   - All Endpoints: http://localhost:8000/")
    print("\nPress Ctrl+C to stop the server...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )