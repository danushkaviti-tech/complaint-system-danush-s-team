from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import ComplaintForm
from google.genai import Client
import json

# 1. Complaint Creation View
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('complaint_success')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/complaint_form.html', {'form': form})

# 2. Hybrid AI Chatbot View (Gemini + Local Knowledge)
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip().lower()

            if not user_message:
                return JsonResponse({"reply": "I'm listening! What's the issue in Vizag?"})

            # --- LOCAL KNOWLEDGE FALLBACK ---
            # This ensures the user gets an answer even if the API is "Busy"
            if "status" in user_message or "track" in user_message:
                return JsonResponse({"reply": "To track your complaint, please enter your 10-digit Reference ID on the Status page."})
            
            if "tax" in user_message or "bill" in user_message:
                return JsonResponse({"reply": "Property tax rebates of 5% are available for early payments before April 30th, 2026."})

            if "ward" in user_message or "zone" in user_message:
                return JsonResponse({"reply": "GVMC Vizag is now divided into 10 zones. You can find your specific ward details in the 'Know Your Ward' section."})

            # --- GEMINI AI PROCESSING ---
            # Using the latest 2.0-flash model
            client = Client(api_key=settings.GOOGLE_API_KEY)
            
            # System prompt ensures the AI stays in character as a GVMC official
            system_context = "You are the GVMC Digital Assistant for Visakhapatnam (Vizag). Be professional, helpful, and concise. "
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{system_context} User Question: {user_message}"
            )

            if response and response.text:
                return JsonResponse({"reply": response.text})
            else:
                raise Exception("Empty AI response")

        except Exception as e:
            print(f"Chat Error Detail: {e}")
            # Final fallback if even the API fails
            return JsonResponse({
                "reply": "I'm having trouble connecting to the main server, but I can still help with general GVMC info! Try asking about 'tax', 'wards', or 'tracking'."
            })

    return JsonResponse({"error": "Invalid request"}, status=400)