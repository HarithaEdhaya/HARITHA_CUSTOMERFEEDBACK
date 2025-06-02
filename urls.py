# feedback/urls.py (app-level URLs)
from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('', views.welcome, name='welcome'),  # This will show the welcome page at /
    path('submit/', views.submit_feedback, name='submit_feedback'),  # Submit form
    path('thank-you/', views.thank_you, name='thank_you'),
    
    # Admin URLs (staff-only access)
    path('feedbacks/', views.feedback_list, name='feedback_list'),  # All feedback (admin)
    path('report/', views.feedback_report, name='feedback_report'),  # Graph/report (admin)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'), 
      # Optional dashboard
      path('logout/', views.user_logout, name='logout'),
      
       path('contact-us/', views.contact_us, name='contact_us'),
        path('contact/call/', views.call_contacts, name='call_contacts'),
]
