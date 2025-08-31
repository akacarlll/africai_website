import os
import streamlit as st
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any, Iterator
from langchain.llms.base import BaseLLM
from langchain.schema import Generation, LLMResult
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.pydantic_v1 import Field

class AgenticLLMService(BaseLLM):
    """
    Simple agentic LLM service using LangChain's BaseLLM.
    Can be inherited to support different providers.
    """
    provider: str = Field(default="google")
    model: str = Field(default="gemini-1.5-flash")
    api_key: str = Field(default=None)

    def __init__(
        self, 
        provider: str = "google",
        model: str = "default",
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the agentic LLM service.
        
        Args:
            provider: LLM provider name
            model: Model name
            api_key: API key (optional, will try to get from env)
            **kwargs: Additional parameters
        """
        super().__init__(**kwargs)
        self.provider = provider
        self.model = model
        self.api_key = api_key or self._get_env_variable(f"{provider.upper()}_API_KEY")
        
    def _get_env_variable(self, key: str) -> str:
        """Get environment variable from streamlit secrets or .env file."""
        if "STREAMLIT_CLOUD" in os.environ:
            return st.secrets.get(key, "")
        else:
            load_dotenv(r"C:\Users\carlf\Documents\GitHub\africai_website\.env")
            return os.getenv(key, "")
    
    @property
    def _llm_type(self) -> str:
        """Return identifier for the LLM type."""
        return f"agentic_{self.provider}"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> str:
        """
        Main method called by LangChain.
        Override this in provider-specific classes.
        """
        # This should be implemented by concrete provider classes
        return self._generate_response(prompt, stop=stop, **kwargs)
    
    def _generate_response(
        self, 
        prompt: str, 
        stop: Optional[List[str]] = None, 
        **kwargs
    ) -> str:
        """
        Generate response - to be implemented by provider classes.
        This is a placeholder method.
        """
        raise NotImplementedError(
            "Provider classes must implement _generate_response method"
        )
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> LLMResult:
        """Generate responses for multiple prompts."""
        generations = []
        
        for prompt in prompts:
            response = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([Generation(text=response)])
            
        return LLMResult(generations=generations)
    
    # Additional agentic-specific methods (work alongside LangChain)
    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate response with system prompt."""
        full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        return self._call(full_prompt, **kwargs)
    
    def generate_structured(self, prompt: str, format_instruction: str, **kwargs) -> str:
        """Generate structured response."""
        structured_prompt = f"{prompt}\n\n{format_instruction}"
        return self._call(structured_prompt, **kwargs)

