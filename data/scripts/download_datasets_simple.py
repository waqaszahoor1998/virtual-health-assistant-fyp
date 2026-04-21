#!/usr/bin/env python3
"""
Simplified Dataset Download Script.

Tries to download from Kaggle if credentials are available.
If not, provides manual download instructions.
"""

import subprocess
import sys
from pathlib import Path
import os

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATASETS_DIR = PROJECT_ROOT / 'datasets'
RAW_DATASETS_DIR = DATASETS_DIR / 'raw'

# Ensure directories exist
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# Datasets to download
DATASETS = [
    {
        'slug': 'kaushil268/disease-symptom-description-dataset',
        'name': 'disease_symptom_description',
        'url': 'https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset',
        'desc': 'Disease Symptom Description (~5,000 records)'
    },
    {
        'slug': 'niyarrbarman/symptom2disease',
        'name': 'symptom2disease',
        'url': 'https://www.kaggle.com/datasets/niyarrbarman/symptom2disease',
        'desc': 'Symptom2Disease (~1,200 records)'
    },
    {
        'slug': 'kaushil268/disease-prediction-using-machine-learning',
        'name': 'disease_prediction_ml',
        'url': 'https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning',
        'desc': 'Disease Prediction ML (~5,000 records)'
    },
    {
        'slug': 'rabieelkharoua/medical-symptoms',
        'name': 'medical_symptoms',
        'url': 'https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms',
        'desc': 'Medical Symptoms (~3,000 records)'
    }
]


def check_kaggle_setup():
    """Check if Kaggle is set up correctly."""
    # Check if kaggle command exists
    try:
        result = subprocess.run(['which', 'kaggle'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Kaggle API not installed. Run: pip install kaggle"
    except:
        return False, "Cannot check for Kaggle API"
    
    # Check for credentials
    kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'
    if not kaggle_json.exists():
        return False, f"Kaggle credentials not found at {kaggle_json}\nRun: python data/scripts/setup_kaggle.py"
    
    return True, "Kaggle is ready!"


def download_with_kaggle_api(dataset_slug, output_dir):
    """Download dataset using Kaggle API."""
    try:
        cmd = [
            'kaggle', 'datasets', 'download',
            '-d', dataset_slug,
            '-p', str(output_dir),
            '--unzip'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return True, "Downloaded successfully"
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, f"Error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return False, "Download timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main download function."""
    print("=" * 60)
    print("DATASET DOWNLOADER")
    print("=" * 60)
    
    # Check Kaggle setup
    is_ready, message = check_kaggle_setup()
    
    if not is_ready:
        print(f"\n❌ {message}")
        print("\n" + "=" * 60)
        print("MANUAL DOWNLOAD INSTRUCTIONS")
        print("=" * 60)
        print("\nSince Kaggle requires authentication, please download manually:\n")
        
        for dataset in DATASETS:
            print(f"📥 {dataset['desc']}")
            print(f"   URL: {dataset['url']}")
            print(f"   Save to: datasets/raw/{dataset['name']}/")
            print()
        
        print("\nSteps:")
        print("1. Visit each URL above")
        print("2. Sign in to Kaggle (free account)")
        print("3. Click 'Download' button")
        print("4. Extract ZIP file")
        print("5. Move CSV files to datasets/raw/{dataset_name}/")
        print("\nThen run: python data/scripts/normalize_datasets.py")
        
        return
    
    # Kaggle is ready - proceed with download
    print(f"\n✓ {message}")
    print("\n" + "=" * 60)
    print("DOWNLOADING DATASETS")
    print("=" * 60)
    
    print(f"\nWill download {len(DATASETS)} datasets...")
    response = input("Continue? (y/n): ")
    
    if response.lower() != 'y':
        print("Download cancelled.")
        return
    
    success_count = 0
    
    for dataset in DATASETS:
        print(f"\n📥 {dataset['desc']}")
        print(f"   Dataset: {dataset['slug']}")
        
        dataset_dir = RAW_DATASETS_DIR / dataset['name']
        dataset_dir.mkdir(exist_ok=True)
        
        success, message = download_with_kaggle_api(dataset['slug'], dataset_dir)
        
        if success:
            print(f"   ✓ {message}")
            success_count += 1
        else:
            print(f"   ❌ {message}")
    
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"\n✓ Successfully downloaded: {success_count}/{len(DATASETS)} datasets")
    
    if success_count > 0:
        print("\nNext steps:")
        print("1. Run normalization: python data/scripts/normalize_datasets.py")
        print("2. Run merge: python data/scripts/merge_datasets.py")
        print("3. Retrain models with expanded dataset")


if __name__ == '__main__':
    main()

