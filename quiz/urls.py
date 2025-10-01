from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:class_id>/subjects/', views.subject_list, name='subject_list'),
    path('subjects/<int:subject_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/', views.profile, name='my_profile'),
]