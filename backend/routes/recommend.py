from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from backend.models import db, Movie, Rating
import joblib
import os
import sys

BASE_DIR = '/Users/vidyansh/Desktop/recommendation-engine'
sys.path.insert(0, BASE_DIR)

recommend_bp = Blueprint('recommend', __name__)

def get_popular_movies(n=10):
    movies = Movie.query.order_by(Movie.avg_rating.desc(), Movie.rating_count.desc()).limit(n).all()
    return [{'id': m.id, 'title': m.title, 'genres': m.genres, 'avg_rating': round(m.avg_rating, 2)} for m in movies]

def get_hybrid_recommendations(user_id, all_movie_ids, rated_movie_ids, top_n=10):
    from models.collaborative import get_cf_recommendations
    from models.content_based import get_similar_movies

    cf_scores = {}
    cbf_scores = {}

    try:
        cf_recs = get_cf_recommendations(user_id, all_movie_ids, rated_movie_ids, top_n=30)
        for rank, mid in enumerate(cf_recs):
            cf_scores[mid] = 1 - (rank / max(len(cf_recs), 1))
    except Exception as e:
        print(f"CF error: {e}")

    try:
        for movie_id in rated_movie_ids[-3:]:
            cbf_recs = get_similar_movies(movie_id, top_n=20)
            for rank, mid in enumerate(cbf_recs):
                if mid not in rated_movie_ids:
                    cbf_scores[mid] = cbf_scores.get(mid, 0) + (1 - rank / max(len(cbf_recs), 1))
    except Exception as e:
        print(f"CBF error: {e}")

    all_ids = set(cf_scores) | set(cbf_scores)
    hybrid = {mid: 0.6 * cf_scores.get(mid, 0) + 0.4 * cbf_scores.get(mid, 0) for mid in all_ids}
    sorted_recs = sorted(hybrid.items(), key=lambda x: x[1], reverse=True)
    return [mid for mid, _ in sorted_recs[:top_n]]

@recommend_bp.route('/recommend')
@login_required
def recommend():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    print(f"User {current_user.id} has {len(user_ratings)} ratings")

    if len(user_ratings) < 5:
        movies = get_popular_movies(10)
        return render_template('recommend.html', movies=movies,
                               message="Rate more movies to get personalized recommendations!",
                               is_cold_start=True)

    try:
        rated_movie_ids = [r.movie_id for r in user_ratings]
        all_movie_ids = [m.id for m in Movie.query.all()]

        recommended_ids = get_hybrid_recommendations(
            user_id=current_user.id,
            all_movie_ids=all_movie_ids,
            rated_movie_ids=rated_movie_ids,
            top_n=10
        )
        print(f"Recommendations: {recommended_ids}")

        movies = []
        for mid in recommended_ids:
            m = Movie.query.get(mid)
            if m:
                movies.append({'id': m.id, 'title': m.title, 'genres': m.genres, 'avg_rating': round(m.avg_rating, 2)})

        return render_template('recommend.html', movies=movies, is_cold_start=False)

    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()
        movies = get_popular_movies(10)
        return render_template('recommend.html', movies=movies,
                               message="Showing top rated movies.", is_cold_start=True)

@recommend_bp.route('/api/recommend')
@login_required
def api_recommend():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    if len(user_ratings) < 5:
        return jsonify({'recommendations': get_popular_movies(10), 'type': 'popular'})
    return jsonify({'recommendations': get_popular_movies(10), 'type': 'popular'})