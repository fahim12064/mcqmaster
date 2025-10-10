# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- Common routes ---
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:class_id>/subjects/', views.subject_list, name='subject_list'),
    path('subjects/<int:subject_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),

    # --- Student result view ---
    path('quizzes/<int:quiz_id>/result/', views.student_quiz_result, name='student_quiz_result'),

    # --- Profile related ---
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/', views.profile, name='my_profile'),

    # --- Mentor related views ---
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentor/quiz/<int:quiz_id>/results/', views.mentor_quiz_results_list, name='mentor_quiz_results_list'),
    path('mentor/attempt/<int:attempt_id>/view/', views.mentor_view_student_attempt, name='mentor_view_student_attempt'),
]
