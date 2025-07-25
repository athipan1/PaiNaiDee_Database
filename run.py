#!/usr/bin/env python3
"""
Run script for PaiNaiDee FastAPI application
"""
import uvicorn
import os

if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    
    # Run the FastAPI application
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )