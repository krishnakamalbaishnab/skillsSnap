import json
import logging
from typing import Dict, List, Any, Optional
from services.llm_handler import llm_handler
from utils.prompt_templates import PromptTemplates

# Configure logging
logger = logging.getLogger(__name__)

class LLMServiceError(Exception):
    """Custom exception for LLM service errors."""
    pass

class LLMJobMatchingService:
    """Service for LLM-based job matching."""
    
    @staticmethod
    async def match_jobs(resume_text: str, job_descriptions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Match resume against job descriptions using LLM.
        
        Args:
            resume_text: Extracted text from resume
            job_descriptions: List of job description dictionaries
            
        Returns:
            Dictionary with job matches and analysis
        """
        try:
            # Generate prompt
            prompt = PromptTemplates.job_matching_prompt(resume_text, job_descriptions)
            
            # Get LLM response
            response = await llm_handler.generate_response(
                prompt,
                max_tokens=3000,
                temperature=0.2
            )
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {response}")
                raise LLMServiceError("Invalid response format from LLM")
            
            # Validate response structure
            if 'matches' not in result:
                raise LLMServiceError("LLM response missing 'matches' field")
            
            return result
            
        except Exception as e:
            logger.error(f"Job matching failed: {str(e)}")
            raise LLMServiceError(f"Job matching failed: {str(e)}")

class LLMSkillGapService:
    """Service for LLM-based skill gap analysis."""
    
    @staticmethod
    async def analyze_skill_gap(resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze skill gap between resume and job description using LLM.
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
            
        Returns:
            Dictionary with skill gap analysis
        """
        try:
            # Generate prompt
            prompt = PromptTemplates.skill_gap_prompt(resume_text, job_description)
            
            # Get LLM response
            response = await llm_handler.generate_response(
                prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {response}")
                raise LLMServiceError("Invalid response format from LLM")
            
            # Validate response structure
            if 'missing_skills' not in result:
                raise LLMServiceError("LLM response missing 'missing_skills' field")
            
            return result
            
        except Exception as e:
            logger.error(f"Skill gap analysis failed: {str(e)}")
            raise LLMServiceError(f"Skill gap analysis failed: {str(e)}")

class LLMResumeImprovementService:
    """Service for LLM-based resume improvement suggestions."""
    
    @staticmethod
    async def improve_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Provide resume improvement suggestions using LLM.
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
            
        Returns:
            Dictionary with improvement suggestions
        """
        try:
            # Generate prompt
            prompt = PromptTemplates.resume_improvement_prompt(resume_text, job_description)
            
            # Get LLM response
            response = await llm_handler.generate_response(
                prompt,
                max_tokens=3000,
                temperature=0.3
            )
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {response}")
                raise LLMServiceError("Invalid response format from LLM")
            
            # Validate response structure
            if 'section_analysis' not in result:
                raise LLMServiceError("LLM response missing 'section_analysis' field")
            
            return result
            
        except Exception as e:
            logger.error(f"Resume improvement analysis failed: {str(e)}")
            raise LLMServiceError(f"Resume improvement analysis failed: {str(e)}")

class LLMSkillsExtractionService:
    """Service for LLM-based skills extraction."""
    
    @staticmethod
    async def extract_skills(resume_text: str) -> Dict[str, Any]:
        """
        Extract and categorize skills from resume using LLM.
        
        Args:
            resume_text: Extracted text from resume
            
        Returns:
            Dictionary with categorized skills
        """
        try:
            # Generate prompt
            prompt = PromptTemplates.extract_skills_prompt(resume_text)
            
            # Get LLM response
            response = await llm_handler.generate_response(
                prompt,
                max_tokens=2000,
                temperature=0.1
            )
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {response}")
                raise LLMServiceError("Invalid response format from LLM")
            
            # Validate response structure
            if 'technical_skills' not in result:
                raise LLMServiceError("LLM response missing 'technical_skills' field")
            
            return result
            
        except Exception as e:
            logger.error(f"Skills extraction failed: {str(e)}")
            raise LLMServiceError(f"Skills extraction failed: {str(e)}")

# Utility function to validate LLM availability
def check_llm_availability() -> Dict[str, Any]:
    """
    Check if LLM services are available and configured.
    
    Returns:
        Dictionary with availability status and provider info
    """
    try:
        provider_info = llm_handler.get_provider_info()
        is_available = len(provider_info['available_providers']) > 0
        
        return {
            'available': is_available,
            'provider_info': provider_info,
            'error': None if is_available else "No LLM providers configured"
        }
    except Exception as e:
        return {
            'available': False,
            'provider_info': {},
            'error': str(e)
        } 