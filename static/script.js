// Global variables
let extractedResumeText = '';
// Use current domain for API calls, works both locally and when deployed
const API_BASE_URL = window.location.origin + '/api';

// Utility Functions
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary mb-3" role="status"></div>
            <p class="text-muted">Processing...</p>
        </div>
    `;
}

function hideLoading(containerId) {
    // Loading is replaced by actual content, so no need to explicitly hide
}

// File Upload Functions
function initializeFileUpload() {
    const fileUploadArea = document.getElementById('fileUploadArea');
    const fileInput = document.getElementById('fileInput');

    if (!fileUploadArea || !fileInput) {
        return;
    }

    // Click to upload
    fileUploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    });

    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.classList.remove('dragover');
    });

    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        showAlert('Please select a PDF file.', 'danger');
        return;
    }

    const fileUploadArea = document.getElementById('fileUploadArea');
    fileUploadArea.innerHTML = `
        <i class="fas fa-file-pdf fa-3x text-danger mb-3"></i>
        <h5>${file.name}</h5>
        <p class="text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</p>
        <button class="btn btn-primary" onclick="uploadFile()">
            <i class="fas fa-upload me-2"></i>Upload Resume
        </button>
    `;
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files[0]) {
        showAlert('Please select a file first.', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    showLoading('uploadResults');

    try {
        const response = await fetch(`${API_BASE_URL}/upload_resume`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            extractedResumeText = data.text;
            displayUploadResults(data);
            showAlert('Resume uploaded and processed successfully!');
            
            // Enable other features
            document.getElementById('recommendJobsBtn').disabled = false;
            document.getElementById('jobDescTextarea').disabled = false;
            document.getElementById('analyzeSkillsBtn').disabled = false;
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        hideLoading('uploadResults');
        showAlert(`Upload failed: ${error.message}`, 'danger');
    }
}

function displayUploadResults(data) {
    const container = document.getElementById('uploadResults');
    container.innerHTML = `
        <div class="result-card">
            <h5><i class="fas fa-check-circle text-success me-2"></i>Resume Processed</h5>
            <p><strong>File:</strong> ${data.filename}</p>
            <p><strong>Characters extracted:</strong> ${data.character_count}</p>
            <div class="mt-3">
                <button class="btn btn-outline-primary btn-sm" onclick="toggleResumeText()">
                    <i class="fas fa-eye me-2"></i>Preview Text
                </button>
            </div>
            <div id="resumeTextPreview" class="mt-3" style="display: none;">
                <div class="p-3 bg-light rounded">
                    <pre style="white-space: pre-wrap; font-size: 0.9rem;">${data.text.substring(0, 500)}${data.text.length > 500 ? '...' : ''}</pre>
                </div>
            </div>
        </div>
    `;
}

function toggleResumeText() {
    const preview = document.getElementById('resumeTextPreview');
    preview.style.display = preview.style.display === 'none' ? 'block' : 'none';
}

// Job Recommendation Functions
async function recommendJobs() {
    if (!extractedResumeText) {
        showAlert('Please upload a resume first.', 'danger');
        return;
    }

    showLoading('jobRecommendations');

    try {
        const response = await fetch(`${API_BASE_URL}/recommend_jobs`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_text: extractedResumeText
            })
        });

        const data = await response.json();

        if (data.success) {
            displayJobRecommendations(data.recommendations);
            showAlert(`Found ${data.total_recommendations} job recommendations!`);
        } else {
            throw new Error(data.error || 'Recommendation failed');
        }
    } catch (error) {
        hideLoading('jobRecommendations');
        showAlert(`Recommendation failed: ${error.message}`, 'danger');
    }
}

function displayJobRecommendations(recommendations) {
    const container = document.getElementById('jobRecommendations');
    
    if (recommendations.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <p class="text-muted">No job recommendations found.</p>
            </div>
        `;
        return;
    }

    const html = recommendations.map((job, index) => `
        <div class="result-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="mb-0">
                    <i class="fas fa-briefcase me-2 text-primary"></i>
                    ${job.title}
                </h5>
                <span class="score-badge">${job.score.toFixed(1)}% Match</span>
            </div>
            <div class="mb-3">
                <small class="text-muted">Matched Skills:</small>
                <div class="mt-1">
                    ${job.matched_keywords.map(skill => `<span class="skill-badge">${skill}</span>`).join('')}
                </div>
            </div>
            <div class="progress mb-2">
                <div class="progress-bar" style="width: ${job.score}%"></div>
            </div>
        </div>
    `).join('');

    container.innerHTML = html;
}

