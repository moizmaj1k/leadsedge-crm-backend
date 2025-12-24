from django.db import models
from apps.common.models import BaseModel

class AuditLog(BaseModel):
    team = models.ForeignKey("tenants.Team", on_delete=models.CASCADE, related_name="audit_logs")
    actor_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64, blank=True, default="")
    entity_id = models.UUIDField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    ip_address = models.CharField(max_length=64, blank=True, default="")
