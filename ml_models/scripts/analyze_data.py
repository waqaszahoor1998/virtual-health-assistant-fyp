#!/usr/bin/env python3
"""
Data Analysis Script for Virtual Health Assistant Project
Analyzes the datasets and provides insights
"""

import pandas as pd
import numpy as np
from collections import Counter

def analyze_drugbank():
    """Analyze the DrugBank dataset"""
    print("=" * 60)
    print("DRUGBANK DATASET ANALYSIS")
    print("=" * 60)
    
    df = pd.read_csv('drugbank_clean.csv')
    print(f"\nTotal records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    # Key columns
    print("\nKey columns:", df.columns.tolist()[:10])
    
    # Check for drugbank-id
    print(f"\nUnique drugbank-ids: {df['drugbank-id'].nunique():,}")
    print(f"Drugs with names: {df['name'].notna().sum():,}")
    print(f"Drugs with indications: {df['indication'].notna().sum():,}")
    
    # States
    if 'state' in df.columns:
        print(f"\nDrug states distribution:")
        print(df['state'].value_counts().head())
    
    return df

def analyze_training_data():
    """Analyze the training dataset"""
    print("\n" + "=" * 60)
    print("TRAINING DATASET ANALYSIS")
    print("=" * 60)
    
    df = pd.read_excel('dataset 2 final.xlsx')
    print(f"\nTotal records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    # Column analysis
    print("\nColumn completeness:")
    for col in df.columns:
        non_null = df[col].notna().sum()
        percentage = (non_null / len(df)) * 100
        print(f"  {col[:50]:50s}: {non_null:4d} ({percentage:5.1f}%)")
    
    # Symptoms analysis
    if 'sumptoms' in df.columns:
        symptom_rows = df[df['sumptoms'].notna()]
        print(f"\nRows with symptoms: {len(symptom_rows):,}")
        
        # Sample symptoms
        print("\nSample symptoms (first 3):")
        for idx, symptom in enumerate(symptom_rows['sumptoms'].head(3), 1):
            print(f"\n{idx}. {symptom[:200]}...")
    
    # Diseases analysis
    if 'diseases' in df.columns:
        disease_rows = df[df['diseases'].notna()]
        print(f"\nRows with diseases: {len(disease_rows):,}")
        print("\nTop 10 diseases:")
        print(disease_rows['diseases'].value_counts().head(10))
    
    # Drug mappings
    if 'drugbank-id' in df.columns:
        drug_rows = df[df['drugbank-id'].notna()]
        print(f"\nRows with drugbank-id: {len(drug_rows):,}")
        print(f"Unique drugbank-ids: {drug_rows['drugbank-id'].nunique():,}")
    
    return df

def analyze_smiles():
    """Analyze the SMILES dataset"""
    print("\n" + "=" * 60)
    print("SMILES DATASET ANALYSIS")
    print("=" * 60)
    
    df = pd.read_excel('SMILIES.xlsx')
    print(f"\nTotal records: {len(df):,}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Unique drugbank-ids: {df['drugbank-id'].nunique():,}")
    
    # Sample SMILES
    print("\nSample SMILES structures (first 3):")
    for idx, row in df.head(3).iterrows():
        print(f"\n{row['name']} ({row['drugbank-id']}):")
        print(f"  {row['smilies']}")
    
    return df

def find_overlaps():
    """Find overlaps between datasets"""
    print("\n" + "=" * 60)
    print("DATASET OVERLAP ANALYSIS")
    print("=" * 60)
    
    # Load datasets
    drugbank = pd.read_csv('drugbank_clean.csv')
    training = pd.read_excel('dataset 2 final.xlsx')
    smiles = pd.read_excel('SMILIES.xlsx')
    
    # Get unique drugbank-ids
    db_ids = set(drugbank['drugbank-id'].unique())
    train_ids = set(training['drugbank-id'].dropna().unique())
    smiles_ids = set(smiles['drugbank-id'].unique())
    
    print(f"\nDrugBank unique IDs: {len(db_ids):,}")
    print(f"Training data unique IDs: {len(train_ids):,}")
    print(f"SMILES unique IDs: {len(smiles_ids):,}")
    
    # Overlaps
    train_in_db = train_ids.intersection(db_ids)
    smiles_in_db = smiles_ids.intersection(db_ids)
    train_in_smiles = train_ids.intersection(smiles_ids)
    
    print(f"\nTraining data IDs in DrugBank: {len(train_in_db):,} ({len(train_in_db)/len(train_ids)*100:.1f}%)")
    print(f"SMILES IDs in DrugBank: {len(smiles_in_db):,} ({len(smiles_in_db)/len(smiles_ids)*100:.1f}%)")
    print(f"Training data IDs in SMILES: {len(train_in_smiles):,} ({len(train_in_smiles)/len(train_ids)*100:.1f}%)")

def main():
    """Main analysis function"""
    print("\n" + "=" * 60)
    print("VIRTUAL HEALTH ASSISTANT - DATA ANALYSIS")
    print("=" * 60)
    
    try:
        drugbank_df = analyze_drugbank()
        training_df = analyze_training_data()
        smiles_df = analyze_smiles()
        find_overlaps()
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print("\nRecommendations:")
        print("1. Clean and standardize symptom text in training data")
        print("2. Create symptom → disease mapping")
        print("3. Link diseases to drugs using drugbank-id")
        print("4. Prepare training dataset for ML models")
        
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

