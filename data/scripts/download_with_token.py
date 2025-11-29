#!/usr/bin/env python3
"""
Download Datasets Using Kaggle API Token (Environment Variable).

This script uses environment variables for Kaggle authentication.
Set KAGGLE_USERNAME and KAGGLE_KEY before running.
"""

import os
import subprocess
import sys
from pathlib import Path

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATASETS_DIR = PROJECT_ROOT / 'datasets'
RAW_DATASETS_DIR = DATASETS_DIR / 'raw'

# Ensure directories exist
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# Kaggle API Token (you provided this)
KAGGLE_KEY = "KGAT_a89cf567db1ca4822286ffdd2ed6ba6f"

# Datasets to download
DATASETS = [
    {
        'slug': 'kaushil268/disease-symptom-description-dataset',
        'name': 'disease_symptom_description',
        'desc': 'Disease Symptom Description (~5,000 records)'
    },
    {
        'slug': 'niyarrbarman/symptom2disease',
        'name': 'symptom2disease',
        'desc': 'Symptom2Disease (~1,200 records)'
    },
    {
        'slug': 'kaushil268/disease-prediction-using-machine-learning',
        'name': 'disease_prediction_ml',
        'desc': 'Disease Prediction ML (~5,000 records)'
    },
    {
        'slug': 'rabieelkharoua/medical-symptoms',
        'name': 'medical_symptoms',
        'desc': 'Medical Symptoms (~3,000 records)'
    }
]


def setup_kaggle_env():
    """Set up Kaggle environment variables."""
    # Set the API key
    os.environ['KAGGLE_KEY'] = KAGGLE_KEY
    
    # Check if username is already set, if not try to get from kaggle config
    if 'KAGGLE_USERNAME' not in os.environ:
        try:
            # Try to get username from kaggle config
            result = subprocess.run(
                ['kaggle', 'config', 'view'],
                capture_output=True,
                text=True,
                env=os.environ.copy()
            )
            # If that doesn't work, we'll need username
            # For now, set a placeholder - user can override
            print("⚠️  KAGGLE_USERNAME not set. Trying to proceed...")
        except:
            pass
    
    print("✓ Kaggle environment variables configured")
    print(f"  KAGGLE_KEY: {KAGGLE_KEY[:10]}...")


def download_dataset(dataset_slug, dataset_name, output_dir):
    """Download a dataset from Kaggle."""
    try:
        print(f"  Downloading {dataset_slug}...")
        
        cmd = [
            'kaggle', 'datasets', 'download',
            '-d', dataset_slug,
            '-p', str(output_dir),
            '--unzip'
        ]
        
        # Run with environment variables
        env = os.environ.copy()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            env=env
        )
        
        if result.returncode == 0:
            return True, "Downloaded successfully"
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Download timeout (over 10 minutes)"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main download function."""
    print("=" * 60)
    print("DOWNLOADING DATASETS FROM KAGGLE")
    print("=" * 60)
    
    # Setup environment
    setup_kaggle_env()
    
    # Check if kaggle is installed
    try:
        result = subprocess.run(['which', 'kaggle'], capture_output=True, text=True)
        if result.returncode != 0:
            print("\n❌ Kaggle API not found. Install it with:")
            print("   pip install kaggle")
            return
    except:
        print("\n❌ Cannot check for Kaggle API")
        return
    
    print(f"\n📥 Will download {len(DATASETS)} datasets")
    print("\nDatasets:")
    for dataset in DATASETS:
        print(f"  - {dataset['desc']}")
    
    print("\n" + "=" * 60)
    print("STARTING DOWNLOADS")
    print("=" * 60)
    
    success_count = 0
    failed = []
    
    for dataset in DATASETS:
        print(f"\n📦 {dataset['desc']}")
        print(f"   Dataset: {dataset['slug']}")
        
        dataset_dir = RAW_DATASETS_DIR / dataset['name']
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        success, message = download_dataset(
            dataset['slug'],
            dataset['name'],
            dataset_dir
        )
        
        if success:
            print(f"   ✓ {message}")
            
            # List downloaded files
            files = list(dataset_dir.glob('*'))
            if files:
                print(f"   Files: {len(files)} file(s)")
            
            success_count += 1
        else:
            print(f"   ❌ Failed: {message}")
            failed.append(dataset['name'])
    
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"\n✓ Successfully downloaded: {success_count}/{len(DATASETS)} datasets")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)} datasets")
        for name in failed:
            print(f"  - {name}")
    
    if success_count > 0:
        print("\n✅ Downloads complete!")
        print("\nNext steps:")
        print("1. Run normalization: python data/scripts/normalize_datasets.py")
        print("2. Run merge: python data/scripts/merge_datasets.py")
        print("3. Retrain models with expanded dataset")
    else:
        print("\n⚠️  No datasets downloaded. Check your Kaggle credentials.")
        print("\nYou may need to also set KAGGLE_USERNAME:")
        print("   export KAGGLE_USERNAME=your_username")
        print("   export KAGGLE_KEY=KGAT_a89cf567db1ca4822286ffdd2ed6ba6f")


if __name__ == '__main__':
    main()

