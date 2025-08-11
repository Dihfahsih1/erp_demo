from celery import shared_task
from django.conf import settings 
import requests 
from erp.models import Item   
from datetime import datetime
from django.utils import timezone 
from django.utils.dateparse import parse_date 
from erp.models import SalesOrder
from django.utils.dateparse import parse_datetime
from .models import CustomerDetails, CustomerAddress, ERPUser, SalesPerson, CustomerSalesTeam, SalesPersonTarget
from django.db import IntegrityError

ERP_BASE_URL = settings.ERP_NEXT_URL
API_KEY = settings.ERP_API_KEY
API_SECRET = settings.ERP_API_SECRET

HEADERS = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}


@shared_task
def fetch_erpnext_customers():
    url = f"{ERP_BASE_URL}/api/resource/Customer"
    response = requests.get(url, headers=HEADERS, params={"limit_page_length": 1000})

    if response.status_code != 200:
        raise Exception(f"Failed to fetch customers: {response.text}")

    customers = response.json().get("data", [])

    for customer in customers:
        customer_id = customer.get("name")
        detail_url = f"{ERP_BASE_URL}/api/resource/Customer/{customer_id}"
        detail_resp = requests.get(detail_url, headers=HEADERS)

        if detail_resp.status_code != 200:
            continue

        detail = detail_resp.json().get("data", {})

        customer_obj, _ = CustomerDetails.objects.update_or_create(
            customer_id=detail.get("name"),
            defaults={
                "customer_name": detail.get("customer_name"),
                "customer_type": detail.get("customer_type"),
                "naming_series": detail.get("naming_series"),
                "customer_group": detail.get("customer_group"),
                "territory": detail.get("territory"),
                "account_manager": detail.get("account_manager"),
                "default_currency": detail.get("default_currency"),
                "default_bank_account": detail.get("default_bank_account"),
                "default_price_list": detail.get("default_price_list"),
                "is_internal_customer": detail.get("is_internal_customer", False),
                "represents_company": detail.get("represents_company"),
                "market_segment": detail.get("market_segment"),
                "industry": detail.get("industry"),
                "customer_pos_id": detail.get("customer_pos_id"),
                "website": detail.get("website"),
                "language": detail.get("language"),
                "customer_details": detail.get("customer_details"),
                "mobile_no": detail.get("mobile_no"),
                "email_id": detail.get("email_id"),
                "tax_id": detail.get("tax_id"),
                "tax_category": detail.get("tax_category"),
                "payment_terms": detail.get("payment_terms"),
                "loyalty_program": detail.get("loyalty_program"),
                "loyalty_program_tier": detail.get("loyalty_program_tier"),
                "so_required": detail.get("so_required", False),
                "dn_required": detail.get("dn_required", False),
                "is_frozen": detail.get("is_frozen", False),
                "disabled": detail.get("disabled", False),
            }
        )

        # Sync addresses
        addr_url = f"{ERP_BASE_URL}/api/resource/Address?fields=[\"name\"]&filters=[[\"Address\",\"link_doctype\",\"=\",\"Customer\"],[\"Address\",\"link_name\",\"=\",\"{customer_id}\"]]"
        addr_resp = requests.get(addr_url, headers=HEADERS)

        if addr_resp.status_code == 200:
            address_list = addr_resp.json().get("data", [])
            for addr in address_list:
                addr_detail = requests.get(f"{ERP_BASE_URL}/api/resource/Address/{addr['name']}", headers=HEADERS)
                if addr_detail.status_code == 200:
                    addr_data = addr_detail.json().get("data", {})
                    CustomerAddress.objects.update_or_create(
                        customer=customer_obj,
                        address_line1=addr_data.get("address_line1", ""),
                        defaults={
                            "address_type": addr_data.get("address_type", "Billing"),
                            "address_line2": addr_data.get("address_line2"),
                            "city": addr_data.get("city"),
                            "state": addr_data.get("state"),
                            "country": addr_data.get("country"),
                            "pincode": addr_data.get("pincode"),
                        }
                    )

        # Sync sales team
        for sales in detail.get("sales_team", []):
            sp, _ = SalesPerson.objects.get_or_create(
                sales_person_name=sales.get("sales_person")
            )
            CustomerSalesTeam.objects.update_or_create(
                customer=customer_obj,
                sales_person=sp,
                defaults={"allocated_percentage": sales.get("allocated_percentage", 0)}
            )

    return f"Imported {len(customers)} ERPNext customers"

#FETCHING THE SALES ORDERS


HEADERS = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

