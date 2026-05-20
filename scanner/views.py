import json
import base64
import re
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import BusinessCard

def scan_card(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            user_note = request.POST.get('manual_note', '')
            
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            url = "http://localhost:11434/api/generate"
            
            payload = {
                "model": "llama3.2-vision",
                "prompt": (
                    "Analyze this business card image. Extract contact details. "
                    "Return ONLY a raw JSON object with keys: 'name', 'email', 'phone', 'company'. "
                    "Do not use markdown backticks, explanations, or introductory text. "
                    "If a value is missing, use null."
                ),
                "stream": False,
                "images": [encoded_image]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            ai_text = result.get('response', '').strip()
            
            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if json_match:
                clean_text = json_match.group(0)
            else:
                clean_text = ai_text.replace('```json', '').replace('```', '').strip()
                
            parsed_data = json.loads(clean_text)
            
            full_name = parsed_data.get('name', '') or ''
            name_parts = full_name.split(' ', 1)
            f_name = name_parts[0] if len(name_parts) > 0 else ''
            l_name = name_parts[1] if len(name_parts) > 1 else ''
            
            BusinessCard.objects.create(
                first_name=f_name,
                last_name=l_name,
                company_name=parsed_data.get('company'),
                email=parsed_data.get('email'),
                phone_number=parsed_data.get('phone'),
                manual_note=user_note,
                card_image=image_file
            )
            
            return JsonResponse(parsed_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e), 'raw_response': ai_text if 'ai_text' in locals() else None}, status=500)
            
    return render(request, 'scanner/index.html')

def dashboard(request):
    cards = BusinessCard.objects.all().order_by('-scanned_at')
    return render(request, 'scanner/view.html', {'cards': cards})