// Skill Gap Analysis Functions
async function analyzeSkillGap() {
    const jobDescription = document.getElementById('jobDescTextarea').value.trim();
    
    if (!extractedResumeText) {
        showAlert('Please upload a resume first.', 'danger');
        return;
    }

    if (!jobDescription) {
        showAlert('Please enter a job description.', 'danger');
        return;
    }

    showLoading('skillGapResults');

    try {
        const response = await fetch(`${API_BASE_URL}/skill_gap`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_text: extractedResumeText,
                job_description: jobDescription
            })
        });

        const data = await response.json();

        if (data.success) {
            displaySkillGapResults(data.analysis);
            showAlert('Skill gap analysis completed!');
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        hideLoading('skillGapResults');
        showAlert(`Analysis failed: ${error.message}`, 'danger');
    }
}

function displaySkillGapResults(missingSkills) {
    const container = document.getElementById('skillGapResults');
    
    if (missingSkills.length === 0) {
        container.innerHTML = `
            <div class="result-card">
                <div class="text-center py-4">
                    <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
                    <h5 class="text-success">Perfect Match!</h5>
                    <p class="text-muted">Your resume covers all the required skills for this job.</p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="result-card">
            <h5><i class="fas fa-exclamation-triangle text-warning me-2"></i>Skills to Develop</h5>
            <p class="text-muted mb-3">The following skills are mentioned in the job description but not found in your resume:</p>
            <div class="mb-3">
                ${missingSkills.map(skill => `<span class="missing-skill-badge">${skill}</span>`).join('')}
            </div>
            <div class="alert alert-info">
                <i class="fas fa-lightbulb me-2"></i>
                <strong>Tip:</strong> Consider adding these skills to your resume if you have experience with them, or plan to learn them to improve your job match.
            </div>
        </div>
    `;
}

// Sample Data Functions
function loadSampleResume() {
    const sampleText = `John Doe - Software Engineer

Experience:
• 3+ years of Python development
• Proficient in JavaScript, React, and Node.js  
• Experience with SQL databases (MySQL, PostgreSQL)
• Familiar with AWS cloud services
• Docker and containerization experience
• Git version control and CI/CD pipelines
• REST API development and testing
• Agile methodology and Scrum

Education:
Bachelor of Science in Computer Science

Skills:
Python, JavaScript, React, Node.js, SQL, AWS, Docker, Git, HTML, CSS, REST APIs, Agile, Scrum`;

    extractedResumeText = sampleText;
    
    const container = document.getElementById('uploadResults');
    container.innerHTML = `
        <div class="result-card">
            <h5><i class="fas fa-file-text text-info me-2"></i>Sample Resume Loaded</h5>
            <p><strong>Characters:</strong> ${sampleText.length}</p>
            <div class="mt-3">
                <button class="btn btn-outline-primary btn-sm" onclick="toggleResumeText()">
                    <i class="fas fa-eye me-2"></i>Preview Text
                </button>
            </div>
            <div id="resumeTextPreview" class="mt-3" style="display: none;">
                <div class="p-3 bg-light rounded">
                    <pre style="white-space: pre-wrap; font-size: 0.9rem;">${sampleText}</pre>
                </div>
            </div>
        </div>
    `;

    // Enable other features
    document.getElementById('recommendJobsBtn').disabled = false;
    document.getElementById('jobDescTextarea').disabled = false;
    document.getElementById('analyzeSkillsBtn').disabled = false;

    showAlert('Sample resume loaded successfully! You can now try job recommendations and skill analysis.');
}

function loadSampleJobDesc() {
    const sampleJobDesc = `We are looking for a Senior Software Engineer to join our team.

Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python and JavaScript
- Experience with React and Node.js frameworks
- Knowledge of SQL and NoSQL databases
- Familiarity with cloud platforms (AWS, Azure)
- Experience with Docker and Kubernetes
- Git version control and CI/CD pipelines
- Understanding of microservices architecture
- Knowledge of machine learning concepts
- Experience with testing frameworks
- Agile/Scrum methodology experience

Nice to have:
- TensorFlow or PyTorch experience
- DevOps experience
- GraphQL knowledge`;

    document.getElementById('jobDescTextarea').value = sampleJobDesc;
    showAlert('Sample job description loaded!');
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    
    // Add event listeners
    document.getElementById('recommendJobsBtn').addEventListener('click', recommendJobs);
    document.getElementById('analyzeSkillsBtn').addEventListener('click', analyzeSkillGap);
    document.getElementById('loadSampleResumeBtn').addEventListener('click', loadSampleResume);
    document.getElementById('loadSampleJobBtn').addEventListener('click', loadSampleJobDesc);
});

// Health check function
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status !== 'healthy') {
            showAlert('Warning: API health check failed. Some features may not work properly.', 'warning');
        }
    } catch (error) {
        showAlert('Warning: Cannot connect to SkillSnap API. Please make sure the backend is running.', 'danger');
    }
}

// Check API health on page load
checkAPIHealth(); 