# 🎬 Movie Recommender System

An AI-powered **Movie Recommender System** that suggests similar movies based on user input — built with **Python**, **Streamlit**, and **The Movie Database (TMDB) API**.

🔗 **Live Demo:** [https://movie-recommender-system-wvjp.onrender.com](https://movie-recommender-system-wvjp.onrender.com)

---

## 🚀 Features

- 🎥 Recommends top 5 similar movies to the selected title  
- 🖼️ Displays high-quality movie posters using TMDB API  
- ⚡ Fast performance with caching and optimized model loading  
- ☁️ Hosted on [Render](https://render.com)  
- 🧠 Machine learning similarity model (cosine similarity on movie features)

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| API | TMDB (The Movie Database) |
| Model | Pickle-based similarity matrix |
| Hosting | Render |
| Data Processing | Pandas, NumPy |

---

## 🧠 How It Works

1. The model reads movie metadata and calculates similarity between movies.  
2. When a user selects a movie, the system finds the 5 most similar movies using precomputed similarity scores.  
3. The TMDB API fetches movie posters dynamically for better user experience.

---

## 🗂️ Project Structure

