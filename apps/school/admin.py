# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Class, School, Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "date_of_birth",
        "student_class",
        "address",
        "floor",
    )
    list_filter = ("date_of_birth",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "password", "last_login", "is_superuser", "email", "full_name", "is_active", "is_staff")
    list_filter = ("last_login", "is_superuser", "is_active", "is_staff")
    raw_id_fields = ("groups", "user_permissions")


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher")
    list_filter = ("teacher",)
    raw_id_fields = ("students",)
    search_fields = ("name",)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    raw_id_fields = ("classes",)
    search_fields = ("name",)
