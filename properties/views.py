from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import Property

@cache_page(60 * 15)  # Cache the page for 15 minutes
def property_list(request):
    """
    Retrieves and displays a list of all properties.
    The entire page response is cached in Redis.
    """
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})