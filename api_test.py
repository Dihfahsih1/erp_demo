import requests

ERP_URL = "http://localhost:8000"
API_KEY = "ac7cdc241be6b5b"
API_SECRET = "61c8a59ed49de1f"

headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

data = {
    "email": "newuser@example.com",
    "first_name": "New",              # Mandatory
    "last_name": "User",              # Optional but recommended
    "full_name": "New User",          # Optional, but good to have
    "enabled": 1,
    "user_type": "System User",
    "roles": [
        {"role": "System Manager"}   # Assign at least one role
    ]
}

response = requests.post(f"{ERP_URL}/api/resource/User", headers=headers, json=data)

if response.status_code in (200, 201):
    print("User created:", response.json())
else:
    print("Error:", response.status_code, response.text)
