from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "user_type": u.user_type,
            "team_id": str(request.team.id) if getattr(request, "team", None) else None,
        })
