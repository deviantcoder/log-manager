import hashlib

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import LogSource


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid authorization header format')
        
        api_key = auth_header.replace('Bearer ', '').strip()

        if not api_key:
            raise AuthenticationFailed('API key not provided')
        
        hashed_key = hashlib.sha256(api_key.encode('utf-8')).hexdigest()

        try:
            source = LogSource.objects.select_related('project').get(
                api_key_hash=hashed_key,
                status=LogSource.SOURCE_STATUSES.ACTIVE
            )

            return (source, None)
        except LogSource.DoesNotExist:
            raise AuthenticationFailed('Invalid API key or source is not active')
