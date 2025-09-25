# FastAPI LangGraph Backend

Production-ready backend API with FastAPI and LangGraph, featuring Google Gemini integration for streaming chat responses.

## Project Setup/Installation

1. **Clone and setup virtual environment**:
```bash
git clone <repo-url>
cd fastapi-langgraph
python -m venv venv
```

2. **Activate virtual environment**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Environment Variables Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
POSTGRES_URL=postgresql://postgres:password123@localhost:5432/fastapi_langgraph_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_langgraph_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123

# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Application Settings
APP_NAME=FastAPI LangGraph Backend
APP_VERSION=0.1.0
DEBUG=true

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Rate Limiting
RATE_LIMIT_REQUESTS=100

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## Database Setup

1. **Install PostgreSQL** (if not already installed)
2. **Create database**:
```sql
CREATE DATABASE fastapi_langgraph_db;
```
3. **Install Redis** (for rate limiting)
4. **Start services**:
```bash
# Start PostgreSQL service
# Start Redis service
```
5. **Database tables** are automatically created when the application starts

## How to Run the Application

**Development mode**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Access the application**:
- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/chat/health`

## API Endpoints Documentation

### 1. Stream Chat Response
**Endpoint**: `POST /api/v1/chat/stream`

**Description**: Send a message and receive streaming AI response from Google Gemini

**Request Body**:
```json
{
  "message": "What is the capital of France?",
  "session_id": "optional-session-id",
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": true
}
```

**Response**: Server-Sent Events (SSE) stream
```json
data: {"content": "The", "session_id": "abc123", "message_id": "msg456"}
data: {"content": " capital", "session_id": "abc123", "message_id": "msg456"}
data: {"content": " of France is Paris.", "session_id": "abc123", "message_id": "msg456"}
data: {"content": "", "is_complete": true, "session_id": "abc123", "message_id": "msg456"}
```

### 2. Health Check
**Endpoint**: `GET /api/v1/chat/health`

**Description**: Check API and database connectivity status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-25T10:30:00Z",
  "version": "0.1.0",
  "database": true,
  "redis": true
}
```

## Basic Usage Examples

### Using curl

**Send a chat message**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you today?",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Check health status**:
```bash
curl -X GET "http://localhost:8000/api/v1/chat/health"
```

### Using Python requests

```python
import requests
import json

# Stream chat response
response = requests.post(
    "http://localhost:8000/api/v1/chat/stream",
    json={
        "message": "Explain quantum computing in simple terms",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    stream=True
)

# Process streaming response
for line in response.iter_lines():
    if line.startswith(b'data: '):
        data = json.loads(line[6:])
        print(data['content'], end='')
```

### Using JavaScript (fetch)

```javascript
async function streamChat(message) {
  const response = await fetch('/api/v1/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      temperature: 0.7,
      max_tokens: 1000
    })
  });

  const reader = response.body.getReader();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = new TextDecoder().decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log(data.content);
      }
    }
  }
}
```