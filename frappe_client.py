# frappe_client.py
import requests
import json

class FrappeClient:
    def __init__(self, url, api_key=None, api_secret=None):
        self.url = url.rstrip('/')
        self.session = requests.Session()
        if api_key and api_secret:
            self.session.headers.update({
                "Authorization": f"token {api_key}:{api_secret}",
                "Content-Type": "application/json"
            })
    
    def post_api(self, method, data):
        response = self.session.post(
            f"{self.url}/api/method/{method}",
            data=data
        )
        return response.json()
    
    def get_doc(self, doctype, name):
        response = self.session.get(
            f"{self.url}/api/resource/{doctype}/{name}"
        )
        return response.json().get('data', {})
    
    def get_value(self, doctype, filters, fieldname):
        params = {
            "filters": json.dumps(filters),
            "fields": json.dumps([fieldname])
        }
        response = self.session.get(
            f"{self.url}/api/resource/{doctype}",
            params=params
        )
        data = response.json().get('data', [])
        return data[0].get(fieldname) if data else None