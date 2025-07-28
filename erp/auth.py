# sales_app/auth.py
import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings

class ERPNextAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            session = requests.Session()
            login_url = f"{settings.ERP_NEXT_URL}/api/method/login"
            login_response = session.post(login_url, data={'usr': username, 'pwd': password})

            if login_response.status_code == 200:
                user_url = f"{settings.ERP_NEXT_URL}/api/resource/User/{username}"
                user_response = session.get(user_url, headers={
                    "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}"
                })

                if user_response.status_code == 200:
                    user_info = user_response.json().get('data', {})
                    User = get_user_model()
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={
                            'first_name': user_info.get('first_name', ''),
                            'last_name': user_info.get('last_name', ''),
                            'email': user_info.get('email', username)
                        }
                    )
                    # Save ERPNext session ID in Django session
                    request.session['erpnext_session'] = session.cookies.get('sid')
                    return user
                return None
            return None
        except requests.RequestException:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None