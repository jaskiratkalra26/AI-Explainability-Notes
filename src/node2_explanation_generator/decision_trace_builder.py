from typing import List, Dict

def build_decision_trace(metadata: Dict[str, str]) -> List[str]:
    """
    Converts metadata into a list of observable system-level steps.
    Each step must be a factual statement about the process.
    """
    trace = []
    
    # Step 1: Identification
    trace.append(f"Identified the prompt as a {metadata['task_type']} request")
    
    # Step 2: Domain Detection
    if metadata['domain'] != 'general':
        trace.append(f"Detected the domain as {metadata['domain']}")
    else:
        trace.append("Analyzed the prompt context for domain relevance")
        
    # Step 3: Action/Selection
    if metadata['task_type'] == 'factual':
        trace.append("Selected a direct information retrieval strategy")
    elif metadata['task_type'] == 'summarization':
        trace.append("Focused on extracting key points for brevity")
    elif metadata['task_type'] == 'reasoning':
        trace.append("Structured the response to provide logical flow")
    else:
        trace.append("Processed the input to generate a relevant response")

    # Step 4: Output Generation
    trace.append(f"Generated a {metadata['answer_style']} response aligned with the prompt")
    
    return trace
