# website/urls.py
from django.urls import path
from . import views
from .views import chatbot_view

urlpatterns = [
    path("chatbot/", views.chatbot_view, name="chatbot"),
    path('', views.home2, name='home2'),
    path('articles/', views.articles, name='articles'),
    path('services/', views.services, name='services'),
    path('service_analysis/', views.service_analysis, name='service_analysis'),
    path('service_dev_tool/', views.service_dev_tool, name='service_dev_tool'),
    path('service_data_management/', views.service_data_management, name='service_data_management'),
    #path('case-studies/', views.case_studies, name='case_studies'),
    path('contact/', views.contact, name='contact'),
    path('corpoFinance/', views.corpoFinance, name='corpoFinance'),   
    path('rates_analysis/',views.rates_analysis, name='rates_analysis'),
    path('meanReversion/',views.meanReversion, name='meanReversion'),
    path('about/', views.about, name='about'),
    path('tool_risk_calculator/', views.tool_risk_calculator, name='tool_risk_calculator'),
    path('article_automation_for_small_business/', views.article_automation_for_small_business, name='article_automation_for_small_business'),
    path('article_ml_for_small_business/', views.article_ml_for_small_business, name='article_ml_for_small_business'),
    path('article_risk_management/', views.article_risk_management, name='article_risk_management'),
    path("chart-data/", views.chart_data, name="chart_data"),
    path("article_automation_email_sending/",views.article_automation_email_sending, name="article_automation_email_sending"),
    path("chart/", views.chart_view, name="chart_view"),
    path("upload/", views.upload_file, name="upload_file"),
    path('process_file/<int:file_id>//', views.process_file, name='process_file'),  
    path('riskCalculator_frontPage/', views.riskCalculator_frontPage, name='riskCalculator_frontPage'), 
    path('riskCalculator_report/', views.riskCalculator_report, name='riskCalculator_report'),   
]