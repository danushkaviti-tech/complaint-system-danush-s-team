from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('complaint/', views.complaint_create, name='complaint_create'),
    path('success/', TemplateView.as_view(template_name='complaints/success.html'), name='complaint_success'),
    path('about/', TemplateView.as_view(template_name='complaints/about.html'), name='about'),

    # Help & Chat
    path('help/', TemplateView.as_view(template_name='complaints/help.html'), name='help'),
    path('help/chat/', views.chat_api, name='chat_api'),
]
