import easyocr
import logging
import re
from django.http import JsonResponse
from django.shortcuts import render
from io import BytesIO
from .models import DeliveryNote, DeliveryNoteItem
from .forms import DeliveryNoteForm

# Initialize EasyOCR reader ONCE at module level to avoid repeated loading
# This is crucial for performance
try:
    reader = easyocr.Reader(['en'])  # English only for faster initialization
except Exception as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize EasyOCR: {str(e)}")
    reader = None

def ocr_local(image_file):
    """Improved EasyOCR implementation with proper error handling"""
    if reader is None:
        return None

    try:
        # Ensure we're at the start of the file
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
        
        # Read the image file directly (EasyOCR can handle bytes)
        image_bytes = image_file.read()
        
        # Perform OCR
        results = reader.readtext(image_bytes)
        
        # Combine all extracted text with line breaks for better parsing
        extracted_text = "\n".join([text for (_, text, _) in results])
        return extracted_text
    except Exception as e:
        logger.error(f"EasyOCR processing failed: {str(e)}")
        return None

# [Keep all your existing extract_* functions unchanged]

def upload_delivery_note(request):
    if request.method == 'POST':
        form = DeliveryNoteForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'message': 'Form is not valid.',
                'errors': form.errors
            }, status=400)

        try:
            if 'image' not in request.FILES:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No image file provided.'
                }, status=400)

            image = request.FILES['image']
            
            # Verify the image is not empty
            if image.size == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Empty image file provided.'
                }, status=400)

            # Try local OCR
            text = ocr_local(image)
            
            if not text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'OCR processing failed. Please try another image.',
                    'debug': 'EasyOCR returned no text'
                }, status=400)

            # Extract all fields
            extracted_data = {
                'estimate_number': extract_estimate_number(text),
                'customer_name_address': extract_customer_name_address(text),
                'sales_person': extract_sales_person(text),
                'date_of_delivery': extract_date_of_delivery(text),
                'items': extract_items(text),
                'raw_text': text  # For debugging
            }

            # Save to database
            delivery_note = form.save(commit=False)
            for field, value in extracted_data.items():
                if field != 'items' and field != 'raw_text':
                    setattr(delivery_note, field, value)
            delivery_note.save()

            # Save items
            for description, quantity in extracted_data['items']:
                DeliveryNoteItem.objects.create(
                    delivery_note=delivery_note,
                    description=description,
                    quantity=quantity
                )

            return JsonResponse({
                'status': 'success',
                'message': 'Delivery Note processed successfully.',
                'data': {k: v for k, v in extracted_data.items() if k != 'raw_text'}
            })

        except Exception as e:
            logger.error(f"Delivery note processing error: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred.',
                'debug': str(e)
            }, status=500)

    # GET request
    form = DeliveryNoteForm()
    return render(request, 'upload_delivery_note.html', {'form': form})