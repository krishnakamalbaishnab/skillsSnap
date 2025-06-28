from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import json
import asyncio
from ml_utils import extract_text_from_pdf, recommend_jobs, analyze_skill_gap
from services.llm_services import (
    LLMJobMatchingService, 
    LLMSkillGapService, 
    LLMResumeImprovementService,
    LLMSkillsExtractionService,
    check_llm_availability,
    LLMServiceError
)

# Create blueprint for routes
api = Blueprint('api', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_job_descriptions():
    """Load job descriptions from sample_jobs.json."""
    try:
        with open('sample_jobs.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load job descriptions: {str(e)}")

# Main page route
@api.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@api.route('/api/upload_resume', methods=['POST'])
def upload_resume():
    """
    Upload and extract text from PDF resume.
    
    Expected: multipart/form-data with 'file' field containing PDF
    Returns: JSON with extracted text
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Only PDF files are allowed'
            }), 400
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file)
        
        if not extracted_text.strip():
            return jsonify({
                'success': False,
                'error': 'No text could be extracted from the PDF'
            }), 400
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'filename': secure_filename(file.filename),
            'character_count': len(extracted_text)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/api/recommend_jobs', methods=['POST'])
def get_job_recommendations():
    """
    Get job recommendations based on resume text.
    
    Expected: JSON with 'resume_text' field
    Returns: JSON with recommended jobs
    """
    try:
        data = request.get_json()
        
        if not data or 'resume_text' not in data:
            return jsonify({
                'success': False,
                'error': 'resume_text field is required'
            }), 400
        
        resume_text = data['resume_text'].strip()
        
        if not resume_text:
            return jsonify({
                'success': False,
                'error': 'resume_text cannot be empty'
            }), 400
        
        # Get recommendations
        recommendations = recommend_jobs(resume_text)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/api/skill_gap', methods=['POST'])
def analyze_skill_gaps():
    """
    Analyze skill gap between resume and job description.
    
    Expected: JSON with 'resume_text' and 'job_description' fields
    Returns: JSON with skill gap analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'resume_text' not in data or 'job_description' not in data:
            return jsonify({
                'success': False,
                'error': 'Both resume_text and job_description fields are required'
            }), 400
        
        resume_text = data['resume_text'].strip()
        job_description = data['job_description'].strip()
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description cannot be empty'
            }), 400
        
        # Analyze skill gap
        missing_skills = analyze_skill_gap(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'analysis': missing_skills
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# New LLM-based endpoints

@api.route('/api/llm_job_match', methods=['POST'])
def llm_job_match():
    """
    LLM-based semantic job matching.
    
    Expected: JSON with 'resume_text' field
    Returns: JSON with LLM-analyzed job matches
    """
    try:
        # Check LLM availability
        llm_status = check_llm_availability()
        if not llm_status['available']:
            return jsonify({
                'success': False,
                'error': 'LLM services not available',
                'details': llm_status['error']
            }), 503
        
        data = request.get_json()
        
        if not data or 'resume_text' not in data:
            return jsonify({
                'success': False,
                'error': 'resume_text field is required'
            }), 400
        
        resume_text = data['resume_text'].strip()
        
        if not resume_text:
            return jsonify({
                'success': False,
                'error': 'resume_text cannot be empty'
            }), 400
        
        # Load job descriptions
        job_descriptions = load_job_descriptions()
        
        # Run LLM job matching
        async def run_llm_matching():
            return await LLMJobMatchingService.match_jobs(resume_text, job_descriptions)
        
        result = asyncio.run(run_llm_matching())
        
        return jsonify({
            'success': True,
            'llm_analysis': result,
            'provider_info': llm_status['provider_info']
        })
        
    except LLMServiceError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Job matching failed: {str(e)}"
        }), 500

@api.route('/api/llm_skill_gap', methods=['POST'])
def llm_skill_gap():
    """
    LLM-based skill gap analysis.
    
    Expected: JSON with 'resume_text' and 'job_description' fields
    Returns: JSON with LLM-analyzed skill gaps and improvement suggestions
    """
    try:
        # Check LLM availability
        llm_status = check_llm_availability()
        if not llm_status['available']:
            return jsonify({
                'success': False,
                'error': 'LLM services not available',
                'details': llm_status['error']
            }), 503
        
        data = request.get_json()
        
        if not data or 'resume_text' not in data or 'job_description' not in data:
            return jsonify({
                'success': False,
                'error': 'Both resume_text and job_description fields are required'
            }), 400
        
        resume_text = data['resume_text'].strip()
        job_description = data['job_description'].strip()
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description cannot be empty'
            }), 400
        
        # Run LLM skill gap analysis
        async def run_llm_analysis():
            return await LLMSkillGapService.analyze_skill_gap(resume_text, job_description)
        
        result = asyncio.run(run_llm_analysis())
        
        return jsonify({
            'success': True,
            'llm_analysis': result,
            'provider_info': llm_status['provider_info']
        })
        
    except LLMServiceError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Skill gap analysis failed: {str(e)}"
        }), 500

@api.route('/api/resume_improve', methods=['POST'])
def resume_improve():
    """
    LLM-based resume improvement suggestions.
    
    Expected: JSON with 'resume_text' and 'job_description' fields
    Returns: JSON with LLM-generated improvement suggestions
    """
    try:
        # Check LLM availability
        llm_status = check_llm_availability()
        if not llm_status['available']:
            return jsonify({
                'success': False,
                'error': 'LLM services not available',
                'details': llm_status['error']
            }), 503
        
        data = request.get_json()
        
        if not data or 'resume_text' not in data or 'job_description' not in data:
            return jsonify({
                'success': False,
                'error': 'Both resume_text and job_description fields are required'
            }), 400
        
        resume_text = data['resume_text'].strip()
        job_description = data['job_description'].strip()
        
        if not resume_text or not job_description:
            return jsonify({
                'success': False,
                'error': 'resume_text and job_description cannot be empty'
            }), 400
        
        # Run LLM resume improvement
        async def run_llm_improvement():
            return await LLMResumeImprovementService.improve_resume(resume_text, job_description)
        
        result = asyncio.run(run_llm_improvement())
        
        return jsonify({
            'success': True,
            'llm_analysis': result,
            'provider_info': llm_status['provider_info']
        })
        
    except LLMServiceError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Resume improvement failed: {str(e)}"
        }), 500

@api.route('/api/llm_status', methods=['GET'])
def llm_status():
    """
    Check LLM service availability and configuration.
    
    Returns: JSON with LLM provider status
    """
    try:
        status = check_llm_availability()
        return jsonify({
            'success': True,
            'llm_status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to check LLM status: {str(e)}"
        }), 500

@api.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns: JSON with health status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'SkillSnap API is running'
    })

# Error handlers
@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@api.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The requested method is not allowed for this endpoint'
    }), 405

@api.errorhandler(413)
def file_too_large(error):
    return jsonify({
        'error': 'File too large',
        'message': 'The uploaded file is too large'
    }), 413

@api.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An internal server error occurred'
    }), 500 