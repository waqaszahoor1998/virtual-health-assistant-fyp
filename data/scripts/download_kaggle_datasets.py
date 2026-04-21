#!/usr/bin/env python3
"""
Kaggle Dataset Download Script.

Downloads recommended datasets from Kaggle for expanding the training dataset.
Requires Kaggle API credentials (kaggle.json in ~/.kaggle/).

This script downloads multiple datasets that will be merged later to create
a comprehensive symptom-disease mapping dataset with 10,000+ records.
"""

import os
import subprocess
import sys
from pathlib import Path
import zipfile
import shutil

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATASETS_DIR = PROJECT_ROOT / 'datasets'
RAW_DATASETS_DIR = DATASETS_DIR / 'raw'
PROCESSED_DATASETS_DIR = DATASETS_DIR / 'processed'

# Ensure directories exist
DATASETS_DIR.mkdir(exist_ok=True)
RAW_DATASETS_DIR.mkdir(exist_ok=True)
PROCESSED_DATASETS_DIR.mkdir(exist_ok=True)

# Kaggle datasets to download
# Format: (dataset_slug, description, expected_format)
KAGGLE_DATASETS = [
    {
        'slug': 'kaushil268/disease-symptom-description-dataset',
        'name': 'disease_symptom_description',
        'description': 'Disease Symptom Dataset - Primary dataset (~5,000 records)',
        'format': 'csv'
    },
    {
        'slug': 'niyarrbarman/symptom2disease',
        'name': 'symptom2disease',
        'description': 'Symptom2Disease dataset (~1,200 records)',
        'format': 'csv'
    },
    {
        'slug': 'kaushil268/disease-prediction-using-machine-learning',
        'name': 'disease_prediction_ml',
        'description': 'Disease Prediction Using ML (~5,000 records)',
        'format': 'csv'
    },
    {
        'slug': 'rabieelkharoua/medical-symptoms',
        'name': 'medical_symptoms',
        'description': 'Medical Symptoms dataset (~3,000 records)',
        'format': 'csv'
    }
]

# Alternative datasets (if primary ones are unavailable)
ALTERNATIVE_DATASETS = [
    {
        'slug': 'itachi9604/disease-symptom-description-dataset',
        'name': 'disease_symptom_alt',
        'description': 'Alternative Disease Symptom dataset',
        'format': 'csv'
    }
]


def check_kaggle_installed():
    """Check if Kaggle API is installed."""
    try:
        import kaggle
        print("✓ Kaggle API is installed")
        return True
    except ImportError:
        print("❌ Kaggle API not installed")
        print("Install it with: pip install kaggle")
        return False


def check_kaggle_credentials():
    """Check if Kaggle credentials are configured."""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if kaggle_json.exists():
        print("✓ Kaggle credentials found")
        return True
    else:
        print("❌ Kaggle credentials not found")
        print(f"Please place kaggle.json in {kaggle_dir}/")
        print("Download it from: https://www.kaggle.com/settings")
        return False


