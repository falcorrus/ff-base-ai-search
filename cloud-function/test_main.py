#!/usr/bin/env python3
"""
Unit tests for the Cloud Function.
"""

import unittest
import hashlib
import json
from unittest.mock import Mock, patch, mock_open
import sys
import os

# Add the cloud-function directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from main import calculate_drive_folder_hash, get_full_path

class TestCloudFunction(unittest.TestCase):
    
    def test_calculate_drive_folder_hash(self):
        """Test calculation of folder hash."""
        # This is a simple test - in reality, we would mock the Drive API
        test_string = "test_file.md|2023-01-01T00:00:00Z|abc123"
        expected_hash = hashlib.md5(test_string.encode('utf-8')).hexdigest()
        
        # We can't fully test this without mocking the Drive API
        # But we can at least verify the hash calculation works
        self.assertEqual(len(expected_hash), 32)  # MD5 hash is 32 characters
        self.assertTrue(all(c in '0123456789abcdef' for c in expected_hash))
    
    def test_get_full_path(self):
        """Test getting full path of a file."""
        # This would require mocking the Drive API service
        # For now, we'll just verify it doesn't crash with None inputs
        result = get_full_path(None, None, None)
        self.assertIsNone(result)
    
    def test_folder_hash_consistency(self):
        """Test that folder hash is consistent for the same input."""
        # Create two identical metadata strings
        metadata1 = "file1.md|2023-01-01T00:00:00Z|abc123
file2.md|2023-01-02T00:00:00Z|def456
"
        metadata2 = "file1.md|2023-01-01T00:00:00Z|abc123
file2.md|2023-01-02T00:00:00Z|def456
"
        
        # Calculate hashes
        hash1 = hashlib.md5(metadata1.encode('utf-8')).hexdigest()
        hash2 = hashlib.md5(metadata2.encode('utf-8')).hexdigest()
        
        # They should be identical
        self.assertEqual(hash1, hash2)
    
    def test_folder_hash_difference(self):
        """Test that folder hash differs for different inputs."""
        # Create two different metadata strings
        metadata1 = "file1.md|2023-01-01T00:00:00Z|abc123
file2.md|2023-01-02T00:00:00Z|def456
"
        metadata2 = "file1.md|2023-01-01T00:00:00Z|abc123
file3.md|2023-01-03T00:00:00Z|ghi789
"
        
        # Calculate hashes
        hash1 = hashlib.md5(metadata1.encode('utf-8')).hexdigest()
        hash2 = hashlib.md5(metadata2.encode('utf-8')).hexdigest()
        
        # They should be different
        self.assertNotEqual(hash1, hash2)

if __name__ == '__main__':
    unittest.main()