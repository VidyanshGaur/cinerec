import pytest
import sys
sys.path.insert(0, '/Users/vidyansh/Desktop/recommendation-engine')

from backend.app import create_app
from backend.models import db, User, Movie, Rating
import bcrypt

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

        # Add test user
        password_hash = bcrypt.hashpw('password123'.encode(), bcrypt.gensalt()).decode()
        user = User(name='Test', email='test@test.com', password_hash=password_hash)
        db.session.add(user)

        # Add test movie
        movie = Movie(id=1, title='Test Movie', genres='Action', avg_rating=4.0, rating_count=10)
        db.session.add(movie)
        db.session.commit()

        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_in_client(client):
    client.post('/login', data={'email': 'test@test.com', 'password': 'password123'})
    return client

# TC-06: Browse movies
def test_browse_movies(logged_in_client):
    response = logged_in_client.get('/browse')
    assert response.status_code == 200
    assert b'Test Movie' in response.data

# TC-07: Movie detail page
def test_movie_detail(logged_in_client):
    response = logged_in_client.get('/movie/1')
    assert response.status_code == 200
    assert b'Test Movie' in response.data

# TC-08: Rate a movie
def test_rate_movie(logged_in_client):
    response = logged_in_client.post('/rate', data={
        'movie_id': 1,
        'score': 4
    })
    assert response.status_code == 200
    import json
    data = json.loads(response.data)
    assert data['success'] == True

# TC-09: Invalid rating score
def test_rate_movie_invalid_score(logged_in_client):
    response = logged_in_client.post('/rate', data={
        'movie_id': 1,
        'score': 10
    })
    assert response.status_code == 400

# TC-10: Unauthenticated rate attempt
def test_rate_requires_login(client):
    response = client.post('/rate', data={
        'movie_id': 1,
        'score': 4
    }, follow_redirects=False)
    assert response.status_code == 302