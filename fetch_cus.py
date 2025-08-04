from erp.models import CustomerDetails

# Loop through each customer and print name and sales person(s)
for customer in CustomerDetails.objects.all():
    print(f"Customer: {customer.customer_name}")