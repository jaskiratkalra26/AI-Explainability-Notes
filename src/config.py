
config = {
    "gemini": {
        "model_name": "gemini-2.5-flash",
        "api_key_env_var": "GEMINI_API_KEY",
        "generation_config": {
            "max_output_tokens": 3000,
            "temperature": 1
        }
    },
    "metadata_extractor": {
        "system_instruction": """You are a metadata extraction engine. Your job is to analyze the following USER PROMPT and AI OUTPUT
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
""",
        "task_keywords": {
            "summarization": ['summarize', 'summary', 'brief', 'shorten', 'digest', 'abstract', 'tl;dr', 'tldr', 'overview'],
            "factual": ['what', 'who', 'when', 'where', 'which', 'define', 'definition', 'list', 'name', 'identify', 'state', 'describe', 'classification', 'type'],
            "reasoning": ['why', 'how', 'explain', 'reason', 'cause', 'effect', 'analyze', 'compare', 'contrast', 'justify', 'evaluate'],
            "opinion": ['opinion', 'think', 'believe', 'view', 'perspective', 'thoughts', 'feel', 'suggest', 'recommend', 'advice']
        },
        "domain_keywords": {
            "politics": ['president', 'government', 'law', 'policy', 'minister', 'vote', 'election', 'polity', 'federal', 'constitution', 'india', 'court', 'democracy', 'parliament', 'legislature'],
            "technology": ['code', 'python', 'java', 'computer', 'software', 'internet', 'technology', 'ai', 'data', 'algorithm', 'app', 'digital', 'cyber', 'robot', 'cloud', 'server'],
            "education": ['school', 'university', 'student', 'teacher', 'learn', 'education', 'exam', 'class', 'course', 'degree', 'study', 'academic', 'college'],
            "healthcare": ['health', 'doctor', 'medicine', 'virus', 'biotech', 'hospital', 'patient', 'treatment', 'symptom', 'disease', 'cure', 'medical', 'clinic', 'therapy'],
            "finance": ['money', 'finance', 'economy', 'stock', 'market', 'bank', 'invest', 'tax', 'currency', 'business', 'profit', 'revenue', 'trade', 'loan'],
            "science": ['science', 'physics', 'chemistry', 'biology', 'space', 'research', 'experiment', 'lab', 'planet', 'universe', 'atom', 'molecule', 'energy', 'gravity'],
            "legal": ['legal', 'lawyer', 'judge', 'court', 'sue', 'rights', 'contract', 'statute', 'regulation', 'attorney', 'justice', 'verdict', 'litigation'],
            "history": ['history', 'historical', 'ancient', 'war', 'century', 'past', 'civilization', 'empire', 'kingdom', 'age', 'era', 'revolution', 'archaeology'],
            "entertainment": ['movie', 'music', 'art', 'song', 'film', 'actor', 'celebrity', 'cinema', 'drama', 'theatre', 'concert', 'band', 'album'],
            "sports": ['sport', 'game', 'player', 'team', 'match', 'score', 'win', 'lose', 'athlete', 'tournament', 'championship', 'olympic', 'league', 'ball']
        },
        "style_thresholds": {
            "concise_max_words": 30,
            "descriptive_min_words": 120
        }
    },
    "validator": {
        "forbidden_phrases": [
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
        ],
        "default_fallback": "This response was generated based on the prompt intent and output characteristics.",
        "max_sentences": 3
    }
}
