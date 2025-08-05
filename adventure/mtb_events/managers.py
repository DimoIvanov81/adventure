from django.db import models
from datetime import date


class MtbEventQuerySet(models.QuerySet):
    def active(self):
        return self.filter(start_date__gte=date.today())

    def expired(self):
        return self.filter(start_date__lt=date.today())


class MtbEventManager(models.Manager):
    def get_queryset(self):
        return MtbEventQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def expired(self):
        return self.get_queryset().expired()
