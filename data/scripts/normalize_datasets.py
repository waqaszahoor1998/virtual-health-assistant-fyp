#!/usr/bin/env python3
"""
Dataset Normalization Script.

Normalizes multiple datasets to a common format for merging.
Handles different column names, formats, and structures across datasets.

This script:
- Standardizes symptom names
- Standardizes disease names
- Creates unified format across all datasets
- Handles different file formats (CSV, Excel, JSON)
"""

import pandas as pd
import numpy as np
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RAW_DATASETS_DIR = PROJECT_ROOT / 'datasets' / 'raw'
PROCESSED_DATASETS_DIR = PROJECT_ROOT / 'datasets' / 'processed'
DATA_PROCESSED_DIR = PROJECT_ROOT / 'data' / 'processed'

# Ensure directories exist
PROCESSED_DATASETS_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Common symptom synonyms mapping
SYMPTOM_SYNONYMS = {
    'fever': ['high temperature', 'elevated temperature', 'pyrexia', 'febrile'],
    'headache': ['head pain', 'cephalgia', 'cephalalgia'],
    'nausea': ['feeling sick', 'queasiness', 'sick feeling'],
    'vomiting': ['throwing up', 'emesis'],
    'diarrhea': ['loose stools', 'loose bowels', 'diarrhoea'],
    'fatigue': ['tiredness', 'exhaustion', 'lethargy', 'weariness'],
    'cough': ['coughing'],
    'sore throat': ['throat pain', 'pharyngitis'],
    'chest pain': ['chest discomfort', 'thoracic pain'],
    'abdominal pain': ['stomach pain', 'belly pain', 'tummy ache'],
    'dizziness': ['vertigo', 'lightheadedness'],
    'rash': ['skin rash', 'skin irritation'],
    'shortness of breath': ['dyspnea', 'difficulty breathing', 'breathlessness'],
}


def normalize_symptom_name(symptom: str) -> str:
    """
    Normalize symptom name to standard form.
    
    Args:
        symptom (str): Raw symptom name
    
    Returns:
        str: Normalized symptom name
    """
    if pd.isna(symptom) or not symptom:
        return None
    
    symptom = str(symptom).strip().lower()
    
    # Remove extra whitespace
    symptom = re.sub(r'\s+', ' ', symptom)
    
    # Check synonyms and normalize
    for standard, variants in SYMPTOM_SYNONYMS.items():
        if symptom in variants or symptom == standard:
            return standard
    
    # Remove common prefixes/suffixes
    symptom = re.sub(r'^(mild|severe|moderate|acute|chronic)\s+', '', symptom)
    symptom = re.sub(r'\s+(mild|severe|moderate|acute|chronic)$', '', symptom)
    
    # Remove punctuation at end
    symptom = re.sub(r'[.,;]+$', '', symptom)
    
    return symptom.strip() if symptom.strip() else None


def normalize_disease_name(disease: str) -> str:
    """
    Normalize disease name to standard form.
    
    Args:
        disease (str): Raw disease name
    
    Returns:
        str: Normalized disease name
    """
    if pd.isna(disease) or not disease:
        return None
    
    disease = str(disease).strip()
    
    # Remove extra whitespace
    disease = re.sub(r'\s+', ' ', disease)
    
    # Capitalize properly (Title Case)
    disease = disease.title()
    
    # Remove common suffixes
    disease = re.sub(r'\s+disease$', '', disease, flags=re.IGNORECASE)
    disease = re.sub(r'\s+syndrome$', '', disease, flags=re.IGNORECASE)
    
    return disease.strip() if disease.strip() else None


def extract_symptoms_from_text(text: str) -> List[str]:
    """
    Extract symptoms from text field (handles various formats).
    
    Args:
        text (str): Text containing symptoms (comma-separated, list, etc.)
    
    Returns:
        list: List of normalized symptom names
    """
    if pd.isna(text) or not text:
        return []
    
    text = str(text)
    symptoms = []
    
    # Try to parse as JSON list first
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            symptoms = parsed
    except (json.JSONDecodeError, ValueError):
        pass
    
    # If not JSON, split by common delimiters
    if not symptoms:
        # Split by comma, semicolon, newline, or pipe
        symptoms = re.split(r'[,;\n|]', text)
    
    # Normalize each symptom
    normalized_symptoms = []
    for symptom in symptoms:
        normalized = normalize_symptom_name(symptom)
        if normalized and normalized not in normalized_symptoms:
            normalized_symptoms.append(normalized)
    
    return normalized_symptoms


