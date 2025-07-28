# sales_app/utils.py
import requests
from django.conf import settings

def erpnext_api_request(endpoint, method="GET", data=None, params=None, request=None):
    """Generic function to interact with ERPNext API."""
    url = f"{settings.ERP_NEXT_URL}/api/resource/{endpoint}"
    headers = {
        "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Expect": ""
    }
    cookies = {}
    if request and 'erpnext_session' in request.session:
        cookies['sid'] = request.session['erpnext_session']

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, cookies=cookies)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error connecting to ERPNext: {str(e)}")
        return None