from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import logging
import os
from urllib.parse import quote, unquote
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
from .models import Customer, Delivery, DeliveryImage, Dispatch, Employee, Estimate, Item, SalesOrder, SalesOrderItem, UserRole
import json
import pandas as pd
from io import BytesIO
from datetime import date, datetime
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
            return redirect('sales_dashboard')
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
    print(f"Making {method} request to {endpoint} with data: {data} and params: {params}")  # Debugging line
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



# sales_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from .utils import erpnext_api_request
from .forms import SalesOrderForm, DeliveryNoteUploadForm, WeeklyReportForm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

from django.views.decorators.csrf import csrf_exempt 

logger = logging.getLogger(__name__)


@login_required
@login_required
def create_sales_order(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Validate required fields
        required_fields = ['customer', 'transaction_date', 'delivery_date']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        if missing_fields:
            return JsonResponse({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Fetch customer details from ERPNext to get sales team
        customer = request.POST.get("customer")
        cust_response = requests.get(
            f"{ERP_URL}/api/resource/Customer/{customer}",
            headers={
                "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}"
            }
        )
        cust_response.raise_for_status()
        cust_data = cust_response.json()['data']
        cust_sales_team = cust_data.get('sales_team', [])
        
        if not cust_sales_team:
            return JsonResponse({'error': 'No sales team defined for this customer'}, status=400)
        
        # Assume only one sales person; take the first one
        sales_person = cust_sales_team[0]['sales_person']
        
        # Build sales_team as a list (required by ERPNext API)
        sales_team = [{
            "sales_person": sales_person,
            "allocated_percentage": 100,
            "commission_rate": 100,
            "allocated_amount": 0  # Will be updated after calculating net total
        }]
        
        # Process items
        item_codes = request.POST.getlist("item_code[]")
        qtys = request.POST.getlist("qty[]")
        rates = request.POST.getlist("rate[]")
        descriptions = request.POST.getlist("description[]")
        warehouses = request.POST.getlist("warehouse[]")
        uoms = request.POST.getlist("uom[]")
        discount_percents = request.POST.getlist("discount_percent[]")

        items = []
        net_total = 0
        for i in range(len(item_codes)):
            try:
                qty = float(qtys[i])
                if qty <= 0:
                    continue
                
                rate = float(rates[i]) if i < len(rates) else 0
                item_total = qty * rate
                net_total += item_total
                
                item_dict = {
                    'item_code': item_codes[i],
                    'qty': qty,
                    'rate': rate,
                    'description': descriptions[i] if i < len(descriptions) else '',
                    'warehouse': warehouses[i] if i < len(warehouses) else '',
                    'uom': uoms[i] if i < len(uoms) else ''
                }
                
                if discount_percents and i < len(discount_percents):
                    item_dict['discount_percentage'] = float(discount_percents[i])
                
                items.append(item_dict)
            except (ValueError, IndexError) as e:
                logger.warning(f"Invalid item data at index {i}: {e}")
                continue

        if not items:
            return JsonResponse({'error': 'No valid items in order (must have quantity > 0)'}, status=400)
        
        # Update allocated_amount to the net total
        sales_team[0]['allocated_amount'] = net_total
        
        # Prepare order data (create in Draft state)
        order_data = {
            'doctype': 'Sales Order',
            'customer': customer,
            'transaction_date': request.POST.get("transaction_date"),
            'delivery_date': request.POST.get("delivery_date"),
            'sales_team': sales_team,
            'docstatus': 0,  # Create as Draft
            'items': items,
            'notes': request.POST.get("notes", "")
        }

        # Create Draft Sales Order
        create_response = requests.post(
            f"{ERP_URL}/api/resource/Sales Order",
            headers={
                "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}",
                "Content-Type": "application/json"
            },
            json=order_data
        )
        create_response.raise_for_status()
        
        # Parse the creation response
        try:
            create_data = create_response.json()
            logger.debug(f"ERPNext create response: {create_data}")
        except ValueError as e:
            logger.error(f"Failed to parse ERPNext create response as JSON: {create_response.text}")
            return JsonResponse({
                'error': 'Invalid response format from ERPNext on create'
            }, status=500)
        
        # Verify creation response structure
        if not isinstance(create_data, dict) or 'data' not in create_data or 'name' not in create_data['data']:
            logger.error(f"Unexpected ERPNext create response structure: {create_data}")
            return JsonResponse({
                'error': 'Unexpected response structure from ERPNext on create'
            }, status=500)
        
        order_name = create_data['data']['name']
        
        # Submit the order and transition to Pending Credit Approval
        submit_response = requests.post(
            f"{ERP_URL}/api/method/frappe.model.workflow.apply_workflow",
            headers={
                "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}",
                "Content-Type": "application/json"
            },
            json={
                "doc": json.dumps({
                    "doctype": "Sales Order",
                    "name": order_name
                }),
                "action": "Submit"  # Action to submit the order
            }
        )
        submit_response.raise_for_status()
        
        # Parse the submit response
        try:
            submit_data = submit_response.json()
            logger.debug(f"ERPNext submit response: {submit_data}")
        except ValueError as e:
            logger.error(f"Failed to parse ERPNext submit response as JSON: {submit_response.text}")
            return JsonResponse({
                'error': 'Invalid response format from ERPNext on submit'
            }, status=500)
        
        # Verify submit response structure and workflow state
        if not isinstance(submit_data, dict) or 'message' not in submit_data or submit_data['message'].get('workflow_state') != 'Pending Credit Approval':
            logger.error(f"Unexpected ERPNext submit response or incorrect workflow state: {submit_data}")
            return JsonResponse({
                'error': 'Failed to transition to Pending Credit Approval'
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'message': 'Sales order created and submitted successfully',
            'order_name': order_name
        })

    except requests.HTTPError as http_err:
        try:
            error_msg = http_err.response.json().get('message', http_err.response.text)
        except ValueError:
            error_msg = http_err.response.text
        logger.error(f"ERPNext API error: {error_msg}")
        return JsonResponse({
            'error': f"ERPNext API error: {error_msg}"
        }, status=http_err.response.status_code)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f"Unexpected error occurred: {str(e)}"
        }, status=500) 
@login_required
def upload_delivery_note(request):
    if request.method == "POST":
        form = DeliveryNoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_note_id = form.cleaned_data["delivery_note_id"]
            file = request.FILES["file"]
            # Upload file to ERPNext
            files = {'file': (file.name, file, file.content_type)}
            upload_response = erpnext_api_request(
                "File",
                method="POST",
                data={"file_name": file.name, "attached_to_doctype": "Delivery Note", "attached_to_name": delivery_note_id},
                files=files,
                request=request
            )
            if upload_response:
                messages.success(request, "Delivery note uploaded successfully.")
                return redirect("dashboard")
            else:
                messages.error(request, "Failed to upload delivery note.")
    else:
        delivery_note_id = request.GET.get("dn")
        initial = {}
        if delivery_note_id:
            dn = erpnext_api_request(
                f"Delivery Note/{delivery_note_id}",
                params={"fields": json.dumps(["name", "customer_name"])},
                request=request
            )
            if dn:
                initial = {"delivery_note_id": dn.get("name"), "customer": dn.get("customer_name")}
        form = DeliveryNoteUploadForm(initial=initial)
    return render(request, 'sales_dashboard.html', {'delivery_note_form': form})

@login_required
def generate_weekly_report(request):
    if request.method == "POST":
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            week_ending = form.cleaned_data["week_ending"]
            report_type = form.cleaned_data["report_type"]
            comments = form.cleaned_data["comments"]

            # Generate PDF report
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Weekly Report: {report_type.replace('_', ' ').title()}")
            p.drawString(100, 730, f"Week Ending: {week_ending}")
            p.drawString(100, 710, "Prepared by: " + request.user.username)
            p.drawString(100, 690, "Comments:")
            p.drawString(100, 670, comments[:200] if comments else "No comments provided.")
            # Add more report content based on report_type
            p.showPage()
            p.save()
            buffer.seek(0)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="weekly_report_{week_ending}.pdf"'
            response.write(buffer.getvalue())
            buffer.close()
            return response
    else:
        form = WeeklyReportForm(initial={'week_ending': datetime.now().date()})
    return render(request, 'sales_dashboard.html', {'weekly_report_form': form})

@login_required
def generate_price_list(request):
    # Fetch items for price list
    items = erpnext_api_request(
        "Item",
        params={
            "fields": json.dumps(["item_code", "item_name", "standard_rate"]),
            "limit_page_length": 100
        },
        request=request
    ) or []
    
    # Generate PDF price list
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "AUTO PRO Master Price List")
    y = 730
    for item in items:
        p.drawString(100, y, f"{item['item_code']}: {item['item_name']} - Shs. {item['standard_rate']}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="price_list.pdf"'
    response.write(buffer.getvalue())
    buffer.close()
    return response

@login_required
def view_customer_contacts(request):
    customers = erpnext_api_request(
        "Customer",
        params={
            "fields": json.dumps(["name", "customer_name", "phone", "territory"]),
            "filters": json.dumps([["sales_team.sales_person", "=", request.user.username], ["sales_team.allocated_percentage", "=", 100]]),
            "limit_page_length": 50
        },
        request=request
    ) or []
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer_contacts.html', {'page_obj': page_obj})

@login_required
def search(request):
    query = request.GET.get('q', '')
    if query:
        sales_orders = erpnext_api_request(
            "Sales Order",
            params={
                "fields": json.dumps(["name", "customer_name", "transaction_date", "grand_total", "status"]),
                "filters": json.dumps([["customer_name", "like", f"%{query}%"]]),
                "limit_page_length": 10
            },
            request=request
        ) or []
        return render(request, 'sales_dashboard.html', {'sales_orders': sales_orders, 'query': query})
    return redirect('dashboard')


#sales order

# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Item
from django.db.models import F

@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.annotate(
        outstanding_amount=F('outstanding_amount')
    ).values('erpnext_id', 'customer_name', 'outstanding_amount')
    return Response(list(customers))


@api_view(['GET'])
def item_list(request):
    items = Item.objects.values(
        'erpnext_id', 'code', 'name', 'standard_rate', 'stock_uom'
    )
    return Response(list(items))

@api_view(['GET'])
def item_stock(request, item_id):
    # Implement your stock checking logic here
    # This might query ERPNext's API or your local database
    return Response({
        'available_qty': 10  # Example value
    })
 

@csrf_exempt
def get_item_details(request):
    item_code = request.GET.get('item_code')
    if not item_code:
        return JsonResponse({'error': 'Item code required'}, status=400)
    
    try:
        item = Item.objects.get(erpnext_id=item_code)
        return JsonResponse({
            'rate': float(item.standard_rate),
            'uom': item.stock_uom,
            'description': item.description
        })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
from datetime import date
from datetime import date, timedelta
import json
import calendar


@login_required
@csrf_exempt
def customer_outstanding(request):
    customer_id = request.GET.get('customer_id')
    if not customer_id:
        return JsonResponse({'error': 'Missing customer_id', 'status': 'error'}, status=400)

    customer_id = unquote(customer_id)
    logger.info(f"Decoded customer ID: {customer_id}")

    ERP_API_SECRET = os.getenv('ERP_API_SECRET')
    ERP_API_KEY = os.getenv('ERP_API_KEY')
    ERP_URL = os.getenv('ERP_URL')

    headers = {"Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}"}

    try:
        # URL encode each segment of the customer_id to handle slashes and special chars
        resource_customer = "/".join(quote(part, safe='') for part in customer_id.split('/'))
        url_customer = f"{ERP_URL}/api/resource/Customer/{resource_customer}"
        
        # Request both customer data and sales team in one call
        params = {
            "fields": json.dumps([
                "name",
                "customer_name",
                "accounts",
                "sales_team.sales_person",
                "sales_team.allocated_percentage",
                "sales_team.commission_rate"
            ])
        }

        # Fetch customer data with sales team
        resp_customer = requests.get(url_customer, headers=headers, params=params)
        if resp_customer.status_code != 200:
            logger.warning(f"Customer API call failed: {resp_customer.status_code} {resp_customer.text}")
            return JsonResponse({'error': 'Customer not found', 'status': 'error'}, status=404)

        customer_data = resp_customer.json().get('data')
        if not customer_data:
            return JsonResponse({'error': 'Customer data missing', 'status': 'error'}, status=404)

        # Process accounts and outstanding balance
        accounts = customer_data.get('accounts', [])
        if not accounts or not (account_name := accounts[0].get('account')):
            return JsonResponse({'error': 'No linked account found', 'status': 'error'}, status=400)

        # Prepare GL Entry query parameters
        filters = [
            ["party", "=", customer_id],
            ["account", "=", account_name],
            ["docstatus", "=", 1]
        ]
        fields = ["sum(debit) as total_debit", "sum(credit) as total_credit"]

        url_gl = f"{ERP_URL}/api/resource/GL Entry"
        params_gl = {
            "filters": json.dumps(filters),
            "fields": json.dumps(fields)
        }

        # Fetch GL Entry data
        resp_gl = requests.get(url_gl, headers=headers, params=params_gl)
        if resp_gl.status_code != 200:
            logger.warning(f"GL Entry API call failed: {resp_gl.status_code} {resp_gl.text}")
            return JsonResponse({'error': 'Failed to get GL entries', 'status': 'error'}, status=500)

        gl_data = (resp_gl.json().get('data') or [{}])[0]
        outstanding = float(gl_data.get('total_debit') or 0) - float(gl_data.get('total_credit') or 0)

        # Process sales team data
        sales_team = []
        for member in customer_data.get('sales_team', []):
            sales_team.append({
                'sales_person': member.get('sales_person'),
                'allocated_percentage': float(member.get('allocated_percentage', 100)),
                'commission_rate': float(member.get('commission_rate', 0))
            })

        return JsonResponse({
            'outstanding': outstanding,
            'account': account_name,
            'sales_team': sales_team,
            'status': 'success'
        })

    except Exception as e:
        logger.exception("Error fetching customer data")
        return JsonResponse({'error': str(e), 'status': 'error'}, status=500)

ERP_API_SECRET = os.getenv('ERP_API_SECRET')
ERP_API_KEY = os.getenv('ERP_API_KEY')
ERP_URL = os.getenv('ERP_URL')
@login_required
def get_warehouses(request):
    

    headers = {
        "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}"
    }

    try:
        url = f"{ERP_URL}/api/resource/Warehouse"
        params = {
            "fields": '["name"]',
            "limit_page_length": 100
        }

        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch warehouses'}, status=500)

        warehouses = resp.json().get('data', [])
        return JsonResponse({'warehouses': warehouses})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def fetch_items_from_erp(request):
    search_term = request.GET.get('search', '').strip()
    warehouse = request.GET.get('warehouse', '')
    limit = int(request.GET.get('limit', 20))

    try:
        # 1️⃣ Step 1: Fast search from ERPNext
        search_payload = {
            'txt': search_term,
            'doctype': 'Item',
            'limit': limit
        }

        if warehouse:
            # Filter only items in given warehouse
            bin_response = requests.get(
                f"{ERP_URL}/api/resource/Bin",
                headers={'Authorization': f'token {ERP_API_KEY}:{ERP_API_SECRET}'},
                params={
                    'fields': '["item_code"]',
                    'filters': f'[["warehouse", "=", "{warehouse}"]]',
                    'limit_page_length': 1000
                },
                timeout=5
            )
            bin_response.raise_for_status()
            item_codes_in_wh = [bin['item_code'] for bin in bin_response.json().get('data', [])]
            if not item_codes_in_wh:
                return JsonResponse({'items': []})
            search_payload['filters'] = {'name': ['in', item_codes_in_wh]}

        search_response = requests.post(
            f"{ERP_URL}/api/method/frappe.desk.search.search_link",
            headers={
                'Authorization': f'token {ERP_API_KEY}:{ERP_API_SECRET}',
                'Content-Type': 'application/json'
            },
            json=search_payload,
            timeout=5
        )
        search_response.raise_for_status()
        search_results = search_response.json().get('message', [])

        if not search_results:
            return JsonResponse({'items': []})

        item_codes = [item['value'] for item in search_results]

        # 2️⃣ Step 2: Get quantities from Bin
        bin_params = {
            'fields': '["item_code", "actual_qty", "warehouse"]',
            'filters': f'[["item_code", "in", {json.dumps(item_codes)}]]',
            'limit_page_length': 1000
        }
        bin_qty_response = requests.get(
            f"{ERP_URL}/api/resource/Bin",
            headers={'Authorization': f'token {ERP_API_KEY}:{ERP_API_SECRET}'},
            params=bin_params,
            timeout=5
        )
        bin_qty_response.raise_for_status()
        bin_data = bin_qty_response.json().get('data', [])
        qty_map = {}
        for b in bin_data:
            code = b['item_code']
            qty_map[code] = qty_map.get(code, 0) + float(b.get('actual_qty', 0))

        # 3️⃣ Step 3: Get prices & UOM in bulk
        price_params = {
            'fields': '["item_code", "price_list_rate"]',
            'filters': f'[["item_code", "in", {json.dumps(item_codes)}], ["selling", "=", 1]]',
            'limit_page_length': 1000
        }
        price_response = requests.get(
            f"{ERP_URL}/api/resource/Item Price",
            headers={'Authorization': f'token {ERP_API_KEY}:{ERP_API_SECRET}'},
            params=price_params,
            timeout=5
        )
        price_response.raise_for_status()
        prices = {p['item_code']: float(p.get('price_list_rate', 0)) for p in price_response.json().get('data', [])}

        # Fetch UOM
        item_params = {
            'fields': '["name", "stock_uom"]',
            'filters': f'[["name", "in", {json.dumps(item_codes)}]]',
            'limit_page_length': 1000
        }
        item_response = requests.get(
            f"{ERP_URL}/api/resource/Item",
            headers={'Authorization': f'token {ERP_API_KEY}:{ERP_API_SECRET}'},
            params=item_params,
            timeout=5
        )
        item_response.raise_for_status()
        uom_map = {i['name']: i.get('stock_uom', '') for i in item_response.json().get('data', [])}

        # 4️⃣ Step 4: Merge data
        items = []
        for sr in search_results:
            code = sr['value']
            items.append({
                'code': code,
                'name': sr.get('description', '').split(' - ')[0],
                'description': sr.get('description', ''),
                'available_qty': qty_map.get(code, 0.0),
                'rate': prices.get(code, 0.0),
                'uom': uom_map.get(code, ''),
                'warehouse': warehouse if warehouse else None
            })

        return JsonResponse({'items': items})

    except requests.RequestException as e:
        logger.error(f"ERP API error: {str(e)}")
        return JsonResponse({'error': 'Failed to search items'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
       
       
@login_required
def fetch_sales_order_details(request):
    order_id = request.GET.get("order_id")
    if not order_id:
        return JsonResponse({'error': 'Order ID required'}, status=400)
    
    try:
        response = requests.get(
            f"{ERP_URL}/api/resource/Sales Order/{order_id}",
            headers={"Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}"}
        )
        response.raise_for_status()
        data = response.json()['data']
        items = [f"{item['item_code']} ({item['qty']})" for item in data.get('items', [])]
        return JsonResponse({
            'success': True,
            'order_id': data['name'],
            'customer': data.get('customer_name', data['customer']),
            'items': items,
            'ordered_amount': f"Shs. {data.get('total', 0):,.2f}",
            'status': data.get('workflow_state', 'Pending')
        })
    except requests.HTTPError as http_err:
        error_msg = http_err.response.json().get('message', http_err.response.text)
        logger.error(f"ERPNext API error: {error_msg}")
        return JsonResponse({'error': f"ERPNext API error: {error_msg}"}, status=http_err.response.status_code)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({'error': f"Unexpected error: {str(e)}"}, status=500)

    
def get_employee_info(user, request): 
    employee_data = erpnext_api_request(
        "Employee",
        params={
            "fields": json.dumps(["branch"]),
            "filters": json.dumps([["user_id", "=", user.username]]),
            "limit_page_length": 1
        },
        request=request
    )

    # Assuming the employee record always exists and branch is set
    return employee_data[0]["branch"]


def get_customers_by_sales_person(branch, request):
    customers = erpnext_api_request(
        "Customer",
        params={
            "fields": json.dumps(["name", "customer_name", "mobile_no"]),
            "filters": json.dumps([
                ["Sales Team", "sales_person", "=", branch]
            ]),
            "limit_page_length": 200
        },
        request=request
    )
    return customers or []

def process_sales_orders(sales_orders_data):
    return [
        {
            'id': order.get('name'),
            'customer': order.get('customer_name', order.get('customer')),
            'date': order.get('transaction_date'),
            'delivery_date': order.get('delivery_date'),
            'amount': float(order.get('grand_total', 0)),
            'status': order.get('status'),
            'billed_percent': float(order.get('per_billed', 0))
        }
        for order in sales_orders_data
    ]

def get_sales_orders_by_sales_person(branch, customers, request):
    sales_orders = []
    try:
        sales_orders_data = erpnext_api_request(
            "Sales Order",
            params={
                "fields": json.dumps([
                    "name", "customer", "customer_name", "transaction_date", 
                    "delivery_date", "grand_total", "status", "per_billed"
                ]),
                "filters": json.dumps([
                    ["Sales Team", "sales_person", "=", branch],
                    ["docstatus", "=", 1]
                ]),
                "order_by": "transaction_date desc",
                "limit_page_length": 50
            },
            request=request
        ) or []
        sales_orders = process_sales_orders(sales_orders_data)
    except Exception as e:
        logger.error(f"Error fetching sales orders by sales person: {str(e)}")
        # Fallback to batch fetch by customers
        customer_names = [c['name'] for c in customers]
        batch_size = 20
        for i in range(0, len(customer_names), batch_size):
            batch = customer_names[i:i + batch_size]
            try:
                batch_orders_data = erpnext_api_request(
                    "Sales Order",
                    params={
                        "fields": json.dumps([
                            "name", "customer", "customer_name", "transaction_date", 
                            "delivery_date", "grand_total", "status", "per_billed"
                        ]),
                        "filters": json.dumps([
                            ["customer", "in", batch],
                            ["docstatus", "=", 1]
                        ]),
                        "limit_page_length": 50
                    },
                    request=request
                ) or []
                sales_orders.extend(process_sales_orders(batch_orders_data))
            except Exception as batch_error:
                logger.error(f"Error fetching batch {i//batch_size + 1}: {str(batch_error)}")
                continue
    return sales_orders

def calculate_sales_stats(sorted_orders, monthly_target):
    total_orders = len(sorted_orders)
    total_sales = sum(order['amount'] for order in sorted_orders)
    average_order_value = total_sales / total_orders if total_orders > 0 else 0

    today = date.today()
    first_day_month = today.replace(day=1)
    last_year_same_month_start = first_day_month.replace(year=today.year - 1)
    last_year_same_month_end = last_year_same_month_start.replace(
        day=calendar.monthrange(last_year_same_month_start.year, last_year_same_month_start.month)[1]
    )

    this_month_orders = [o for o in sorted_orders if o['date'] and o['date'] >= str(first_day_month)]
    customers_billed_this_month = len(set(o['customer'] for o in this_month_orders))
    this_month_sales = sum(o['amount'] for o in this_month_orders)

    last_year_orders = [
        o for o in sorted_orders
        if o['date'] and last_year_same_month_start <= date.fromisoformat(o['date']) <= last_year_same_month_end
    ]
    last_year_sales = sum(o['amount'] for o in last_year_orders)

    monthly_achievement_percent = (this_month_sales / monthly_target * 100) if monthly_target else 0
    yearly_growth_percent = ((this_month_sales - last_year_sales) / last_year_sales * 100) if last_year_sales else 0

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "average_order_value": average_order_value,
        "customers_billed_this_month": customers_billed_this_month,
        "monthly_sales": this_month_sales,
        "monthly_achievement_percent": monthly_achievement_percent,
        "yearly_growth_percent": yearly_growth_percent,
    }



import datetime, json
from dateutil.relativedelta import relativedelta

def get_sales_person_stats(user, request):
    # 1. Get sales person name dynamically
    sales_person_name = get_employee_info(user, request)  # Assuming this returns branch or sales person name as string

    # 2. Get yearly target from ERPNext
    sp_data = erpnext_api_request(
        f"Sales Person/{sales_person_name}",
        request=request
    )
    targets = sp_data.get("targets", [])
    yearly_target = targets[0]["target_amount"] if targets else 0
    monthly_target = yearly_target / 12 if yearly_target else 0

    # 3. Date ranges for current partial month and last month partial
    today = datetime.date.today()
    start_current_month = today.replace(day=1)

    # Calculate last month start date
    start_last_month = (start_current_month - relativedelta(months=1))

    # Calculate end date for last month period — same day number as today or last day of last month if day too high
    try:
        end_last_period = start_last_month.replace(day=today.day)
    except ValueError:
        # If day doesn't exist in last month (e.g., Feb 30), use last day of last month
        end_last_period = (start_last_month + relativedelta(months=1)) - datetime.timedelta(days=1)

    # Current period is from 1st to today (inclusive)
    end_current_period = today

    # 4. Fetch sales for current partial month
    current_month_invoices = erpnext_api_request(
        "Sales Invoice",
        params={
            "fields": json.dumps(["grand_total"]),
            "filters": json.dumps([
                ["posting_date", ">=", str(start_current_month)],
                ["posting_date", "<=", str(end_current_period)],
                ["docstatus", "=", 1],
                ["Sales Team", "sales_person", "=", sales_person_name]
            ])
        },
        request=request
    )
    current_month_total = sum(inv["grand_total"] for inv in current_month_invoices)

    # 5. Fetch sales for last month partial period
    last_month_invoices = erpnext_api_request(
        "Sales Invoice",
        params={
            "fields": json.dumps(["grand_total"]),
            "filters": json.dumps([
                ["posting_date", ">=", str(start_last_month)],
                ["posting_date", "<=", str(end_last_period)],
                ["docstatus", "=", 1],
                ["Sales Team", "sales_person", "=", sales_person_name]
            ])
        },
        request=request
    )
    last_month_total = sum(inv["grand_total"] for inv in last_month_invoices)

    # 6. Pro-rate the monthly target for days passed so far in current month
    total_days_current_month = (start_current_month + relativedelta(months=1) - datetime.timedelta(days=1)).day
    days_passed = today.day
    pro_rated_target = (monthly_target / total_days_current_month) * days_passed if monthly_target else 0

    # 7. Calculate stats
    achievement_pct = (current_month_total / pro_rated_target) * 100 if pro_rated_target else 0
    if last_month_total > 0:
        cm_vs_lm_growth_pct = ((current_month_total - last_month_total) / last_month_total) * 100
    else:
        cm_vs_lm_growth_pct = 100 if current_month_total > 0 else 0

    return {
        "sales_person": sales_person_name,
        "yearly_target": yearly_target,
        "monthly_target": monthly_target,
        "pro_rated_target": pro_rated_target,
        "current_month_sales": current_month_total,
        "last_month_sales": last_month_total,
        "achievement_pct": round(achievement_pct, 2),
        "cm_vs_lm_growth_pct": round(cm_vs_lm_growth_pct, 2)
    }
def sales_dashboard(request):
    monthly_target = 5_000_000 
    user = request.user

    sales_person_name = get_employee_info(user, request)
    customers = get_customers_by_sales_person(sales_person_name, request)
    sales_orders = get_sales_orders_by_sales_person(sales_person_name, customers, request)

    # Remove duplicates and sort orders by date descending
    unique_orders = {order['id']: order for order in sales_orders}
    sorted_orders = sorted(unique_orders.values(), key=lambda x: x['date'] or "", reverse=True)

    stats = calculate_sales_stats(sorted_orders, monthly_target)
    monthly_stats = get_sales_person_stats(user, request)

    context = {
        "monthly_stats": monthly_stats,
        'today': date.today(),
        "branch": sales_person_name,
        "user": user,
        "sales_person_name": sales_person_name,
        "customers": customers,
        "customers_count": len(customers),
        "sales_orders": sorted_orders,
        "recent_orders": sorted_orders[:10],
        "monthly_target": monthly_target,
        **stats
    }
    return render(request, "dashboards/sales_dashboard.html", context)