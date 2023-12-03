from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response


@permission_classes((permissions.AllowAny,))
class HealthCheck(APIView):

    def get(self, request):
        return Response([], status=200)
