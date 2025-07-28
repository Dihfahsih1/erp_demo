from collections import defaultdict
from venv import logger
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_POST
from django.views .decorators.csrf import csrf_exempt
from django.urls import reverse
import requests
from erp.forms import BillingForm, DispatchForm, DeliveryForm, EstimateForm, DeliveryUploadForm, DispatchVerificationForm, EstimateUploadForm, OfficerReviewForm, SalesAgentNoteForm, CustomerForm, EmployeeLoginForm, EmployeeRegistrationForm
from erp_demo import settings
from .models import Customer, Delivery, DeliveryImage, Dispatch, Employee, Estimate, UserRole
import json
import pandas as pd
from io import BytesIO
from datetime import datetime
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
import pandas as pd
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages


import requests
from django.http import JsonResponse
from django.conf import settings

# sales_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

# sales_app/views.py
from django.contrib.auth import logout

def erpnext_logout(request):
    if 'erpnext_session' in request.session:
        del request.session['erpnext_session']
    logout(request)
    return redirect('login')

def erpnext_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            try:
                # Check ERPNext response for specific error
                session = requests.Session()
                login_url = f"{settings.ERP_NEXT_URL}/api/method/login"
                login_response = session.post(login_url, data={'usr': username, 'pwd': password})
                if login_response.status_code != 200:
                    error_info = login_response.json()
                    frappe_msg = error_info.get('message', 'Invalid ERPNext credentials')
                    messages.error(request, f"ERPNext error: {frappe_msg}")
                else:
                    messages.error(request, 'Failed to fetch user info from ERPNext')
            except Exception as e:
                messages.error(request, f"Error connecting to ERPNext: {e}")

    return render(request, 'accounts/login.html')

HEADERS = {
    "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Expect": ""  
}

def erpnext_api_request(endpoint, method="GET", data=None, params=None):
    """Generic function to interact with ERPNext API."""
    url = f"{settings.ERP_NEXT_URL}/api/resource/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"Error connecting to ERPNext: {str(e)}")
        return None

def sales_dashboard(request):
    # Fetch latest 10 sales orders
    sales_orders = []
    customers = []
    delivery_notes = []

    try:
        so_resp = requests.get(
            f"{settings.ERP_NEXT_URL}/api/resource/Sales Order",
            headers=HEADERS,
            params={"limit_page_length": 10, "order_by": "creation desc"}
        )
        sales_orders = so_resp.json().get("data", [])

        cust_resp = requests.get(
            f"{settings.ERP_NEXT_URL}/api/resource/Customer",
            headers=HEADERS,
            params={"limit_page_length": 5}
        )
        customers = cust_resp.json().get("data", [])

        dn_resp = requests.get(
            f"{settings.ERP_NEXT_URL}/api/resource/Delivery Note",
            headers=HEADERS,
            params={"limit_page_length": 5}
        )
        delivery_notes = dn_resp.json().get("data", [])

    except Exception as e:
        print("Error connecting to ERP:", str(e))

    return render(request, "sales_dashboard.html", {
        "sales_orders": sales_orders,
        "customers": customers,
        "delivery_notes": delivery_notes
    })

def fetch_sales_person_performance():
    """Fetches sales data from ERPNext API"""
    headers = {
        "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}",
        "Content-Type": "application/json"
    }
    
    # 1. Get all sales persons
    response = requests.get(
        f"{settings.ERP_NEXT_URL}/api/resource/Sales Person",
        headers=headers
    )
    sales_persons = response.json().get("data", [])
    
    # 2. Get performance data for each
    performance_data = []
    for person in sales_persons:
        detail_response = requests.get(
            f"{settings.ERP_NEXT_URL}/api/resource/Sales Person/{person['name']}",
            headers=headers
        )
        data = detail_response.json().get("data", {})
        
        performance_data.append({
            "name": data.get("sales_person_name", person['name']),
            "achieved": float(data.get("total_sales", 0)),  # Use your actual field
            "commission": data.get("commission_rate", 0)
        })
    
    return performance_data

