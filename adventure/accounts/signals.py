from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from adventure.accounts.models import AppProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        AppProfile.objects.create(user=instance)
