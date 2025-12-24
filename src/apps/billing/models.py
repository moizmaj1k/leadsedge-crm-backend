from django.db import models
from apps.common.models import BaseModel

class WalletStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "ACTIVE"
    FROZEN = "FROZEN", "FROZEN"

class Wallet(BaseModel):
    team = models.OneToOneField("tenants.Team", on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="USD")
    low_balance_threshold = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=16, choices=WalletStatus.choices, default=WalletStatus.ACTIVE)

class WalletTransactionType(models.TextChoices):
    TOPUP = "TOPUP", "TOPUP"
    SMS = "SMS", "SMS"
    CALL = "CALL", "CALL"
    NUMBER_PURCHASE = "NUMBER_PURCHASE", "NUMBER_PURCHASE"
    NUMBER_FEE = "NUMBER_FEE", "NUMBER_FEE"
    ADJUSTMENT = "ADJUSTMENT", "ADJUSTMENT"
    PLATFORM_FEE = "PLATFORM_FEE", "PLATFORM_FEE"

class WalletTransaction(BaseModel):
    team = models.ForeignKey("tenants.Team", on_delete=models.CASCADE, related_name="wallet_transactions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=32, choices=WalletTransactionType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=8, default="USD")
    reference_type = models.CharField(max_length=32, blank=True, default="")
    reference_id = models.UUIDField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    meta = models.JSONField(null=True, blank=True)
    created_by_user = models.ForeignKey(
        "accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="wallet_transactions_created"
    )

    class Meta:
        indexes = [
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["team", "type", "created_at"]),
        ]
