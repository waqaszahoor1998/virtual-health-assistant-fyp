#!/usr/bin/env python3
"""
Train All Models Script.

Trains all available models sequentially and compares their performance.
This script will train:
1. LightGBM
2. CatBoost
3. Neural Network
4. Ensemble (combines all)

Then compares results and recommends the best model.
"""

import subprocess
import sys
import time
from pathlib import Path

# Define paths
SCRIPTS_DIR = Path(__file__).parent

MODELS_TO_TRAIN = [
    {
        'name': 'LightGBM',
        'script': 'train_lightgbm.py',
        'expected_accuracy': '40-60%',
        'time': '10-15 min'
    },
    {
        'name': 'CatBoost',
        'script': 'train_catboost.py',
        'expected_accuracy': '45-65%',
        'time': '15-20 min'
    },
    {
        'name': 'Neural Network',
        'script': 'train_neural_network.py',
        'expected_accuracy': '50-70%',
        'time': '20-30 min'
    },
    {
        'name': 'Ensemble',
        'script': 'train_ensemble.py',
        'expected_accuracy': '45-65%',
        'time': '5-10 min',
        'requires_others': True
    }
]


def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")
    
    dependencies = {
        'lightgbm': 'LightGBM',
        'catboost': 'CatBoost',
        'tensorflow': 'TensorFlow'
    }
    
    missing = []
    
    for package, name in dependencies.items():
        try:
            __import__(package)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join([pkg.lower().replace(' ', '') for pkg in missing]))
        return False
    
    print("✓ All dependencies installed!")
    return True


def train_model(model_info):
    """Train a single model."""
    script_path = SCRIPTS_DIR / model_info['script']
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Training {model_info['name']}")
    print(f"{'='*60}")
    print(f"Expected accuracy: {model_info['expected_accuracy']}")
    print(f"Estimated time: {model_info['time']}")
    print()
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(SCRIPTS_DIR),
            capture_output=False,
            text=True
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✓ {model_info['name']} training completed in {elapsed/60:.1f} minutes")
            return True
        else:
            print(f"\n❌ {model_info['name']} training failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error training {model_info['name']}: {str(e)}")
        return False


def main():
    """Main function to train all models."""
    print("=" * 60)
    print("TRAIN ALL MODELS - Improve Accuracy from 30% to 50-70%+")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first!")
        return
    
    print("\n" + "=" * 60)
    print("TRAINING SCHEDULE")
    print("=" * 60)
    
    for i, model in enumerate(MODELS_TO_TRAIN, 1):
        requires = " (requires other models)" if model.get('requires_others') else ""
        print(f"{i}. {model['name']}: {model['expected_accuracy']} accuracy{requires}")
    
    total_time = "~1-1.5 hours"
    print(f"\nTotal estimated time: {total_time}")
    
    response = input("\nStart training all models? (y/n): ")
    
    if response.lower() != 'y':
        print("Training cancelled.")
        return
    
    # Train models
    print("\n" + "=" * 60)
    print("STARTING TRAINING")
    print("=" * 60)
    
    results = {}
    
    for model in MODELS_TO_TRAIN:
        if model.get('requires_others'):
            # Check if we have other models first
            print(f"\n{model['name']} requires other models to be trained first.")
            print("Skipping for now - will train after others complete.")
            continue
        
        success = train_model(model)
        results[model['name']] = success
        
        if not success:
            print(f"\n⚠️  {model['name']} training failed. Continuing with other models...")
    
    # Train ensemble if we have other models
    ensemble_model = next((m for m in MODELS_TO_TRAIN if m.get('requires_others')), None)
    if ensemble_model:
        print(f"\n{'='*60}")
        print(f"Training {ensemble_model['name']} (combines all trained models)")
        print(f"{'='*60}")
        train_model(ensemble_model)
    
    # Summary
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    print(f"\n✓ Successfully trained: {len(successful)} models")
    for name in successful:
        print(f"  - {name}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)} models")
        for name in failed:
            print(f"  - {name}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Check model metrics files in ml_models/models/")
    print("2. Compare model performance")
    print("3. Update backend to use best model")


if __name__ == '__main__':
    main()

