#!/usr/bin/env python3
"""
Script to initialize the knowledge base from local directory specified by `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`).
"""

import asyncio
import sys
import os

# Add the backend directory to the path so we can import from main.py
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main import update_knowledge_base_from_local

async def main():
    print("Initializing knowledge base from directory specified by `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`)...")
    result = await update_knowledge_base_from_local()
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())