def normalize_dataset_1_disease_symptom(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Disease Symptom Description dataset.
    
    Expected columns: Disease, Symptom, Description
    """
    print("  Normalizing Disease Symptom Description dataset...")
    
    normalized_records = []
    
    for _, row in df.iterrows():
        # Extract disease
        disease = row.get('Disease') or row.get('disease') or row.get('DISEASE')
        if pd.isna(disease):
            continue
        disease = normalize_disease_name(disease)
        
        # Extract symptoms
        symptom = row.get('Symptom') or row.get('symptom') or row.get('SYMPTOM')
        symptoms_list = []
        
        if not pd.isna(symptom):
            symptoms_list = extract_symptoms_from_text(str(symptom))
        
        # If single symptom, convert to list
        if symptoms_list:
            normalized_records.append({
                'disease': disease,
                'symptoms': symptoms_list,
                'source': 'disease_symptom_description'
            })
    
    return pd.DataFrame(normalized_records)


def normalize_dataset_2_symptom2disease(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Symptom2Disease dataset.
    
    Expected columns: symptom, disease (or similar)
    """
    print("  Normalizing Symptom2Disease dataset...")
    
    normalized_records = []
    
    for _, row in df.iterrows():
        # Extract disease
        disease = row.get('disease') or row.get('Disease') or row.get('label')
        if pd.isna(disease):
            continue
        disease = normalize_disease_name(disease)
        
        # Extract symptoms
        symptom_text = row.get('symptom') or row.get('Symptom') or row.get('text') or row.get('symptoms')
        symptoms_list = []
        
        if not pd.isna(symptom_text):
            symptoms_list = extract_symptoms_from_text(str(symptom_text))
        
        if symptoms_list:
            normalized_records.append({
                'disease': disease,
                'symptoms': symptoms_list,
                'source': 'symptom2disease'
            })
    
    return pd.DataFrame(normalized_records)


def normalize_dataset_3_disease_prediction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Disease Prediction ML dataset.
    
    Expected format: Binary symptom columns, Disease column
    """
    print("  Normalizing Disease Prediction ML dataset...")
    
    normalized_records = []
    
    # Find disease column
    disease_col = None
    for col in df.columns:
        if col.lower() in ['disease', 'prognosis', 'label', 'target']:
            disease_col = col
            break
    
    if not disease_col:
        print("    ⚠️  Warning: Disease column not found")
        return pd.DataFrame()
    
    # Find symptom columns (binary features)
    symptom_cols = [col for col in df.columns 
                   if col != disease_col and df[col].dtype in [np.int64, np.float64, bool]]
    
    for _, row in df.iterrows():
        disease = row.get(disease_col)
        if pd.isna(disease):
            continue
        
        disease = normalize_disease_name(str(disease))
        
        # Extract symptoms (columns with value 1 or True)
        symptoms_list = []
        for col in symptom_cols:
            value = row.get(col)
            if pd.notna(value) and (value == 1 or value == True or value > 0):
                symptom_name = normalize_symptom_name(col)
                if symptom_name and symptom_name not in symptoms_list:
                    symptoms_list.append(symptom_name)
        
        if symptoms_list:
            normalized_records.append({
                'disease': disease,
                'symptoms': symptoms_list,
                'source': 'disease_prediction_ml'
            })
    
    return pd.DataFrame(normalized_records)


def normalize_current_dataset() -> pd.DataFrame:
    """
    Normalize the current dataset (dataset 2 final.xlsx).
    Reuses existing cleaning logic.
    """
    print("  Normalizing current dataset (dataset 2 final.xlsx)...")
    
    current_dataset_file = PROJECT_ROOT / 'data' / 'raw' / 'dataset 2 final.xlsx'
    
    if not current_dataset_file.exists():
        print("    ⚠️  Warning: Current dataset file not found")
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(current_dataset_file)
        
        normalized_records = []
        
        for _, row in df.iterrows():
            # Extract disease
            disease = row.get('diseases') or row.get('Diseases')
            if pd.isna(disease):
                continue
            disease = normalize_disease_name(str(disease))
            
            # Extract symptoms
            symptoms_text = row.get('sumptoms') or row.get('symptoms') or row.get('Symptoms')
            symptoms_list = []
            
            if not pd.isna(symptoms_text):
                symptoms_list = extract_symptoms_from_text(str(symptoms_text))
            
            if symptoms_list and disease:
                normalized_records.append({
                    'disease': disease,
                    'symptoms': symptoms_list,
                    'source': 'dataset_2_final'
                })
        
        return pd.DataFrame(normalized_records)
        
    except Exception as e:
        print(f"    ❌ Error processing current dataset: {str(e)}")
        return pd.DataFrame()


def load_and_normalize_dataset(dataset_dir: Path) -> pd.DataFrame:
    """
    Load and normalize a dataset from directory.
    
    Args:
        dataset_dir (Path): Directory containing dataset files
    
    Returns:
        pd.DataFrame: Normalized dataset
    """
    dataset_name = dataset_dir.name
    
    print(f"\n📂 Processing: {dataset_name}")
    
    # Find data files (CSV, Excel, JSON)
    data_files = []
    for ext in ['*.csv', '*.xlsx', '*.xls', '*.json']:
        data_files.extend(list(dataset_dir.glob(ext)))
    
    if not data_files:
        print(f"  ⚠️  No data files found in {dataset_name}")
        return pd.DataFrame()
    
    all_normalized = []
    
    for data_file in data_files:
        print(f"  📄 Processing file: {data_file.name}")
        
        try:
            # Load file based on extension
            if data_file.suffix == '.csv':
                df = pd.read_csv(data_file, low_memory=False)
            elif data_file.suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(data_file)
            elif data_file.suffix == '.json':
                df = pd.read_json(data_file)
            else:
                continue
            
            print(f"    Loaded {len(df)} records")
            
            # Normalize based on dataset type
            if 'disease_symptom_description' in dataset_name:
                normalized = normalize_dataset_1_disease_symptom(df)
            elif 'symptom2disease' in dataset_name:
                normalized = normalize_dataset_2_symptom2disease(df)
            elif 'disease_prediction' in dataset_name or 'medical_symptoms' in dataset_name:
                normalized = normalize_dataset_3_disease_prediction(df)
            else:
                # Generic normalization
                normalized = normalize_dataset_1_disease_symptom(df)
            
            if len(normalized) > 0:
                all_normalized.append(normalized)
                print(f"    ✓ Normalized {len(normalized)} records")
            
        except Exception as e:
            print(f"    ❌ Error processing {data_file.name}: {str(e)}")
            continue
    
    if all_normalized:
        result = pd.concat(all_normalized, ignore_index=True)
        return result
    else:
        return pd.DataFrame()


def normalize_all_datasets():
    """
    Normalize all datasets in the raw datasets directory.
    
    Returns:
        pd.DataFrame: Combined normalized dataset
    """
    print("=" * 60)
    print("DATASET NORMALIZATION")
    print("=" * 60)
    
    all_datasets = []
    
    # Normalize current dataset
    current_normalized = normalize_current_dataset()
    if len(current_normalized) > 0:
        all_datasets.append(current_normalized)
        print(f"✓ Normalized current dataset: {len(current_normalized)} records")
    
    # Normalize downloaded datasets
    if RAW_DATASETS_DIR.exists():
        dataset_dirs = [d for d in RAW_DATASETS_DIR.iterdir() if d.is_dir()]
        
        for dataset_dir in dataset_dirs:
            normalized = load_and_normalize_dataset(dataset_dir)
            if len(normalized) > 0:
                all_datasets.append(normalized)
    
    if not all_datasets:
        print("\n❌ No datasets to normalize")
        return pd.DataFrame()
    
    # Combine all normalized datasets
    print("\n" + "=" * 60)
    print("COMBINING NORMALIZED DATASETS")
    print("=" * 60)
    
    combined = pd.concat(all_datasets, ignore_index=True)
    print(f"Total normalized records: {len(combined)}")
    
    # Remove duplicates (same disease + symptoms combination)
    print("Removing duplicates...")
    before_count = len(combined)
    
    # Convert symptoms list to sorted tuple for duplicate detection
    combined['symptoms_tuple'] = combined['symptoms'].apply(lambda x: tuple(sorted(x)))
    combined = combined.drop_duplicates(subset=['disease', 'symptoms_tuple'], keep='first')
    combined = combined.drop(columns=['symptoms_tuple'])
    
    after_count = len(combined)
    duplicates_removed = before_count - after_count
    print(f"Removed {duplicates_removed} duplicates")
    print(f"Final record count: {after_count}")
    
    # Save normalized dataset
    output_file = PROCESSED_DATASETS_DIR / 'normalized_datasets.xlsx'
    combined.to_excel(output_file, index=False)
    print(f"\n✓ Saved normalized dataset to: {output_file}")
    
    # Also save as CSV for easier inspection
    csv_file = PROCESSED_DATASETS_DIR / 'normalized_datasets.csv'
    combined.to_csv(csv_file, index=False)
    print(f"✓ Saved normalized dataset to: {csv_file}")
    
    # Save statistics
    stats = {
        'total_records': len(combined),
        'unique_diseases': combined['disease'].nunique(),
        'datasets_combined': combined['source'].nunique(),
        'records_per_source': combined['source'].value_counts().to_dict()
    }
    
    stats_file = PROCESSED_DATASETS_DIR / 'normalization_stats.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📊 Statistics:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Unique diseases: {stats['unique_diseases']}")
    print(f"  Datasets combined: {stats['datasets_combined']}")
    print(f"  Records per source: {stats['records_per_source']}")
    
    return combined


def main():
    """Main function to normalize all datasets."""
    print("This script will normalize all datasets to a common format.")
    print("It handles different column names, formats, and structures.")
    
    response = input("\nContinue with normalization? (y/n): ")
    
    if response.lower() != 'y':
        print("Normalization cancelled.")
        return
    
    normalized = normalize_all_datasets()
    
    if len(normalized) > 0:
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("1. Review normalized dataset:", PROCESSED_DATASETS_DIR / 'normalized_datasets.xlsx')
        print("2. Run merge script: python data/scripts/merge_datasets.py")
        print("3. Update feature engineering with expanded dataset")
        print("4. Retrain models")


if __name__ == '__main__':
    main()

