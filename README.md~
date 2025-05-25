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

- **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database:** PostgreSQL (Neon DB)
- **API Integration:** AniList GraphQL API
- **Authentication:** JWT Tokens
- **Frontend:** HTML, CSS, JavaScript (minimal UI)
- **Deployment:** Docker, Docker Compose

## Setup and Installation

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.9+ (for local development)
- Neon DB account (or any PostgreSQL database)
- Git

### Running the Application

#### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/anime-recommendation-system.git
cd anime-recommendation-system
```

2. Create a `.env` file with your Neon DB credentials:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-me
DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-endpoint/anime_recommendation
JWT_SECRET_KEY=your-jwt-secret-key-change-me
ANILIST_API_URL=https://graphql.anilist.co
```

3. Build and run with Docker Compose:
```bash
docker-compose up -d
```

4. Access the application at http://localhost:5000

#### Option 2: Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/anime-recommendation-system.git
cd anime-recommendation-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# On Linux/macOS
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-change-me
export DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-endpoint/anime_recommendation
export JWT_SECRET_KEY=your-jwt-secret-key-change-me
export ANILIST_API_URL=https://graphql.anilist.co

# On Windows
set FLASK_APP=run.py
set FLASK_ENV=development
set SECRET_KEY=your-secret-key-change-me
set DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-endpoint/anime_recommendation
set JWT_SECRET_KEY=your-jwt-secret-key-change-me
set ANILIST_API_URL=https://graphql.anilist.co
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
flask run
```

7. Access the application at http://localhost:5000

#### Option 3: Deploy with Docker to a Cloud Provider

##### Deploying to a VPS or Cloud VM

1. Build the Docker image:
```bash
docker build -t anime-recommendation-system .
```

2. Push to Docker Hub (optional):
```bash
docker tag anime-recommendation-system yourusername/anime-recommendation-system
docker push yourusername/anime-recommendation-system
```

3. On your server, run:
```bash
docker run -d -p 80:5000 \
 -e FLASK_APP=run.py \
 -e FLASK_ENV=production \
 -e SECRET_KEY=your-secret-key \
 -e DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-endpoint/anime_recommendation \
 -e JWT_SECRET_KEY=your-jwt-secret-key \
 -e ANILIST_API_URL=https://graphql.anilist.co \
 yourusername/anime-recommendation-system
```

### Setting Up Neon DB

1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project
3. Create a database named `anime_recommendation`
4. Copy your connection string from the dashboard (format: `postgresql://username:password@endpoint/dbname`)
5. Use this connection string in your `.env` file or environment variables

## API Documentation

### Authentication Endpoints

#### Register a New User

```
POST /auth/register
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "anime_fan",
  "email": "anime_fan@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/auth/register \
 -H "Content-Type: application/json" \
 -d '{"username":"anime_fan","email":"anime_fan@example.com","password":"securepassword123"}'
```

#### Login

```
POST /auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "anime_fan",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "anime_fan",
    "email": "anime_fan@example.com",
    "created_at": "2023-07-15T10:30:00"
  }
}
```

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/auth/login \
 -H "Content-Type: application/json" \
 -d '{"username":"anime_fan","password":"securepassword123"}'
```

#### Get User Profile

```
GET /auth/profile
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "anime_fan",
  "email": "anime_fan@example.com",
  "created_at": "2023-07-15T10:30:00"
}
```

**Example using cURL:**
```bash
curl -X GET http://localhost:5000/auth/profile \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Anime Endpoints

#### Search for Anime

```
GET /anime/search?query=<search_term>&genre=<genre>
```

**Query Parameters:**
- `query` (optional): Title to search for
- `genre` (optional): Genre to filter by

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 16498,
      "title": {
        "romaji": "Shingeki no Kyojin",
        "english": "Attack on Titan"
      },
      "genres": ["Action", "Drama", "Fantasy"],
      "description": "Several hundred years ago, humans were nearly exterminated by titans...",
      "coverImage": {
        "large": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx16498-C6FPmWm59CyP.jpg"
      },
      "popularity": 373179,
      "averageScore": 84
    }
  ]
}
```

**Example using cURL:**
```bash
curl -X GET "http://localhost:5000/anime/search?query=attack%20on%20titan"
```

#### Get Recommendations

```
GET /anime/recommendations
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "recommendations": [
    {
      "id": 101922,
      "title": {
        "romaji": "Kimetsu no Yaiba",
        "english": "Demon Slayer"
      },
      "genres": ["Action", "Fantasy"],
      "description": "It is the Taisho Period in Japan...",
      "coverImage": {
        "large": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx101922-PEn1CTc93blC.jpg"
      },
      "popularity": 310932,
      "averageScore": 85
    }
  ]
}
```

**Example using cURL:**
```bash
curl -X GET http://localhost:5000/anime/recommendations \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Add Anime to Watched List

