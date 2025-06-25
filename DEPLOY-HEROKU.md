# 🚀 Deploy SkillSnap to Heroku for Interview Demo

## Prerequisites
- Git installed
- Heroku account (free): https://signup.heroku.com/
- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli

## Quick Deployment Steps

### 1. **Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 2. **Login to Heroku**
```bash
heroku login
```

### 3. **Initialize Git (if not already)**
```bash
git init
git add .
git commit -m "Initial commit - SkillSnap ready for deployment"
```

### 4. **Create Heroku App**
```bash
# Create app with unique name
heroku create skillsnap-demo-[your-name]
# Example: heroku create skillsnap-demo-john

# Or let Heroku generate a name
heroku create
```

### 5. **Deploy to Heroku**
```bash
git push heroku main
```

### 6. **Open Your App**
```bash
heroku open
```

## 🎯 **For Your Interview**

Your app will be available at:
```
https://your-app-name.herokuapp.com
```

### **Demo Script for Interviewer:**
1. **"Let me show you SkillSnap, a resume analysis tool I built"**
2. **Upload Resume**: "I can upload a PDF resume here"
3. **Job Matching**: "It analyzes the resume and matches it against different job types"
4. **Skill Gap**: "It also identifies missing skills for specific job descriptions"
5. **Technology**: "Built with Flask backend, JavaScript frontend, deployed on Heroku"

### **Key Points to Mention:**
- ✅ **Full-stack development** (Python Flask + JavaScript)
- ✅ **PDF processing** with text extraction
- ✅ **Keyword matching algorithms**
- ✅ **Responsive UI** with Bootstrap
- ✅ **API design** with REST endpoints
- ✅ **Cloud deployment** on Heroku
- ✅ **Error handling** and user experience

## 🔧 **Troubleshooting**

### If deployment fails:
```bash
# Check logs
heroku logs --tail

# Common fixes
heroku config:set PYTHON_VERSION=3.11.0
heroku restart
```

### If app crashes:
```bash
# Check what's running
heroku ps
# Restart
heroku restart
```

## 📱 **Test Your Deployment**
1. Visit your Heroku URL
2. Upload a test PDF resume
3. Try job recommendations
4. Test skill gap analysis
5. Verify everything works smoothly

**Your SkillSnap demo is ready for the interview! 🎉** 