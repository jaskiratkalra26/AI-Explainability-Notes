import os
import yaml
import google.generativeai as genai
from typing import Optional

# Determine the path to the configuration file relative to this file
# Structure: src/node1_answer_generator/llm_client.py -> ../../Config/config.yaml
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR, 'Config', 'config.yaml')

def _load_config():
    """Loads configuration from the yaml file."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found at: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def _get_api_key(config: dict) -> str:
    """Retrieves the API key from environment variables based on config."""
    env_var_name = config.get('gemini', {}).get('api_key_env_var', 'GEMINI_API_KEY')
    api_key = os.getenv(env_var_name)
    if not api_key:
        raise ValueError(f"API Key not found. Please set the {env_var_name} environment variable.")
    return api_key

def call_llm(prompt: str) -> str:
    """
    Calls the Gemini model with the given prompt and returns the response text.
    
    Args:
        prompt: The input string to send to the model.
        
    Returns:
        The text response from the model.
        
    Raises:
        RuntimeError: If the API call fails or configuration is invalid.
    """
    try:
        config = _load_config()
        api_key = _get_api_key(config)
        model_name = config.get('gemini', {}).get('model_name', 'gemini-2.5-flash')
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # Determine generation config if needed, keeping it simple for now
        response = model.generate_content(prompt)
        
        if not response.text:
            return ""
            
        return response.text
        
    except Exception as e:
        # Wrap all exceptions in a RuntimeError for the caller to handle gracefully
        raise RuntimeError(f"Failed to communicate with LLM: {str(e)}") from e
