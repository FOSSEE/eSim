import subprocess

def explain_simulation_error(error_message):

    prompt = f"""
You are an expert electronic engineer helping debug circuits in eSim.

Simulation Error:
{error_message}

Explain the problem and suggest how to fix it.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5-coder:3b", prompt],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as e:
        return f"Error running AI model: {str(e)}"


if __name__ == "__main__":

    test_error = "Error: floating node detected at node N3"

    explanation = explain_simulation_error(test_error)

    print("Simulation Error:")
    print(test_error)

    print("\nAI Explanation:")
    print(explanation)
