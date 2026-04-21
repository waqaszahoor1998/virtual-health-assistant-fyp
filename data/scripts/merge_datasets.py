#!/usr/bin/env python3
"""
Dataset Merging Script.

Merges normalized datasets with the existing cleaned dataset to create
a comprehensive training dataset with 10,000+ records.

This script:
- Combines normalized datasets from multiple sources
- Merges with existing cleaned dataset
- Groups by disease and combines symptoms
- Creates final training-ready dataset
- Validates data quality
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
PROCESSED_DATASETS_DIR = PROJECT_ROOT / 'datasets' / 'processed'
DATA_PROCESSED_DIR = PROJECT_ROOT / 'data' / 'processed'
DATA_RAW_DIR = PROJECT_ROOT / 'data' / 'raw'

# Output file
FINAL_DATASET_FILE = DATA_PROCESSED_DIR / 'dataset_expanded_final.xlsx'


def load_normalized_datasets() -> pd.DataFrame:
    """
    Load normalized datasets from processed directory.
    
    Returns:
        pd.DataFrame: Combined normalized datasets
    """
    print("Loading normalized datasets...")
    
    normalized_file = PROCESSED_DATASETS_DIR / 'normalized_datasets.xlsx'
    
    if not normalized_file.exists():
        print(f"❌ Normalized dataset not found: {normalized_file}")
        print("Please run normalize_datasets.py first")
        return pd.DataFrame()
    
    df = pd.read_excel(normalized_file)
    print(f"✓ Loaded {len(df)} normalized records")
    
    return df


def load_existing_cleaned_dataset() -> pd.DataFrame:
    """
    Load the existing cleaned dataset.
    
    Returns:
        pd.DataFrame: Existing cleaned dataset
    """
    print("Loading existing cleaned dataset...")
    
    cleaned_file = DATA_PROCESSED_DIR / 'dataset_cleaned.xlsx'
    
    if not cleaned_file.exists():
        print("⚠️  Existing cleaned dataset not found, will use normalized datasets only")
        return pd.DataFrame()
    
    df = pd.read_excel(cleaned_file)
    print(f"✓ Loaded {len(df)} records from existing cleaned dataset")
    
    return df


def merge_disease_symptoms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge multiple records for the same disease, combining symptoms.
    
    Args:
        df (pd.DataFrame): Dataset with disease and symptoms columns
    
    Returns:
        pd.DataFrame: Merged dataset with combined symptoms per disease
    """
    print("\nMerging disease-symptom combinations...")
    
    # Group by disease and combine symptoms
    disease_symptoms = defaultdict(set)
    
    for _, row in df.iterrows():
        disease = row.get('disease')
        symptoms = row.get('symptoms', [])
        
        if pd.isna(disease) or not symptoms:
            continue
        
        disease = str(disease).strip()
        
        # Convert symptoms to set and add
        if isinstance(symptoms, str):
            try:
                symptoms = json.loads(symptoms)
            except:
                symptoms = [s.strip() for s in symptoms.split(',')]
        
        if isinstance(symptoms, list):
            disease_symptoms[disease].update(symptoms)
    
    # Create merged records
    merged_records = []
    for disease, symptoms_set in disease_symptoms.items():
        if symptoms_set:  # Only add if has symptoms
            merged_records.append({
                'disease': disease,
                'symptoms': sorted(list(symptoms_set)),
                'symptom_count': len(symptoms_set)
            })
    
    merged_df = pd.DataFrame(merged_records)
    print(f"✓ Merged to {len(merged_df)} unique disease-symptom combinations")
    
    return merged_df