```
POST /anime/watched
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "anime_id": 16498,
  "anime_title": "Attack on Titan",
  "rating": 9.5
}
```

**Response (201 Created):**
```json
{
  "message": "Anime added to watched list",
  "watched": {
    "id": 1,
    "anime_id": 16498,
    "anime_title": "Attack on Titan",
    "rating": 9.5,
    "watched_at": "2023-07-15T11:20:00"
  }
}
```

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/anime/watched \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
 -d '{"anime_id":16498,"anime_title":"Attack on Titan","rating":9.5}'
```

#### Get Watched Anime

```
GET /anime/watched
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "watched_anime": [
    {
      "id": 1,
      "anime_id": 16498,
      "anime_title": "Attack on Titan",
      "rating": 9.5,
      "watched_at": "2023-07-15T11:20:00"
    }
  ]
}
```

**Example using cURL:**
```bash
curl -X GET http://localhost:5000/anime/watched \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Remove Anime from Watched List

```
DELETE /anime/watched/<anime_id>
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Anime removed from watched list"
}
```

**Example using cURL:**
```bash
curl -X DELETE http://localhost:5000/anime/watched/16498 \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### User Preferences Endpoints

#### Get User Preferences

```
GET /user/preferences
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "preferences": [
    {
      "id": 1,
      "genre": "Action",
      "created_at": "2023-07-15T10:40:00"
    },
    {
      "id": 2,
      "genre": "Fantasy",
      "created_at": "2023-07-15T10:42:00"
    }
  ]
}
```

**Example using cURL:**
```bash
curl -X GET http://localhost:5000/user/preferences \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Add a Genre Preference

```
POST /user/preferences
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "genre": "Romance"
}
```

**Response (201 Created):**
```json
{
  "message": "Preference added successfully",
  "preference": {
    "id": 3,
    "genre": "Romance",
    "created_at": "2023-07-15T11:30:00"
  }
}
```

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/user/preferences \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
 -d '{"genre":"Romance"}'
```

#### Delete a Preference

```
DELETE /user/preferences/<pref_id>
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Preference deleted successfully"
}
```

**Example using cURL:**
```bash
curl -X DELETE http://localhost:5000/user/preferences/3 \
 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Database Schema

The application uses the following database models:

### User
Stores user authentication information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String(64) | Unique username |
| email | String(120) | Unique email address |
| password_hash | String(256) | Hashed password |
| created_at | DateTime | Account creation timestamp |

### UserPreference
Stores genre preferences for recommendations.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| genre | String(64) | Anime genre |
| created_at | DateTime | Preference creation timestamp |

### WatchedAnime
Tracks anime that users have watched.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| anime_id | Integer | AniList anime ID |
| anime_title | String(255) | Anime title |
| rating | Float | User's rating (1-10) |
| watched_at | DateTime | Timestamp when marked as watched |

### CachedAnime
Caches anime data from AniList API for improved performance.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| anilist_id | Integer | AniList anime ID |
| title | String(255) | Anime title |
| genres | String(255) | Comma-separated genres |
| description | Text | Anime description |
| image_url | String(255) | Cover image URL |
| popularity | Integer | Popularity score |
| average_score | Float | Average rating |
| cached_at | DateTime | Timestamp when cached |

## Frontend Usage

The application includes a simple frontend for interacting with the API:

- **Home:** Landing page with links to register or login
- **Register/Login:** Authentication forms
- **Search:** Search for anime by title or genre
- **Recommendations:** View personalized anime recommendations
- **Preferences:** Manage genre preferences
- **Watched Anime:** View and manage watched anime list

## Troubleshooting

### Database Connection Issues

If you're having trouble connecting to Neon DB:
- Verify your connection string is correct
- Ensure your IP address is allowed in Neon DB's security settings
- Check if your database user has appropriate permissions

### JWT Token Issues

If you're experiencing authentication problems:
- Make sure your JWT secret key is properly set
- Check that the token is being sent in the Authorization header
- Verify the token hasn't expired

### Docker Issues

If you're having Docker-related problems:
- Make sure Docker and Docker Compose are installed and up to date
- Check if ports are already in use with `netstat -tulpn | grep 5000`
- Examine container logs with `docker-compose logs -f`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.