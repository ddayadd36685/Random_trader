#!/usr/bin/env python3

import uvicorn
import sys
import os

if __name__ == "__main__":
    print("🎲 启动 Random Trader vs Index...")
    print("=" * 50)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
