import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.collaborative import get_cf_recommendations
from models.content_based import get_similar_movies

class HybridRecommender:
    def recommend(self, user_id, all_movie_ids, rated_movie_ids, top_n=10):
        if len(rated_movie_ids) < 5:
            return []

        cf_scores = {}
        cbf_scores = {}

        # CF recommendations
        try:
            cf_recs = get_cf_recommendations(user_id, all_movie_ids, rated_movie_ids, top_n=30)
            for rank, mid in enumerate(cf_recs):
                cf_scores[mid] = 1 - (rank / max(len(cf_recs), 1))
        except Exception as e:
            print(f"CF error: {e}")

        # CBF from last 3 rated movies
        try:
            for movie_id in rated_movie_ids[-3:]:
                cbf_recs = get_similar_movies(movie_id, top_n=20)
                for rank, mid in enumerate(cbf_recs):
                    if mid not in rated_movie_ids:
                        cbf_scores[mid] = cbf_scores.get(mid, 0) + (1 - rank / max(len(cbf_recs), 1))
        except Exception as e:
            print(f"CBF error: {e}")

        # Weighted merge — 60% CF, 40% CBF
        all_ids = set(cf_scores) | set(cbf_scores)
        hybrid = {}
        for mid in all_ids:
            hybrid[mid] = 0.6 * cf_scores.get(mid, 0) + 0.4 * cbf_scores.get(mid, 0)

        sorted_recs = sorted(hybrid.items(), key=lambda x: x[1], reverse=True)
        return [mid for mid, _ in sorted_recs[:top_n]]

if __name__ == '__main__':
    rec = HybridRecommender()
    print("Hybrid recommender ready")