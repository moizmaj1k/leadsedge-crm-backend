from django.http import JsonResponse
from .models import Team, TeamMembership

class TeamHeaderMiddleware:
    """
    Resolves request.team via X-Team-ID header.
    - Only enforced for authenticated requests.
    - You can later exempt certain endpoints or support a default team.
    """
    HEADER_NAME = "HTTP_X_TEAM_ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.team = None

        if request.user.is_authenticated:
            team_id = request.META.get(self.HEADER_NAME)
            if team_id:
                try:
                    team = Team.objects.get(id=team_id)
                except Team.DoesNotExist:
                    return JsonResponse({"detail": "Invalid X-Team-ID"}, status=400)

                # membership check
                is_member = TeamMembership.objects.filter(
                    team=team, user=request.user, is_active=True
                ).exists()

                # platform users can access without membership if needed
                if not is_member and getattr(request.user, "user_type", "") != "PLATFORM":
                    return JsonResponse({"detail": "You are not a member of this team"}, status=403)

                request.team = team

        return self.get_response(request)
