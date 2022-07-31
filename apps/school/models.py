from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.managers import CustomTeacherManager
from school.utils.constants import ModelConst


class Teacher(PermissionsMixin, AbstractBaseUser):
    phone_number = models.CharField(verbose_name="Phone Number", max_length=64, unique=True)
    email = models.EmailField(ModelConst.EMAIL, unique=True)
    full_name = models.CharField(verbose_name="Student Full Name", max_length=128)
    is_active = models.BooleanField(ModelConst.IS_ACTIVE, default=True)
    is_staff = models.BooleanField(ModelConst.IS_ACTIVE, default=False)

    USERNAME_FIELD = "email"

    objects = CustomTeacherManager()

    def __str__(self) -> str:
        return self.full_name


class Student(models.Model):
    full_name = models.CharField(verbose_name="Student Full Name", max_length=128)
    email = models.EmailField(verbose_name="Student Email")
    date_of_birth = models.DateField(verbose_name="Student Date Of Birth")
    student_class = models.CharField(verbose_name="Student Class", max_length=64)
    address = models.CharField(verbose_name="Student Address", max_length=128)
    floor = models.IntegerField(verbose_name="Student Floor")

    created_by = models.ForeignKey(Teacher, verbose_name="Created By", on_delete=models.SET_NULL, null=True)
    

class Class(models.Model):
    name = models.CharField(verbose_name="Class Name", max_length=64)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Class Teacher")
    students = models.ManyToManyField(Student, blank=True)


class School(models.Model):
    name = models.CharField(verbose_name="School Name", max_length=64)
    classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.name
