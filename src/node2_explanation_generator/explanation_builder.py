from typing import List, Dict

def build_human_explanation(trace: List[str], metadata: Dict[str, str]) -> str:
    """
    Synthesizes a short natural language explanation from the decision trace.
    Strictly avoids mentioning internal states.
    """
    
    # Constructing a sentence that combines the key observations
    task_desc = f"identified the prompt as a {metadata['task_type']} request"
    
    domain_desc = ""
    if metadata['domain'] != 'general':
        domain_desc = f" within the {metadata['domain']} domain"
        
    style_desc = f"producing a {metadata['answer_style']} response"
    
    explanation = (
        f"The system {task_desc}{domain_desc} and "
        f"processed the input according to the detected intent, "
        f"{style_desc}."
    )
    
    return explanation
