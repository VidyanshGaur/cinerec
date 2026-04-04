import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.content_based import train_cbf
from models.collaborative import train_cf
from models.hybrid import HybridRecommender
import joblib

if __name__ == '__main__':
    print("=== Training Content-Based Filter ===")
    train_cbf()

    print("\n=== Training Collaborative Filter ===")
    train_cf()

    print("\n=== Saving Hybrid Model ===")
    hybrid = HybridRecommender()
    model_path = os.path.join(os.path.dirname(__file__), 'hybrid_model.pkl')
    joblib.dump(hybrid, model_path)
    print("Hybrid model saved!")

    print("\n✅ All models trained successfully!")