# 🐳 Docker Deployment Guide for SkillSnap

## Prerequisites
- Docker installed: https://docs.docker.com/get-docker/
- Docker Compose installed (usually comes with Docker Desktop)

## 🚀 Quick Start

### **Option 1: Docker Compose (Recommended)**
```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### **Option 2: Docker Commands**
```bash
# Build the image
docker build -t skillsnap .

# Run the container
docker run -p 5001:5001 --name skillsnap-app skillsnap

# Run in background
docker run -d -p 5001:5001 --name skillsnap-app skillsnap

# Stop and remove
docker stop skillsnap-app
docker rm skillsnap-app
```

## 🌐 **Access Your App**
- **Local**: http://localhost:5001
- **Network**: http://[your-ip]:5001

## 🎯 **For Interview Demo**

### **Deployment Options:**

#### **1. Local Demo**
```bash
docker-compose up --build
```
Then show at `http://localhost:5001`

#### **2. Cloud Deployment**

##### **Digital Ocean / AWS / GCP:**
```bash
# Push to registry
docker tag skillsnap your-registry/skillsnap:latest
docker push your-registry/skillsnap:latest

# Deploy on cloud instance
docker pull your-registry/skillsnap:latest
docker run -d -p 80:5001 --name skillsnap your-registry/skillsnap:latest
```

##### **Docker Hub (Free):**
```bash
# Tag and push
docker tag skillsnap your-dockerhub-username/skillsnap:latest
docker push your-dockerhub-username/skillsnap:latest

# Deploy anywhere
docker run -d -p 5001:5001 your-dockerhub-username/skillsnap:latest
```

## 🎬 **Interview Demo Script**

### **Technical Highlights to Mention:**

1. **"I've containerized the application with Docker"**
   - Show Dockerfile with multi-stage optimization
   - Explain security (non-root user)
   - Health checks included

2. **"Using Docker Compose for orchestration"**
   - Easy deployment and scaling
   - Environment management
   - Network isolation

3. **"Production-ready features"**
   - Optimized Python slim image
   - Layer caching for faster builds
   - .dockerignore for smaller images
   - Health monitoring

### **Demo Flow:**
1. **Show Dockerfile**: "Here's how I containerized the app"
2. **Build & Run**: `docker-compose up --build`
3. **Show App**: Demonstrate all features
4. **Show Logs**: `docker-compose logs`
5. **Show Scaling**: "Could easily scale with multiple containers"

## 🔧 **Development Commands**

```bash
# Rebuild after changes
docker-compose up --build

# Shell into container
docker-compose exec skillsnap bash

# View logs
docker-compose logs -f skillsnap

# Clean up
docker-compose down --volumes --rmi all
```

## 📊 **Docker Benefits to Highlight**

- ✅ **Consistent Environment**: Works same everywhere
- ✅ **Easy Deployment**: Single command deployment
- ✅ **Scalability**: Can run multiple instances
- ✅ **Security**: Isolated from host system
- ✅ **Portability**: Runs on any Docker-enabled system
- ✅ **Version Control**: Image versioning and rollbacks

## 🚨 **Troubleshooting**

### Container won't start:
```bash
docker-compose logs skillsnap
```

### Port conflicts:
```bash
# Use different port
docker run -p 8080:5001 skillsnap
```

### Permission issues:
```bash
# Check if Docker daemon is running
docker ps
```

## 🌟 **Advanced Features**

### **Multi-stage build** (already included):
- Optimized image size
- Security best practices
- Efficient layer caching

### **Health checks** (already included):
- Container health monitoring
- Automatic restart on failure

**Your Dockerized SkillSnap is ready for professional demo! 🐳** 