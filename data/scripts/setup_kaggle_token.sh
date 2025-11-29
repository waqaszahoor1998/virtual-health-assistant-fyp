#!/bin/bash
# Quick script to set up Kaggle API token as environment variable

export KAGGLE_KEY=KGAT_a89cf567db1ca4822286ffdd2ed6ba6f

echo "✓ Kaggle API token set as environment variable"
echo ""
echo "To use it, run:"
echo "  source data/scripts/setup_kaggle_token.sh"
echo ""
echo "Or for this session only:"
echo "  export KAGGLE_KEY=KGAT_a89cf567db1ca4822286ffdd2ed6ba6f"
echo ""
echo "Then run download script:"
echo "  python data/scripts/download_datasets_simple.py"

