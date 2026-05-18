# 🎬 CineRec — Personalized Movie Recommendation Engine

A movie recommendation web application built using Python and Flask that provides personalized movie suggestions using machine learning techniques.

The system combines Content-Based Filtering and Collaborative Filtering to generate hybrid recommendations based on user preferences and ratings.

---

## Features

- User registration and login system
- Secure password hashing with bcrypt
- Browse and search through 1,682 movies
- Rate movies on a 1–5 star scale
- Content-Based Filtering using genre similarity
- Collaborative Filtering using SVD
- Hybrid recommendation engine
- Cold-start support for new users
- Automated testing with pytest

---

## Recommendation Flow

```text
User Ratings
     ↓
Collaborative Filtering (SVD)
     +
Content-Based Filtering (TF-IDF)
     ↓
Hybrid Recommendation Engine
     ↓
Top Personalized Movie Suggestions
```

---

## Model & Dataset Information

| Metric | Value |
|---|---|
| Dataset | MovieLens 100K |
| Total Ratings | 100,000 |
| Unique Users | 943 |
| Unique Movies | 1,682 |
| SVD RMSE | 0.9352 |
| Dataset Sparsity | 93.7% |

---

## Tech Stack

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite

### Machine Learning
- scikit-learn
- scikit-surprise
- pandas
- numpy

### Frontend
- HTML5
- CSS3
- Bootstrap 5

### Authentication & Testing
- Flask-Login
- bcrypt
- pytest

---

## Project Structure

```bash
recommendation-engine/
│
├── backend/
├── data/
├── frontend/
├── instance/
├── models/
├── tests/
├── README.md
└── requirements.txt
```

---

## Setup

### Clone Repository

```bash
git clone https://github.com/VidyanshGaur/recommendation-engine.git
cd recommendation-engine
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Load Dataset

```bash
cd backend
python load_data.py
```

### Train Models

```bash
cd ..
python models/train.py
```

### Run Application

```bash
cd backend
python app.py
```

Open in browser:

```bash
http://127.0.0.1:5000
```

---

## Testing

```bash
pytest tests/ -v
```

10/10 test cases passing.

---

## Future Improvements

- Deep learning based recommendation models
- Real-time recommendation updates
- REST API integration
- Docker support
- Cloud deployment

---

## Author

**Vidyansh Gaur**  
B.Tech CSE (AI/ML)  
The NorthCap University, Gurgaon
