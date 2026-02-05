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
       - healthcare
       - finance
       - science
       - legal
       - history
       - entertainment
       - sports
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
    task_keywords = {
        'summarization': ['summarize', 'summary', 'brief', 'shorten', 'digest', 'abstract', 'tl;dr', 'tldr', 'overview'],
        'factual': ['what', 'who', 'when', 'where', 'which', 'define', 'definition', 'list', 'name', 'identify', 'state', 'describe', 'classification', 'type'],
        'reasoning': ['why', 'how', 'explain', 'reason', 'cause', 'effect', 'analyze', 'compare', 'contrast', 'justify', 'evaluate'],
        'opinion': ['opinion', 'think', 'believe', 'view', 'perspective', 'thoughts', 'feel', 'suggest', 'recommend', 'advice']
    }
    
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
    domain_keywords = {
        'politics': ['president', 'government', 'law', 'policy', 'minister', 'vote', 'election', 'polity', 'federal', 'constitution', 'india', 'court', 'democracy', 'parliament', 'legislature'],
        'technology': ['code', 'python', 'java', 'computer', 'software', 'internet', 'technology', 'ai', 'data', 'algorithm', 'app', 'digital', 'cyber', 'robot', 'cloud', 'server'],
        'education': ['school', 'university', 'student', 'teacher', 'learn', 'education', 'exam', 'class', 'course', 'degree', 'study', 'academic', 'college'],
        'healthcare': ['health', 'doctor', 'medicine', 'virus', 'biotech', 'hospital', 'patient', 'treatment', 'symptom', 'disease', 'cure', 'medical', 'clinic', 'therapy'],
        'finance': ['money', 'finance', 'economy', 'stock', 'market', 'bank', 'invest', 'tax', 'currency', 'business', 'profit', 'revenue', 'trade', 'loan'],
        'science': ['science', 'physics', 'chemistry', 'biology', 'space', 'research', 'experiment', 'lab', 'planet', 'universe', 'atom', 'molecule', 'energy', 'gravity'],
        'legal': ['legal', 'lawyer', 'judge', 'court', 'sue', 'rights', 'contract', 'statute', 'regulation', 'attorney', 'justice', 'verdict', 'litigation'],
        'history': ['history', 'historical', 'ancient', 'war', 'century', 'past', 'civilization', 'empire', 'kingdom', 'age', 'era', 'revolution', 'archaeology'],
        'entertainment': ['movie', 'music', 'art', 'song', 'film', 'actor', 'celebrity', 'cinema', 'drama', 'theatre', 'concert', 'band', 'album'],
        'sports': ['sport', 'game', 'player', 'team', 'match', 'score', 'win', 'lose', 'athlete', 'tournament', 'championship', 'olympic', 'league', 'ball']
    }

    best_domain = 'general'
    max_domain_score = 0
    
    for domain, keywords in domain_keywords.items():
        score = get_score(prompt_lower, keywords)
        if score > max_domain_score:
            max_domain_score = score
            best_domain = domain

    # --- 3. Determine Answer Style ---
    # Based on output characteristics
    word_count = len(output.split())
    
    if word_count < 30:
        answer_style = 'concise'
    elif "is defined as" in output_lower or "refers to" in output_lower or output_lower.startswith("definition:"):
        answer_style = 'definition-based'
    elif word_count > 120 or "\n- " in output or "\n1. " in output: # List or long text
        answer_style = 'descriptive'
    else:
        answer_style = 'explanatory'

    return {
        "task_type": best_task,
        "domain": best_domain,
        "answer_style": answer_style
    }
