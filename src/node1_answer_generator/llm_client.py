import os
import google.generativeai as genai

try:
    # Attempt to import from src (if running from root or src is a package)
    from src.config import config as PROJECT_CONFIG
except ImportError:
    # Attempt to import directly if src is in PYTHONPATH
    import config as PROJECT_CONFIG

def _load_config():
    """Loads configuration."""
    return PROJECT_CONFIG

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
        
        # Get generation config from settings
        gen_config_dict = config.get('gemini', {}).get('generation_config', {})
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=gen_config_dict.get('max_output_tokens', 300),
            temperature=gen_config_dict.get('temperature', 0.7)
        )
        
        # Determine generation config if needed, keeping it simple for now
        response = model.generate_content(prompt, generation_config=generation_config)
        
        if not response.text:
            return ""
            
        return response.text
        
    except Exception as e:
        # Wrap all exceptions in a RuntimeError for the caller to handle gracefully
        raise RuntimeError(f"Failed to communicate with LLM: {str(e)}") from e