def sales_performance_dashboard(request):
    # Fetch data from ERPNext (modified to exclude targets)
    performance_data = []
    sales_persons = requests.get(
        f"{settings.ERP_NEXT_URL}/api/resource/Sales Person",
        headers=HEADERS
    ).json().get("data", [])
    
    for person in sales_persons:
        sales_data = requests.get(
            f"{settings.ERP_NEXT_URL}/api/resource/Sales Person/{person['name']}",
            headers=HEADERS
        ).json().get("data", {})
        
        performance_data.append({
            "name": sales_data.get("sales_person_name", person['name']),
            "achieved": sales_data.get("total_sales", 0),  # Use your actual sales field
            "commission": sales_data.get("commission_rate", 0)
        })
    
    # Create bar chart
    df = pd.DataFrame(performance_data)
    fig = px.bar(
        df,
        x="name",
        y="achieved",
        title="Sales Performance by Person",
        labels={"achieved": "Total Sales ($)", "name": "Sales Person"},
        color="commission",  # Color by commission rate
        color_continuous_scale="Blues"
    )
    
    return render(request, "dashboard.html", {
        "performance_data": performance_data,
        "graph_html": fig.to_html(full_html=False)
    })


import plotly.express as px
import pandas as pd

def sales_performance_dashboard(request):
    # Get data from ERPNext
    performance_data = fetch_sales_person_performance()
    
    # Convert to DataFrame
    df = pd.DataFrame(performance_data)
    
    # Create bar chart
    fig = px.bar(
        df,
        x="name",
        y=["target", "achieved"],
        barmode="group",
        title="Sales Performance: Target vs Achieved",
        labels={"value": "Amount ($)", "name": "Sales Person"},
        color_discrete_sequence=["#FFA07A", "#20B2AA"]  # Custom colors
    )
    
    # Convert plot to HTML
    graph_html = fig.to_html(full_html=False)
    
    return render(request, "dashboard.html", {"graph_html": graph_html})

 


        
 
 



import json
import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from requests.exceptions import HTTPError
from django.conf import settings

