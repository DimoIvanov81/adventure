from django.db import models


class TrackDifficulty(models.TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'
    Unknown = 'unknown', 'Unknown'
