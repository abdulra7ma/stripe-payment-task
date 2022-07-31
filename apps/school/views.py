from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, FormView, ListView, TemplateView
from school.models import Student

from .forms import StudentForm

__all__ = ["MainView", "Student", "StudentView"]


class MainView(LoginRequiredMixin, TemplateView):
    """Main view for displaying the main page"""

    template_name = "index.html"


class StudentListView(LoginRequiredMixin, ListView):
    """Main view for displaying the main page"""

    template_name = "students_list.html"

    def get_queryset(self):
        queryset = Student.objects.all()
        search_string = self.request.GET.get("search", None)

        if search_string and search_string != "":
            queryset = Student.objects.filter(
                Q(full_name__icontains=search_string)
                | Q(email__icontains=search_string)
                | Q(date_of_birth__icontains=search_string)
                | Q(student_class__icontains=search_string)
                | Q(address__icontains=search_string)
                | Q(floor__icontains=search_string)
            )
            
        return queryset.values("pk", "full_name", "email", "date_of_birth", "student_class", "address", "floor")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateStudentView(LoginRequiredMixin, FormView):
    form_class = StudentForm
    template_name = "student.html"
    success_url = reverse_lazy("school:students-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create Student"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.save(True)
        return super().form_valid(form)


class UpdateStudentView(LoginRequiredMixin, FormView):
    form_class = StudentForm
    template_name = "student.html"
    success_url = reverse_lazy("school:students-list")

    def get_object(self):
        try:
            return get_object_or_404(Student, pk=self.kwargs.get("student_id"))
        except Http404:
            return None

    def form_valid(self, form):
        form.update(True)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Student"
        context["student"] = self.get_object()
        return context


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        try:
            obj = Student.objects.get(pk=self.kwargs["student_id"])
        except Student.DoesNotExist:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object:
            self.object.delete()

        return HttpResponseRedirect(reverse("school:students-list"))
