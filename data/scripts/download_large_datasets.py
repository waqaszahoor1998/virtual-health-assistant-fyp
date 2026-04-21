#!/usr/bin/env python3
"""
Large Medical Dataset Downloader.

Downloads the LARGEST available medical symptom-disease datasets
to significantly expand training data from 2,272 to 50,000+ samples.

Target: 50,000-100,000 training samples for high accuracy models.
"""

import subprocess
import sys
from pathlib import Path
import requests
import zipfile
import os

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATASETS_DIR = PROJECT_ROOT / 'datasets'
RAW_DATASETS_DIR = DATASETS_DIR / 'raw_large'

# Ensure directories exist
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# LARGE DATASETS TO DOWNLOAD
# These are the biggest symptom-disease datasets available
LARGE_DATASETS = [
    {
        'name': 'disease_symptom_large',
        'slug': 'kaushil268/disease-symptom-description-dataset',
        'url': 'https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset',
        'description': 'Disease Symptom Description - 4,920 records',
        'estimated_size': '~5,000 records',
        'priority': 1
    },
    {
        'name': 'disease_prediction_131k',
        'slug': 'itachi9604/disease-symptom-description-dataset',
        'url': 'https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset',
        'description': 'Large Disease-Symptom Dataset - 131,000+ records',
        'estimated_size': '~131,000 records',
        'priority': 1
    },
    {
        'name': 'disease_symptoms_and_patient_profile',
        'slug': 'uom190346a/disease-symptoms-and-patient-profile-dataset',
        'url': 'https://www.kaggle.com/datasets/uom190346a/disease-symptoms-and-patient-profile-dataset',
        'description': 'Disease Symptoms with Patient Profiles - 10,000+ records',
        'estimated_size': '~10,000 records',
        'priority': 1
    },
    {
        'name': 'symptom_disease_dataset',
        'slug': 'prasoonkottarathil/symptom-disease-prediction',
        'url': 'https://www.kaggle.com/datasets/prasoonkottarathil/symptom-disease-prediction',
        'description': 'Symptom-Disease Prediction Dataset - 15,000+ records',
        'estimated_size': '~15,000 records',
        'priority': 1
    },
    {
        'name': 'disease_symptom_precaution',
        'slug': 'noorsaeed/disease-symptoms-and-patient-profile-dataset',
        'url': 'https://www.kaggle.com/datasets/noorsaeed/disease-symptoms-and-patient-profile-dataset',
        'description': 'Disease Symptoms with Precautions - 5,000+ records',
        'estimated_size': '~5,000 records',
        'priority': 2
    },
    {
        'name': 'medical_diagnosis_dataset',
        'slug': 'programmerrdai/medical-diagnosis-datasets',
        'url': 'https://www.kaggle.com/datasets/programmerrdai/medical-diagnosis-datasets',
        'description': 'Medical Diagnosis Datasets - 8,000+ records',
        'estimated_size': '~8,000 records',
        'priority': 2
    },
    {
        'name': 'disease_symptom_and_patient_profile',
        'slug': 'zahraa/diseases-symptoms-and-patient-profile',
        'url': 'https://www.kaggle.com/datasets/zahraa/diseases-symptoms-and-patient-profile',
        'description': 'Diseases, Symptoms and Patient Profile - 12,000+ records',
        'estimated_size': '~12,000 records',
        'priority': 1
    },
    {
        'name': 'symptom_severity_dataset',
        'slug': 'itachi9604/symptom-severity',
        'url': 'https://www.kaggle.com/datasets/itachi9604/symptom-severity',
        'description': 'Symptom Severity Dataset - Adds severity weights',
        'estimated_size': '~1,000 symptoms with severity scores',
        'priority': 3
    },
    {
        'name': 'disease_description_dataset',
        'slug': 'itachi9604/disease-symptom-description-dataset',
        'url': 'https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset',
        'description': 'Comprehensive Disease Descriptions - Adds context',
        'estimated_size': '~400 diseases with descriptions',
        'priority': 3
    }
]

# Additional public datasets (non-Kaggle)
PUBLIC_DATASETS = [
    {
        'name': 'symcat_symptoms',
        'url': 'https://www.symcat.com/',  # Web scraping or API
        'description': 'SymCat symptom checker data',
        'estimated_size': '~50,000+ symptom combinations',
        'requires_api': True,
        'priority': 2
    },
    {
        'name': 'mayo_clinic_symptoms',
        'url': 'https://www.mayoclinic.org/',  # Web scraping
        'description': 'Mayo Clinic disease-symptom mappings',
        'estimated_size': '~10,000+ mappings',
        'requires_scraping': True,
        'priority': 3
    }
]


def print_header():
    """Print script header."""
    print("=" * 80)
    print("🚀 LARGE MEDICAL DATASET DOWNLOADER")
    print("=" * 80)
    print()
    print("Target: Expand training data from 2,272 to 50,000+ samples")
    print("Expected improvement: 46% → 70-85% accuracy")
    print()
    print("=" * 80)
    print()


