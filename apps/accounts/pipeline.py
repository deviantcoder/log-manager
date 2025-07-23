import logging

from django.contrib import messages
from django.utils.timezone import now
from apps.orgs.models import OrgInvite, OrgMember


logger = logging.getLogger(__name__)


def process_invite(backend, user, request, *args, **kwargs):
    token = request.session.get('invite_token')

    if token:
        try:
            invite = OrgInvite.objects.get(token=token, email__iexact=user.email, accepted=False, declined=False)

            invite.accepted = True
            invite.save(update_fields=['accepted'])

            OrgMember.objects.get_or_create(org=invite.org, user=user)

            try:
                del request.session['invite_token']
            except KeyError:
                logger.warning(f'No invite_token in session for {user}')

            messages.success(request, f"You've joined {invite.org.name}")
        except OrgInvite.DoesNotExist:
            messages.warning(request, "This invitation is no longer valid.")
