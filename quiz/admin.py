# quiz/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Class, Subject, Quiz, StudentProfile

# CustomUser মডেল রেজিস্টার করার জন্য নতুন কোড
class CustomUserAdmin(UserAdmin):
    # UserAdmin ক্লাসটি ইউজার ম্যানেজমেন্টের জন্য একটি শক্তিশালী ইন্টারফেস প্রদান করে।
    # আপাতত এখানে কোনো পরিবর্তনের প্রয়োজন নেই।
    pass

# অ্যাডমিন সাইটে আপনার CustomUser মডেলটি রেজিস্টার করুন
admin.site.register(CustomUser, CustomUserAdmin)


# আপনার আগের কোড (এখানে কোনো পরিবর্তন করা হয়নি)
class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name')
    list_filter = ('class_name',)
    inlines = [QuizInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'duration_minutes', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution', 'student_class')
    search_fields = ('user__username', 'institution')
