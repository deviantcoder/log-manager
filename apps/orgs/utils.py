import logging

from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import OrgInvite


logger = logging.getLogger(__name__)


def send_invite_email(invite: OrgInvite):
    try:
        if invite:
            accept_invite_url = settings.DOMAIN + reverse(
                'orgs:accept_invite',
                kwargs={
                    'token': str(invite.token),
                }
            )

            subject = "You've been invited to join an organization"

            message = render_to_string(
                'email_invitation/invite_email.html',
                {
                    'invite': invite,
                    'accept_invite_url': accept_invite_url,
                }
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[invite.email],
                html_message=message
            )

    except Exception as e:
        logger.error(f'Error during sending invitation email: {e}')