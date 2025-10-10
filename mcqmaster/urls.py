# mcqmaster/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView
from quiz import views as quiz_views  # quiz অ্যাপের ভিউগুলো ইম্পোর্ট করুন

urlpatterns = [
    path('admin/', admin.site.urls),

    # আমাদের কাস্টম লগইন ভিউ ব্যবহার করুন
    path('login/', quiz_views.login_view, name='login'),
    
    # ডিফল্ট লগআউট ভিউ ব্যবহার করুন
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # পাসওয়ার্ড পরিবর্তনের জন্য URL
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # আপনার quiz অ্যাপের অন্যান্য URL গুলো অন্তর্ভুক্ত করুন
    path('', include('quiz.urls')),
    
    # Favicon URL
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]
