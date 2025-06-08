from typing import Any, List, Optional
import os
import requests
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManagerForLLMRun


class SimpleLLM(LLM):
    """LLM wrapper supporting multiple API providers: Together AI, DeepSeek"""
    
    def __init__(
        self, 
        provider: str = "together",  # "together", "deepseek"
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.provider = provider.lower()
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Set up provider-specific configurations
        if self.provider == "together":
            self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
            self.base_url = base_url or "https://api.together.xyz/v1"
            self.model = model or "meta-llama/Llama-2-7b-chat-hf"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        elif self.provider == "deepseek":
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            self.base_url = base_url or "https://api.deepseek.com/v1"
            self.model = model or "deepseek-chat"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
        if not self.api_key:
            raise ValueError(f"API key required for {self.provider}. Set {self.provider.upper()}_API_KEY environment variable.")
    
    @property
    def _llm_type(self) -> str:
        return f"{self.provider}_llm"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # Prepare the API request
        url = f"{self.base_url}/chat/completions"
        
        # Format messages for chat completion
        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False
        }
        
        # Add stop sequences if provided
        if stop:
            payload["stop"] = stop
            
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            return f"Error calling {self.provider} API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing {self.provider} response: {str(e)}"
    
    def generate(self, prompt_template: PromptTemplate, **kwargs) -> str:
        """
        Generate text from a PromptTemplate
        
        Args:
            prompt_template: The PromptTemplate to use for generation
            **kwargs: Additional variables for the prompt template
            
        Returns:
            Generated text as string
        """
        # Format the template into a string prompt
        formatted_prompt = prompt_template.format(**kwargs)
        
        # Use the _call method to generate response
        return self._call(formatted_prompt)
