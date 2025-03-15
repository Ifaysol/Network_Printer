import requests
from config import PRINT_API

def send_print_request(file_path):
    """Sends a print request by uploading the file to the backend"""
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(PRINT_API, files=files, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
