import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

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
    

def get_redis_cache_metrics():
    """
    Connects to Redis to retrieve and calculate cache hit/miss metrics.
    """
    try:
        # Get the low-level Redis client connection
        redis_conn = get_redis_connection("default")
        
        # Get the INFO dictionary from Redis
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate the hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
        # Log the metrics to the console for analysis
        print("--- Redis Cache Metrics ---")
        print(f"Keyspace Hits: {keyspace_hits}")
        print(f"Keyspace Misses: {keyspace_misses}")
        print(f"Total Requests: {total_requests}")
        print(f"Hit Ratio: {hit_ratio:.2f}%")
        print("---------------------------")
        
        # Log metrics
        logger.info(
            f"Cache metrics - keyspace_hits: {keyspace_hits}, keyspace_misses: {keyspace_misses}, "
            f"hit_ratio: {hit_ratio:.2%}"
        )
        
        # Return the metrics as a dictionary
        return {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2)
        }
        
    except Exception as e:
        print(f"Error retrieving Redis metrics: {e}")
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e)
        }