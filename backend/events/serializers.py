"""
Serializers for Eventify API.

Serializers convert Django model instances to/from JSON format,
enabling the frontend to communicate with the backend via REST API.
"""

from rest_framework import serializers
from .models import Event, Participant, Registration


class EventSerializer(serializers.ModelSerializer):
    """
    Serializes Event model data to JSON.
    Includes computed fields: registered_count, seats_left, is_full.
    """
    registered_count = serializers.ReadOnlyField()
    seats_left = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'event_date', 'venue',
            'max_seats', 'category', 'image_url', 'is_active',
            'registered_count', 'seats_left', 'is_full',
            'created_at', 'updated_at'
        ]


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializes Participant model data to JSON."""

    class Meta:
        model = Participant
        fields = ['id', 'name', 'email', 'phone', 'college', 'created_at']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes Registration data with nested event and participant details.
    This demonstrates JOIN-like behavior in the API response.
    """
    event_name = serializers.CharField(source='event.name', read_only=True)
    participant_name = serializers.CharField(source='participant.name', read_only=True)
    participant_email = serializers.CharField(source='participant.email', read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id', 'event', 'participant', 'event_name',
            'participant_name', 'participant_email', 'registered_at'
        ]


class EventRegistrationSerializer(serializers.Serializer):
    """
    Custom serializer for the registration endpoint.
    Accepts participant details + event_id and handles:
      1. Creating or finding the participant (INSERT or SELECT)
      2. Creating the registration record (INSERT with FK references)
    """
    event_id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, required=False, default='')
    college = serializers.CharField(max_length=200, required=False, default='')

    def validate_event_id(self, value):
        """Check that the event exists and has available seats."""
        try:
            event = Event.objects.get(id=value, is_active=True)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found or is not active.")

        if event.is_full:
            raise serializers.ValidationError("This event is fully booked. No seats available.")

        return value

    def create(self, validated_data):
        """
        Handle registration:
          1. GET or CREATE participant (demonstrates SELECT + INSERT)
          2. CREATE registration (demonstrates INSERT with Foreign Keys)
        """
        event = Event.objects.get(id=validated_data['event_id'])

        # get_or_create: SELECT first, INSERT if not found
        participant, created = Participant.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'name': validated_data['name'],
                'phone': validated_data.get('phone', ''),
                'college': validated_data.get('college', ''),
            }
        )

        # Check for duplicate registration
        if Registration.objects.filter(event=event, participant=participant).exists():
            raise serializers.ValidationError(
                {"detail": "You are already registered for this event."}
            )

        # Create the registration (INSERT with Foreign Keys)
        registration = Registration.objects.create(
            event=event,
            participant=participant
        )

        return registration