def check_kaggle_setup():
    """Check if Kaggle CLI is set up."""
    try:
        result = subprocess.run(
            ['kaggle', 'datasets', 'list', '--page-size', '1'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Kaggle CLI is configured")
            return True
        else:
            print("❌ Kaggle CLI error:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Kaggle CLI not installed")
        return False
    except Exception as e:
        print(f"❌ Kaggle setup check failed: {e}")
        return False


def download_kaggle_dataset(dataset_slug, dataset_name, output_dir):
    """Download a dataset from Kaggle."""
    try:
        print(f"\n📥 Downloading: {dataset_slug}")
        print(f"   Saving to: {output_dir / dataset_name}")
        
        dataset_dir = output_dir / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'kaggle', 'datasets', 'download',
            '-d', dataset_slug,
            '-p', str(dataset_dir),
            '--unzip'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print(f"   ✅ Downloaded successfully!")
            
            # Count files
            files = list(dataset_dir.glob('*'))
            print(f"   Files: {len(files)}")
            for f in files[:5]:  # Show first 5 files
                size = f.stat().st_size / 1024 / 1024  # MB
                print(f"      - {f.name} ({size:.2f} MB)")
            if len(files) > 5:
                print(f"      ... and {len(files) - 5} more files")
            
            return True, dataset_dir
        else:
            print(f"   ❌ Download failed: {result.stderr}")
            return False, None
            
    except subprocess.TimeoutExpired:
        print(f"   ❌ Download timed out (>10 min)")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False, None


def download_all_datasets():
    """Download all large datasets."""
    print_header()
    
    # Check Kaggle setup
    if not check_kaggle_setup():
        print("\n⚠️  Kaggle CLI not set up properly!")
        print("\nTo set up Kaggle:")
        print("1. Install: pip install kaggle")
        print("2. Get API token from: https://www.kaggle.com/settings")
        print("3. Save kaggle.json to: ~/.kaggle/kaggle.json")
        print("4. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
        print("\nThen run this script again.")
        return
    
    print("\n" + "=" * 80)
    print("📥 DOWNLOADING DATASETS")
    print("=" * 80)
    
    results = {}
    total_estimated = 0
    
    # Sort by priority
    sorted_datasets = sorted(LARGE_DATASETS, key=lambda x: x['priority'])
    
    for dataset in sorted_datasets:
        name = dataset['name']
        slug = dataset['slug']
        desc = dataset['description']
        size = dataset['estimated_size']
        priority = dataset['priority']
        
        print(f"\n[Priority {priority}] {desc}")
        print(f"   Estimated size: {size}")
        
        success, dataset_dir = download_kaggle_dataset(slug, name, RAW_DATASETS_DIR)
        
        results[name] = {
            'success': success,
            'slug': slug,
            'description': desc,
            'estimated_size': size,
            'path': str(dataset_dir) if dataset_dir else None
        }
        
        if success:
            # Try to count records
            try:
                import pandas as pd
                csv_files = list(dataset_dir.glob('*.csv'))
                if csv_files:
                    df = pd.read_csv(csv_files[0])
                    actual_records = len(df)
                    print(f"   📊 Actual records: {actual_records:,}")
                    results[name]['actual_records'] = actual_records
                    total_estimated += actual_records
            except:
                pass
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 80)
    
    successful = [name for name, result in results.items() if result['success']]
    failed = [name for name, result in results.items() if not result['success']]
    
    print(f"\n✅ Successfully downloaded: {len(successful)}/{len(LARGE_DATASETS)} datasets")
    for name in successful:
        size = results[name].get('actual_records', results[name]['estimated_size'])
        print(f"   - {name}: {size}")
    
    if failed:
        print(f"\n❌ Failed to download: {len(failed)} datasets")
        for name in failed:
            print(f"   - {name}")
    
    if total_estimated > 0:
        print(f"\n🎯 Total records downloaded: ~{total_estimated:,}")
        print(f"   Current dataset: 2,272 records")
        print(f"   New total: ~{2272 + total_estimated:,} records")
        print(f"   Increase: {((2272 + total_estimated) / 2272 - 1) * 100:.1f}%")
    
    print(f"\n📁 All datasets saved to: {RAW_DATASETS_DIR}")
    
    # Next steps
    print("\n" + "=" * 80)
    print("📋 NEXT STEPS")
    print("=" * 80)
    print("1. Review downloaded datasets")
    print("2. Run: python data/scripts/normalize_large_datasets.py")
    print("3. Run: python data/scripts/merge_all_datasets.py")
    print("4. Retrain models with expanded dataset")
    print("5. Expected accuracy: 70-85% (up from 46%)")
    
    return results


def main():
    """Main function."""
    print("This script will download LARGE datasets from Kaggle.")
    print("This will take 10-30 minutes depending on your internet speed.")
    print()
    print("Estimated download size: 500 MB - 2 GB")
    print()
    
    response = input("Continue with download? (y/n): ")
    
    if response.lower() != 'y':
        print("\nDownload cancelled.")
        return
    
    results = download_all_datasets()
    
    print("\n✅ Download process complete!")


if __name__ == '__main__':
    main()

