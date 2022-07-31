from sys import prefix

from django.forms import ModelForm
from school.models import Student


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "email", "date_of_birth", "student_class", "address", "floor"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                }
            )

    def update(self, commit=True):
        object = super().save(commit)
        return object

    def save(self, commit):
        object = super().save(False)
        object.created_by = self.request.user
        object.save()
        return object
