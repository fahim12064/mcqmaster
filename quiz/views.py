# quiz/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import CustomUserCreationForm
from .models import Class, Subject, Quiz, QuizAttempt, StudentProfile

User = get_user_model( )

# --- নতুন কাস্টম লগইন ভিউ ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        if not identifier or not password:
            messages.error(request, 'Please provide both username/email and password.')
            return render(request, 'registration/login.html')

        # কাস্টম অথেনটিকেশন ব্যাকএন্ড ব্যবহার করে ইউজারকে ভেরিফাই করুন
        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # ইউজার সঠিক না হলে, কারণ খুঁজে বের করে এরর মেসেজ দিন
            try:
                User.objects.get(Q(username__iexact=identifier) | Q(email__iexact=identifier))
                # ইউজার আছে, তার মানে পাসওয়ার্ড ভুল
                messages.error(request, 'Incorrect password. Please try again.')
            except User.DoesNotExist:
                # ইউজার নেই
                messages.error(request, 'User with this email or username does not exist.')
            
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # নতুন ইউজারের জন্য স্বয়ংক্রিয়ভাবে StudentProfile তৈরি করুন
            StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'quiz/landing.html')
    
    classes = Class.objects.all()
    return render(request, 'quiz/home.html', {'classes': classes})


@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'quiz/class_list.html', {'classes': classes})


@login_required
def subject_list(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    subjects = Subject.objects.filter(class_name=class_obj)
    return render(request, 'quiz/subject_list.html', {'class_obj': class_obj, 'subjects': subjects})


@login_required
def quiz_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    quizzes = Quiz.objects.filter(subject=subject).order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'subject': subject, 'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempted = QuizAttempt.objects.filter(user=request.user, quiz=quiz).exists()
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'attempted': attempted})


@login_required
@csrf_exempt
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if QuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('quiz_result', quiz_id=quiz_id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})
            
            questions = quiz.questions_json.get('questions', [])
            score = 0
            user_answers_dict = {}
            correct_answers_dict = {}
            
            for q in questions:
                q_id = str(q.get('id')) # Ensure q_id is a string for consistency
                user_answer = answers.get(q_id)
                correct_answer = q.get('rightAnswerIndex')
                
                user_answers_dict[q_id] = user_answer
                correct_answers_dict[q_id] = correct_answer
                
                if user_answer is not None and int(user_answer) == correct_answer:
                    score += 1
            
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total_questions=len(questions),
                answers=answers,
                user_answers=user_answers_dict,
                correct_answers=correct_answers_dict
            )
            
            return JsonResponse({'success': True, 'score': score, 'total': len(questions)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'quiz_data': quiz.questions_json
    })


@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(QuizAttempt, user=request.user, quiz=quiz)
    
    leaderboard = QuizAttempt.objects.filter(quiz=quiz).order_by('-score', 'timestamp')[:5]
    
    user_answers = attempt.user_answers
    correct_answers = attempt.correct_answers
    
    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'attempt': attempt,
        'leaderboard': leaderboard,
        'user_answers': user_answers,
        'correct_answers': correct_answers
    })


@login_required
def profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user
    
    profile, created = StudentProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST' and user == request.user:
        profile.institution = request.POST.get('institution', '')
        profile.student_class = request.POST.get('student_class', '')
        
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        return JsonResponse({'success': True})
    
    return render(request, 'quiz/profile.html', {'profile': profile, 'is_owner': user == request.user})
