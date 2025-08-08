# AI Playground Backend

A FastAPI-based backend service that provides multi-modal AI capabilities including conversation analysis, image analysis, and document summarization using Google's Gemini API.

## Features

- **JWT Authentication** - Secure user authentication and authorization
- **Conversation Analysis** - Audio file processing with speech-to-text and speaker diarization
- **Image Analysis** - AI-powered image description using Gemini Vision
- **Document Summarization** - PDF, DOC, and URL content summarization
- **CORS Support** - Configured for frontend integration

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Google Generative AI** - Gemini API for AI capabilities
- **JWT** - JSON Web Tokens for authentication
- **Python 3.11+** - Programming language
- **Uvicorn** - ASGI server for running the application

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Google AI Studio API key

## Installation & Setup

### 1. Clone the Repository

git clone https://github.com/Balaji-kurakula/AIPlaygroundHub_Backend.git
cd AIPlaygroundHub_Backend


### 2. Create Virtual Environment

Create virtual environment
python -m venv venv

Activate virtual environment
On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt


### 4. Environment Variables

Create a `.env` file in the root directory:

Required
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET=your_super_secret_jwt_key_make_it_long_and_random

Optional
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=8000
**Getting Gemini API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key
5. Copy the API key to your `.env` file

### 5. Project Structure

backend/
├── app/
│ ├── init.py
│ └── services/
│ ├── init.py
│ ├── auth.py # Authentication service
│ ├── conversation.py # Audio processing service
│ ├── image.py # Image analysis service
│ └── document.py # Document summarization service
├── main.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── .env # Environment variables (create this)
├── .gitignore
└── README.md


## Running the Application

### Local Development

Make sure virtual environment is activated
uvicorn main:app --reload

Or using Python
python main.py

text

The API will be available at: `http://localhost:8000`

### API Documentation

Once running, visit these URLs:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `POST /auth/refresh` - Refresh JWT token

### AI Features (Protected)
- `POST /conversation/analyze` - Audio analysis
- `POST /image/analyze` - Image analysis
- `POST /document/summarize` - Document/URL summarization

### Health Check
- `GET /health` - Application health status

## Authentication

### Demo Credentials
Username: demo
Password: demo123

text

### Usage Example
Login
curl -X POST http://localhost:8000/auth/login
-H "Content-Type: application/json"
-d '{"username": "demo", "password": "demo123"}'
Use the returned token for authenticated requests
curl -X GET http://localhost:8000/auth/me
-H "Authorization: Bearer YOUR_JWT_TOKEN"

text

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GEMINI_API_KEY` | Yes | Google AI Studio API key | `AIzaSyD...` |
| `JWT_SECRET` | Yes | Secret key for JWT tokens | `your-super-secret-key-256-bit` |
| `JWT_ALGORITHM` | No | JWT algorithm (default: HS256) | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token expiry time (default: 30) | `30` |
| `PORT` | No | Server port (default: 8000) | `8000` |

## Deployment

### Railway Deployment

1. **Push to GitHub** (Already done for this repo)

2. **Create Railway Project**
   - Visit [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Connect to `https://github.com/Balaji-kurakula/AIPlaygroundHub_Backend`

3. **Configure Environment Variables in Railway**
   Add these variables in Railway dashboard:
GEMINI_API_KEY=your_actual_gemini_api_key
JWT_SECRET=your_super_secret_jwt_key
PORT=8000

text

4. **Railway Configuration**
Railway auto-detects FastAPI. The configuration is:
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Build Command**: `pip install -r requirements.txt`

### Live Demo
- **API Documentation**: [Railway Deployment URL]/docs
- **Health Check**: [Railway Deployment URL]/health

## File Upload Specifications

| File Type | Max Size | Supported Formats |
|-----------|----------|-------------------|
| Audio | 25MB | MP3, WAV, M4A, OGG |
| Images | 10MB | JPEG, PNG, GIF, WebP |
| Documents | 15MB | PDF, DOC, DOCX |

## Security Considerations

