import os
import json
import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import openai
from openai import OpenAI
import anthropic
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response from the LLM."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured."""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI GPT-4 provider implementation."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.client)
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume and job matching analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.3),
                top_p=kwargs.get('top_p', 0.9)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate response from OpenAI: {str(e)}")

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation."""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
        self.client = None
        
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return bool(self.api_key and self.client)
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.3),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise Exception(f"Failed to generate response from Anthropic: {str(e)}")

class MistralProvider(LLMProvider):
    """Mistral AI provider implementation."""
    
    def __init__(self):
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.model = os.getenv('MISTRAL_MODEL', 'mistral-large-latest')
        self.base_url = "https://api.mistral.ai/v1"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise Exception("Mistral API key not configured")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": kwargs.get('max_tokens', 2000),
                "temperature": kwargs.get('temperature', 0.3)
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Mistral API error: {response.status_code} - {response.text}")
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Mistral API error: {str(e)}")
            raise Exception(f"Failed to generate response from Mistral: {str(e)}")

class LLMHandler:
    """Main LLM handler that manages different providers."""
    
    def __init__(self):
        self.providers = {
            'openai': OpenAIProvider(),
            'anthropic': AnthropicProvider(),
            'mistral': MistralProvider()
        }
        
        # Get preferred provider from environment
        self.preferred_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        
        # Fallback order if preferred provider is not available
        self.fallback_order = ['openai', 'anthropic', 'mistral']
    
    def get_available_provider(self) -> LLMProvider:
        """Get the first available provider in order of preference."""
        
        # Try preferred provider first
        if self.preferred_provider in self.providers:
            provider = self.providers[self.preferred_provider]
            if provider.is_available():
                logger.info(f"Using preferred LLM provider: {self.preferred_provider}")
                return provider
        
        # Try fallback providers
        for provider_name in self.fallback_order:
            if provider_name in self.providers:
                provider = self.providers[provider_name]
                if provider.is_available():
                    logger.info(f"Using fallback LLM provider: {provider_name}")
                    return provider
        
        raise Exception("No LLM provider is available. Please configure at least one API key.")
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using the best available provider."""
        provider = self.get_available_provider()
        return await provider.generate_response(prompt, **kwargs)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about available providers."""
        info = {
            'preferred_provider': self.preferred_provider,
            'available_providers': [],
            'configured_providers': []
        }
        
        for name, provider in self.providers.items():
            if provider.is_available():
                info['available_providers'].append(name)
            if hasattr(provider, 'api_key') and provider.api_key:
                info['configured_providers'].append(name)
        
        return info

# Global LLM handler instance
llm_handler = LLMHandler() 