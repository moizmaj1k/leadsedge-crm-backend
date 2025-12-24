from django.db import models
from apps.common.models import TeamScopedModel, SoftDeleteModel

class ContactSource(models.TextChoices):
    IMPORT = "IMPORT", "IMPORT"
    MANUAL = "MANUAL", "MANUAL"
    API = "API", "API"

class LeadStatus(TeamScopedModel):
    name = models.CharField(max_length=64)
    is_won = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("team", "name")

    def __str__(self):
        return f"{self.team_id}:{self.name}"

class Contact(TeamScopedModel, SoftDeleteModel):
    full_name = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True, null=True)
    source = models.CharField(max_length=16, choices=ContactSource.choices, default=ContactSource.MANUAL)
    status = models.ForeignKey(LeadStatus, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts")
    assigned_to_user = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_contacts"
    )
    notes = models.TextField(blank=True, default="")
    last_activity_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone"]),
            models.Index(fields=["team", "phone"]),
        ]

class ContactTag(TeamScopedModel):
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ("team", "name")

class ContactTagMap(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    tag = models.ForeignKey(ContactTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "tag")

class ContactList(TeamScopedModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ("team", "name")

class ContactListMap(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    list = models.ForeignKey(ContactList, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "list")
