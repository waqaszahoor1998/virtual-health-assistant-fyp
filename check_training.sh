#!/bin/bash
# Quick script to check CatBoost training status

cd /Users/m.w.zahoor/Desktop/rehan

echo "════════════════════════════════════════════════════════"
echo "  CatBoost Training Status Check"
echo "════════════════════════════════════════════════════════"
echo ""

# Check if process is running
if ps -p 1640 > /dev/null 2>&1; then
    echo "✅ Process Status: RUNNING"
    echo "   Process ID: 1640"
    TIME=$(ps -p 1640 -o etime= | xargs)
    echo "   Running Time: $TIME"
    echo ""
else
    echo "❌ Process Status: NOT RUNNING"
    echo ""
fi

# Check if model file exists
if [ -f "ml_models/models/catboost_model.pkl" ]; then
    echo "✅ Model File: SAVED (Training Complete!)"
    SIZE=$(ls -lh ml_models/models/catboost_model.pkl | awk '{print $5}')
    echo "   File Size: $SIZE"
    echo ""
else
    echo "⏳ Model File: NOT SAVED (Still Training)"
    echo ""
fi

# Check CatBoost training progress
if [ -f "ml_models/scripts/catboost_info/learn_error.tsv" ]; then
    echo "📊 Training Progress (Last 5 iterations):"
    echo "────────────────────────────────────────────────────"
    tail -5 ml_models/scripts/catboost_info/learn_error.tsv | column -t
    echo ""
    echo "   (Lower Logloss = Better)"
    echo ""
fi

# Summary
echo "════════════════════════════════════════════════════════"
if [ -f "ml_models/models/catboost_model.pkl" ]; then
    echo "✅ Training is COMPLETE!"
elif ps -p 1640 > /dev/null 2>&1; then
    echo "⏳ Training is IN PROGRESS"
    echo "   Check back in a few minutes"
else
    echo "❌ No training process found"
fi
echo "════════════════════════════════════════════════════════"

