#!/usr/bin/env python3
"""
Symptom Cleaning and Normalization Script.

This script:
- Cleans and normalizes symptoms from the training dataset
- Standardizes symptom text format
- Creates structured symptom lists
- Handles missing values
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path

# Define paths
RAW_DATA_DIR = Path(__file__).parent.parent / 'raw'
PROCESSED_DATA_DIR = Path(__file__).parent.parent / 'processed'


def clean_symptom_text(symptom_text):
    """
    Clean and normalize symptom text.
    
    Args:
        symptom_text (str): Raw symptom text (may be comma-separated)
    
    Returns:
        list: List of cleaned symptom strings
    """
    if pd.isna(symptom_text) or symptom_text == '':
        return []
    
    # Convert to string if not already
    symptom_text = str(symptom_text)
    
    # Remove common prefixes/suffixes
    symptom_text = symptom_text.strip()
    
    # Split by common delimiters (comma, semicolon, newline)
    symptoms = re.split(r'[,;\n]', symptom_text)
    
    # Clean each symptom
    cleaned_symptoms = []
    for symptom in symptoms:
        # Strip whitespace
        symptom = symptom.strip()
        
        # Remove bullet points and dashes
        symptom = re.sub(r'^[•\-\*]\s*', '', symptom)
        
        # Remove extra whitespace
        symptom = re.sub(r'\s+', ' ', symptom)
        
        # Remove trailing punctuation (except if part of medical term)
        symptom = re.sub(r'[.,;]+$', '', symptom)
        
        # Convert to lowercase for consistency
        symptom = symptom.lower()
        
        # Skip empty strings
        if symptom and len(symptom) > 2:
            cleaned_symptoms.append(symptom)
    
    return cleaned_symptoms


def normalize_symptom_name(symptom):
    """
    Normalize symptom names (handle synonyms and variations).
    
    Args:
        symptom (str): Symptom name
    
    Returns:
        str: Normalized symptom name
    """
    # Common symptom synonyms mapping
    synonym_map = {
        'fever': ['high temperature', 'elevated body temperature', 'pyrexia'],
        'headache': ['head pain', 'cephalalgia'],
        'nausea': ['feeling sick', 'queasiness'],
        'fatigue': ['tiredness', 'exhaustion', 'lethargy'],
        'shortness of breath': ['dyspnea', 'breathlessness', 'difficulty breathing'],
        'chest pain': ['chest discomfort', 'thoracic pain'],
    }
    
    symptom_lower = symptom.lower()
    
    # Check if symptom matches any synonym
    for key, synonyms in synonym_map.items():
        if symptom_lower == key or symptom_lower in synonyms:
            return key
        for synonym in synonyms:
            if synonym in symptom_lower:
                return key
    
    return symptom_lower


def extract_and_clean_symptoms(df):
    """
    Extract and clean symptoms from the training dataset.
    
    Args:
        df (pd.DataFrame): Training dataset
    
    Returns:
        pd.DataFrame: Dataset with cleaned symptom lists
    """
    print("Extracting and cleaning symptoms...")
    
    # Create new column for cleaned symptoms
    df['symptoms_cleaned'] = None
    df['symptoms_list'] = None
    df['symptom_count'] = 0
    
    symptom_column = 'sumptoms'  # Note: typo in original data
    
    if symptom_column not in df.columns:
        print(f"Warning: Column '{symptom_column}' not found. Available columns: {df.columns.tolist()}")
        return df
    
    # Process each row
    for idx, row in df.iterrows():
        symptom_text = row[symptom_column]
        
        # Clean symptoms
        cleaned_symptoms = clean_symptom_text(symptom_text)
        
        # Normalize symptom names
        normalized_symptoms = [normalize_symptom_name(s) for s in cleaned_symptoms]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_symptoms = []
        for s in normalized_symptoms:
            if s not in seen:
                seen.add(s)
                unique_symptoms.append(s)
        
        # Update dataframe
        df.at[idx, 'symptoms_cleaned'] = ', '.join(unique_symptoms)
        df.at[idx, 'symptoms_list'] = json.dumps(unique_symptoms)
        df.at[idx, 'symptom_count'] = len(unique_symptoms)
        
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(df)} rows...")
    
    print(f"Completed symptom extraction!")
    print(f"Total rows with symptoms: {df['symptom_count'].gt(0).sum()}")
    print(f"Average symptoms per record: {df['symptom_count'].mean():.2f}")
    
    return df


def clean_disease_names(df):
    """
    Clean and standardize disease names.
    
    Args:
        df (pd.DataFrame): Training dataset
    
    Returns:
        pd.DataFrame: Dataset with cleaned disease names
    """
    print("\nCleaning disease names...")
    
    if 'diseases' not in df.columns:
        print("Warning: 'diseases' column not found")
        return df
    
    # Clean disease names
    df['disease_cleaned'] = df['diseases'].apply(
        lambda x: str(x).strip().lower() if pd.notna(x) else None
    )
    
    # Remove common prefixes/suffixes
    df['disease_cleaned'] = df['disease_cleaned'].str.replace(r'^disease:\s*', '', regex=True, case=False)
    df['disease_cleaned'] = df['disease_cleaned'].str.replace(r'\s+', ' ', regex=True)
    
    # Count unique diseases
    unique_diseases = df['disease_cleaned'].dropna().nunique()
    print(f"Found {unique_diseases} unique diseases")
    
    return df


def create_symptom_disease_mapping(df):
    """
    Create mapping between symptoms and diseases.
    
    Args:
        df (pd.DataFrame): Training dataset with cleaned symptoms
    
    Returns:
        pd.DataFrame: Symptom-disease mapping
    """
    print("\nCreating symptom-disease mapping...")
    
    mappings = []
    
    for idx, row in df.iterrows():
        if pd.isna(row['symptoms_list']) or pd.isna(row['disease_cleaned']):
            continue
        
        try:
            symptoms = json.loads(row['symptoms_list'])
            disease = row['disease_cleaned']
            
            # Create mapping for each symptom-disease pair
            for symptom in symptoms:
                mappings.append({
                    'symptom': symptom,
                    'disease': disease,
                    'source_record_id': idx
                })
        except (json.JSONDecodeError, TypeError):
            continue
    
    mapping_df = pd.DataFrame(mappings)
    
    # Count occurrences (symptom-disease pairs that appear multiple times)
    mapping_df['frequency'] = mapping_df.groupby(['symptom', 'disease']).transform('size')
    
    print(f"Created {len(mapping_df)} symptom-disease mappings")
    print(f"Unique symptom-disease pairs: {mapping_df[['symptom', 'disease']].drop_duplicates().shape[0]}")
    
    return mapping_df


def main():
    """Main function to run the cleaning process."""
    print("=" * 60)
    print("SYMPTOM CLEANING AND NORMALIZATION")
    print("=" * 60)
    
    # Ensure processed directory exists
    PROCESSED_DATA_DIR.mkdir(exist_ok=True)
    
    # Load training dataset
    print(f"\nLoading dataset from {RAW_DATA_DIR / 'dataset 2 final.xlsx'}...")
    df = pd.read_excel(RAW_DATA_DIR / 'dataset 2 final.xlsx')
    print(f"Loaded {len(df)} records")
    
    # Extract and clean symptoms
    df = extract_and_clean_symptoms(df)
    
    # Clean disease names
    df = clean_disease_names(df)
    
    # Create symptom-disease mapping
    mapping_df = create_symptom_disease_mapping(df)
    
    # Save cleaned dataset
    output_file = PROCESSED_DATA_DIR / 'dataset_cleaned.xlsx'
    print(f"\nSaving cleaned dataset to {output_file}...")
    df.to_excel(output_file, index=False)
    print("✓ Saved cleaned dataset")
    
    # Save symptom-disease mapping
    mapping_file = PROCESSED_DATA_DIR / 'symptom_disease_mapping.csv'
    print(f"Saving symptom-disease mapping to {mapping_file}...")
    mapping_df.to_csv(mapping_file, index=False)
    print("✓ Saved symptom-disease mapping")
    
    # Generate statistics
    print("\n" + "=" * 60)
    print("CLEANING STATISTICS")
    print("=" * 60)
    print(f"Original records: {len(df)}")
    print(f"Records with symptoms: {df['symptom_count'].gt(0).sum()}")
    print(f"Records with diseases: {df['disease_cleaned'].notna().sum()}")
    print(f"Average symptoms per record: {df['symptom_count'].mean():.2f}")
    print(f"Unique symptoms found: {mapping_df['symptom'].nunique()}")
    print(f"Unique diseases found: {df['disease_cleaned'].nunique()}")
    print(f"Symptom-disease pairs: {mapping_df[['symptom', 'disease']].drop_duplicates().shape[0]}")
    
    print("\n✓ Cleaning complete!")


if __name__ == "__main__":
    main()

