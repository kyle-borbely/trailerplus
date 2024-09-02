from .models import Custom, Fleet
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import custom_email, fleet_email


@receiver(post_save, sender=Custom)
def send_custom(sender, instance, created, **kwargs):
    if created:
        custom_email.run(instance.pk)


@receiver(post_save, sender=Fleet)
def send_fleet(sender, instance, created, **kwargs):
    if created:
        fleet_email.run(instance.pk)
