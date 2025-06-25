import json
import pdfplumber
import re
from typing import List, Dict, Tuple

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        pdf_file: File object or file-like object containing PDF data
    
    Returns:
        str: Extracted text from the PDF
    
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def recommend_jobs(resume_text: str, top_k: int = 3) -> List[Dict[str, str]]:
    """
    Recommend jobs based on resume text using simple keyword matching.
    (Simplified version without ML - will add ML later)
    
    Args:
        resume_text: The text content of the resume
        top_k: Number of top recommendations to return
    
    Returns:
        List of dictionaries containing job titles and match scores
    """
    try:
        # Load sample jobs
        with open('sample_jobs.json', 'r') as f:
            jobs = json.load(f)
        
        # Simple keyword-based matching (temporary solution)
        job_scores = []
        resume_lower = resume_text.lower()
        
        for job in jobs:
            # Count keyword matches
            job_desc_lower = job['description'].lower()
            
            # Extract common tech keywords
            tech_keywords = [
                'python', 'javascript', 'react', 'node', 'sql', 'git', 'aws', 'azure',
                'machine learning', 'data', 'analysis', 'statistics', 'pandas', 'numpy',
                'tensorflow', 'pytorch', 'tableau', 'power bi', 'spark', 'hadoop',
                'docker', 'kubernetes', 'api', 'rest', 'frontend', 'backend', 'database',
                'mongodb', 'postgresql', 'mysql', 'java', 'spring', 'microservices',
                'agile', 'scrum', 'ci/cd', 'testing', 'unit testing', 'integration'
            ]
            
            score = 0
            matched_keywords = []
            
            for keyword in tech_keywords:
                if keyword in resume_lower and keyword in job_desc_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            # Calculate percentage match
            total_keywords_in_job = sum(1 for kw in tech_keywords if kw in job_desc_lower)
            match_percentage = (score / max(total_keywords_in_job, 1)) * 100 if total_keywords_in_job > 0 else 0
            
            job_scores.append({
                'title': job['title'],
                'score': match_percentage,
                'matched_keywords': matched_keywords
            })
        
        # Sort by score and return top k
        job_scores.sort(key=lambda x: x['score'], reverse=True)
        return job_scores[:top_k]
        
    except Exception as e:
        raise Exception(f"Failed to recommend jobs: {str(e)}")

def analyze_skill_gap(resume_text: str, job_description: str) -> List[str]:
    """
    Analyze skill gap between resume and job description using simple text processing.
    (Simplified version without spaCy - will add NLP later)
    
    Args:
        resume_text: The text content of the resume
        job_description: The job description text
    
    Returns:
        List of skills that are missing from the resume
    """
    try:
        # Define common skills/technologies
        skills_db = [
            'python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform',
            'git', 'jenkins', 'ci/cd', 'devops', 'linux', 'bash', 'shell scripting',
            'machine learning', 'deep learning', 'data science', 'artificial intelligence',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
            'tableau', 'power bi', 'excel', 'r', 'matlab', 'spss',
            'html', 'css', 'bootstrap', 'sass', 'tailwind',
            'rest api', 'graphql', 'microservices', 'soap', 'json', 'xml',
            'agile', 'scrum', 'kanban', 'project management',
            'testing', 'unit testing', 'integration testing', 'selenium', 'junit',
            'spark', 'hadoop', 'kafka', 'airflow', 'etl', 'data pipeline'
        ]
        
        # Convert to lowercase for case-insensitive matching
        resume_lower = resume_text.lower()
        job_desc_lower = job_description.lower()
        
        # Find skills mentioned in job description
        job_skills = []
        for skill in skills_db:
            if skill in job_desc_lower:
                job_skills.append(skill)
        
        # Find skills missing from resume
        missing_skills = []
        for skill in job_skills:
            if skill not in resume_lower:
                missing_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(missing_skills))
        
    except Exception as e:
        raise Exception(f"Failed to analyze skill gap: {str(e)}") 