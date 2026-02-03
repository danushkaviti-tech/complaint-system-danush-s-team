from django.shortcuts import render
from .forms import ComplaintForm
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google.genai import Client  # new package

def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'complaints/success.html')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/complaint_form.html', {'form': form})

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "Please type a message."})

            # ✅ Initialize Gemini client
            client = Client(api_key=settings.GOOGLE_API_KEY)

            # ✅ Create a chat session and get response
            response = client.chat(
                model="gemini-pro",
                messages=[{"author": "user", "content": [{"type": "text", "text": user_message}]}],
            )

            # ✅ Get the first text output from response
            bot_reply = response.last or "Sorry, I didn't understand."

            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            print("Chat API error:", e)  # Logs the real error
            return JsonResponse({"reply": "Server error. Please try again."})

    return JsonResponse({"error": "Invalid request"}, status=400)
