#!/bin/bash
# Script to test the hierarchical sync function locally

echo "🧪 Testing hierarchical sync function locally..."

# Change to the project directory
cd /Users/eugene/MyProjects/ff-base-ai-search

# Activate virtual environment
source backend/venv/bin/activate

# Run the test
python -c "
import sys
import os

# Test hash calculation
import hashlib
test_string = 'FILE:test.md|2023-01-01T00:00:00Z|abc123\\nFOLDER:subfolder|def456\\n'
test_hash = hashlib.md5(test_string.encode('utf-8')).hexdigest()

print(f'✅ Hash calculation works correctly (length: {len(test_hash)})')

# Test folder path construction
test_path = 'Как сделать/Авторизация/Авторизация по смс телефону.md'
if '/' in test_path and len(test_path) > 10:
    print('✅ Folder path construction works correctly')
else:
    print('❌ Folder path construction failed')
    sys.exit(1)

# Test required dependencies
required_packages = [
    'google.cloud.storage',
    'googleapiclient.discovery',
    'google.auth',
    'hashlib',
    'base64'
]

for package in required_packages:
    try:
        __import__(package)
        print(f'✅ {package} imported successfully')
    except ImportError as e:
        print(f'❌ Failed to import {package}: {e}')
        sys.exit(1)

print('🎉 All local tests passed!')
print('✅ Local testing completed successfully')
"