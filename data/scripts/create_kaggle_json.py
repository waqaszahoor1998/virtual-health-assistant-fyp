#!/usr/bin/env python3
"""
Create kaggle.json file from API token.

Kaggle requires both username and API key in kaggle.json format.
"""

import json
import os
from pathlib import Path

# Your Kaggle API token
KAGGLE_KEY = "KGAT_a89cf567db1ca4822286ffdd2ed6ba6f"

def create_kaggle_json():
    """Create kaggle.json file."""
    print("=" * 60)
    print("KAGGLE.JSON SETUP")
    print("=" * 60)
    
    # Get username
    print("\nWe need your Kaggle username to create the credentials file.")
    print("You can find it at: https://www.kaggle.com/")
    print("It's in your profile URL: https://www.kaggle.com/YOUR_USERNAME")
    print()
    
    username = input("Enter your Kaggle username: ").strip()
    
    if not username:
        print("❌ Username is required!")
        return False
    
    # Create credentials
    credentials = {
        "username": username,
        "key": KAGGLE_KEY
    }
    
    # Create .kaggle directory
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    # Create kaggle.json
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    with open(kaggle_json, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    # Set permissions (Unix-like)
    if os.name != 'nt':
        os.chmod(kaggle_json, 0o600)
    
    print(f"\n✅ Created {kaggle_json}")
    print(f"   Username: {username}")
    print(f"   Key: {KAGGLE_KEY[:10]}...")
    
    print("\n✅ Kaggle credentials ready!")
    print("\nYou can now run:")
    print("  python data/scripts/download_with_token.py")
    
    return True

if __name__ == '__main__':
    create_kaggle_json()

