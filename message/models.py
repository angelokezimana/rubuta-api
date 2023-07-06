import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from core.models import BaseModel


class Message(BaseModel):
    DEFAULT_MSG_STATUS_SENDER_CHOICES = "sent"
    MSG_STATUS_SENDER_CHOICES = [
        ("draft", "draft"),
        (DEFAULT_MSG_STATUS_SENDER_CHOICES, "sent"),
        ("bin", "bin"),
        ("delete", "delete"),
    ]

    MSG_STATUS_RECIPIENT_CHOICES = [
        ("unread", "unread"),
        ("read", "read"),
        ("bin", "bin"),
        ("delete", "delete"),
        ("bin_unread", "bin_unread"),
        ("delete_unread", "delete_unread"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg_object = models.CharField(verbose_name="Object of the message", max_length=255)
    msg_content = models.TextField(verbose_name="Message content")
    msg_status_sender = models.CharField(
        verbose_name="Message status for sender",
        max_length=30,
        choices=MSG_STATUS_SENDER_CHOICES,
        default=DEFAULT_MSG_STATUS_SENDER_CHOICES,
    )
    msg_status_recipient = models.CharField(
        verbose_name="Message status for recipient",
        max_length=30,
        choices=MSG_STATUS_RECIPIENT_CHOICES,
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender_user",
        verbose_name="Sender user",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipient_user",
        verbose_name="Recipient user",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