def download_dataset(dataset_slug, dataset_name, output_dir):
    """
    Download a dataset from Kaggle.
    
    Args:
        dataset_slug (str): Kaggle dataset slug (e.g., 'user/dataset-name')
        dataset_name (str): Local name for the dataset
        output_dir (Path): Directory to save the dataset
    
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        print(f"\n📥 Downloading: {dataset_slug}")
        print(f"   Saving as: {dataset_name}")
        
        # Use Kaggle API to download
        cmd = [
            'kaggle', 'datasets', 'download',
            '-d', dataset_slug,
            '-p', str(output_dir),
            '--unzip'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ Successfully downloaded {dataset_name}")
            return True
        else:
            print(f"❌ Error downloading {dataset_name}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout downloading {dataset_name}")
        return False
    except Exception as e:
        print(f"❌ Error downloading {dataset_name}: {str(e)}")
        return False


def extract_zip_files(directory):
    """Extract any zip files in the directory."""
    zip_files = list(directory.glob('*.zip'))
    
    for zip_file in zip_files:
        try:
            print(f"📦 Extracting {zip_file.name}...")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(directory)
            print(f"✓ Extracted {zip_file.name}")
            # Optionally remove zip file after extraction
            # zip_file.unlink()
        except Exception as e:
            print(f"❌ Error extracting {zip_file.name}: {str(e)}")


def download_datasets():
    """
    Download all recommended datasets from Kaggle.
    
    Returns:
        dict: Status of each dataset download
    """
    print("=" * 60)
    print("KAGGLE DATASET DOWNLOADER")
    print("=" * 60)
    
    # Check prerequisites
    if not check_kaggle_installed():
        print("\n⚠️  Please install Kaggle API first:")
        print("   pip install kaggle")
        return {}
    
    if not check_kaggle_credentials():
        print("\n⚠️  Please set up Kaggle credentials:")
        print("   1. Go to https://www.kaggle.com/settings")
        print("   2. Create API token")
        print("   3. Save kaggle.json to ~/.kaggle/")
        print("   4. Run: chmod 600 ~/.kaggle/kaggle.json")
        return {}
    
    print("\n" + "=" * 60)
    print("DOWNLOADING DATASETS")
    print("=" * 60)
    
    download_results = {}
    
    # Download primary datasets
    for dataset in KAGGLE_DATASETS:
        slug = dataset['slug']
        name = dataset['name']
        
        # Create dataset-specific directory
        dataset_dir = RAW_DATASETS_DIR / name
        dataset_dir.mkdir(exist_ok=True)
        
        success = download_dataset(slug, name, dataset_dir)
        download_results[name] = {
            'success': success,
            'slug': slug,
            'description': dataset['description']
        }
        
        if success:
            # Extract any zip files
            extract_zip_files(dataset_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    
    successful = [name for name, result in download_results.items() if result['success']]
    failed = [name for name, result in download_results.items() if not result['success']]
    
    print(f"\n✓ Successfully downloaded: {len(successful)}/{len(KAGGLE_DATASETS)} datasets")
    for name in successful:
        print(f"  - {name}")
    
    if failed:
        print(f"\n❌ Failed to download: {len(failed)} datasets")
        for name in failed:
            print(f"  - {name}")
        print("\n💡 Tip: You can download these manually from Kaggle and place them in:")
        print(f"   {RAW_DATASETS_DIR}")
    
    print(f"\n📁 Datasets saved to: {RAW_DATASETS_DIR}")
    
    return download_results


def list_downloaded_datasets():
    """List all downloaded dataset files."""
    print("\n" + "=" * 60)
    print("DOWNLOADED DATASETS")
    print("=" * 60)
    
    if not RAW_DATASETS_DIR.exists():
        print("No datasets directory found.")
        return
    
    dataset_dirs = [d for d in RAW_DATASETS_DIR.iterdir() if d.is_dir()]
    
    if not dataset_dirs:
        print("No datasets downloaded yet.")
        return
    
    for dataset_dir in dataset_dirs:
        print(f"\n📂 {dataset_dir.name}:")
        files = list(dataset_dir.glob('*'))
        for file in files:
            if file.is_file():
                size = file.stat().st_size / 1024  # KB
                print(f"  - {file.name} ({size:.1f} KB)")


def main():
    """Main function to download datasets."""
    print("This script will download datasets from Kaggle to expand the training data.")
    print("Expected total: 10,000-15,000 records")
    print("\nPrerequisites:")
    print("1. Kaggle account (free)")
    print("2. Kaggle API token (from account settings)")
    print("3. kaggle.json file in ~/.kaggle/")
    
    response = input("\nContinue with download? (y/n): ")
    
    if response.lower() != 'y':
        print("Download cancelled.")
        return
    
    # Download datasets
    results = download_datasets()
    
    # List downloaded files
    list_downloaded_datasets()
    
    # Next steps
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Review downloaded datasets in:", RAW_DATASETS_DIR)
    print("2. Run normalization script: python data/scripts/normalize_datasets.py")
    print("3. Run merge script: python data/scripts/merge_datasets.py")
    print("4. Retrain models with expanded dataset")


if __name__ == '__main__':
    main()

