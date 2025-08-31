from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Gets properties from the cache, or the database if not found.
    Stores the queryset in the cache for 1 hour.
    """
    cache_key = 'all_properties'
    cached_queryset = cache.get(cache_key)

    if cached_queryset:
        print("Retrieving properties from cache...")
        return cached_queryset
    else:
        print("Fetching properties from the database and caching...")
        queryset = Property.objects.all()
        # Store the queryset in cache for 3600 seconds (1 hour)
        cache.set(cache_key, queryset, 3600)
        return queryset