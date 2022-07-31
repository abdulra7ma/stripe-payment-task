from django.urls import path

from .views import MainView, StudentListView, CreateStudentView, UpdateStudentView, DeleteStudentView

app_name = 'school'

urlpatterns = [
    path("", MainView.as_view(), name="school-index"),
    path("student/add/", CreateStudentView.as_view(), name="add-student"),
    path("student/edit/<int:student_id>/", UpdateStudentView.as_view(), name="edit-student"),
    path("student/delete/<int:student_id>/", DeleteStudentView.as_view(), name="delete-student"),
    path("students/", StudentListView.as_view(), name="students-list"),
]
