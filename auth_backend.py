# auth_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import requests
from urllib.parse import urljoin
from django.conf import settings
import frappe_client  # Custom ERPNext client

User = get_user_model()

class ERPNextAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Initialize ERPNext client
        erp = frappe_client.FrappeClient(
            url=settings.ERP_NEXT_URL,
            api_key=settings.ERP_API_KEY,
            api_secret=settings.ERP_API_SECRET
        )
        
        try:
            # 1. Authenticate with ERPNext
            auth_response = erp.post_api("login", data={"usr": username, "pwd": password})
            
            if auth_response.get('message') == "Logged In":
                # 2. Get user details from ERPNext
                user_data = erp.get_doc("User", username)
                
                if not user_data.get('enabled', 0):
                    return None  # User disabled in ERPNext
                
                # 3. Get linked employee (if exists)
                employee = None
                if user_data.get('user_type') == 'System User':
                    employee = erp.get_value("Employee", {"user_id": username}, "name")
                
                # 4. Get linked sales person (if exists)
                sales_person = None
                if employee:
                    sales_person = erp.get_value("Sales Person", {"employee": employee}, "name")
                
                # 5. Create or update Django user
                user, created = User.objects.update_or_create(
                    username=username,
                    defaults={
                        'email': user_data.get('email') or username,
                        'first_name': user_data.get('first_name', ''),
                        'last_name': user_data.get('last_name', ''),
                        'is_active': user_data.get('enabled', 0),
                        'erpnext_user_id': username,
                        'employee_id': employee,
                        'sales_person_id': sales_person
                    }
                )
                
                return user
        except Exception as e:
            print(f"ERPNext Auth Error: {str(e)}")
            return None