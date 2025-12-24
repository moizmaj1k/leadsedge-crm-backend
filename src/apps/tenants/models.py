from django.db import models
from apps.common.models import BaseModel

class TeamStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "ACTIVE"
    SUSPENDED = "SUSPENDED", "SUSPENDED"

class Team(BaseModel):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=TeamStatus.choices, default=TeamStatus.ACTIVE)
    created_by_platform_user = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_teams"
    )
    timezone = models.CharField(max_length=64, blank=True, default="UTC")
    default_currency = models.CharField(max_length=8, blank=True, default="USD")
    low_balance_threshold = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class TeamRole(models.TextChoices):
    TEAM_ADMIN = "TEAM_ADMIN", "TEAM_ADMIN"
    SUPERVISOR = "SUPERVISOR", "SUPERVISOR"
    AGENT = "AGENT", "AGENT"

class TeamMembership(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="team_memberships")
    role = models.CharField(max_length=16, choices=TeamRole.choices)
    is_active = models.BooleanField(default=True)
    invited_by_user = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="team_invites_sent"
    )
    joined_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("team", "user")
