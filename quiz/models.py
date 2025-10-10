from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.username

class Class(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        return f"{self.class_name.name} - {self.name}"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    duration_minutes = models.IntegerField()
    questions_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=dict, blank=True)  # এই লাইনটি যোগ করুন
    user_answers = models.JSONField(default=dict, blank=True)  # এই লাইনটি যোগ করুন
    correct_answers = models.JSONField(default=dict, blank=True)  # এই লাইনটি যোগ করুন
    
    class Meta:
        unique_together = ('user', 'quiz')

class StudentProfile(models.Model):
    # settings.AUTH_USER_MODEL ব্যবহার করে আপনার কাস্টম ইউজার মডেলকে রেফার করা হয়েছে
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, blank=True)
    student_class = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
