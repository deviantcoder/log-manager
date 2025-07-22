import logging
import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone

from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import User


logger = logging.getLogger(__name__)


def send_verification_email(user: User):
    try:
        if user:
            if user.last_verification_email_sent:
                now = timezone.now()
                cooldown_delta = now - user.last_verification_email_sent

                if cooldown_delta < datetime.timedelta(minutes=settings.EMAIL_RESEND_COOLDOWN):
                    logger.info(f'Verification email for: {user.username}, skipped due to cooldown.')
                    return False

            token_generator = PasswordResetTokenGenerator()

            public_id = urlsafe_base64_encode(force_bytes(user.public_id))
            token = token_generator.make_token(user)

            verification_url = settings.DOMAIN + reverse(
                'accounts:verify_email',
                kwargs={
                    'uidb64': public_id,
                    'token': token,
                }
            )

            subject = 'Email Verification'

            message = render_to_string(
                'email_verification/verify_email.html',
                {
                    'user': user,
                    'verification_url': verification_url,
                }
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=message
            )

            user.last_verification_email_sent = timezone.now()
            user.save(update_fields=['last_verification_email_sent'])

            return True

    except Exception as e:
        logger.error(f'Error during sending email verification: {e}')