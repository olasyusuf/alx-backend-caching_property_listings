from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Property
from properties.serializers import PropertySerializer

@cache_page(60 * 15)  # Cache the page for 15 minutes
def property_list(request):
    """
    Retrieves and displays a list of all properties.
    The entire page response is cached in Redis.
    """
    if request.method == "GET":
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse({"properties": serializer.data}, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)