@shared_task
def fetch_erpnext_sales_orders(): 

    # Get all Sales Orders
    url = f"{ERP_BASE_URL}/api/resource/Sales Order?limit_page_length=1000"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "Failed to fetch sales orders list"

    sales_orders = response.json().get("data", [])

    for order in sales_orders:
        name = order.get("name")
        if SalesOrder.objects.filter(title=name).exists():
            continue  # Avoid duplicates by title (used as order name)

        detail_url = f"{ERP_BASE_URL}/api/resource/Sales Order/{name}"
        detail_res = requests.get(detail_url, headers=HEADERS)
        if detail_res.status_code != 200:
            continue

        data = detail_res.json().get("data", {})

        # Fetch sales person from customer
        sales_person = None
        if data.get("customer"):
            cust_url = f"{ERP_BASE_URL}/api/resource/Customer/{data['customer']}"
            cust_res = requests.get(cust_url, headers=HEADERS)
            if cust_res.status_code == 200:
                sales_team = cust_res.json().get("data", {}).get("sales_team", [])
                if sales_team:
                    sales_person = sales_team[0].get("sales_person")

        # Create the order
        SalesOrder.objects.create(
            title=data.get("name"),
            naming_series=data.get("naming_series", ""),
            customer=data.get("customer", ""),
            customer_name=data.get("customer_name"),
            tax_id=data.get("tax_id"),
            order_type=data.get("order_type"),
            transaction_date=parse_date(data.get("transaction_date")),
            delivery_date=parse_date(data.get("delivery_date")) if data.get("delivery_date") else None,
            po_no=data.get("po_no"),
            po_date=parse_date(data.get("po_date")) if data.get("po_date") else None,
            company=data.get("company", ""),
            skip_delivery_note=data.get("skip_delivery_note", False),
            has_unit_price_items=data.get("has_unit_price_items", False),
            amended_from=data.get("amended_from"),
            cost_center=data.get("cost_center"),
            project=data.get("project"),
            currency=data.get("currency", "USD"),
            conversion_rate=data.get("conversion_rate") or 1.0,
            selling_price_list=data.get("selling_price_list"),
            price_list_currency=data.get("price_list_currency"),
            plc_conversion_rate=data.get("plc_conversion_rate") or 1.0,
            ignore_pricing_rule=data.get("ignore_pricing_rule", False),
            set_warehouse=data.get("set_warehouse"),
            reserve_stock=data.get("reserve_stock", False),
            total_qty=data.get("total_qty") or 0.0,
            total_net_weight=data.get("total_net_weight") or 0.0,
            base_total=data.get("base_total") or 0,
            base_net_total=data.get("base_net_total") or 0,
            total=data.get("total") or 0,
            net_total=data.get("net_total") or 0,
            tax_category=data.get("tax_category"),
            taxes_and_charges=data.get("taxes_and_charges"),
            shipping_rule=data.get("shipping_rule"),
            incoterm=data.get("incoterm"),
            named_place=data.get("named_place"),
            base_grand_total=data.get("base_grand_total") or 0,
            base_rounding_adjustment=data.get("base_rounding_adjustment") or 0,
            base_rounded_total=data.get("base_rounded_total") or 0,
            base_in_words=data.get("base_in_words"),
            grand_total=data.get("grand_total") or 0,
            rounding_adjustment=data.get("rounding_adjustment") or 0,
            rounded_total=data.get("rounded_total") or 0,
            in_words=data.get("in_words"),
            advance_paid=data.get("advance_paid") or 0,
            disable_rounded_total=data.get("disable_rounded_total", False),
            status=data.get("status"),
            delivery_status=data.get("delivery_status"),
            per_delivered=data.get("per_delivered") or 0.0,
            per_billed=data.get("per_billed") or 0.0,
            per_picked=data.get("per_picked") or 0.0,
            billing_status=data.get("billing_status"),
            sales_partner=data.get("sales_partner"),
            amount_eligible_for_commission=data.get("amount_eligible_for_commission") or 0,
            commission_rate=data.get("commission_rate") or 0.0,
            total_commission=data.get("total_commission") or 0,
            loyalty_points=data.get("loyalty_points") or 0,
            loyalty_amount=data.get("loyalty_amount") or 0,
            from_date=parse_date(data.get("from_date")) if data.get("from_date") else None,
            to_date=parse_date(data.get("to_date")) if data.get("to_date") else None,
            language=data.get("language"),
            is_internal_customer=data.get("is_internal_customer", False),
            source=data.get("source"),
        )

    return f"Fetched {len(sales_orders)} sales orders"


#fetch the items from erpnext



 

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

