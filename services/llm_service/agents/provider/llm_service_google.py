import os
import requests
from typing import Optional, Dict, Any, List
import streamlit as st
from dotenv import load_dotenv

from langchain.llms.base import BaseLLM
from langchain.schema import LLMResult, Generation
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.callbacks.manager import CallbackManagerForLLMRun
from services.llm_service.agents.agentic_llm_service import AgenticLLMService
from langchain_core.pydantic_v1 import Field

class GoogleAgenticLLM(AgenticLLMService):
    """
    Agentic LLM Service for Google Gemini models.
    """
    provider: str = Field(default="google")  # ✅ Declare explicitly
    model: str = Field(default="gemini-1.5-flash")
    api_key: Optional[str] = Field(default=None)
    endpoint: str = Field(default="")
    def __init__(
        self,
        model: str = "gemini-1.5-flash",
        api_key: Optional[str] = None,
        **kwargs
    ):
        super().__init__(provider="google", model=model, api_key=api_key, **kwargs)
        self.endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

    def _generate_response(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        # Prepare headers and payload for Gemini
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 512)
            }
        }
        response = requests.post(self.endpoint, headers=headers, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract text from the first candidate
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        raise Exception("No response generated from Google Gemini")