def get_customer_fields(request):
    try:
        # Get the Customer doctype definition
        url = f"{settings.ERP_NEXT_URL}/api/resource/DocType/Customer"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        doctype_info = response.json().get('data', {})
        
        # Extract field definitions
        fields = []
        for field in doctype_info.get('fields', []):
            fields.append({
                'fieldname': field.get('fieldname'),
                'label': field.get('label'),
                'fieldtype': field.get('fieldtype'),
                'options': field.get('options'),
                'reqd': field.get('reqd', False),
                'read_only': field.get('read_only', False),
                'description': field.get('description')
            })
        
        # Get child table definitions
        child_tables = []
        for table in doctype_info.get('fields', []):
            if table.get('fieldtype') == 'Table':
                child_tables.append({
                    'fieldname': table.get('fieldname'),
                    'label': table.get('label'),
                    'options': table.get('options')  # This is the child doctype name
                })
        
        return JsonResponse({
            'doctype': 'Customer',
            'fields': fields,
            'child_tables': child_tables,
            'meta': {
                'is_submittable': doctype_info.get('is_submittable', False),
                'istable': doctype_info.get('istable', False),
                'custom': doctype_info.get('custom', False)
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'response': getattr(e, 'response', {}).text if hasattr(e, 'response') else None
        }, status=500)
        



def sales_persons(request):
    """Get all sales persons with extended information"""
    try:
        url = f"{settings.ERP_NEXT_URL}/api/resource/Sales Person"
        params = {
            "fields": json.dumps([
                "name",
                "sales_person_name",
                "employee",
                "enabled",
                "parent_sales_person",
                "commission_rate",
                "territory"
            ]),
            "limit_page_length": 1000
        }
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json().get("data", [])
        return JsonResponse({
            'sales_persons': data,
            'count': len(data)
        }, status=200)
    
    except requests.exceptions.HTTPError as e:
        return JsonResponse({
            'error': 'API request failed',
            'details': str(e),
            'response': e.response.text if hasattr(e, 'response') else None
        }, status=500)
    
    except Exception as e:
        return JsonResponse({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)

import requests
from requests.exceptions import HTTPError
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
import json

HEADERS = {
    "Authorization": f"token {settings.ERP_API_KEY}:{settings.ERP_API_SECRET}",
    "Content-Type": "application/json"
}

def customer_sales_dashboard(request):
    try:
        # Fetch all sales persons for ID-to-name mapping
        sales_persons = {}
        sales_url = f"{settings.ERP_NEXT_URL}/api/resource/Sales Person"
        sales_params = {
            "fields": json.dumps(["name", "sales_person_name"]),
            "limit_page_length": 1000
        }
        sales_response = requests.get(sales_url, headers=HEADERS, params=sales_params)
        sales_response.raise_for_status()
        
        for sp in sales_response.json().get("data", []):
            sales_persons[sp['name']] = sp['sales_person_name']

        # Fetch customers (first 100, more on-demand via search/pagination)
        customers_url = f"{settings.ERP_NEXT_URL}/api/resource/Customer"
        customers_params = {
            "fields": json.dumps(["name", "customer_name"]),
            "limit_page_length": 100  # fetch first 100 customers (can adjust)
        }
        customers_response = requests.get(customers_url, headers=HEADERS, params=customers_params)
        customers_response.raise_for_status()
        customers_list = customers_response.json().get("data", [])

        customer_data = []

        # For each customer, fetch their sales_team child table
        for customer in customers_list:
            customer_name = customer.get('name')

            # Fetch full Customer document to get sales_team
            single_customer_url = f"{settings.ERP_NEXT_URL}/api/resource/Customer/{customer_name}"
            single_customer_response = requests.get(single_customer_url, headers=HEADERS)
            single_customer_response.raise_for_status()
            full_customer = single_customer_response.json().get("data", {})

            sales_team = full_customer.get('sales_team', [])

            # Determine primary sales person
            primary_sales_person = None
            for member in sales_team:
                if member.get('allocated_percentage') == 100:
                    primary_sales_person = member.get('sales_person')
                    break
                elif not primary_sales_person:
                    primary_sales_person = member.get('sales_person')

            customer_data.append({
                'id': customer_name,
                'name': customer.get('customer_name', customer_name),
                'sales_person_id': primary_sales_person,
                'sales_person': sales_persons.get(primary_sales_person, 'Not Assigned')
            })

        # Paginate results
        paginator = Paginator(customer_data, 50)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return render(request, 'customer_sales_dashboard.html', {
            'page_obj': page_obj,
            'total_customers': len(customer_data)
        })

    except Exception as e:
        return render(request, 'error.html', {
            'error_message': f"Failed to load data: {str(e)}",
            'title': 'Data Loading Error'
        })
def get_sales_persons():
    """Fetch all active sales persons"""
    url = f"{settings.ERP_NEXT_URL}/api/resource/Sales Person"
    params = {
        "fields": json.dumps([
            "name",
            "sales_person_name",
            "employee",
            "territory",
            "enabled"
        ]),
        "filters": json.dumps([["enabled", "=", 1]]),
        "limit_page_length": 1000
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("data", [])

def get_customers_for_sales_person(sales_person_name):
    """Get customers assigned to a specific sales person"""
    url = f"{settings.ERP_NEXT_URL}/api/resource/Customer"
    params = {
        "fields": json.dumps(["name", "customer_name"]),
        "filters": json.dumps([["sales_team.sales_person", "=", sales_person_name]]),
        "limit_page_length": 1000
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("data", [])

def get_customer_details(customer_id):
    """Get detailed information about a specific customer"""
    url = f"{settings.ERP_NEXT_URL}/api/resource/Customer/{customer_id}"
    params = {
        "fields": json.dumps([
            "customer_name",
            "territory",
            "customer_group",
            "mobile_no",
            "email_id",
            "primary_address",
            "tax_id",
            "default_price_list"
        ])
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("data", {})
     
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_employee(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = EmployeeLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-date_filled')
    paginator = Paginator(customers, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer_list.html', {'page_obj': page_obj})
 
@login_required
def register_customer(request):
    submitted = False
    user = request.user  

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CustomerForm()
            submitted = True
    else:
        form = CustomerForm()
 
    form.fields['prepared_by'].widget.attrs.update({
        'readonly': 'readonly',
        'placeholder': user.get_full_name() or user.username
    })

    return render(request, 'register_customer.html', {'form': form, 'submitted': submitted})


@login_required
def customer_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_view.html', {'customer': customer})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {'form': form, 'edit_mode': True})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')

@login_required
@require_http_methods(["PATCH"])
def mark_delivered(request, dispatch_id):
    try:
        dispatch = Dispatch.objects.get(pk=dispatch_id)
        dispatch.mark_as_delivered()
        return JsonResponse({
            'status': 'success',
            'message': 'Dispatch marked as delivered'
        })
    except Dispatch.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Dispatch not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    
@login_required
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'active_page': 'dashboard',
    }
    return render(request, 'index.html', context)

@login_required
def dispatch_view(request):
   
    """
    Simplified dispatch view that handles:
    - GET: Show empty form
    - POST: Save form data to database
    - PATCH (AJAX): Mark dispatch as delivered
    """
    
    if request.method == 'GET':
        # Show empty form
        form = DispatchForm()
        return render(request, 'dispatch_form.html', {'form': form})
        
    elif request.method == 'POST':
         
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatch = form.save()
            messages.success(request, _("Dispatch saved successfully!"))
            return redirect('mark_dispatch_delivered')   
        else:
             
            return render(request, 'dispatch_form.html', {'form': form})
    
    elif request.method == 'PATCH' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            data = json.loads(request.body)
            dispatch_id = data.get('dispatch_id')
            if not dispatch_id:
                return HttpResponseBadRequest(_("Missing dispatch ID"))
            
            dispatch = Dispatch.objects.get(pk=dispatch_id)
            dispatch.mark_as_delivered()
            return JsonResponse({
                'status': 'success',
                'message': _("Marked as delivered"),
                'is_delivered': True
            })
            
        except Dispatch.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': _("Dispatch not found")
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': _(f"Error: {str(e)}")
            }, status=400)
    
    return HttpResponseBadRequest(_("Invalid request"))

@login_required
def dispatch_list_view(request):
    """
    Display all submitted dispatches in a table format
    """
    dispatches = Dispatch.objects.all().order_by('-billing_date')
    
    context = {
        'dispatches': dispatches,
        'table_headers': [
            _("Estimate ID"),
            _("Proforma ID"),
            _("Transport Cost"),
            _("Vehicle"),
            _("Driver"),
            _("Contact"),
            _("Dispatch Time"),
            _("Status"),
            _("Actions")
        ]
    }
    return render(request, 'dispatch_list.html', context)

 
from django.utils import timezone

@login_required 
def record_billing(request, estimate_id):
    estimate = get_object_or_404(Estimate, id=estimate_id, status='verified')

    if request.method == 'POST':
        form = BillingForm(request.POST, instance=estimate)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.billing_officer = request.user
            billing.status = 'billed'
            billing.date_billed = timezone.now()  # set billing date automatically
            billing.save()
            return redirect('billed_estimates_list')
    return redirect('billed_estimates_list') 

@login_required
def all_billed_estimates(request):
    employees = Employee.objects.filter(department__name='Stores')
    billed_estimates = Estimate.objects.filter(status__in=['billed', 'dispatchready', 'dispatched']).order_by('-date_billed')
  
    return render(request, 'billed_estimates_list.html', 
                  {'billed_estimates': billed_estimates,
                   'employees': employees
                  }) 

@login_required
def record_estimate(request):
    sales_persons = Employee.objects.filter(role__name='Sales Officer')
    if request.method == 'POST': 
        form = EstimateForm(request.POST)
        print(form.errors)
        if form.is_valid():
            try:
                estimate = form.save(commit=False)
                estimate.created_by = request.user 
                # Ensure sales person is properly assigned
                if hasattr(form, 'cleaned_data') and 'sales_person' in form.cleaned_data:
                    estimate.sales_person = form.cleaned_data['sales_person']
                
                estimate.save()
                messages.success(request, "Estimate created successfully!")
                return redirect('list_estimates')
                
            except Exception as e:
                messages.error(request, f"Error saving estimate: {str(e)}")
    else:
        form = EstimateForm(initial={
            'status': Estimate.Status.SUBMITTED,
            'bk_estimate_id': generate_estimate_id(request),
            
        })
    
    return render(request, 'record_estimate.html', {'form': form,'sales_person': sales_persons})


@login_required
@require_POST
def update_stock(request, pk): 
    estimate = get_object_or_404(Estimate, pk=pk)
    
    if estimate.status != Estimate.Status.VERIFIED:
        return JsonResponse({'error': 'Can only update stock for verified estimates'}, status=400)
    
    stock_status = request.POST.get('stock_status') 
    if stock_status not in dict(Estimate.StockStatus.choices):
        return JsonResponse({'error': 'Invalid stock status'}, status=400)
    
    estimate.stock_status = stock_status
    estimate.save()
    
    return JsonResponse({
        'success': True,
        'display_status': estimate.get_stock_status_display()
    })

def autocomplete_customers(request):
    term = request.GET.get('term', '')
    customers = Customer.objects.filter(
        owner_name__icontains=term
    ).values('id', 'owner_name')[:10]
    
    return JsonResponse({
        'results': [
            {'id': cust['id'], 'text': cust['owner_name']} 
            for cust in customers
        ]
    })


def estimate_detail(request, pk):
    estimate = get_object_or_404(Estimate, pk=pk)
    return render(request, 'estimates/detail.html', {'estimate': estimate})

@login_required
def handle_excel_upload(request):
    upload_form = EstimateUploadForm(request.POST, request.FILES)
    
    if not upload_form.is_valid():
        for error in upload_form.errors.values():
            messages.error(request, error)
        return redirect('record_estimate')
    
    try:
        excel_file = request.FILES['excel_file']
        
        # Validate file extension
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            raise ValueError("Only .xlsx or .xls files are allowed")
        
        with transaction.atomic():
            df = pd.read_excel(excel_file)
            required_columns = ['bk_estimate_id', 'customer', 'status']
            
            # Validate required columns
            if not all(col in df.columns for col in required_columns):
                missing = set(required_columns) - set(df.columns)
                raise ValueError(f"Missing required columns: {', '.join(missing)}")
            
            success_count = 0
            for index, row in df.iterrows():
                try:
                    # Get or create customer
                    customer, _ = Customer.objects.get_or_create(
                        owner_name=row['customer'].strip()
                    )
                    
                    # Create estimate
                    Estimate.objects.create(
                        bk_estimate_id=row['bk_estimate_id'].strip(),
                        owner_name=customer,
                        sales_person=row.get('sales_person') or request.user.get_full_name() or request.user.username,
                        status=row.get('status', Estimate.Status.DRAFT),
                        created_date=row.get('created_date', datetime.now()),
                        created_by=request.user
                    )
                    success_count += 1
                    
                except Exception as e:
                    messages.warning(
                        request, 
                        f"Row {index + 2}: {str(e)}"
                    )
                    continue
            
            messages.success(
                request, 
                f"Successfully imported {success_count} estimates!"
            )
            return redirect('list_estimates')
    
    except Exception as e:
        messages.error(request, f"Error processing Excel file: {str(e)}")
        
        return redirect('record_estimate')
    
@login_required
def generate_estimate_id(request):
    """Generate a new estimate ID in EST-YYYY-NNNN format"""
    from django.utils import timezone
    year = timezone.now().strftime('%Y')
    last_estimate = Estimate.objects.order_by('-bk_estimate_id').first()
    if last_estimate:
        last_num = int(last_estimate.bk_estimate_id.split('-')[-1])
        return f"EST-{year}-{last_num + 1:04d}"
    return f"EST-{year}-0001"


@login_required
def list_estimates(request):

    estimates = Estimate.objects.all().order_by('-created_at') 

    # Pagination
    paginator = Paginator(estimates, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Estimate.Status.choices,
        'can_change_status': request.user.has_perm('estimates.change_estimate_status'),
    }
    return render(request, 'list_estimates.html', context)

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Estimate

def estimate_search(request):
    query = request.GET.get('q', '')
    estimates = Estimate.objects.filter(
        Q(bk_estimate_id__icontains=query) |
        Q(customer_name__owner_name__icontains=query) |
        Q(sales_person__username__icontains=query)  # or .first_name if you prefer
    ).order_by('-created_at')

    paginator = Paginator(estimates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/estimate_table.html', {'page_obj': page_obj})
    else:
        return render(request, 'your_main_template.html', {'page_obj': page_obj})


@login_required
def estimate_action(request, pk):
    estimate = get_object_or_404(Estimate, pk=pk)
    action = request.POST.get("action")

    # Only credit officers can perform these actions
    if request.user.role.name != "Credit Officer":
        messages.error(request, "You are not authorized to perform this action.")
        return redirect(estimate.get_absolute_url())

    if action == "verify":
        estimate.status = Estimate.Status.VERIFIED
        messages.success(request, "Estimate verified successfully.")
    elif action == "on-hold":
        estimate.status = Estimate.Status.ON_HOLD
        messages.warning(request, "Estimate put on hold.")
    elif action == "reject":
        estimate.status = Estimate.Status.REJECTED
        messages.error(request, "Estimate rejected.")
    # elif action == "cancel":
    #     estimate.status = Estimate.Status.CANCELLED
    #     messages.error(request, "Estimate cancelled.")
    else:
        messages.error(request, "Invalid action.")

    estimate.date_verified = timezone.now()  
    estimate.verified_by = request.user
    estimate.save()
    return redirect(request.META.get("HTTP_REFERER", estimate.get_absolute_url()))
 
 
 
def submit_hold_reason(request, pk):
    if request.method == 'POST':
        estimate = get_object_or_404(Estimate, pk=pk)
        reason = request.POST.get('hold_reason')
        if reason:
            estimate.hold_reason = reason
            estimate.save()
            messages.success(request, "Hold reason submitted successfully.")
        else:
            messages.error(request, "Reason cannot be empty.")
    return redirect(request.META.get('HTTP_REFERER', 'estimates-list')) 

@login_required
def download_estimate_template(request):
    # Create a sample DataFrame
    data = {
        'bk_estimate_id': ['EST-2023-0001', 'EST-2023-0002'],
        'customer': ['Customer A', 'Customer B'],
        'sales_person': ['Agent 1', 'Agent 2'],
        'status': ['draft', 'submitted'],
        'created_at': [datetime.now(), datetime.now()]
    }
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Estimates')
    
    # Prepare response
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=estimate_template.xlsx'
    return response

from django.utils import timezone

@login_required
def verify_dispatch(request, dispatch_id):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_id)
    
    # Get the estimate if exists
    estimate = None
    if dispatch.estimate:
        estimate = Estimate.objects.filter(bk_estimate_id=dispatch.estimate).first()
    
    if request.method == 'POST':
        form = DispatchVerificationForm(request.POST, instance=dispatch)
        if form.is_valid():
            if 'verify' in request.POST:
                dispatch = form.save(commit=False)
                dispatch.mark_as_in_transit()
                messages.success(request, 'Dispatch verified and marked as In Transit!')
            elif 'cancel' in request.POST:
                dispatch = form.save(commit=False)
                messages.warning(request, 'Dispatch cancelled with reason.')
            return redirect('dispatch-detail', dispatch_id=dispatch.id)
    else:
        form = DispatchVerificationForm(instance=dispatch)
    
    context = {
        'dispatch': dispatch,
        'estimate': estimate,
        'form': form,
        'now': timezone.now().strftime("%Y-%m-%d %H:%M"),
    }
    return render(request, 'verify_dispatch.html', context)
 
@require_POST
def confirm_delivery(request, pk):
    note = get_object_or_404(Delivery, pk=pk)
    note.status = 'confirmed'
    note.save()
    return JsonResponse({'success': True})


sales_exec_role = UserRole.objects.filter(name='Sales Executive').first()
@login_required
def create_delivery_note(request, pk):
    estimate = get_object_or_404(Estimate, pk=pk)
    
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery_note = form.save(commit=False)
            delivery_note.estimate_number = estimate
            delivery_note.sales_person = estimate.sales_person
            
            # Handle delivery method
            delivery_method = request.POST.get('delivery_method')
            if delivery_method == 'stores':
                delivery_note.delivery_person_id = request.POST.get('delivery_person')
                delivery_note.delivery_by_customer = None
            elif delivery_method == 'customer':
                delivery_note.delivery_by_customer = request.POST.get('delivery_by_customer')
                delivery_note.delivery_person = None
            
            delivery_note.save()
            estimate.delivery_note = delivery_note
            estimate.status = 'dispatched'
            estimate.save()
            
            messages.success(request, "Delivery note created successfully.")
            return redirect('delivery_note_list')
    
    messages.error(request, "Invalid request.")
    return redirect('delivery_estimates')

@csrf_exempt
def create_dispatch_details(request, pk):
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatch = form.save(commit=False)
            estimate = get_object_or_404(Estimate, pk=pk)
            dispatch.estimate_number = estimate
            dispatch.save()
            estimate.status = 'dispatchready'
            estimate.save()

            return redirect("billed_estimates_list")
        else:
            print("❌ Form validation failed:", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)


@login_required
def upload_signed_note(request, note_id):
    delivery = get_object_or_404(
        Delivery, 
        id=note_id,
        estimate_number__sales_person=request.user  #  user is linked to Employee
    )
    

    if request.method == 'POST':
        receiver_type = request.POST.get('receiver_type')  # either 'customer' or 'other'

        # Initialize form data dictionary
        form_data = {
            'received_by': receiver_type, 
            'date_of_receipt': request.POST.get('date_of_receipt'),
            'delivery_status': 'being_processed',
            'received_by_customer': None,
            'receiver_name': None,
            'receiver_contact': None
        }

        # Handle based on selected type
        if receiver_type == 'customer':
            form_data['received_by_customer'] = request.POST.get('received_by_customer')
        elif receiver_type == 'other':
            form_data['receiver_name'] = request.POST.get('receiver_name') or None
            form_data['receiver_contact'] = request.POST.get('receiver_contact') or None

        
        # Update delivery info
        for field, value in form_data.items():
            if value:
                setattr(delivery, field, value)
        
        delivery.save()
        
        # Process images
        images = request.FILES.getlist('images')
        if not images:
            return JsonResponse({
                'success': False,
                'message': 'At least one image is required'
            }, status=400)
        
        try:
            for i, image_file in enumerate(images):
                DeliveryImage.objects.create(
                    delivery=delivery,
                    delivery_image=image_file,
                    uploaded_by=request.user,
                    is_primary=(i == 0)  # Mark first image as primary
                )
            
            # Update estimate status
            delivery.estimate_number.status = 'delivered'
            delivery.estimate_number.save()
            
            return JsonResponse({
                'success': True,
                'message': f'{len(images)} images uploaded successfully',
                'redirect_url': reverse('delivery_note_list_by_sales_person')
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error uploading images: {str(e)}'
            }, status=500)

    else:
        # GET request - render the form
        context = {
            'customer': delivery.estimate_number.customer_name,
            'note': {
                
                'delivery_note_number': delivery.delivery_note_number,
                'date_goods_received': delivery.date_goods_received.strftime('%Y-%m-%d') if delivery.date_goods_received else None,
                'delivery_status': delivery.delivery_status,
            }
        }
        return render(request, 'delivery_notes/upload_signed_delivery.html', context)
    
@login_required
def delivery_note_list(request):
    delivery_notes = Delivery.objects.all().order_by('-id')
    return render(request, 'delivery_notes/list.html', {'delivery_notes': delivery_notes})

def delivery_note_details(request, note_id):
    note = get_object_or_404(Delivery, id=note_id)
    return render(request, 'delivery_notes/details_partial.html', {
        'note': note
    })

@login_required
def confirm_delivery_note(request, pk):
    note = get_object_or_404(Delivery, pk=pk)

    if request.method == 'POST':
        form = OfficerReviewForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            status = form.cleaned_data.get('status')
            if status == 'received':
                note.status = 'received'
                messages.success(request, "Delivery note marked as received.")
            elif status == 'rejected':
                note.status = 'rejected'
                messages.warning(request, "Delivery note marked as rejected.")
            note.save()
            return redirect('delivery_note_list')
    else:
        form = OfficerReviewForm(instance=note)
    
    return render(request, 'delivery_notes/confirm.html', {'form': form, 'note': note})


@login_required
def delivery_note_list_by_sales_person(request):
    user_role = request.user.role.name.lower() if request.user.role else ""
    
    if user_role == "sales officer":
        # Use prefetch_related to optimize image loading
        delivery_notes = Delivery.objects.filter(
            estimate_number__sales_person=request.user
        ).prefetch_related('images').select_related(
            'estimate_number',
            'sales_person'
        ).order_by('-date_of_receipt')
    else:
        delivery_notes = Delivery.objects.none()

    context = {
        'delivery_notes': delivery_notes,
        'user_role': user_role
    }
    return render(request, 'delivery_notes/sales_person_list.html', context)
 
@require_POST
@csrf_exempt   
def update_note_status(request):
    note_id = request.POST.get('note_id')
    status = request.POST.get('status')
    
    try:
        note = Delivery.objects.get(id=note_id)
        estimate = note.estimate_number
        estimate.status = 'delivered'
        estimate.save()
        note.delivery_status = status
        note.save()
        return JsonResponse({'success': True})
    except Delivery.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Delivery note not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



