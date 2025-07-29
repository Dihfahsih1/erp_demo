# sales_app/utils.py
import requests
import json
from django.conf import settings
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
def erpnext_api_request(endpoint, method="GET", data=None, params=None, request=None, files=None):
    """Generic function to interact with ERPNext API."""
    url = f"{settings.ERP_NEXT_URL}/api/resource/{endpoint}"
    cookies = {'sid': request.session.get('erpnext_session')} if request and request.session.get('erpnext_session') else {}
    if params:
        params = {k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in params.items()}
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.headers.pop('Expect', None)  # Explicitly disable Expect header
        
        logger.debug(f"Making {method} request to {url} with params: {params}, data: {data}, cookies: {cookies}")
        
        if method == "GET":
            response = session.get(url, params=params, cookies=cookies, timeout=10)
        elif method == "POST":
            response = session.post(url, json=data, cookies=cookies, files=files, timeout=10)
        elif method == "PUT":
            response = session.put(url, json=data, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}, URL: {url}, Response: {response.text if 'response' in locals() else 'No response'}")
        if request:
            messages.error(request, f"Error connecting to ERPNext: {str(e)}")
        return None