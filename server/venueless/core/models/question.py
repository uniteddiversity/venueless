import uuid
from functools import cached_property

from django.contrib.postgres.fields import JSONField
from django.db import models
from rest_framework import serializers


class Question(models.Model):
    class States(models.TextChoices):
        VISIBLE = "visible"
        MOD_QUEUE = "mod_queue"  # This question is waiting to be moderated
        ARCHIVED = "archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField()
    state = models.CharField(
        default=States.MOD_QUEUE, choices=States.choices, max_length=10
    )
    answered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    room = models.ForeignKey(
        to="Room",
        related_name="questions",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="questions",
    )
    moderator = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="moderated_questions",
    )

    @cached_property
    def score(self):
        return self.votes.all().count()


class QuestionVote(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="votes"
    )
    sender = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="question_votes",
    )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "state",
            "answered",
            "timestamp",
            "room_id",
        )