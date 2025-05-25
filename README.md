# Anime Recommendation System

A Flask-based RESTful API service that allows users to search for anime, get personalized recommendations, and manage their anime preferences. This project integrates with the AniList GraphQL API and uses Neon DB (PostgreSQL) for data persistence.

## Features

🔐 User authentication with JWT tokens  
🔍 Search anime by title or genre using AniList GraphQL API  
🎯 Get personalized anime recommendations based on user preferences  
📊 Manage favorite genres and track watched anime  
💾 PostgreSQL database integration with Neon DB  
🐳 Docker support for easy deployment  
🌐 Simple UI for interacting with the system  

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: PostgreSQL (Neon DB)
- **API Integration**: AniList GraphQL API
- **Authentication**: JWT Tokens
- **Frontend**: HTML, CSS, JavaScript (minimal UI)
- **Deployment**: Docker, Docker Compose

## Setup and Installation

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.9+ (for local development)
- Neon DB account (or any PostgreSQL database)
- Git

### Running the Application

#### Option 1: Using Docker (Recommended)

```bash
git clone https://github.com/yourusername/anime-recommendation-system.git
cd anime-recommendation-system

# Create .env file
echo "FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-me
DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-endpoint/anime_recommendation
JWT_SECRET_KEY=your-jwt-secret-key-change-me
ANILIST_API_URL=https://graphql.anilist.co" > .env

docker-compose up -d