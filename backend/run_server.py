#!/usr/bin/env python3
"""
Simple script to run the Lesson Planner Bot FastAPI server
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Lesson Planner Bot API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Interactive API docs at: http://localhost:8000/redoc")
    print("🏥 Health check at: http://localhost:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 