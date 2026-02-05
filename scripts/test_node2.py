import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from node2_explanation_generator import build_explanation

def test_explanation():
    test_cases = [
        {
            "prompt": "What type of federal system does India follow?",
            "output": "India follows a quasi-federal system."
        },
        {
            "prompt": "Summarize the history of AI in 5 words.",
            "output": "AI evolved from rules to learning."
        }
    ]

    for i, case in enumerate(test_cases):
        print(f"--- Test Case {i+1} ---")
        print(f"Prompt: {case['prompt']}")
        print(f"Output: {case['output']}")
        
        result = build_explanation(case['prompt'], case['output'])
        
        print("Result:")
        print(result)
        print("\n")

if __name__ == "__main__":
    test_explanation()
