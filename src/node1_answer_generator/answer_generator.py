from .llm_client import call_llm

def generate_answer(prompt: str) -> str:
    """
    Generates an answer for the given prompt using the configured LLM.
    
    Args:
        prompt: The user input string.
        
    Returns:
        A clean string containing the AI-generated response.
        
    Raises:
        ValueError: If the prompt is empty or invalid.
        RuntimeError: If there is an issue generating the answer.
    """
    if not prompt or not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    
    try:
        raw_response = call_llm(prompt)
        
        # Normalize the output: strip whitespace
        clean_response = raw_response.strip()
        
        return clean_response
        
    except RuntimeError as e:
        # Re-raise or handle specific errors if needed. 
        # Requirement says "Handle API errors gracefully with clear exceptions"
        # Since call_llm raises RuntimeError, we can pass it up or wrap it.
        # We will pass it up as it contains the error message.
        raise
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e
