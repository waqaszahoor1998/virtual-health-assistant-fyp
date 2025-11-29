"""
DrugBank Service.

Handles loading and searching the DrugBank database for drug suggestions.
"""

import pandas as pd
from pathlib import Path
from flask import current_app
import re


class DrugBankService:
    """
    Service class for DrugBank database operations.
    
    Handles loading drug database and searching for drugs.
    """
    
    def __init__(self):
        """Initialize DrugBank service with data path."""
        # Get data directory from config
        data_dir = Path(current_app.config.get('DATA_DIR',
            Path(__file__).parent.parent.parent / 'data'
        ))
        
        # DrugBank CSV file
        self.drugbank_file = data_dir / 'raw' / 'drugbank_clean.csv'
        
        # Loaded dataframe (lazy loading)
        self.drug_df = None
        self.drugs_loaded = False
    
    def load_drugs(self):
        """Load DrugBank database from CSV file."""
        if self.drugs_loaded:
            return
        
        try:
            if not self.drugbank_file.exists():
                raise FileNotFoundError(
                    f"DrugBank CSV not found at {self.drugbank_file}"
                )
            
            print(f"Loading DrugBank database from {self.drugbank_file}...")
            
            # Load CSV (use low_memory=False to avoid dtype warnings)
            self.drug_df = pd.read_csv(self.drugbank_file, low_memory=False)
            
            # Keep only essential columns to save memory
            essential_columns = [
                'drugbank-id', 'name', 'indication', 'mechanism-of-action',
                'description', 'state'
            ]
            
            # Filter to columns that exist
            available_columns = [col for col in essential_columns if col in self.drug_df.columns]
            self.drug_df = self.drug_df[available_columns]
            
            # Filter to approved/active drugs only
            if 'state' in self.drug_df.columns:
                self.drug_df = self.drug_df[
                    self.drug_df['state'].isin(['solid', 'liquid', 'approved'])
                ]
            
            self.drugs_loaded = True
            print(f"✓ Loaded {len(self.drug_df)} drugs from DrugBank")
            
        except Exception as e:
            print(f"❌ Error loading DrugBank: {e}")
            raise
    
    def search_drugs(self, query, limit=20):
        """
        Search drugs by name.
        
        Args:
            query (str): Search query (drug name or part of name)
            limit (int): Maximum number of results
        
        Returns:
            list: List of drug dictionaries
        """
        if not self.drugs_loaded:
            self.load_drugs()
        
        query_lower = query.lower().strip()
        
        if not query_lower:
            return []
        
        # Search in drug names
        mask = self.drug_df['name'].str.lower().str.contains(query_lower, na=False)
        results = self.drug_df[mask].head(limit)
        
        # Convert to list of dictionaries
        drugs = []
        for _, row in results.iterrows():
            drugs.append({
                'drugbank_id': row.get('drugbank-id', ''),
                'name': row.get('name', ''),
                'indication': row.get('indication', '')[:500] if pd.notna(row.get('indication')) else None,  # Limit length
                'description': row.get('description', '')[:300] if pd.notna(row.get('description')) else None,
                'state': row.get('state', '')
            })
        
        return drugs
    
    def suggest_drugs_for_disease(self, disease_name, limit=10):
        """
        Suggest drugs based on disease name.
        
        Searches DrugBank indications for drugs that treat the given disease.
        
        Args:
            disease_name (str): Name of the disease
            limit (int): Maximum number of suggestions
        
        Returns:
            list: List of suggested drugs
        """
        if not self.drugs_loaded:
            self.load_drugs()
        
        disease_lower = disease_name.lower().strip()
        
        if not disease_lower:
            return []
        
        # Search in indication column
        if 'indication' not in self.drug_df.columns:
            return []
        
        # Create mask for drugs with matching indication
        mask = self.drug_df['indication'].str.lower().str.contains(
            disease_lower, 
            na=False, 
            regex=False
        )
        
        results = self.drug_df[mask].head(limit)
        
        # Convert to list of dictionaries
        drugs = []
        for _, row in results.iterrows():
            indication = str(row.get('indication', ''))[:500]
            
            # Extract relevant part of indication if it's long
            if disease_lower in indication.lower():
                # Find position of disease mention
                idx = indication.lower().find(disease_lower)
                start = max(0, idx - 100)
                end = min(len(indication), idx + len(disease_name) + 100)
                indication = indication[start:end]
            
            drugs.append({
                'drugbank_id': row.get('drugbank-id', ''),
                'name': row.get('name', ''),
                'indication': indication,
                'relevance_score': 1.0  # Could calculate based on match quality
            })
        
        return drugs
    
    def get_drug_by_id(self, drugbank_id):
        """
        Get drug details by DrugBank ID.
        
        Args:
            drugbank_id (str): DrugBank ID (e.g., 'DB00001')
        
        Returns:
            dict: Drug details or None if not found
        """
        if not self.drugs_loaded:
            self.load_drugs()
        
        result = self.drug_df[self.drug_df['drugbank-id'] == drugbank_id]
        
        if result.empty:
            return None
        
        row = result.iloc[0]
        return {
            'drugbank_id': row.get('drugbank-id', ''),
            'name': row.get('name', ''),
            'indication': row.get('indication', ''),
            'mechanism_of_action': row.get('mechanism-of-action', ''),
            'description': row.get('description', ''),
            'state': row.get('state', '')
        }
    
    def is_available(self):
        """Check if DrugBank database is available."""
        return self.drugbank_file.exists()


# Global instance (singleton pattern)
_drugbank_service = None


def get_drugbank_service():
    """
    Get global DrugBank service instance.
    
    Returns:
        DrugBankService: DrugBank service instance
    """
    global _drugbank_service
    if _drugbank_service is None:
        _drugbank_service = DrugBankService()
    return _drugbank_service

