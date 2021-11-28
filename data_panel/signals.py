from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


from .models import Subscription


@receiver(post_save, sender=User)
def create_subscriptions(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user=instance,
            valid_until=timezone.now() + timedelta(days=15),
            is_trial=True,
        )


@receiver(post_save, sender=User)
def save_subscriptions(sender, instance, **kwargs):
    instance.subscription.save()
