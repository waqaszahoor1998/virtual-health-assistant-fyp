# Dataset Download - Quick Reference

## ⚡ Fastest Way to Download

### If You Have Kaggle Account:

1. **Get API token**: https://www.kaggle.com/settings → Create API Token
2. **Save to**: `~/.kaggle/kaggle.json` (macOS/Linux) or `%USERPROFILE%\.kaggle\kaggle.json` (Windows)
3. **Set permissions**: `chmod 600 ~/.kaggle/kaggle.json` (macOS/Linux only)
4. **Run**: `python data/scripts/download_datasets_simple.py`

### If You Don't Have Kaggle Account:

1. **Create free account**: https://www.kaggle.com/
2. Then follow steps above

### If API Doesn't Work:

1. Download manually from Kaggle
2. Save to `datasets/raw/{dataset_name}/`
3. Run normalization script

---

## 📋 Available Scripts

| Script | Purpose | Requirements |
|--------|---------|--------------|
| `download_datasets_simple.py` | Simple download with auto-check | Kaggle credentials |
| `download_kaggle_datasets.py` | Full-featured download | Kaggle credentials |
| `setup_kaggle.py` | Help set up credentials | Interactive |
| `normalize_datasets.py` | Normalize downloaded datasets | Datasets in `datasets/raw/` |
| `merge_datasets.py` | Merge all datasets | Normalized datasets |

---

## 🔗 Direct Links

1. https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
2. https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
3. https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
4. https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms

---

**See `QUICK_DOWNLOAD_GUIDE.md` for detailed instructions.**

