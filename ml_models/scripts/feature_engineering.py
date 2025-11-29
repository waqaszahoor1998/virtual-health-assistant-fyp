#!/usr/bin/env python3
"""
Feature Engineering Script for ML Model Training.

This script prepares the cleaned symptom data for machine learning:
- Converts symptoms to feature vectors (TF-IDF)
- Creates symptom-disease mapping matrix
- Prepares training data for multi-label classification
- Splits data into train/validation/test sets
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import pickle
import joblib

# Define paths
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MODEL_DIR = Path(__file__).parent.parent / 'models'
SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'


def load_cleaned_data():
    """
    Load cleaned dataset and symptom-disease mapping.
    
    Returns:
        tuple: (cleaned_dataset, symptom_disease_mapping)
    """
    print("Loading cleaned data...")
    
    # Load cleaned dataset
    dataset_file = PROCESSED_DATA_DIR / 'dataset_cleaned.xlsx'
    if not dataset_file.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found at {dataset_file}.\n"
            "Please run data/scripts/clean_symptoms.py first."
        )
    
    df = pd.read_excel(dataset_file)
    print(f"Loaded {len(df)} records from cleaned dataset")
    
    # Load symptom-disease mapping
    mapping_file = PROCESSED_DATA_DIR / 'symptom_disease_mapping.csv'
    if mapping_file.exists():
        mapping_df = pd.read_csv(mapping_file)
        print(f"Loaded {len(mapping_df)} symptom-disease mappings")
    else:
        mapping_df = None
        print("Warning: Symptom-disease mapping not found")
    
    return df, mapping_df


def prepare_symptom_features(df):
    """
    Convert symptom lists to TF-IDF feature vectors.
    
    Args:
        df (pd.DataFrame): Dataset with symptoms_list column
    
    Returns:
        tuple: (feature_matrix, symptom_vectorizer, symptom_list)
    """
    print("\nCreating symptom feature vectors using TF-IDF...")
    
    # Extract symptom lists from JSON strings
    symptom_lists = []
    for idx, row in df.iterrows():
        if pd.notna(row.get('symptoms_list')):
            try:
                symptoms = json.loads(row['symptoms_list'])
                # Join symptoms into a single string for TF-IDF
                symptom_text = ' '.join(symptoms)
                symptom_lists.append(symptom_text)
            except (json.JSONDecodeError, TypeError):
                symptom_lists.append('')
        else:
            symptom_lists.append('')
    
    # Create TF-IDF vectorizer
    # Using character-level n-grams to handle variations in symptom names
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Top 5000 features
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=2,  # Ignore symptoms that appear in less than 2 records
        max_df=0.95,  # Ignore symptoms that appear in more than 95% of records
        lowercase=True,
        strip_accents='unicode'
    )
    
    # Fit and transform symptoms
    feature_matrix = vectorizer.fit_transform(symptom_lists)
    
    print(f"Created feature matrix: {feature_matrix.shape}")
    print(f"Number of features (symptoms): {len(vectorizer.get_feature_names_out())}")
    
    return feature_matrix, vectorizer, symptom_lists


def prepare_disease_labels(df):
    """
    Prepare disease labels for multi-label classification.
    
    Args:
        df (pd.DataFrame): Dataset with disease_cleaned column
    
    Returns:
        tuple: (label_matrix, disease_encoder, unique_diseases)
    """
    print("\nPreparing disease labels...")
    
    # Extract disease labels
    disease_labels = []
    for idx, row in df.iterrows():
        if pd.notna(row.get('disease_cleaned')):
            # Convert to list format for multi-label binarizer
            disease_labels.append([row['disease_cleaned']])
        else:
            disease_labels.append([])
    
    # Use MultiLabelBinarizer for multi-label classification
    mlb = MultiLabelBinarizer()
    label_matrix = mlb.fit_transform(disease_labels)
    
    unique_diseases = mlb.classes_
    print(f"Found {len(unique_diseases)} unique diseases")
    print(f"Label matrix shape: {label_matrix.shape}")
    
    return label_matrix, mlb, unique_diseases


def filter_valid_records(df, feature_matrix, label_matrix):
    """
    Filter records that have both symptoms and diseases.
    
    Args:
        df (pd.DataFrame): Original dataset
        feature_matrix: Feature matrix
        label_matrix: Label matrix
    
    Returns:
        tuple: (filtered_df, filtered_features, filtered_labels)
    """
    print("\nFiltering valid records (must have both symptoms and diseases)...")
    
    # Find rows with both symptoms and diseases
    has_symptoms = (feature_matrix.sum(axis=1) > 0).A1  # Convert to 1D array
    has_diseases = (label_matrix.sum(axis=1) > 0)
    valid_mask = has_symptoms & has_diseases
    
    filtered_df = df[valid_mask].reset_index(drop=True)
    filtered_features = feature_matrix[valid_mask]
    filtered_labels = label_matrix[valid_mask]
    
    print(f"Valid records: {valid_mask.sum()}/{len(df)} ({valid_mask.sum()/len(df)*100:.1f}%)")
    
    return filtered_df, filtered_features, filtered_labels


def split_data(features, labels, test_size=0.2, val_size=0.15, random_state=42):
    """
    Split data into train, validation, and test sets.
    
    Args:
        features: Feature matrix
        labels: Label matrix
        test_size (float): Proportion for test set
        val_size (float): Proportion for validation set (from remaining after test)
        random_state (int): Random seed
    
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    print(f"\nSplitting data (train/val/test): {1-test_size-val_size*0.85:.1%}/{val_size:.1%}/{test_size:.1%}...")
    
    # First split: train+val and test
    X_temp, X_test, y_temp, y_test = train_test_split(
        features, labels,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )
    
    # Second split: train and validation
    val_size_adjusted = val_size / (1 - test_size)  # Adjust for remaining data
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_size_adjusted,
        random_state=random_state,
        shuffle=True
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def save_preprocessed_data(X_train, X_val, X_test, y_train, y_val, y_test,
                           vectorizer, mlb, unique_diseases):
    """
    Save preprocessed data for model training.
    
    Args:
        X_train, X_val, X_test: Feature matrices
        y_train, y_val, y_test: Label matrices
        vectorizer: TF-IDF vectorizer
        mlb: MultiLabelBinarizer
        unique_diseases: List of unique diseases
    """
    print("\nSaving preprocessed data...")
    
    # Ensure model directory exists
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save feature matrices
    joblib.dump(X_train, MODEL_DIR / 'X_train.pkl')
    joblib.dump(X_val, MODEL_DIR / 'X_val.pkl')
    joblib.dump(X_test, MODEL_DIR / 'X_test.pkl')
    
    # Save label matrices
    joblib.dump(y_train, MODEL_DIR / 'y_train.pkl')
    joblib.dump(y_val, MODEL_DIR / 'y_val.pkl')
    joblib.dump(y_test, MODEL_DIR / 'y_test.pkl')
    
    # Save vectorizer and encoder
    joblib.dump(vectorizer, MODEL_DIR / 'symptom_vectorizer.pkl')
    joblib.dump(mlb, MODEL_DIR / 'disease_encoder.pkl')
    
    # Save disease list
    with open(MODEL_DIR / 'unique_diseases.txt', 'w') as f:
        for disease in unique_diseases:
            f.write(f"{disease}\n")
    
    # Save metadata
    metadata = {
        'num_features': X_train.shape[1],
        'num_diseases': len(unique_diseases),
        'train_samples': X_train.shape[0],
        'val_samples': X_val.shape[0],
        'test_samples': X_test.shape[0]
    }
    
    import json
    with open(MODEL_DIR / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✓ Saved all preprocessed data")
    print(f"  - Feature matrices: X_train, X_val, X_test")
    print(f"  - Label matrices: y_train, y_val, y_test")
    print(f"  - Vectorizer: symptom_vectorizer.pkl")
    print(f"  - Encoder: disease_encoder.pkl")
    print(f"  - Diseases list: unique_diseases.txt")
    print(f"  - Metadata: metadata.json")


def main():
    """Main function to run feature engineering."""
    print("=" * 60)
    print("FEATURE ENGINEERING FOR ML MODELS")
    print("=" * 60)
    
    try:
        # Load cleaned data
        df, mapping_df = load_cleaned_data()
        
        # Prepare symptom features (TF-IDF)
        feature_matrix, vectorizer, symptom_lists = prepare_symptom_features(df)
        
        # Prepare disease labels
        label_matrix, mlb, unique_diseases = prepare_disease_labels(df)
        
        # Filter valid records
        df_valid, features_valid, labels_valid = filter_valid_records(
            df, feature_matrix, label_matrix
        )
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(
            features_valid, labels_valid,
            test_size=0.15,
            val_size=0.15,
            random_state=42
        )
        
        # Save preprocessed data
        save_preprocessed_data(
            X_train, X_val, X_test,
            y_train, y_val, y_test,
            vectorizer, mlb, unique_diseases
        )
        
        print("\n" + "=" * 60)
        print("FEATURE ENGINEERING COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run train_xgboost.py to train XGBoost model")
        print("2. Run train_random_forest.py to train Random Forest model")
        print("3. Compare model performance")
        
    except Exception as e:
        print(f"\n❌ Error during feature engineering: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

