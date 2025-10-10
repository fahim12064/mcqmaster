# quiz/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import CustomUserCreationForm
from .models import Class, Subject, Quiz, QuizAttempt, StudentProfile

User = get_user_model()

# ===============================================================
# 🔐 Authentication Views
# ===============================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        if not identifier or not password:
            messages.error(request, 'Please provide both username/email and password.')
            return render(request, 'registration/login.html')

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            try:
                User.objects.get(Q(username__iexact=identifier) | Q(email__iexact=identifier))
                messages.error(request, 'Incorrect password. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'User with this email or username does not exist.')
            
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ===============================================================
# 🏠 General Views
# ===============================================================

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


# ===============================================================
# 🧠 Quiz Attempt + Result Logic
# ===============================================================

@login_required
@csrf_exempt
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if QuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('student_quiz_result', quiz_id=quiz_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})

            questions = quiz.questions_json.get('questions', [])
            score = 0
            user_answers_dict = {}
            correct_answers_dict = {}

            for q in questions:
                q_id = str(q.get('id'))
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
                user_answers=user_answers_dict,
                correct_answers=correct_answers_dict
            )

            return JsonResponse({'success': True, 'score': score, 'total': len(questions)})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'quiz_data': quiz.questions_json})


# ===============================================================
# 🎓 Student Result View
# ===============================================================

@login_required
@user_passes_test(lambda u: u.user_type == 'student', login_url='home')
def student_quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    try:
        attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).latest('timestamp')
    except QuizAttempt.DoesNotExist:
        messages.error(request, "You haven't attempted this quiz yet.")
        return redirect('quiz_detail', quiz_id=quiz.id)

    leaderboard = QuizAttempt.objects.filter(quiz=quiz).order_by('-score', 'timestamp')[:5]

    context = {
        'quiz': quiz,
        'attempt': attempt,
        'leaderboard': leaderboard,
        'user_answers': attempt.user_answers or {},
        'correct_answers': attempt.correct_answers or {},
    }
    return render(request, 'quiz/quiz_result.html', context)


# ===============================================================
# 🧑‍🏫 Mentor Views
# ===============================================================

def is_mentor(user):
    return user.is_authenticated and user.user_type == 'mentor'


@login_required
@user_passes_test(is_mentor, login_url='home')
def mentor_dashboard(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/mentor_dashboard.html', {'quizzes': quizzes})


@login_required
@user_passes_test(is_mentor, login_url='home')
def mentor_quiz_results_list(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-score', 'timestamp').select_related('user')

    context = {
        'quiz': quiz,
        'attempts': attempts
    }
    return render(request, 'quiz/quiz_results_for_mentor.html', context)


@login_required
@user_passes_test(is_mentor, login_url='home')
def mentor_view_student_attempt(request, attempt_id):
    try:
        attempt = QuizAttempt.objects.select_related('user', 'quiz').get(id=attempt_id)
    except QuizAttempt.DoesNotExist:
        raise Http404("This quiz attempt does not exist.")

    quiz = attempt.quiz
    leaderboard = QuizAttempt.objects.filter(quiz=quiz).order_by('-score', 'timestamp')[:5]

    context = {
        'quiz': quiz,
        'attempt': attempt,
        'leaderboard': leaderboard,
        'user_answers': attempt.user_answers or {},
        'correct_answers': attempt.correct_answers or {},
        'is_mentor_view': True,
    }
    return render(request, 'quiz/quiz_result.html', context)


# ===============================================================
# 👤 Profile View
# ===============================================================

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
