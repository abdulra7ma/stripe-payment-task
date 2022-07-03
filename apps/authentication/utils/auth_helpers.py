# Django imports
from django.utils import timezone

# external imports
from user_agents import parse


def deactivate_account(user):
    """
    Deactivate user account
    """
    user.is_superuser = False
    user.is_staff = False
    user.is_active = False
    user.is_frozen = True
    user.last_login = timezone.now()
    user.save()


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def get_user_agent(request):
    ua_string = request.META.get("HTTP_USER_AGENT")

    if ua_string:
        user_agent = parse(request.META.get("HTTP_USER_AGENT"))
        browser = user_agent.browser
        os = user_agent.os
        device = user_agent.is_pc and "PC" or user_agent.device.family

        return (
            device,
            os.family,
            browser.family,
        )
    else:
        return (
            "Other",
            "Other",
            "Other",
        )


def set_last_login(login_device, user=None):
    now = timezone.now()

    login_device.last_login = now
    login_device.save(update_fields=["last_login"])

    if not user:
        user = login_device.user
    user.last_login = now
    user.save(update_fields=["last_login"])


def delete_device(login_device):
    if login_device:
        login_device.delete()
