# Explainability Notes for AI Decisions

This project is an AI-powered system designed to not only generate answers to user queries but also provide **post-hoc explanations** for how those answers were derived. It uses a two-node architecture: one for generating the content (using Google Gemini) and another for analyzing the context to build a decision trace and explanation.

## Features

- **node1_answer_generator**: Generates AI responses using Google's Gemini models.
- **node2_explanation_generator**: Analyzes prompt intent, domain, and answer style to construct a human-readable explanation and decision trace.
- **FastAPI Interface**: Exposes endpoints for generating answers with explanations or explaining existing outputs.
- **Configurable**: Metadata extraction rules and API settings are easily configurable.

## Project Structure

```
├── api/                  # FastAPI application and routes
│   ├── routes/           # API endpoints (generate, explain, health)
│   ├── main.py           # Application entry point
│   └── schemas.py        # Pydantic models
├── scripts/              # Helper scripts for testing and running pipelines
├── src/                  # Core logic
│   ├── config.py         # Configuration settings
│   ├── node1_answer_generator/  # LLM Client and Answer Logic
│   └── node2_explanation_generator/ # Explanation Engine, Validators, Metadata
├── .env                  # Environment variables (not committed)
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- A Google Gemini API Key

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd explainability-notes-ai
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup:**
    Create a `.env` file in the root directory and add your Google Gemini API Key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

### Running the API Server

Start the FastAPI server using uvicorn:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the automatic documentation at `http://localhost:8000/docs`.

### API Endpoints

-   **`POST /generate-with-explanation`**
    -   Generates an answer using Gemini and provides an explanation.
    -   **Body:** `{"prompt": "Your question here"}`
    
-   **`POST /explain`**
    -   Generates an explanation for a provided prompt and output pair.
    -   **Body:** `{"prompt": "...", "output": "..."}`

-   **`GET /health`**
    -   Health check endpoint.

### Running Scripts

You can run individual test scripts to verify components:

```bash
# Test the explanation generation logic
python scripts/test_node2.py
```

## Configuration

Configuration settings for models, metadata extraction rules, and validation thresholds are located in `src/config.py`.