@shared_task
def fetch_erpnext_items():
    url = f"{ERP_BASE_URL}/api/resource/Item?limit_page_length=1000"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "Failed to fetch items list"

    items = response.json().get("data", [])

    for item in items:
        item_code = item.get("name")
        if Item.objects.filter(item_code=item_code).exists():
            continue  # Avoid duplicates

        detail_url = f"{ERP_BASE_URL}/api/resource/Item/{item_code}"
        detail_res = requests.get(detail_url, headers=HEADERS)
        if detail_res.status_code != 200:
            continue

        data = detail_res.json().get("data", {})

        Item.objects.create(
            item_code=data.get("name"),
            item_name=data.get("item_name"),
            item_group=data.get("item_group"),
            stock_uom=data.get("stock_uom"),
            is_stock_item=data.get("is_stock_item", False),
            is_sales_item=data.get("is_sales_item", False),
            is_purchase_item=data.get("is_purchase_item", False),
            description=data.get("description"),
            image=data.get("image"),
            brand=data.get("brand"),
            default_supplier=data.get("default_supplier"),
            disabled=data.get("disabled", False),
            valuation_method=data.get("valuation_method"),
            weight_per_unit=data.get("weight_per_unit") or 0.0,
            weight_uom=data.get("weight_uom"),
            default_warehouse=data.get("default_warehouse"),
            barcode=data.get("barcode"),
            end_of_life=parse_date(data.get("end_of_life")),
            has_batch_no=data.get("has_batch_no", False),
            has_expiry_date=data.get("has_expiry_date", False),
            shelf_life_in_days=data.get("shelf_life_in_days") or 0,
            warranty_period=data.get("warranty_period") or 0,
            min_order_qty=data.get("min_order_qty") or 0,
            safety_stock=data.get("safety_stock") or 0,
            reorder_level=data.get("reorder_level") or 0,
            reorder_qty=data.get("reorder_qty") or 0,
            last_purchase_rate=data.get("last_purchase_rate") or 0.0,
            standard_rate=data.get("standard_rate") or 0.0,
            opening_stock=data.get("opening_stock") or 0.0,
            valuation_rate=data.get("valuation_rate") or 0.0,
        )

    return f"Fetched {len(items)} items from ERPNext"


@shared_task
def fetch_erpnext_users():
    url = f"{ERP_BASE_URL}/api/resource/User?limit_page_length=1000"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return "Failed to fetch users list"

    users = response.json().get("data", [])
    created_count = 0
    skipped_count = 0
    failed_count = 0

    for user in users:
        username = user.get("name")
        if ERPUser.objects.filter(username=username).exists():
            skipped_count += 1
            continue  # Skip existing users

        # Get full user details
        detail_url = f"{ERP_BASE_URL}/api/resource/User/{username}"
        detail_res = requests.get(detail_url, headers=HEADERS)
        if detail_res.status_code != 200:
            failed_count += 1
            continue

        data = detail_res.json().get("data", {})

        try:
            ERPUser.objects.create(
                username=username,
                email=data.get("email", ""),
                first_name=data.get("first_name", ""),
                middle_name=data.get("middle_name", ""),
                last_name=data.get("last_name", ""),
                full_name=data.get("full_name", ""),
                enabled=data.get("enabled", True),
                gender=data.get("gender", ""),
                phone=data.get("phone", ""),
                mobile_no=data.get("mobile_no", ""),
                location=data.get("location", ""),
                language=data.get("language", ""),
                time_zone=data.get("time_zone", ""),
                email_signature=data.get("email_signature", ""),
                default_app=data.get("default_module", ""),
                default_workspace=data.get("home_page", ""),
                user_type=data.get("user_type", ""),
                last_login=parse_datetime(data.get("last_login")) if data.get("last_login") else None,
                last_active=timezone.now()
            )
            created_count += 1
        except IntegrityError:
            skipped_count += 1
            continue  # Likely a duplicate email or other unique field conflict

    return f"Created: {created_count}, Skipped: {skipped_count}, Failed: {failed_count} users from ERPNext"

@shared_task
def fetch_erpnext_salespersons():
    url = f"{ERP_BASE_URL}/api/resource/Sales Person?limit_page_length=1000"
    res = requests.get(url, headers=HEADERS)
    
    if res.status_code != 200:
        return f"Failed to fetch Sales Persons: {res.status_code}"
    
    sales_people = res.json().get("data", [])
    created_count = 0

    for sp in sales_people:
        sales_person_name = sp.get("name")
        if SalesPerson.objects.filter(sales_person_name=sales_person_name).exists():
            continue  # Avoid duplicates

        # Get full details
        detail_url = f"{ERP_BASE_URL}/api/resource/Sales Person/{sales_person_name}"
        detail_res = requests.get(detail_url, headers=HEADERS)
        if detail_res.status_code != 200:
            continue

        data = detail_res.json().get("data", {})

        SalesPerson.objects.create(
            
            sales_person_name=data.get("sales_person_name", ""),
            parent_sales_person=data.get("parent_sales_person") or None,
            commission_rate=data.get("commission_rate") or 0.0,
            is_group=data.get("is_group", False),
            enabled=data.get("enabled", True),
            employee=data.get("employee") or None,
            department=data.get("department") or None,
            lft=data.get("lft") or 0,
            rgt=data.get("rgt") or 0,
            old_parent=data.get("old_parent", ""),
        )
        created_count += 1

    return f"{created_count} new sales persons imported from ERPNext"