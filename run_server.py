#!/usr/bin/env python3
"""
Script to run the PaiNaiDee API server
"""
import sys
import os

# Add the current directory to Python path to resolve imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from api.main import app
    
    print("Starting PaiNaiDee API server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
