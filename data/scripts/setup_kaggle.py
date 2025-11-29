#!/usr/bin/env python3
"""
Quick Kaggle Setup Helper Script.

This script helps set up Kaggle credentials for downloading datasets.
"""

import os
import json
from pathlib import Path

def setup_kaggle_credentials():
    """Interactive setup for Kaggle credentials."""
    print("=" * 60)
    print("KAGGLE CREDENTIALS SETUP")
    print("=" * 60)
    
    print("\nTo download datasets from Kaggle, you need:")
    print("1. A Kaggle account (free)")
    print("2. An API token")
    
    print("\nSteps:")
    print("1. Go to: https://www.kaggle.com/")
    print("2. Sign in or create account (free)")
    print("3. Go to: https://www.kaggle.com/settings")
    print("4. Scroll to 'API' section")
    print("5. Click 'Create New API Token'")
    print("6. Download kaggle.json file")
    
    print("\n" + "-" * 60)
    response = input("\nDo you have the kaggle.json file? (y/n): ")
    
    if response.lower() == 'y':
        # Get path to kaggle.json
        json_path = input("Enter path to kaggle.json file: ").strip()
        json_path = Path(json_path).expanduser()
        
        if not json_path.exists():
            print(f"❌ File not found: {json_path}")
            return False
        
        # Read and validate JSON
        try:
            with open(json_path, 'r') as f:
                creds = json.load(f)
            
            # Check required keys
            if 'username' not in creds or 'key' not in creds:
                print("❌ Invalid kaggle.json format. Should have 'username' and 'key'.")
                return False
            
            print(f"✓ Valid kaggle.json found")
            print(f"  Username: {creds['username']}")
            
        except json.JSONDecodeError:
            print("❌ Invalid JSON file")
            return False
        
        # Create .kaggle directory
        kaggle_dir = Path.home() / '.kaggle'
        kaggle_dir.mkdir(exist_ok=True)
        
        # Copy file
        target_file = kaggle_dir / 'kaggle.json'
        
        import shutil
        shutil.copy(json_path, target_file)
        print(f"✓ Copied to: {target_file}")
        
        # Set permissions (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(target_file, 0o600)
            print("✓ Set file permissions (600)")
        
        print("\n✅ Kaggle credentials set up successfully!")
        print("\nYou can now run:")
        print("  python data/scripts/download_kaggle_datasets.py")
        
        return True
    
    else:
        print("\n📝 Manual Setup Instructions:")
        print("\n1. Download kaggle.json from Kaggle")
        print("2. Create directory: ~/.kaggle/")
        print("3. Copy kaggle.json to ~/.kaggle/kaggle.json")
        print("4. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
        print("\nThen run this script again or download script directly.")
        return False


if __name__ == '__main__':
    setup_kaggle_credentials()

