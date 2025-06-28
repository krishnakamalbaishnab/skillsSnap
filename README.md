# 🎯 SkillSnap - AI-Powered Resume Analysis Platform

**A containerized web application that analyzes PDF resumes and provides intelligent job matching and skill gap analysis with advanced LLM capabilities.**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-Backend-green?logo=flask)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?logo=bootstrap)](https://getbootstrap.com/)
[![LLM](https://img.shields.io/badge/LLM-Enhanced-orange?logo=openai)](https://openai.com/)

## 🚀 Features

- **📄 PDF Resume Processing**: Extract and analyze text from PDF resumes
- **🎯 Intelligent Job Matching**: Match resumes against job descriptions with similarity scoring
- **📊 Skill Gap Analysis**: Identify missing skills for specific job requirements
- **🧠 LLM-Enhanced Analysis**: Advanced AI-powered job matching and skill analysis
- **✏️ Resume Improvement**: Get AI-powered suggestions to improve your resume
- **🌐 Modern Web Interface**: Responsive Bootstrap UI with drag-and-drop functionality
- **🐳 Containerized Deployment**: Docker-ready for consistent deployment anywhere
- **⚡ Real-time Processing**: Instant analysis and recommendations
- **🔄 Multi-LLM Support**: OpenAI GPT-4, Anthropic Claude, and Mistral AI

## 🛠️ Technology Stack

- **Backend**: Python Flask, PDF processing with pdfplumber
- **Frontend**: JavaScript, Bootstrap 5, Font Awesome icons
- **AI/ML**: OpenAI GPT-4, Anthropic Claude, Mistral AI
- **Deployment**: Docker, Docker Compose
- **Architecture**: RESTful API with JSON responses

## 🧠 LLM Features

### **Semantic Job Matching** (`/api/llm_job_match`)
- Contextual understanding of resume content
- Intelligent scoring and ranking of job matches
- Detailed analysis with strengths, concerns, and reasoning
- Support for multiple LLM providers

### **Advanced Skill Gap Analysis** (`/api/llm_skill_gap`)
- Comprehensive skill gap identification
- Actionable improvement suggestions
- Experience gap analysis
- Priority-based recommendations

### **Resume Improvement** (`/api/resume_improve`)
- Section-by-section analysis
- Keyword optimization suggestions
- Rewritten content examples
- Actionable improvement items

## 🐳 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- LLM API keys (optional for basic features)

### Run with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/krishnakamalbaishnab/skillsnap.git
cd skillsnap

# Copy environment template
cp env.example .env

# Edit .env file with your API keys (optional)
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# MISTRAL_API_KEY=your_mistral_api_key_here

# Build and run
docker-compose up --build

# Access the application
open http://localhost:5001
```

### Alternative: Docker Commands
```bash
# Build the image
docker build -t skillsnap .

# Run the container
docker run -d -p 5001:5001 --name skillsnap-app skillsnap

# Access the application
open http://localhost:5001
```

## 🔧 LLM Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai  # openai, anthropic, mistral

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Mistral Configuration
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-large-latest

# Flask Configuration
SECRET_KEY=your_secret_key_here_change_in_production
FLASK_ENV=development
```

### Supported LLM Providers

1. **OpenAI GPT-4** (Default)
   - Models: gpt-4, gpt-4-turbo, gpt-3.5-turbo
   - Best for: General analysis and reasoning

2. **Anthropic Claude**
   - Models: claude-3-sonnet-20240229, claude-3-haiku-20240307
   - Best for: Detailed analysis and writing

3. **Mistral AI**
   - Models: mistral-large-latest, mistral-medium-latest
   - Best for: Cost-effective analysis

## 🎯 How It Works

1. **Upload Resume**: Drag and drop a PDF resume or use the sample data
2. **Choose Analysis Type**: 
   - **Basic**: Simple keyword-based matching
   - **LLM Enhanced**: Advanced AI-powered analysis
3. **Get Recommendations**: AI analyzes your skills and matches against job categories
4. **Skill Gap Analysis**: Compare your resume against specific job descriptions
5. **Resume Improvement**: Get personalized suggestions to improve your resume
6. **View Results**: See detailed analysis with actionable insights

## 📂 Project Structure

```
skillsnap/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container orchestration
├── app.py                  # Flask application entry point
├── routes.py               # API route definitions
├── ml_utils.py             # Basic resume processing and matching logic
├── services/               # LLM services
│   ├── __init__.py
│   ├── llm_handler.py      # LLM provider management
│   └── llm_services.py     # LLM business logic
├── utils/                  # Utilities
│   ├── __init__.py
│   └── prompt_templates.py # LLM prompt templates
├── sample_jobs.json        # Job description database
├── requirements-production.txt # Python dependencies
├── static/
│   ├── script.js          # Frontend JavaScript
│   └── style.css          # Custom styling
├── templates/
│   └── index.html         # Main web interface
└── env.example            # Environment variables template
```

## 🔧 API Endpoints

### Basic Endpoints
- `GET /` - Main web interface
- `POST /api/upload_resume` - Upload and process PDF resume
- `POST /api/recommend_jobs` - Get basic job recommendations
- `POST /api/skill_gap` - Basic skill gap analysis
- `GET /api/health` - Health check endpoint

### LLM-Enhanced Endpoints
- `POST /api/llm_job_match` - LLM-powered semantic job matching
- `POST /api/llm_skill_gap` - Advanced LLM skill gap analysis
- `POST /api/resume_improve` - Resume improvement suggestions
- `GET /api/llm_status` - Check LLM service availability

## 📋 Job Categories

Currently matches against 5 professional categories:
- **Software Engineer** - Full-stack development roles
- **Data Scientist** - ML/AI and analytics positions  
- **DevOps Engineer** - Infrastructure and deployment roles
- **Frontend Developer** - UI/UX focused positions
- **Product Manager** - Strategy and product development roles

## 🔒 Security Features

- **Containerized Environment**: Isolated application runtime
- **Non-root User**: Container runs with restricted privileges
- **Input Validation**: PDF file type and size restrictions
- **Health Monitoring**: Built-in health checks and monitoring
- **Environment Variables**: Secure API key management
- **CORS Protection**: Configurable cross-origin resource sharing

## 🚀 Deployment Options

### Local Development
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-production.txt
python app.py
```

### Cloud Deployment
- **Heroku**: Ready for platform deployment
- **AWS/GCP/Azure**: Container-ready for cloud platforms
- **Docker Hub**: Shareable container images

### Environment Variables for Production
```bash
# Set these in your production environment
LLM_PROVIDER=openai
OPENAI_API_KEY=your_production_api_key
SECRET_KEY=your_production_secret_key
FLASK_ENV=production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@krishnakamalbaishnab](https://github.com/krishnakamalbaishnab)
- LinkedIn: [@krishnakamalbaishnab](https://linkedin.com/in/krishnakamalbaishnab)

---

**Built with ❤️ for better career matching and skill development**

## 🔄 Version History

### v2.0.0 (LLM Enhanced)
- ✨ Added LLM-powered job matching
- ✨ Advanced skill gap analysis with actionable suggestions
- ✨ Resume improvement recommendations
- ✨ Multi-LLM provider support (OpenAI, Claude, Mistral)
- ✨ Enhanced UI with LLM status indicators
- 🔧 Improved error handling and validation
- 📚 Comprehensive documentation updates

### v1.0.0 (Basic)
- 📄 PDF resume processing
- 🎯 Basic job matching
- 📊 Simple skill gap analysis
- 🌐 Modern web interface
- 🐳 Docker containerization 