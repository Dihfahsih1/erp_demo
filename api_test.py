import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
ERP_URL = os.getenv("ERP_URL")
API_KEY = os.getenv("ERP_API_KEY")
API_SECRET = os.getenv("ERP_API_SECRET")

# Set up headers
headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

SALES_ORDERS_ENDPOINT = "/api/resource/Sales Order"  # Common for Frappe/ERPNext

try:    
    response = requests.get(
        f"{ERP_URL}{SALES_ORDERS_ENDPOINT}",
        headers=headers,
        params={
            "fields": "[\"name\", \"customer\", \"total\", \"status\"]",  # Request specific fields
            "limit_page_length": 100  # Limit results
        }
    )

    if response.status_code == 200:
        sales_orders = response.json().get("data", [])
        print(f"Found {len(sales_orders)} sales orders:")
        for order in sales_orders:
            print(f"ID: {order.get('name')}, Customer: {order.get('customer')}, Total: {order.get('total')}")
    else:
        print(f"Error: {response.status_code}", response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {str(e)}")