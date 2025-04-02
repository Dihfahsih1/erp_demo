# utils/delivery_ocr.py
import pytesseract
from PIL import Image
import re
from dateutil import parser

def extract_delivery_data(image_path):
    """Extract structured data from delivery note image"""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        
        # Custom extraction patterns (adjust based on your document format)
        patterns = {
            'customer_name': r"Customer:\s*(.+)",
            'estimate_number': r"Estimate\s*#:\s*(\w+)",
            'date': r"Date:\s*(\d{2}/\d{2}/\d{4})"
        }
        
        results = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                results[field] = match.group(1).strip()
        
        # Parse date if found
        if 'date' in results:
            results['date'] = parser.parse(results['date']).date()
            
        return results
    except Exception as e:
        return {'error': str(e)}