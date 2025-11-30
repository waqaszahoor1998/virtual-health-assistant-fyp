# 📊 Comprehensive ML Models Report
## Virtual Health Assistant - Disease Prediction from Symptoms

**Generated**: $(date)  
**Project**: Virtual Health Assistant  
**Task**: Multi-label Disease Classification from Symptoms

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Dataset Overview](#dataset-overview)
3. [Data Preprocessing](#data-preprocessing)
4. [Model 1: XGBoost](#model-1-xgboost)
5. [Model 2: LightGBM](#model-2-lightgbm)
6. [Model 3: Random Forest](#model-3-random-forest)
7. [Model 4: Neural Network](#model-4-neural-network)
8. [Model Comparison](#model-comparison)
8. [Model Files & Storage](#model-files--storage)
9. [Training Details](#training-details)
10. [How Each Model Works](#how-each-model-works)

---

## 🎯 Executive Summary

This report documents all machine learning models trained for the Virtual Health Assistant project. The goal is to predict diseases from patient symptoms using a multi-label classification approach.

### Training Results Summary:

| Model | Accuracy | F1-Macro | F1-Micro | Training Time | Status |
|-------|----------|----------|----------|---------------|--------|
| **LightGBM** | **46.31%** 🥇 | 10.06% | 53.76% | ~45 min | ✅ **Best Accuracy** |
| **Neural Network** | 45.08% 🥈 | 4.75% | **59.41%** ⭐ | **47 seconds** ⚡ | ✅ **Best F1-Micro** |
| **XGBoost** | 30.33% | 4.08% | 41.17% | ~30 min | ✅ Trained |
| **Random Forest** | 8.61% | 0.69% | 15.82% | ~20 min | ✅ Baseline |

**Best Performing Models**:
- **Best Accuracy**: LightGBM (46.31%)
- **Best F1-Micro**: Neural Network (59.41%)
- **Fastest Training**: Neural Network (47 seconds!)

---

## 📊 Dataset Overview

### Training Data Statistics:

- **Total Training Samples**: 2,272 records
- **Validation Samples**: 487 records  
- **Test Samples**: 488 records
- **Total Dataset Size**: 3,247 records
- **Number of Features**: 5,000 (TF-IDF vectors from symptoms)
- **Number of Diseases**: 1,140 unique diseases

### Data Split:
- **Training Set**: 70% (2,272 samples)
- **Validation Set**: 15% (487 samples)
- **Test Set**: 15% (488 samples)

### Data Source:
- Original dataset: `dataset 2 final.xlsx` (3,963 records)
- Expanded dataset: `dataset_expanded_final.xlsx` (3,254 records after normalization)
- Data augmentation: Multiple Kaggle datasets merged and normalized

---

## 🔧 Data Preprocessing

### Step 1: Symptom Cleaning (`clean_symptoms.py`)
- Extracts symptoms from raw text
- Normalizes symptom names (lowercase, remove duplicates)
- Creates symptom-disease mappings

### Step 2: Feature Engineering (`feature_engineering.py`)

#### Input Features (Symptoms):
- Symptoms are converted to **TF-IDF vectors**
- **TF-IDF (Term Frequency-Inverse Document Frequency)**:
  - Converts text symptoms into numerical feature vectors
  - Captures importance of symptoms across all records
  - Creates 5,000-dimensional feature vectors

#### Output Labels (Diseases):
- Diseases are encoded using **MultiLabelBinarizer**
- Creates binary label matrix (1,140 diseases × samples)
- Each row indicates which diseases are present for that symptom set

#### Data Format:
```python
X_train: (2272, 5000)  # TF-IDF feature matrix
y_train: (2272, 1140)  # Binary disease labels
X_val:   (487, 5000)   # Validation features
y_val:   (487, 1140)   # Validation labels
X_test:  (488, 5000)   # Test features
y_test:  (488, 1140)   # Test labels
```

### Key Preprocessing Components:
- **TF-IDF Vectorizer**: Converts symptoms to numerical features
- **MultiLabelBinarizer**: Encodes multiple diseases per sample
- **Train/Val/Test Split**: 70%/15%/15% split with random_state=42

---

## 🤖 Model 1: XGBoost

### Overview:
XGBoost (Extreme Gradient Boosting) is a powerful gradient boosting framework that uses ensemble of decision trees with regularization.

### Model Architecture:
- **Type**: Multi-label Classifier using `MultiOutputClassifier`
- **Strategy**: One binary classifier per disease (1,140 classifiers)
- **Base Classifier**: XGBClassifier with binary logistic objective

### Hyperparameters:
```python
n_estimators: 100          # Number of boosting rounds
max_depth: 6               # Maximum tree depth
learning_rate: 0.1         # Step size shrinkage
subsample: 0.8             # Row subsampling ratio
colsample_bytree: 0.8      # Column subsampling ratio
min_child_weight: 3        # Minimum sum of instance weight
gamma: 0.1                 # Minimum loss reduction
reg_alpha: 0.1             # L1 regularization
reg_lambda: 1.0            # L2 regularization
base_score: 0.5            # Initial prediction score
objective: 'binary:logistic'  # Binary classification
eval_metric: 'logloss'     # Evaluation metric
tree_method: 'hist'        # Tree construction algorithm
n_jobs: -1                 # Use all CPU cores
```

### Training Details:
- **Training Time**: ~30 minutes
- **Parallelization**: Uses all available CPU cores
- **Prediction Strategy**: Top-k predictions (top 3 diseases with probability > 0.05)

### Performance Metrics:

| Metric | Score |
|--------|-------|
| **Accuracy** | **30.33%** |
| Precision (Macro) | 3.58% |
| Recall (Macro) | 5.28% |
| F1-Score (Macro) | 4.08% |
| Precision (Micro) | 37.05% |
| Recall (Micro) | 46.31% |
| F1-Score (Micro) | 41.17% |

### How It Works:

1. **Training Process**:
   - Trains 1,140 separate binary classifiers (one per disease)
   - Each classifier predicts: "Does this symptom set indicate Disease X?"
   - Uses gradient boosting: combines weak learners (shallow trees) into strong model
   - Sequential learning: each tree corrects errors of previous trees

2. **Prediction Process**:
   - Input: TF-IDF vector of symptoms (5,000 features)
   - Each of 1,140 classifiers outputs probability
   - Uses top-k strategy: selects top 3 diseases with probability > 0.05
   - Returns predicted diseases with confidence scores

3. **Strengths**:
   - Handles non-linear relationships well
   - Built-in regularization prevents overfitting
   - Fast training and prediction
   - Good for sparse multi-label data

4. **Weaknesses**:
   - Lower accuracy than LightGBM (30.33% vs 46.31%)
   - Requires careful hyperparameter tuning

### Model Files:
- **Model**: `xgboost_model.pkl` (81 MB)
- **Info**: `xgboost_model_info.json`
- **Metrics**: `xgboost_model_metrics.json`

---

## 🤖 Model 2: LightGBM ⭐ (Best Model)

### Overview:
LightGBM (Light Gradient Boosting Machine) is a gradient boosting framework optimized for speed and efficiency, using histogram-based algorithms.

### Model Architecture:
- **Type**: Multi-label Classifier using `MultiOutputClassifier`
- **Strategy**: One binary classifier per disease (1,140 classifiers)
- **Base Classifier**: LGBMClassifier with binary objective

### Hyperparameters:
```python
n_estimators: 200          # Number of boosting rounds
max_depth: 8               # Maximum tree depth
learning_rate: 0.05        # Step size shrinkage
num_leaves: 31             # Maximum tree leaves
subsample: 0.8             # Row subsampling ratio
colsample_bytree: 0.8      # Column subsampling ratio
min_child_samples: 20      # Minimum samples in leaf
reg_alpha: 0.1             # L1 regularization
reg_lambda: 1.0            # L2 regularization
objective: 'binary'        # Binary classification
n_jobs: -1                 # Use all CPU cores
```

### Training Details:
- **Training Time**: ~45 minutes
- **Parallelization**: Uses all available CPU cores
- **Prediction Strategy**: Top-k predictions (top 3 diseases with probability > 0.05)

### Performance Metrics:

| Metric | Score |
|--------|-------|
| **Accuracy** | **46.31%** ⭐ |
| Precision (Macro) | 9.71% |
| Recall (Macro) | 10.84% |
| F1-Score (Macro) | 10.06% |
| Precision (Micro) | 47.28% |
| Recall (Micro) | 62.30% |
| F1-Score (Micro) | **53.76%** ⭐ |

### How It Works:

1. **Training Process**:
   - Trains 1,140 separate binary classifiers (one per disease)
   - Uses **histogram-based algorithm**: groups data into bins for faster training
   - **Leaf-wise tree growth**: Grows trees vertically (best-first) instead of level-wise
   - This makes it faster and more memory-efficient than XGBoost

2. **Prediction Process**:
   - Input: TF-IDF vector of symptoms (5,000 features)
   - Each of 1,140 classifiers outputs probability
   - Uses top-k strategy: selects top 3 diseases with probability > 0.05
   - Returns predicted diseases with confidence scores

3. **Strengths**:
   - **Highest accuracy** (46.31%)
   - Fast training due to histogram-based approach
   - Low memory usage
   - Good F1-micro score (53.76%)
   - Handles large feature spaces well

4. **Why It Performs Best**:
   - Histogram-based algorithm captures feature interactions better
   - Leaf-wise growth allows deeper trees with fewer splits
   - Better handling of sparse multi-label data

### Model Files:
- **Model**: `lightgbm_model.pkl` (193 MB)
- **Info**: `lightgbm_model_info.json`
- **Metrics**: `lightgbm_model_metrics.json`

---

## 🤖 Model 3: Random Forest

### Overview:
Random Forest is an ensemble method that combines multiple decision trees using bagging (bootstrap aggregating).

### Model Architecture:
- **Type**: Multi-label Classifier
- **Strategy**: Direct multi-label classification
- **Base Classifier**: RandomForestClassifier

### Hyperparameters:
```python
n_estimators: 200          # Number of trees in forest
max_depth: 15              # Maximum tree depth
min_samples_split: 5       # Minimum samples to split node
min_samples_leaf: 2        # Minimum samples in leaf
max_features: 'sqrt'       # Features to consider for split
bootstrap: True            # Bootstrap sampling
random_state: 42           # Random seed
n_jobs: -1                 # Use all CPU cores
```

### Training Details:
- **Training Time**: ~20 minutes
- **Parallelization**: Uses all available CPU cores
- **Prediction Strategy**: Standard threshold-based predictions

### Performance Metrics:

| Metric | Score |
|--------|-------|
| **Accuracy** | 8.61% |
| Precision (Macro) | 0.85% |
| Recall (Macro) | 0.62% |
| F1-Score (Macro) | 0.69% |
| Precision (Micro) | 97.67% |
| Recall (Micro) | 8.61% |
| F1-Score (Micro) | 15.82% |

### How It Works:

1. **Training Process**:
   - Creates 200 decision trees
   - Each tree trained on random subset of data (bootstrap sampling)
   - Each split considers random subset of features (`sqrt(n_features)`)
   - Trees vote on predictions, majority wins

2. **Prediction Process**:
   - Input: TF-IDF vector of symptoms (5,000 features)
   - Each tree makes prediction
   - Aggregates predictions from all 200 trees
   - Returns predicted diseases

3. **Strengths**:
   - Simple and interpretable
   - Fast training
   - Handles missing values well
   - Good baseline model

4. **Weaknesses**:
   - **Lowest accuracy** (8.61%)
   - Poor performance on sparse multi-label data
   - Not well-suited for high-dimensional feature spaces
   - High precision but very low recall (predicts very conservatively)

### Model Files:
- **Model**: `random_forest_model.pkl` (350 MB)
- **Info**: `random_forest_model_info.json`
- **Metrics**: `random_forest_model_metrics.json`

---

## 🤖 Model 4: Neural Network

### Overview:
Neural Network (Deep Learning) using Multi-Layer Perceptron (MLP) architecture. Uses deep learning to capture complex non-linear relationships between symptoms and diseases.

### Model Architecture:
- **Type**: Multi-label Classifier (Sequential Neural Network)
- **Architecture**: Deep Multi-Layer Perceptron
- **Strategy**: Single neural network with multiple output neurons (one per disease)

### Network Structure:
```python
Input Layer:     5,000 features (TF-IDF vectors)
Hidden Layer 1:  512 neurons (ReLU + BatchNorm + Dropout 0.3)
Hidden Layer 2:  256 neurons (ReLU + BatchNorm + Dropout 0.3)
Hidden Layer 3:  128 neurons (ReLU + BatchNorm + Dropout 0.2)
Hidden Layer 4:  64 neurons (ReLU + Dropout 0.2)
Output Layer:    1,140 neurons (Sigmoid activation for multi-label)
```

### Hyperparameters:
```python
optimizer: 'Adam'
learning_rate: 0.001
loss: 'binary_crossentropy'
activation: 'sigmoid' (multi-label classification)
batch_size: 32
epochs: 100 (with early stopping)
patience: 10 epochs
total_parameters: 2,810,676
```

### Training Details:
- **Training Time**: **47.63 seconds** ⚡ (Fastest!)
- **Epochs Trained**: 61 (early stopping at epoch 51)
- **Hardware**: Optimized for M2 MacBook Air (8 CPU cores + Metal GPU)
- **Prediction Strategy**: Top-k predictions (top 3 diseases with probability > 0.05)

### Performance Metrics:

| Metric | Score |
|--------|-------|
| **Accuracy** | 45.08% |
| Precision (Macro) | 4.83% |
| Recall (Macro) | 4.82% |
| F1-Score (Macro) | 4.75% |
| **Precision (Micro)** | **86.33%** ⭐ |
| Recall (Micro) | 45.29% |
| **F1-Score (Micro)** | **59.41%** ⭐ |

### How It Works:

1. **Training Process**:
   - Forward pass: Data flows through layers, weights multiply inputs
   - Backpropagation: Errors propagate backwards, weights are updated
   - Gradient descent: Adam optimizer adjusts learning rate adaptively
   - Regularization: Dropout and BatchNorm prevent overfitting
   - Early stopping: Stops training when validation loss stops improving

2. **Prediction Process**:
   - Input: TF-IDF vector of symptoms (5,000 features)
   - Forward pass through all layers
   - Output layer produces probabilities for all 1,140 diseases
   - Uses top-k strategy: selects top 3 diseases with probability > 0.05
   - Returns predicted diseases with confidence scores

3. **Strengths**:
   - **Fastest training** (47 seconds!)
   - **Best F1-Micro score** (59.41%)
   - **Excellent precision** (86.33%)
   - Captures complex non-linear relationships
   - Can learn intricate patterns in data
   - Good balance between precision and recall

4. **Why It Performs Well**:
   - Deep architecture learns hierarchical symptom-disease relationships
   - Batch normalization stabilizes training
   - Dropout prevents overfitting
   - Sigmoid activation perfect for multi-label classification
   - Early stopping finds optimal training point

5. **Weaknesses**:
   - Slightly lower accuracy than LightGBM (45.08% vs 46.31%)
   - Lower recall than LightGBM (45.29% vs 62.30%)
   - Requires more memory than tree-based models

### Model Files:
- **Model**: `neural_network_model.h5` (32 MB)
- **Info**: `neural_network_model_info.json`
- **Metrics**: `neural_network_model_metrics.json`
- **Training History**: `neural_network_training_history.json`

---

## 📊 Model Comparison

### Performance Ranking:

1. **🥇 LightGBM**: 46.31% accuracy ⭐ **Best Accuracy**
2. **🥈 Neural Network**: 45.08% accuracy, **Best F1-Micro (59.41%)**, **Fastest Training (47 sec)** ⚡
3. **🥉 XGBoost**: 30.33% accuracy
4. **4️⃣ Random Forest**: 8.61% accuracy (Baseline)

### Detailed Comparison:

| Metric | LightGBM | Neural Network | XGBoost | Random Forest |
|--------|----------|----------------|---------|---------------|
| **Accuracy** | **46.31%** 🥇 | 45.08% 🥈 | 30.33% | 8.61% |
| **F1-Micro** | 53.76% | **59.41%** ⭐ | 41.17% | 15.82% |
| **F1-Macro** | **10.06%** | 4.75% | 4.08% | 0.69% |
| **Precision (Micro)** | 47.28% | **86.33%** ⭐ | 37.05% | 97.67% |
| **Recall (Micro)** | **62.30%** | 45.29% | 46.31% | 8.61% |
| **Training Time** | ~45 min | **47 seconds** ⚡ | ~30 min | ~20 min |
| **Model Size** | 193 MB | **32 MB** | 81 MB | 350 MB |

### Key Insights:

1. **LightGBM wins on accuracy**:
   - Best accuracy (46.31%)
   - Best recall (62.30%)
   - Good overall balance

2. **Neural Network wins on precision and speed**:
   - Best F1-Micro score (59.41%)
   - Excellent precision (86.33%)
   - Fastest training (47 seconds!)
   - Very close accuracy (45.08%)

3. **XGBoost performs well**:
   - Good accuracy (30.33%)
   - Faster training than LightGBM
   - Could benefit from more hyperparameter tuning

4. **Random Forest struggles**:
   - Very conservative predictions (high precision, low recall)
   - Not suitable for sparse multi-label classification
   - Better as baseline/reference

### Recommendation:
- **For Production**: Use **LightGBM** for best accuracy, or **Neural Network** for precision and fast retraining
- **For Best Overall**: Train an **Ensemble** combining LightGBM + Neural Network

---

## 💾 Model Files & Storage

### Preprocessing Files:
- `symptom_vectorizer.pkl` (195 KB) - TF-IDF vectorizer
- `disease_encoder.pkl` (39 KB) - MultiLabelBinarizer
- `X_train.pkl` (1.6 MB) - Training features
- `X_val.pkl` (351 KB) - Validation features
- `X_test.pkl` (338 KB) - Test features
- `y_train.pkl` (20 MB) - Training labels
- `y_val.pkl` (4.2 MB) - Validation labels
- `y_test.pkl` (4.2 MB) - Test labels
- `metadata.json` - Dataset metadata

### Trained Models:
- `xgboost_model.pkl` (81 MB) ⭐ Currently used in backend
- `lightgbm_model.pkl` (193 MB) ⭐ **Best accuracy** (46.31%)
- `neural_network_model.h5` (32 MB) ⭐ **Best F1-Micro** (59.41%), fastest training (47 sec)
- `random_forest_model.pkl` (350 MB) - Baseline reference

### Model Information Files:
- `*_model_info.json` - Model architecture and parameters
- `*_model_metrics.json` - Performance metrics

### Storage Location:
```
ml_models/models/
├── *.pkl              # Models and preprocessed data
├── *.json             # Model info and metrics
└── unique_diseases.txt # List of all diseases
```

---

## 🔬 Training Details

### Common Training Configuration:
- **Random Seed**: 42 (for reproducibility)
- **CPU Usage**: All available cores (`n_jobs=-1`)
- **Cross-Platform**: Auto-detects CPU cores on any system
- **Data Split**: 70% train / 15% validation / 15% test

### Training Environment:
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Hardware Optimization**: Auto-detects and uses all CPU cores
- **GPU Support**: TensorFlow automatically uses GPU if available (Metal/CUDA)

### Prediction Strategy:
- **Top-k Approach**: Predicts top 3 diseases with probability > 0.05
- **Fallback**: If no predictions above threshold, predicts top-1 disease
- **Multi-label**: Can predict multiple diseases per symptom set

---

## 🧠 How Each Model Works (Detailed)

### XGBoost - Gradient Boosting:

1. **Initialization**: Starts with simple predictions (base_score=0.5)
2. **Boosting Rounds**: For each of 100 rounds:
   - Builds a decision tree
   - Finds splits that reduce prediction error
   - Adds tree to ensemble with learning_rate weighting
3. **Regularization**: L1 and L2 penalties prevent overfitting
4. **Final Prediction**: Sum of all tree predictions

**Example**:
- Tree 1 predicts: Disease A (0.3), Disease B (0.1)
- Tree 2 predicts: Disease A (0.2), Disease C (0.4)
- Tree 3 predicts: Disease A (0.1), Disease B (0.2)
- **Final**: Disease A (0.6), Disease B (0.3), Disease C (0.4)

### LightGBM - Histogram-Based Gradient Boosting:

1. **Histogram Creation**: Groups continuous features into bins
2. **Leaf-wise Growth**: Grows trees by finding best leaf to split
3. **Gradient-based One-Side Sampling**: Focuses on samples with large gradients
4. **Exclusive Feature Bundling**: Reduces feature space

**Why It's Faster**:
- Histogram algorithm reduces computation from O(data × features) to O(data × bins)
- Leaf-wise growth allows deeper trees with same memory
- Handles large feature spaces (5,000 features) efficiently

### Random Forest - Bagging Ensemble:

1. **Bootstrap Sampling**: Creates 200 random subsets of training data
2. **Tree Building**: Each tree built on different subset
3. **Random Feature Selection**: Each split considers sqrt(5000) ≈ 71 random features
4. **Voting**: All 200 trees vote, majority wins

**Why It Struggles**:
- Sparse multi-label data (many diseases, few positive examples)
- High-dimensional features (5,000 dimensions)
- Needs more data or simpler feature space

---

## 🎯 Recommendations

### Current Best Model: **LightGBM**
- **Accuracy**: 46.31%
- **Status**: Ready for production use
- **File**: `lightgbm_model.pkl`

### Next Steps:
1. ✅ **Use LightGBM in backend** (currently XGBoost is used)
2. ⏳ Train Neural Network model (expected 50-70% accuracy)
3. ⏳ Train Ensemble model (combines best models)
4. ⏳ Fine-tune hyperparameters for better accuracy

### Production Deployment:
- Switch backend from XGBoost to LightGBM for better accuracy
- Monitor model performance in production
- Collect feedback for future improvements

---

## 📝 Notes

- All models use **multi-label classification** (can predict multiple diseases)
- **Top-k prediction strategy** ensures at least one disease is always predicted
- Models are **cross-platform compatible** (Windows, macOS, Linux)
- Training is **reproducible** (random_state=42)
- Models are stored using `joblib` for fast loading/saving

---

**Report Generated**: $(date)  
**Status**: ✅ All trained models documented  
**Best Model**: LightGBM (46.31% accuracy)

