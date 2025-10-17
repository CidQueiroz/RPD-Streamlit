from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HealthCheckView(APIView):
    """
    A simple view to check if the API is up and running.
    """
    def get(self, request, *args, **kwargs):
        """
        Returns a 200 OK response with a success message.
        """
        return Response({"status": "ok"}, status=status.HTTP_200_OK)