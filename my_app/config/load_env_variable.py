"""This module is used to load environment variables from a .env file in local development."""

import os
from dotenv import load_dotenv


def init_env_variables():
    """Initialize app environment depending on context."""
    if "STREAMLIT_CLOUD" not in os.environ:
        load_dotenv()
