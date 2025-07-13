# Lesson Planner Bot API

An AI-powered lesson planning assistant that scrapes educational content from the web and creates comprehensive lesson plans.

## Features

- 🔍 **Web Scraping**: Automatically searches and extracts educational content from reliable sources
- 📚 **Lesson Planning**: Generates structured lesson plans with objectives, materials, exercises, and assessments
- 🤖 **AI-Powered**: Uses OpenAI's latest agents to create high-quality educational content
- 🚀 **FastAPI Backend**: Modern, fast, and well-documented REST API

## Setup

1. **Activate your virtual environment**:
   ```bash
   # On Windows
   backend\venv\Scripts\activate
   
   # On macOS/Linux
   source backend/venv/bin/activate
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the backend directory with:
   ```
   GOOGLE_SEARCH_API_KEY=your_google_search_api_key
   CSE_ID=your_custom_search_engine_id
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Server

### Option 1: Using the run script
```bash
python run_server.py
```

### Option 2: Direct execution
```bash
python main.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. GET `/`
- **Description**: Root endpoint with API information
- **Response**: API version and available endpoints

#### 2. GET `/health`
- **Description**: Health check endpoint
- **Response**: Server status

#### 3. POST `/create-lesson-plan`
- **Description**: Create a comprehensive lesson plan
- **Request Body**:
  ```json
  {
    "topic": "Simple Machines",
    "grade_level": "grade 6"  // Optional
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "lesson_plan": {
      "topic": "Simple Machines",
      "grade_level": "6th Grade",
      "duration_minutes": 45,
      "learning_objectives": [...],
      "materials_needed": [...],
      "lesson_overview": [...],
      "exercises": [...],
      "assessment": [...],
      "urls": [...]
    },
    "message": "Successfully created lesson plan for 'Simple Machines'"
  }
  ```

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Example Usage

### Using curl
```bash
curl -X POST "http://localhost:8000/create-lesson-plan" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "Photosynthesis",
       "grade_level": "grade 5"
     }'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8000/create-lesson-plan",
    json={
        "topic": "Photosynthesis",
        "grade_level": "grade 5"
    }
)

if response.status_code == 200:
    result = response.json()
    if result["success"]:
        lesson_plan = result["lesson_plan"]
        print(f"Created lesson plan for: {lesson_plan['topic']}")
        print(f"Duration: {lesson_plan['duration_minutes']} minutes")
        print(f"Grade Level: {lesson_plan['grade_level']}")
    else:
        print(f"Error: {result['error']}")
```

## How It Works

1. **Content Scraping**: The system searches Google for educational content about the topic
2. **Content Filtering**: Filters out non-educational sources and extracts readable content
3. **AI Processing**: Uses OpenAI agents to analyze the content and create a structured lesson plan
4. **Structured Output**: Returns a complete lesson plan with all necessary components

## Troubleshooting

- **Environment Variables**: Make sure all required API keys are set in your `.env` file
- **Virtual Environment**: Ensure you're using the correct virtual environment
- **Port Conflicts**: If port 8000 is busy, change it in the run command
- **API Limits**: Be aware of Google Search API and OpenAI API rate limits

## Dependencies

The main dependencies include:
- FastAPI (web framework)
- OpenAI Agents (AI processing)
- Newspaper3k (web scraping)
- BeautifulSoup (HTML parsing)
- Pydantic (data validation)
- Uvicorn (ASGI server) 