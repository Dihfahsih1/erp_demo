 
from django.contrib import admin
from django.urls import path,include 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.dashboard, name='dashboard'),
     path('dispatches/', views.dispatch_list_view, name='dispatch_list'),
     path('dispatch/mark-delivered/', views.dispatch_view, name='mark_dispatch_delivered'),
     path('dispatch/<int:dispatch_id>/mark-delivered/', views.mark_delivered, name='mark_delivered'), 
    
     path('record/', views.record_estimate, name='record_estimate'),
     path('list/', views.list_estimates, name='list_estimates'),
     path('download-template/', views.download_estimate_template, name='download_estimate_template'),
     path('dispatch/<int:dispatch_id>/verify/', views.verify_dispatch, name='verify-dispatch'),

     #customer module
     path('register/', views.register_customer, name='register_customer'),
     path('customers/', views.customer_list, name='customer_list'),
     path('customers/<int:pk>/view/', views.customer_view, name='customer_view'),
     path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
     path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),


     #Account registration and login
     path('accounts/RegisterEmployee/', views.register_employee, name='register'),
     path('accounts/login/', views.login_employee, name='login'),
     path('accounts/loggedout/', auth_views.LogoutView.as_view(), name='log_out'),
     
     # Upload the delivery notes
     path('delivery-notes/upload/', views.upload_signed_note, name='upload_signed_note'),
     path('delivery-details/form/', views.create_delivery_note, name='create_delivery_note'),
     path('delivery/notes/', views.delivery_note_list, name='delivery_note_list'),
     
     path('delivery-details/<int:pk>/confirm/', views.confirm_delivery, name='confirm_delivery_note'),
     
     path('my-deliveries/', views.delivery_note_list_by_sales_person, name='delivery_note_list_by_sales_person'),
     path('upload-note/<int:note_id>/', views.upload_signed_note, name='upload_signed_note'),
     path('delivery-notes/<int:note_id>/', views.delivery_note_details, name='delivery_note_details'),
     path('update-note-status/', views.update_note_status, name='update_note_status'),
     
     path('customers/autocomplete/', views.autocomplete_customers, name='autocomplete_customers'),
     path('estimates/search/', views.estimate_search, name='estimate_search'),
     path('estimates/<int:pk>/action/', views.estimate_action, name='estimate-action'),
     path('estimates/<int:pk>/', views.estimate_detail, name='estimate-detail'),
    
     path('record-billing/<int:estimate_id>/', views.record_billing, name='record_billing'),
     path('billed-estimates/', views.all_billed_estimates, name='billed_estimates_list'),
     
     path('create-delivery-note/<int:pk>/', views.create_delivery_note, name='create_delivery_note'),




    
]
