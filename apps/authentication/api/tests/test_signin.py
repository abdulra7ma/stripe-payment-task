# Django imports
from django.urls import reverse

# external imports
import pytest
from rest_framework import status


# app imports
from .factory import UserFactory

pytestmark = pytest.mark.django_db
login_url = reverse("login-api")


def test_login_user_with_valid_credentials(client):
    password = "vdjvnjfkvjdsjvnEJBD766"

    # creates a new user object and save into DB
    user = UserFactory.create(password=password)

    # prepare auth login credintails
    credintails = {"email": user.email, "password": password}

    response = client.post(login_url, data=credintails)

    assert response.status_code == 200
    assert response.data["user"]["email"] == user.email
    assert response.data["user"]["first_name"] == user.first_name
    assert response.data["user"]["middle_name"] == user.middle_name
    assert response.data["user"]["surname"] == user.surname
    assert response.data["user"]["phone_number"] == user.phone_number
    assert response.data["user"]["birthday"] == user.birthday


def test_login_user_with_invalid_credentials(client):
    credintails = {
        "email": "gdsvfuvsdjfv",
        "password": "qwerty1234",
    }

    # login request
    response = client.post(login_url, data=credintails)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_uncorrect_password_and_email_fields(client):
    unvaild_pass_msg = "invaild credentials"
    unvaild_email_msg = "Invalid email address."

    # creates a new user object but not save it to the DB
    unsaved_user = UserFactory.build()

    # creates a new user object and save into DB
    user = UserFactory.create()

    credintails = {
        "email": unsaved_user.email,
        "password": "qwer1234",
    }

    # login request for the unvaild email error
    response = client.post(login_url, data=credintails)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # compare the `unvaild_email_msg` variable and
    # the returned unvaild email message
    assert response.data["non_field_errors"] == unvaild_email_msg

    # change the value of the `email` key to a vaild email
    credintails["email"] = user.email

    # login request for the unvaild password error
    response = client.post(login_url, data=credintails)

    # compare the `unvaild_pass_msg` variable and
    # the returned unvaild password message
    assert response.data["detail"] == unvaild_pass_msg


def test_empty_values_for_password_and_email(client):
    credintails = {"email": "", "password": ""}

    response = client.post(login_url, data=credintails)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["email"] == "Email may not be blank"
    assert response.data["password"] == "Password may not be blank"
