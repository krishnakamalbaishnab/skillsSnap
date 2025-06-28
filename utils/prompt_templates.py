"""
Prompt templates for SkillSnap LLM features.
These templates are designed to work with various LLM providers.
"""

class PromptTemplates:
    """Collection of prompt templates for different LLM tasks."""
    
    @staticmethod
    def job_matching_prompt(resume_text: str, job_descriptions: list) -> str:
        """
        Generate prompt for semantic job matching.
        
        Args:
            resume_text: Extracted text from resume
            job_descriptions: List of job description dictionaries with 'title' and 'description'
        
        Returns:
            Formatted prompt string
        """
        jobs_text = "\n\n".join([
            f"Job Title: {job['title']}\nDescription: {job['description']}"
            for job in job_descriptions
        ])
        
        return f"""
You are an expert resume and job matching analyst. Your task is to analyze a resume and match it against available job positions based on skills, experience, and overall fit.

RESUME TEXT:
{resume_text}

AVAILABLE JOBS:
{jobs_text}

INSTRUCTIONS:
1. Analyze the resume for skills, experience, education, and career objectives
2. For each job, evaluate the match based on:
   - Skills alignment (technical and soft skills)
   - Experience relevance
   - Industry fit
   - Career progression alignment
3. Score each job from 0-100 based on overall fit
4. Provide specific reasons for the match score
5. Return results in the following JSON format:

{{
    "matches": [
        {{
            "job_title": "Job Title",
            "score": 85,
            "reasons": [
                "Strong technical skills match: Python, React, AWS",
                "Relevant experience in software development",
                "Good alignment with company culture and values"
            ],
            "strengths": ["List of candidate's strengths for this role"],
            "concerns": ["List of potential concerns or gaps"]
        }}
    ],
    "analysis_summary": "Brief overall analysis of the candidate's profile"
}}

IMPORTANT: Return ONLY valid JSON. Do not include any additional text or explanations outside the JSON structure.
"""

    @staticmethod
    def skill_gap_prompt(resume_text: str, job_description: str) -> str:
        """
        Generate prompt for skill gap analysis.
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
        
        Returns:
            Formatted prompt string
        """
        return f"""
You are an expert career advisor and skills analyst. Your task is to analyze the gap between a candidate's resume and a specific job description to identify missing skills and provide actionable improvement suggestions.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
1. Identify skills and experiences mentioned in the job description
2. Compare against what's present in the resume
3. Identify missing or underdeveloped skills
4. Provide specific, actionable suggestions for improvement
5. Return results in the following JSON format:

{{
    "missing_skills": [
        {{
            "skill": "Skill Name",
            "importance": "high|medium|low",
            "description": "Why this skill is important for the role",
            "improvement_suggestions": [
                "Specific action item 1",
                "Specific action item 2"
            ]
        }}
    ],
    "experience_gaps": [
        {{
            "area": "Area of experience",
            "description": "What experience is missing",
            "suggestions": ["How to gain this experience"]
        }}
    ],
    "overall_assessment": "Summary of the candidate's readiness for this role",
    "priority_improvements": ["Top 3 most important improvements to focus on"]
}}

IMPORTANT: Return ONLY valid JSON. Do not include any additional text or explanations outside the JSON structure.
"""

    @staticmethod
    def resume_improvement_prompt(resume_text: str, job_description: str) -> str:
        """
        Generate prompt for resume improvement suggestions.
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
        
        Returns:
            Formatted prompt string
        """
        return f"""
You are an expert resume writer and career coach. Your task is to analyze a resume against a specific job description and provide suggestions for improvement, including potential rewrites of key sections.

RESUME TEXT:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
1. Analyze how well the resume aligns with the job requirements
2. Identify sections that could be improved or rewritten
3. Provide specific suggestions for each section
4. If requested, provide rewritten versions of key sections
5. Return results in the following JSON format:

{{
    "overall_assessment": "Brief assessment of resume quality and alignment",
    "section_analysis": [
        {{
            "section": "summary|experience|skills|education",
            "current_content": "What's currently in this section",
            "issues": ["List of issues or areas for improvement"],
            "suggestions": ["Specific improvement suggestions"],
            "rewritten_content": "Improved version of this section (if applicable)"
        }}
    ],
    "keyword_optimization": [
        {{
            "keyword": "Important keyword from job description",
            "current_usage": "How it's currently used in resume",
            "suggested_usage": "How to better incorporate this keyword"
        }}
    ],
    "action_items": [
        "Specific action items to improve the resume"
    ],
    "priority_score": 85
}}

IMPORTANT: Return ONLY valid JSON. Do not include any additional text or explanations outside the JSON structure.
"""

    @staticmethod
    def extract_skills_prompt(resume_text: str) -> str:
        """
        Generate prompt for skills extraction from resume.
        
        Args:
            resume_text: Extracted text from resume
        
        Returns:
            Formatted prompt string
        """
        return f"""
You are an expert skills analyst. Your task is to extract and categorize all skills mentioned in a resume.

RESUME TEXT:
{resume_text}

INSTRUCTIONS:
1. Identify all technical skills, soft skills, tools, and technologies
2. Categorize them appropriately
3. Provide confidence levels for each skill
4. Return results in the following JSON format:

{{
    "technical_skills": [
        {{
            "skill": "Skill Name",
            "confidence": "high|medium|low",
            "context": "How the skill was mentioned or demonstrated"
        }}
    ],
    "soft_skills": [
        {{
            "skill": "Skill Name",
            "confidence": "high|medium|low",
            "context": "How the skill was mentioned or demonstrated"
        }}
    ],
    "tools_technologies": [
        {{
            "tool": "Tool/Technology Name",
            "confidence": "high|medium|low",
            "context": "How the tool was mentioned or used"
        }}
    ],
    "languages": [
        {{
            "language": "Programming Language",
            "confidence": "high|medium|low",
            "context": "How the language was mentioned or used"
        }}
    ],
    "certifications": [
        {{
            "certification": "Certification Name",
            "issuer": "Issuing Organization",
            "year": "Year obtained (if mentioned)"
        }}
    ]
}}

IMPORTANT: Return ONLY valid JSON. Do not include any additional text or explanations outside the JSON structure.
""" 