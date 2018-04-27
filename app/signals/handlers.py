from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Query
from app.tasks import extract_audio_link


@receiver(post_save, sender=Query)
def new_query(sender, **kwargs):
    instance = kwargs['instance']
    extract_audio_link.delay(instance.pk)
