from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils.translation import gettext as _

from erp.forms import DispatchForm
from .models import Dispatch, Estimate
import json


def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'active_page': 'dashboard',
    }
    return render(request, 'index.html', context)


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
        # Save form data
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatch = form.save()
            messages.success(request, _("Dispatch saved successfully!"))
            return redirect('mark_dispatch_delivered')  # Redirect to same page to clear form
        else:
            # Show form with errors
            return render(request, 'dispatch_form.html', {'form': form})
    
    elif request.method == 'PATCH' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX endpoint for marking as delivered
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