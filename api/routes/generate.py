from fastapi import APIRouter, HTTPException
from api.schemas import GenerateRequest, GenerateResponse
from node1_answer_generator.answer_generator import generate_answer
from node2_explanation_generator.explanation_engine import build_explanation
from dotenv import load_dotenv

# Ensure environment variables are loaded (crucial for LLM key)
load_dotenv()

router = APIRouter()

@router.post("/generate-with-explanation", response_model=GenerateResponse)
def generate_with_explanation(request: GenerateRequest):
    """
    End-to-end pipeline: Generates an AI answer and provides an explanation.
    """
    try:
        # 1. Generate Answer (Node 1)
        answer = generate_answer(request.prompt)
        
        # 2. Generate Explanation (Node 2)
        # Node 2 expects (prompt, output)
        explanation_data = build_explanation(request.prompt, answer)
        
        return GenerateResponse(
            answer=answer,
            explanation=explanation_data["explanation"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
