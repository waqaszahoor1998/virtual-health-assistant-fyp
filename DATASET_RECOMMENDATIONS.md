# Dataset Recommendations - Virtual Health Assistant

## 🔍 Current Dataset Issues

- **Small size**: 3,963 records (only 1,848 with symptoms)
- **Incomplete**: 53.4% missing symptoms
- **Limited coverage**: Only 493 unique diseases

## ✅ Recommended Datasets to Add

### 1. **Disease Symptom Dataset (Kaggle)** ⭐ Recommended
- **Name**: "Disease Symptom Dataset"
- **Size**: 5,000+ records
- **Link**: https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
- **Content**: 
  - Symptoms mapped to diseases
  - Disease descriptions
  - Preprocessed format
- **Easy to integrate**: CSV format

### 2. **Symptom2Disease Dataset**
- **Name**: "Symptom2Disease"
- **Size**: 1,200+ records
- **Link**: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
- **Content**: 
  - Symptom text → Disease classification
  - Clean, structured data

### 3. **Medical Symptoms Dataset**
- **Name**: "Medical Symptoms"
- **Size**: 3,000+ records
- **Link**: https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms
- **Content**: 
  - Comprehensive symptom lists
  - Multiple diseases per symptom set

### 4. **Disease Prediction Dataset**
- **Name**: "Disease Prediction Using Machine Learning"
- **Size**: 5,000+ records
- **Link**: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
- **Content**: 
  - Binary symptom features
  - Disease labels

## 🔧 Data Augmentation Strategies

### 1. **Combine Multiple Datasets**
- Merge all datasets using common columns
- Create unified symptom-disease mapping
- Expected result: 10,000-15,000 records

### 2. **Symptom Synonym Expansion**
- "Fever" = "High temperature" = "Elevated body temperature"
- Expand symptom vocabulary
- Increases feature coverage

### 3. **Synthetic Data Generation**
- Use existing patterns to generate new combinations
- Maintain medical validity
- Increase dataset size by 20-30%

### 4. **Web Scraping (Ethically)**
- Public health websites (with permission)
- Medical knowledge bases
- Always check terms of service

## 📊 Expected Combined Dataset Size

| Source | Records | Status |
|--------|---------|--------|
| Current dataset 2 final.xlsx | 1,848 (with symptoms) | ✅ Available |
| Disease Symptom Dataset (Kaggle) | ~5,000 | 📥 Download |
| Symptom2Disease | ~1,200 | 📥 Download |
| Medical Symptoms | ~3,000 | 📥 Download |
| **Total Expected** | **~11,000+** | 🎯 Target |

*This will significantly improve model accuracy*

## 🔄 Data Integration Plan

### Step 1: Download and Clean
```python
# datasets/download_datasets.py
# Download from Kaggle API or manual download
```

### Step 2: Normalize Format
```python
# data/scripts/normalize_datasets.py
# - Standardize symptom names
# - Map to common disease taxonomy
# - Remove duplicates
```

### Step 3: Merge and Enrich
```python
# data/scripts/merge_datasets.py
# - Combine all datasets
# - Link to DrugBank via drugbank-id
# - Add metadata
```

### Step 4: Validation
```python
# data/scripts/validate_data.py
# - Check data quality
# - Remove invalid entries
# - Generate statistics
```

## 📥 Download Instructions

### Option 1: Kaggle API (Recommended)
```bash
# Install Kaggle API
pip install kaggle

# Set up credentials (from Kaggle account)
# Place kaggle.json in ~/.kaggle/

# Download datasets
kaggle datasets download -d kaushil268/disease-symptom-description-dataset
kaggle datasets download -d niyarrbarman/symptom2disease
kaggle datasets download -d rabieelkharoua/medical-symptoms
```

### Option 2: Manual Download
1. Visit Kaggle datasets
2. Download as CSV
3. Place in `datasets/` folder

## 🎯 Data Quality Requirements

After merging, ensure:
- ✅ At least 10,000+ records
- ✅ 80%+ data completeness
- ✅ Symptom standardization (same symptom = same name)
- ✅ Disease standardization (same disease = same name)
- ✅ Linked to DrugBank (where possible)

## 📝 Data Processing Scripts Needed

1. `data/scripts/download_datasets.py` - Download from sources
2. `data/scripts/clean_symptoms.py` - Clean and normalize symptoms
3. `data/scripts/merge_datasets.py` - Combine all datasets
4. `data/scripts/validate_merged.py` - Quality checks
5. `data/scripts/enrich_with_drugbank.py` - Link to DrugBank

## ✅ Action Items

- [ ] Create Kaggle account (if needed)
- [ ] Download recommended datasets
- [ ] Create data processing scripts
- [ ] Merge and validate combined dataset
- [ ] Update training pipeline

## 🚀 Quick Start

```bash
# Create datasets folder
mkdir -p datasets/raw datasets/processed

# Download datasets (manual or via script)
# Then run processing scripts
python data/scripts/download_datasets.py
python data/scripts/merge_datasets.py
```

