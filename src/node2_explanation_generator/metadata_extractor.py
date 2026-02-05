import json
import re
from typing import Dict
from node1_answer_generator.llm_client import call_llm
from src.utils import load_config

# Load config
config = load_config()
extractor_config = config.get('metadata_extractor', {})

def extract_metadata(prompt: str, output: str) -> Dict[str, str]:
    """
    Extracts structured metadata from the prompt and output using an LLM.
    
    Returns:
        Dict with keys: 'task_type', 'domain', 'answer_style'
    """
    system_instruction = extractor_config.get('system_instruction', "")
    
    formatted_prompt = system_instruction.format(user_prompt=prompt, ai_output=output)
    
    try:
        # Call the LLM to get the classification
        response_text = call_llm(formatted_prompt)
        
        # Clean up the response to ensure it's valid JSON
        cleaned_response = re.sub(r'```json\s*|\s*```', '', response_text).strip()
        
        # Handle case where LLM might output extra text
        if "{" in cleaned_response:
            start = cleaned_response.find("{")
            end = cleaned_response.rfind("}") + 1
            cleaned_response = cleaned_response[start:end]

        metadata = json.loads(cleaned_response)
        
        # Validate keys exist
        required_keys = ["task_type", "domain", "answer_style"]
        if not all(key in metadata for key in required_keys):
             # Try to repair if possible or just log warning?
             # For now, if missing allow default fallback for missing keys if we partially parsed
             pass

        return {
            "task_type": metadata.get("task_type", "general"),
            "domain": metadata.get("domain", "general"),
            "answer_style": metadata.get("answer_style", "explanatory")
        }
        
    except Exception as e:
        # Fallback mechanism in case of LLM failure or parsing error
        print(f"Metadata extraction failed: {e}. Falling back to rule-based.")
        return _fallback_rule_based_extraction(prompt, output)

def _fallback_rule_based_extraction(prompt: str, output: str) -> Dict[str, str]:
    """
    Fallback method using robust keyword scoring if LLM fails.
    """
    prompt_lower = prompt.lower()
    output_lower = output.lower()
    
    # Helper to tokenize and score
    def get_score(text: str, keywords: list) -> int:
        score = 0
        for kw in keywords:
            # Create a regex to match the keyword with potential suffixes
            # This is a simple heuristic for stemming
            pattern = r'\b' + re.escape(kw) + r'(?:s|es|ing|ed|ment|tion|er|or)?\b'
            if re.search(pattern, text):
                score += 1
        return score

    # --- 1. Determine Task Type ---
    task_keywords = extractor_config.get('task_keywords', {})
    
    best_task = 'general'
    max_task_score = 0
    
    for task, keywords in task_keywords.items():
        score = get_score(prompt_lower, keywords)
        if score > max_task_score:
            max_task_score = score
            best_task = task
            
    # Default to factual if 'what' etc are present but score is low, or keep general
    # If no keywords matched, it remains 'general'

    # --- 2. Determine Domain ---
    domain_keywords = extractor_config.get('domain_keywords', {})

    best_domain = 'general'
    max_domain_score = 0
    
    for domain, keywords in domain_keywords.items():
        score = get_score(prompt_lower, keywords)
        if score > max_domain_score:
            max_domain_score = score
            best_domain = domain

    # --- 3. Determine Answer Style ---
    # Based on output characteristics
    style_thresholds = extractor_config.get('style_thresholds', {})
    concise_max = style_thresholds.get('concise_max_words', 30)
    descriptive_min = style_thresholds.get('descriptive_min_words', 120)
    
    word_count = len(output.split())
    
    if word_count < concise_max:
        answer_style = 'concise'
    elif "is defined as" in output_lower or "refers to" in output_lower or output_lower.startswith("definition:"):
        answer_style = 'definition-based'
    elif word_count > descriptive_min or "\n- " in output or "\n1. " in output: # List or long text
        answer_style = 'descriptive'
    else:
        answer_style = 'explanatory'

    return {
        "task_type": best_task,
        "domain": best_domain,
        "answer_style": answer_style
    }
