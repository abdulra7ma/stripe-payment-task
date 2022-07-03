# Python imports
from typing import Any, Sequence

# external imports
from user.models import User
from factory import Faker, django, post_generation
from faker import Faker as FakerClass


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker("first_name")
    middle_name = Faker("name")
    phone_number = Faker("phone_number")
    surname = Faker("name")
    email = Faker("email")
    birthday = Faker("date")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FakerClass().password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)

    @classmethod
    def create(cls, **kwargs):
        instance = super().create(**kwargs)
        instance.is_active = True
        instance.save()
        return instance