def create_training_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create final training dataset format matching original structure.
    
    Args:
        df (pd.DataFrame): Disease-symptom dataset (with individual records)
    
    Returns:
        pd.DataFrame: Training-ready dataset
    """
    print("\nCreating final training format...")
    
    training_records = []
    
    for _, row in df.iterrows():
        disease = row.get('disease') or row.get('diseases')
        symptoms = row.get('symptoms', [])
        
        if pd.isna(disease) or not symptoms:
            continue
        
        # Ensure symptoms is a list
        if isinstance(symptoms, str):
            try:
                symptoms = json.loads(symptoms)
            except:
                symptoms = [s.strip() for s in str(symptoms).split(',') if s.strip()]
        
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            continue
        
        # Convert symptoms list to JSON string (matching original format)
        symptoms_json = json.dumps(symptoms)
        
        # Create symptom text (for compatibility)
        symptoms_text = ', '.join(symptoms) if isinstance(symptoms, list) else str(symptoms)
        
        training_records.append({
            'diseases': str(disease).strip(),
            'symptoms_list': symptoms_json,
            'symptoms_text': symptoms_text,
            'symptom_count': len(symptoms) if isinstance(symptoms, list) else 1
        })
    
    training_df = pd.DataFrame(training_records)
    print(f"✓ Created {len(training_df)} training records")
    
    return training_df


def validate_merged_dataset(df: pd.DataFrame) -> dict:
    """
    Validate the merged dataset and generate statistics.
    
    Args:
        df (pd.DataFrame): Merged dataset
    
    Returns:
        dict: Validation statistics
    """
    print("\n" + "=" * 60)
    print("VALIDATING MERGED DATASET")
    print("=" * 60)
    
    stats = {
        'total_records': len(df),
        'unique_diseases': df['diseases'].nunique() if 'diseases' in df.columns else 0,
        'total_symptoms': 0,
        'unique_symptoms': set(),
        'avg_symptoms_per_record': 0,
        'min_symptoms': 0,
        'max_symptoms': 0,
        'records_with_symptoms': 0
    }
    
    if len(df) == 0:
        return stats
    
    symptom_counts = []
    all_symptoms = set()
    
    for _, row in df.iterrows():
        symptoms_list = row.get('symptoms_list', '[]')
        
        try:
            if isinstance(symptoms_list, str):
                symptoms = json.loads(symptoms_list)
            else:
                symptoms = symptoms_list if isinstance(symptoms_list, list) else []
            
            symptom_count = len(symptoms)
            symptom_counts.append(symptom_count)
            
            if symptom_count > 0:
                stats['records_with_symptoms'] += 1
                all_symptoms.update(symptoms)
        
        except (json.JSONDecodeError, TypeError):
            continue
    
    if symptom_counts:
        stats['total_symptoms'] = sum(symptom_counts)
        stats['unique_symptoms'] = len(all_symptoms)
        stats['avg_symptoms_per_record'] = np.mean(symptom_counts)
        stats['min_symptoms'] = np.min(symptom_counts)
        stats['max_symptoms'] = np.max(symptom_counts)
    
    # Print statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"  Total records: {stats['total_records']:,}")
    print(f"  Unique diseases: {stats['unique_diseases']:,}")
    print(f"  Unique symptoms: {stats['unique_symptoms']:,}")
    print(f"  Records with symptoms: {stats['records_with_symptoms']:,}")
    print(f"  Average symptoms per record: {stats['avg_symptoms_per_record']:.1f}")
    print(f"  Min symptoms: {stats['min_symptoms']}")
    print(f"  Max symptoms: {stats['max_symptoms']}")
    
    # Quality checks
    print(f"\n✅ Quality Checks:")
    
    if stats['total_records'] >= 10000:
        print(f"  ✓ Dataset size: {stats['total_records']:,} records (target achieved!)")
    else:
        print(f"  ⚠️  Dataset size: {stats['total_records']:,} records (target: 10,000+)")
    
    if stats['records_with_symptoms'] / stats['total_records'] >= 0.8:
        print(f"  ✓ Data completeness: {stats['records_with_symptoms']/stats['total_records']*100:.1f}%")
    else:
        print(f"  ⚠️  Data completeness: {stats['records_with_symptoms']/stats['total_records']*100:.1f}%")
    
    if stats['unique_diseases'] >= 500:
        print(f"  ✓ Disease coverage: {stats['unique_diseases']:,} diseases")
    else:
        print(f"  ⚠️  Disease coverage: {stats['unique_diseases']:,} diseases")
    
    return stats


def merge_all_datasets():
    """
    Merge all datasets into a comprehensive training dataset.
    
    Returns:
        pd.DataFrame: Final merged dataset
    """
    print("=" * 60)
    print("DATASET MERGING")
    print("=" * 60)
    
    # Load normalized datasets
    normalized_df = load_normalized_datasets()
    
    # Load existing cleaned dataset
    existing_df = load_existing_cleaned_dataset()
    
    # Combine datasets
    print("\nCombining all datasets...")
    
    all_datasets = []
    
    if len(normalized_df) > 0:
        all_datasets.append(normalized_df)
    
    if len(existing_df) > 0:
        # Convert existing format to normalized format
        existing_normalized = []
        for _, row in existing_df.iterrows():
            disease = row.get('diseases') or row.get('disease')
            symptoms_str = row.get('symptoms_list') or row.get('symptoms')
            
            if pd.isna(disease) or pd.isna(symptoms_str):
                continue
            
            try:
                symptoms = json.loads(symptoms_str) if isinstance(symptoms_str, str) else symptoms_str
            except:
                continue
            
            existing_normalized.append({
                'disease': disease,
                'symptoms': symptoms if isinstance(symptoms, list) else [],
                'source': 'existing_cleaned'
            })
        
        if existing_normalized:
            existing_normalized_df = pd.DataFrame(existing_normalized)
            all_datasets.append(existing_normalized_df)
            print(f"✓ Converted {len(existing_normalized_df)} records from existing dataset")
    
    if not all_datasets:
        print("❌ No datasets to merge")
        return pd.DataFrame()
    
    # Combine all datasets
    combined = pd.concat(all_datasets, ignore_index=True)
    print(f"✓ Combined {len(combined)} total records")
    
    # IMPORTANT: Don't merge by disease - keep all individual records!
    # Merging by disease reduces training samples (bad for ML)
    # Instead, just create training format with all records
    print("\n⚠️  Keeping all individual records (not merging by disease)")
    print("This preserves multiple training samples per disease for better ML training")
    
    # Create training format directly from combined dataset (without merging)
    final_dataset = create_training_format(combined)
    
    # Validate
    stats = validate_merged_dataset(final_dataset)
    
    # Save final dataset
    print(f"\n💾 Saving final merged dataset...")
    final_dataset.to_excel(FINAL_DATASET_FILE, index=False)
    print(f"✓ Saved to: {FINAL_DATASET_FILE}")
    
    # Save as CSV too
    csv_file = FINAL_DATASET_FILE.with_suffix('.csv')
    final_dataset.to_csv(csv_file, index=False)
    print(f"✓ Saved to: {csv_file}")
    
    # Save statistics (convert numpy types to native Python types for JSON)
    stats_file = DATA_PROCESSED_DIR / 'expanded_dataset_stats.json'
    
    # Convert numpy types to native Python types
    stats_json_safe = {}
    for key, value in stats.items():
        if isinstance(value, (np.integer, np.int64, np.int32)):
            stats_json_safe[key] = int(value)
        elif isinstance(value, (np.floating, np.float64, np.float32)):
            stats_json_safe[key] = float(value)
        elif isinstance(value, dict):
            stats_json_safe[key] = {k: (int(v) if isinstance(v, (np.integer, np.int64, np.int32)) 
                                       else float(v) if isinstance(v, (np.floating, np.float64, np.float32)) 
                                       else v) for k, v in value.items()}
        else:
            stats_json_safe[key] = value
    
    with open(stats_file, 'w') as f:
        json.dump(stats_json_safe, f, indent=2)
    print(f"✓ Saved statistics to: {stats_file}")
    
    return final_dataset


def main():
    """Main function to merge all datasets."""
    print("This script will merge all normalized datasets into a comprehensive training dataset.")
    print("Expected result: 10,000+ records for improved model accuracy.")
    
    response = input("\nContinue with merging? (y/n): ")
    
    if response.lower() != 'y':
        print("Merging cancelled.")
        return
    
    final_dataset = merge_all_datasets()
    
    if len(final_dataset) > 0:
        print("\n" + "=" * 60)
        print("✅ MERGING COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review merged dataset:", FINAL_DATASET_FILE)
        print("2. Update feature engineering to use expanded dataset")
        print("3. Retrain models: python ml_models/scripts/train_xgboost.py")
        print("4. Compare accuracy improvements!")


if __name__ == '__main__':
    main()

