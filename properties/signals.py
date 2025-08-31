from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Property

@receiver(post_save, sender=Property)
@receiver(post_delete, sender=Property)
def clear_properties_cache(sender, instance, **kwargs):
    """
    Signal handler to clear the 'all_properties' cache key.
    """
    print("A Property object was changed. Clearing 'all_properties' cache...")
    cache.delete('all_properties')