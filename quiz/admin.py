# quiz/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Class, Subject, Quiz, StudentProfile

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type')

    list_filter = UserAdmin.list_filter + ('user_type',)

admin.site.register(CustomUser, CustomUserAdmin)


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
