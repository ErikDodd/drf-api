from rest_framework import serializers
from .models import Car

# Defines a new class, ThingSerializer, which subclasses serializers.ModelSerializer. This means that the ThingSerializer class inherits all the behavior of serializers.ModelSerializer, but can also add or override behavior as needed.

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "owner", "name", "description", "created_at")
        model = Car
