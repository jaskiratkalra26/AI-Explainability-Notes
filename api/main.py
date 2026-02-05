import sys
import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to python path to allow imports from node1 and node2
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
src_dir = os.path.join(root_dir, "src")
sys.path.append(src_dir)

from api.routes import generate, explain, health

app = FastAPI(
    title="Explainability Notes for AI Decisions",
    description="API for generating AI responses with post-hoc explainability."
)

# Register routers
app.include_router(generate.router)
app.include_router(explain.router)
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
