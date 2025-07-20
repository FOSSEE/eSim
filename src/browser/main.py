import requests

# Note: The URL "http://192.168.243.207:5000/chat" will be updated based on the hosting server's provided link.
def get_bot_response(prompt: str) -> str:
    try:
        res = requests.post("http://192.168.243.207:5000/chat", json={"prompt": prompt})
        return res.json().get("response", "No response")
    except Exception as e:
        return f"Error: {str(e)}"
