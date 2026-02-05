from fastapi import APIRouter, HTTPException
from api.schemas import ExplainRequest, ExplainResponse
from node2_explanation_generator.explanation_engine import build_explanation

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse)
def explain_output(request: ExplainRequest):
    """
    Standalone explainability endpoint.
    Takes an existing prompt and output, and returns an explanation with decision trace.
    """
    try:
        # Call Node 2 to build explanation and trace
        result = build_explanation(request.prompt, request.output)
        
        return ExplainResponse(
            explanation=result["explanation"],
            decision_trace=result["decision_trace"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
