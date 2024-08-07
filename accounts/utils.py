from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


def detectUser(user):
    if user.role == 1:
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "custDashboard"
        return redirectUrl
    elif user.role is None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl


def send_mail(request, user, mail_subject, template_name):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(
        template_name,
        context={
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context.get("user").email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


def checkIfItsVendor(request):
    if detectUser(request.user) != "vendorDashboard":
        raise PermissionDenied


def checkIfItsCustomer(request):
    if detectUser(request.user) != "custDashboard":
        raise PermissionDenied
