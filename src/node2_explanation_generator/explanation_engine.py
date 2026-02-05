from typing import Dict
from .metadata_extractor import extract_metadata
from .decision_trace_builder import build_decision_trace
from .explanation_builder import build_human_explanation
from .validator import validate_explanation, get_safe_fallback

def build_explanation(prompt: str, output: str) -> Dict[str, any]:
    """
    Orchestrates the explanation generation pipeline.
    
    Args:
        prompt: The user input text.
        output: The AI-generated answer.
        
    Returns:
        A dictionary containing the 'explanation' and 'decision_trace'.
    """
    
    # 1. Extract Metadata
    metadata = extract_metadata(prompt, output)
    
    # 2. Build Decision Trace
    trace = build_decision_trace(metadata)
    
    # 3. Generate Explanation
    explanation = build_human_explanation(trace, metadata)
    
    # 4. Validation
    is_valid = validate_explanation(explanation, trace)
    
    if not is_valid:
        explanation = get_safe_fallback()
        # In a strict mode, we might also sanitize the trace, 
        # but the trace generator is designed to be deterministic and safe by default.
        
    return {
        "explanation": explanation,
        "decision_trace": trace
    }
