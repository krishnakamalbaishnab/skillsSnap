# 🎯 SkillSnap - AI-Powered Resume Analysis Platform

**A containerized web application that analyzes PDF resumes and provides intelligent job matching and skill gap analysis.**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-Backend-green?logo=flask)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?logo=bootstrap)](https://getbootstrap.com/)

## 🚀 Features

- **📄 PDF Resume Processing**: Extract and analyze text from PDF resumes
- **🎯 Intelligent Job Matching**: Match resumes against job descriptions with similarity scoring
- **📊 Skill Gap Analysis**: Identify missing skills for specific job requirements
- **🌐 Modern Web Interface**: Responsive Bootstrap UI with drag-and-drop functionality
- **🐳 Containerized Deployment**: Docker-ready for consistent deployment anywhere
- **⚡ Real-time Processing**: Instant analysis and recommendations

## 🛠️ Technology Stack

- **Backend**: Python Flask, PDF processing with pdfplumber
- **Frontend**: JavaScript, Bootstrap 5, Font Awesome icons
- **Deployment**: Docker, Docker Compose
- **Architecture**: RESTful API with JSON responses

## 🐳 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### Run with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/skillsnap.git
cd skillsnap

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

## 🎯 How It Works

1. **Upload Resume**: Drag and drop a PDF resume or use the sample data
2. **Get Recommendations**: AI analyzes your skills and matches against job categories
3. **Skill Gap Analysis**: Compare your resume against specific job descriptions
4. **View Results**: See percentage matches, matched skills, and improvement suggestions

## 📂 Project Structure

```
skillsnap/
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container orchestration
├── app.py                  # Flask application entry point
├── routes.py               # API route definitions
├── ml_utils.py             # Resume processing and matching logic
├── sample_jobs.json        # Job description database
├── requirements-production.txt # Python dependencies
├── static/
│   ├── script.js          # Frontend JavaScript
│   └── style.css          # Custom styling
├── templates/
│   └── index.html         # Main web interface
└── docs/
    ├── DEPLOY-DOCKER.md   # Docker deployment guide
    └── DEPLOYMENT.md      # General deployment guide
```

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /api/upload_resume` - Upload and process PDF resume
- `POST /api/recommend_jobs` - Get job recommendations
- `POST /api/skill_gap` - Analyze skill gaps
- `GET /api/health` - Health check endpoint

## 🎬 Demo

![SkillSnap Demo](demo-screenshot.png)

*Upload your resume, get instant job matches, and identify skill gaps to improve your career prospects.*

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
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

**Built with ❤️ for better career matching and skill development** 