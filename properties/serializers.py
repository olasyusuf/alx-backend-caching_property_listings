from rest_framework import serializers

from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for the Property model
    """
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ["id", "created_at"]