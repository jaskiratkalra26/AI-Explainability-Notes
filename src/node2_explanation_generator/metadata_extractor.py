import json
import re
from typing import Dict
from node1_answer_generator.llm_client import call_llm

def extract_metadata(prompt: str, output: str) -> Dict[str, str]:
    """
    Extracts structured metadata from the prompt and output using an LLM.
    
    Returns:
        Dict with keys: 'task_type', 'domain', 'answer_style'
    """
    system_instruction = """
    You are a metadata extraction engine. Your job is to analyze the following USER PROMPT and AI OUTPUT
    and classify them into specific categories.
    
    Return ONLY a JSON object with the following keys and valid values:
    
    1. "task_type":
       - factual (asking for facts, definitions, specific info)
       - summarization (requesting a summary or shortening)
       - reasoning (asking why, how, or complex explanation)
       - opinion (asking for views or thoughts)
       - general (chit-chat or other)
       
    2. "domain":
       - politics
       - technology
       - education
       - general
       - other
       
    3. "answer_style":
       - definition-based (starts with a definition or defines something)
       - descriptive (long, detailed response)
       - concise (short, direct answer)
       - explanatory (explains a concept clearly)

    Input Context:
    User Prompt: {user_prompt}
    AI Output: {ai_output}
    
    Response format:
    {{
        "task_type": "...",
        "domain": "...",
        "answer_style": "..."
    }}
    """
    
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
    Fallback method using simple heuristics if LLM fails.
    """
    prompt_lower = prompt.lower()
    output_lower = output.lower()
    
    # 1. Determine Task Type
    if any(word in prompt_lower for word in ['summarize', 'summary', 'brief', 'shorten']):
        task_type = 'summarization'
    elif any(word in prompt_lower for word in ['what', 'who', 'when', 'where', 'define', 'which', 'classification', 'type']):
        task_type = 'factual'
    elif any(word in prompt_lower for word in ['why', 'how', 'explain', 'reason']):
        task_type = 'reasoning'
    elif any(word in prompt_lower for word in ['opinion', 'think', 'believe']):
        task_type = 'opinion'
    else:
        task_type = 'general'

    # 2. Determine Domain
    if any(word in prompt_lower for word in ['president', 'government', 'law', 'policy', 'minister', 'vote', 'election', 'polity', 'federal', 'constitution', 'india', 'court']):
        domain = 'politics'
    elif any(word in prompt_lower for word in ['code', 'python', 'java', 'computer', 'software', 'internet', 'technology', 'ai', 'data']):
        domain = 'technology'
    elif any(word in prompt_lower for word in ['school', 'university', 'student', 'teacher', 'learn', 'education']):
        domain = 'education'
    else:
        domain = 'general'
        
    # 3. Determine Answer Style
    word_count = len(output.split())
    if word_count < 20: 
        answer_style = 'concise'
    elif "is defined as" in output_lower or "refers to" in output_lower:
        answer_style = 'definition-based'
    elif word_count > 100:
        answer_style = 'descriptive'
    else:
        answer_style = 'explanatory'

    return {
        "task_type": task_type,
        "domain": domain,
        "answer_style": answer_style
    }
