import os
import requests
from dotenv import load_dotenv
from datetime import date

# Load environment variables from .env file
load_dotenv()

# Get ERP credentials from environment
ERP_URL = os.getenv("ERP_URL")
API_KEY = os.getenv("ERP_API_KEY")
API_SECRET = os.getenv("ERP_API_SECRET")

# Set up request headers
headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

# Endpoint to access Sales Orders
SALES_ORDERS_ENDPOINT = "/api/resource/Sales Order"

# Get today's date in YYYY-MM-DD format
today_str = "2025-08-01"  # e.g., "2025-08-04"

# Prepare filter for today's sales orders
params = {
    "fields": '["name", "customer", "transaction_date", "total", "status"]',
    "filters": f'[["transaction_date", "=", "{today_str}"]]',
    "limit_page_length": 100
}

try:
    # Make GET request to ERPNext
    response = requests.get(
        f"{ERP_URL}{SALES_ORDERS_ENDPOINT}",
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        sales_orders = response.json().get("data", [])
        print(f"Found {len(sales_orders)} sales orders for {today_str}:")
        for order in sales_orders:
            print(f"ID: {order.get('name')}, Date: {order.get('transaction_date')}, Customer: {order.get('customer')}, Total: {order.get('total')}, Status: {order.get('status')}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {str(e)}")
