from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Subscription
from datetime import date, timedelta


@receiver(post_save, sender=User)
def create_subscriptions(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user=instance,
            valid_until=date.today() + timedelta(days=15),
            is_trial=True,
            is_active=True
        )


@receiver(post_save, sender=User)
def save_subscriptions(sender, instance, **kwargs):
    instance.subscription.save()
