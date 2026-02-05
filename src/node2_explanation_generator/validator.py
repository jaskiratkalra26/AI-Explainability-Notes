from typing import List

FORBIDDEN_PHRASES = [
    "I thought",
    "I reasoned",
    "my internal weights",
    "training data",
    "neural network",
    "transformer layers",
    "chain of thought",
    "because I believe",
    "model parameters",
    "internal state"
]

DEFAULT_FALLBACK = "This response was generated based on the prompt intent and output characteristics."

def validate_explanation(explanation: str, trace: List[str]) -> bool:
    """
    Validates the generated explanation and trace for safety & compliance.
    Returns True if valid, False otherwise.
    """
    combined_text = explanation.lower() + " ".join(trace).lower()
    
    # Check 1: Forbidden phrases (Internal Reasoning Claims)
    for phrase in FORBIDDEN_PHRASES:
        if phrase in combined_text:
            return False
            
    # Check 2: Length Constraints (Explanation should be short)
    # Simple heuristic: Split by sentence delimiters. Should be 1-3 sentences approx.
    sentences = explanation.split('.')
    # Removing empty strings resulting from split
    sentences = [s for s in sentences if s.strip()]
    
    if len(sentences) > 3:
        return False
        
    return True

def get_safe_fallback() -> str:
    return DEFAULT_FALLBACK
