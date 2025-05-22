import requests

ERP_URL = "http://your-erpnext-server"  # Replace with your ERPNext URL
API_KEY = "ac7cdc241be6b5b"
API_SECRET = "61c8a59ed49de1f"

# Example: Get current user details
headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}"
}

response = requests.get(f"{ERP_URL}/api/resource/User", headers=headers)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
