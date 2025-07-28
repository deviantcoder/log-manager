from rest_framework import views, status
from rest_framework.response import Response

from .authentication import APIKeyAuthentication
from .serializers import LogEntrySerializer


class LogIngestionAPIView(views.APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        source = request.user

        serilizer = LogEntrySerializer(
            data=request.data,
            context={'source': source}
        )

        if serilizer.is_valid():
            log_entry = serilizer.save()

            return Response(
                {
                    'status': 'success',
                    'message': 'Log entry created',
                    'log_id': log_entry.id,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'errors': serilizer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