- **JWT Secrets**: Use a strong, randomly generated secret key in production
- **API Keys**: Never commit API keys to version control
- **CORS**: Update CORS origins for production deployment
- **Rate Limiting**: Consider implementing rate limiting for production use

## Performance Notes

- **File Upload Limits**: Default FastAPI limit is 16MB
- **Timeout Settings**: API requests timeout after 30 seconds
- **Concurrent Requests**: FastAPI handles concurrent requests efficiently
- **Audio Processing**: Currently uses mock data - can be enhanced with real processing

## Testing

### Health Check
curl http://localhost:8000/health

text

### Login Test
curl -X POST http://localhost:8000/auth/login
-H "Content-Type: application/json"
-d '{"username": "demo", "password": "demo123"}'

text

### Image Analysis Test (with authentication)
First get token from login, then:
curl -X POST http://localhost:8000/image/analyze
-H "Authorization: Bearer YOUR_JWT_TOKEN"
-F "image=@path/to/your/image.jpg"

text

## Troubleshooting

### Common Issues

**1. Import Errors**
Ensure all files exist and have proper imports
ls -la app/services/

text

**2. API Key Issues**
Check if API key is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GEMINI_API_KEY', 'Not set')[:10])"

text

**3. CORS Errors**
- Update `allow_origins` in `main.py` with your frontend URL
- Restart the server after CORS changes

**4. Dependency Issues**
Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

text

**5. Railway Deployment Issues**
- Check Railway build logs for specific errors
- Ensure all environment variables are set correctly
- Verify requirements.txt includes all necessary dependencies

## Production Checklist

- [x] Environment variables set correctly
- [x] CORS origins updated for production domain
- [x] JWT secret is secure and unique
- [x] Error logging configured
- [x] Health check endpoint responds correctly
- [ ] API rate limiting implemented (optional)
- [ ] Database connection established (if needed)
- [ ] SSL/HTTPS configured (handled by Railway)

## Known Limitations

- **Audio Processing**: Currently shows mock data for conversation analysis
- **File Size**: Large files may cause timeout issues
- **Rate Limiting**: No built-in rate limiting (add if needed)
- **Database**: Uses in-memory user storage (suitable for demo)

## Future Enhancements

- [ ] Real-time audio processing with actual STT services
- [ ] Database integration for user management
- [ ] Rate limiting and request throttling
- [ ] Advanced error logging and monitoring
- [ ] Batch file processing capabilities
- [ ] WebSocket support for real-time features
- [ ] Multi-language support for AI responses

## API Response Examples

### Successful Login Response
{
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
"token_type": "bearer",
"user": {
"username": "demo",
"name": "Demo User"
}
}

text

### Image Analysis Response
{
"description": "This image shows a beautiful sunset over a mountain landscape. The sky is painted in vibrant shades of orange and pink, with silhouetted peaks in the foreground. The composition creates a serene and peaceful atmosphere."
}

text

### Document Summarization Response
{
"summary": "This document discusses the key principles of artificial intelligence and machine learning, covering topics such as neural networks, deep learning algorithms, and their practical applications in modern technology."
}

text

## Version History

- **v1.0.0** - Initial release with JWT auth, Gemini AI integration
- **v1.1.0** - Added document summarization
- **v1.2.0** - Enhanced error handling and CORS configuration
- **v1.3.0** - Railway deployment optimization and production ready

## Demo & Live Preview

- **GitHub Repository**: [https://github.com/Balaji-kurakula/AIPlaygroundHub_Backend](https://github.com/Balaji-kurakula/AIPlaygroundHub_Backend)
- **API Documentation**: [Deploy on Railway to get live URL]/docs
- **Demo Credentials**: 
  - Username: `demo`
  - Password: `demo123`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact & Support

- **Developer**: Balaji Kurakula
- **GitHub**: [@Balaji-kurakula](https://github.com/Balaji-kurakula)
- **Repository**: [AIPlaygroundHub_Backend](https://github.com/Balaji-kurakula/AIPlaygroundHub_Backend)
**Made with ❤️ by Balaji Kurakula**
