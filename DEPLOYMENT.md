# SkillSnap - Deployment Guide

## Production Deployment

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Setup

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd skillSnap
   python -m venv skillsnap_env
   source skillsnap_env/bin/activate  # On Windows: skillsnap_env\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements-production.txt
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Access Application**
   - Open browser to `http://localhost:5001`
   - Upload PDF resume or use sample data
   - Get job recommendations and skill gap analysis

### File Structure
```
skillSnap/
├── app.py                    # Main Flask application
├── routes.py                 # API endpoints
├── ml_utils.py              # Resume processing and job matching
├── sample_jobs.json         # Job descriptions database
├── requirements-production.txt  # Clean production dependencies
├── static/
│   ├── script.js           # Frontend JavaScript (cleaned)
│   └── style.css           # Styling
└── templates/
    └── index.html          # Main interface
```

### Features
- **PDF Resume Upload**: Extract text from PDF files
- **Job Matching**: Match resume against 5 job categories with percentage scores
- **Skill Gap Analysis**: Identify missing skills for specific job descriptions
- **Sample Data**: Test functionality without uploading files

### API Endpoints
- `GET /` - Main web interface
- `POST /api/upload_resume` - Upload and process PDF resume
- `POST /api/recommend_jobs` - Get job recommendations
- `POST /api/skill_gap` - Analyze skill gaps
- `GET /api/health` - Health check

### Production Notes
- Debug mode is disabled
- Error handling included
- CORS configured for web deployment
- File size limit: 16MB
- Clean console output

### Troubleshooting
- **Port 5001 in use**: Change port in `app.py` or stop existing process
- **Missing files**: Ensure `sample_jobs.json` exists
- **PDF errors**: Check file size (max 16MB) and format (PDF only) 