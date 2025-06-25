# 🚀 Heroku Deployment Guide for SkillSnap

This guide will help you deploy SkillSnap to Heroku for production use.

## 📋 Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git Repository**: Your code should be pushed to GitHub
4. **Local Testing**: Ensure your app works locally with Docker

## 🛠️ Deployment Steps

### 1. Install Heroku CLI

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows/Linux:**
Download from [Heroku CLI page](https://devcenter.heroku.com/articles/heroku-cli)

### 2. Login to Heroku

```bash
heroku login
```

This will open a browser window for authentication.

### 3. Create Heroku Application

```bash
# Navigate to your project directory
cd skillsnap

# Create new Heroku app (replace 'your-app-name' with desired name)
heroku create your-skillsnap-app

# Or let Heroku generate a random name
heroku create
```

### 4. Configure Environment Variables

```bash
# Set a secure secret key for production
heroku config:set SECRET_KEY="your-super-secure-random-secret-key-here"

# Optional: Set any other environment variables
heroku config:set FLASK_ENV=production
```

### 5. Deploy to Heroku

```bash
# Add Heroku remote (if not done automatically)
heroku git:remote -a your-skillsnap-app

# Deploy to Heroku
git push heroku main
```

### 6. Scale the Application

```bash
# Ensure at least one web dyno is running
heroku ps:scale web=1
```

### 7. Open Your Application

```bash
# Open in browser
heroku open

# Or check the URL
heroku info
```

## 🔧 Configuration Files

Your repository should include these Heroku-specific files:

### `Procfile`
```
web: gunicorn app:app
```

### `requirements.txt`
```
Flask==2.3.3
flask-cors==4.0.0
pdfplumber==0.9.0
Werkzeug==2.3.7
gunicorn==21.2.0
```

### `runtime.txt` (Optional)
```
python-3.11.9
```

## 🔍 Monitoring and Logs

### View Application Logs
```bash
# Real-time logs
heroku logs --tail

# Recent logs
heroku logs

# Specific number of lines
heroku logs -n 200
```

### Check Application Status
```bash
# App info
heroku info

# Dyno status
heroku ps

# Config variables
heroku config
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Application Error (H10)
```bash
# Check logs for detailed error
heroku logs --tail

# Ensure Procfile is correct
cat Procfile

# Scale dynos
heroku ps:scale web=1
```

#### 2. Build Failures
```bash
# Check if all dependencies are in requirements.txt
pip freeze > requirements.txt

# Ensure Python version compatibility
echo "python-3.11.9" > runtime.txt
```

#### 3. File Upload Issues
- Heroku has ephemeral filesystem
- Uploaded files are temporary
- Consider cloud storage for persistent files

#### 4. Memory Issues
```bash
# Upgrade to higher tier if needed
heroku ps:resize web=standard-1x
```

### Environment-Specific Debugging

#### Check Python Version
```bash
heroku run python --version
```

#### Test Dependencies
```bash
heroku run pip list
```

#### Run Shell Commands
```bash
heroku run bash
```

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit secrets to Git
# Use Heroku config vars instead
heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
```

### 2. CORS Configuration
The app is configured for production domains. Update if needed:
```python
# In app.py, origins are dynamically handled
CORS(app, resources={
    r"/*": {
        "origins": ["*"],  # Configure as needed
        "methods": ["GET", "POST", "OPTIONS"]
    }
})
```

## 📊 Performance Optimization

### 1. Dyno Sleeping
Free dynos sleep after 30 minutes of inactivity:
```bash
# Upgrade to hobby tier to prevent sleeping
heroku ps:resize web=hobby
```

### 2. Static File Serving
Heroku serves static files automatically through Flask.

## 🔄 Continuous Deployment

### GitHub Integration
1. Go to Heroku Dashboard
2. Select your app
3. Go to Deploy tab
4. Connect to GitHub
5. Enable Automatic Deploys

### Manual Deployment
```bash
# Deploy latest changes
git add .
git commit -m "Update for production"
git push heroku main
```

## 📱 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app-name.herokuapp.com/api/health
```

### 2. Upload Test
```bash
# Test file upload endpoint
curl -X POST -F "file=@test_resume.pdf" \
  https://your-app-name.herokuapp.com/api/upload_resume
```

### 3. Full Application Test
1. Visit your Heroku app URL
2. Upload a PDF resume
3. Get job recommendations
4. Analyze skill gaps

## 💰 Cost Considerations

### Free Tier Limitations
- 550-1000 free dyno hours per month
- Apps sleep after 30 minutes of inactivity
- No custom domains on free tier

### Paid Tiers
- **Hobby ($7/month)**: No sleeping, custom domains
- **Standard ($25/month)**: Better performance, metrics
- **Performance**: High-performance dynos

## 🔧 Advanced Configuration

### Custom Domain
```bash
# Add custom domain (requires paid tier)
heroku domains:add yourdomain.com
```

### SSL Certificate
```bash
# Enable SSL (automatic on paid tiers)
heroku certs:auto:enable
```

### Database (if needed later)
```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev
```

## 📞 Support

- **Heroku Documentation**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Heroku Support**: Available for paid plans
- **Community**: [stackoverflow.com/questions/tagged/heroku](https://stackoverflow.com/questions/tagged/heroku)

---

## 🎯 Quick Deployment Checklist

- [ ] Heroku CLI installed and logged in
- [ ] `Procfile` with `web: gunicorn app:app`
- [ ] `requirements.txt` with all dependencies
- [ ] Environment variables configured
- [ ] Code pushed to GitHub
- [ ] Heroku app created
- [ ] Deployed with `git push heroku main`
- [ ] Scaled with `heroku ps:scale web=1`
- [ ] Tested application endpoints

**Your SkillSnap app is now live on Heroku! 🎉** 