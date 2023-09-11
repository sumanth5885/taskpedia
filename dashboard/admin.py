from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_student', 'is_admin', 'is_lecture', 'is_active', 'is_staff', 'date_joined']

@admin.register(HomeWork)
class HomeWorkModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "subject", "title", "description", "start_date", "due_date", "completed"]

@admin.register(EmailVerify)
class EmailVerifyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'is_verified']

@admin.register(Notes)
class NotesModelAdmin(admin.ModelAdmin):
    list_display = [ "id", "user", "title", "description", "date"]

@admin.register(ToDo)
class ToDoModelAdmin(admin.ModelAdmin):
    list_display = [ "id", "user", "title", "finished", "date_time"]

@admin.register(StudentProfile)
class StudentProfileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "reg_no", "cls", "full_name", "email", "phone", "img"]

@admin.register(LectureProfile)
class LectureProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'department', 'email', 'phone', 'img' ]

@admin.register(Assignments)
class AssignmentsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'lecture', 'title', 'description', 'document', 'date', 'valued']