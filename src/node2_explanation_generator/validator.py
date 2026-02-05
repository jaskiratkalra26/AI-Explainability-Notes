from typing import List
from src.utils import load_config

# Load config once at module level (or could do inside functions)
config = load_config()
validator_config = config.get('validator', {})

FORBIDDEN_PHRASES = validator_config.get('forbidden_phrases', [])
DEFAULT_FALLBACK = validator_config.get('default_fallback', "This response was generated based on the prompt intent and output characteristics.")
MAX_SENTENCES = validator_config.get('max_sentences', 3)

def validate_explanation(explanation: str, trace: List[str]) -> bool:
    """
    Validates the generated explanation and trace for safety & compliance.
    Returns True if valid, False otherwise.
    """
    combined_text = explanation.lower() + " ".join(trace).lower()
    
    # Check 1: Forbidden phrases (Internal Reasoning Claims)
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in combined_text:
            return False
            
    # Check 2: Length Constraints (Explanation should be short)
    # Simple heuristic: Split by sentence delimiters. Should be 1-3 sentences approx.
    sentences = explanation.split('.')
    # Removing empty strings resulting from split
    sentences = [s for s in sentences if s.strip()]
    
    if len(sentences) > MAX_SENTENCES:
        return False
        
    return True

def get_safe_fallback() -> str:
    return DEFAULT_FALLBACK
