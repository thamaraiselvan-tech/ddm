"""
API Views for Eventify - Event Registration System.

Each view demonstrates a different type of database operation:
  - EventListView:        SELECT all events (with optional filtering)
  - EventDetailView:      SELECT single event by ID
  - EventCreateView:      INSERT new event
  - EventUpdateView:      UPDATE event by ID
  - EventDeleteView:      DELETE event by ID
  - RegisterView:         INSERT participant + INSERT registration (transaction)
  - EventRegistrations:   SELECT with JOIN (registrations + participant details)
  - DashboardStats:       Aggregate queries (COUNT, SUM)
  - SearchEvents:         SELECT with WHERE + LIKE (search/filter)
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.utils import timezone

from .models import Event, Participant, Registration
from .serializers import (
    EventSerializer,
    ParticipantSerializer,
    RegistrationSerializer,
    EventRegistrationSerializer,
)


# ============================================================
# EVENT CRUD OPERATIONS
# ============================================================

@api_view(['GET'])
def event_list(request):
    """
    GET /api/events/
    Fetch all active events from the database.

    SQL: SELECT * FROM events WHERE is_active = 1 ORDER BY event_date;

    Optional query params:
      ?category=hackathon  → Filter by category
      ?upcoming=true       → Only future events
    """
    events = Event.objects.filter(is_active=True)

    # Filter by category if provided
    category = request.query_params.get('category')
    if category:
        events = events.filter(category=category)

    # Filter upcoming events only
    upcoming = request.query_params.get('upcoming')
    if upcoming == 'true':
        events = events.filter(event_date__gte=timezone.now())

    serializer = EventSerializer(events, many=True)
    return Response({
        'status': 'success',
        'count': events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
def event_detail(request, event_id):
    """
    GET /api/events/<id>/
    Fetch a single event by its primary key.

    SQL: SELECT * FROM events WHERE id = <event_id>;
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = EventSerializer(event)
    return Response({'status': 'success', 'data': serializer.data})


@api_view(['POST'])
def event_create(request):
    """
    POST /api/events/create/
    Create a new event in the database.

    SQL: INSERT INTO events (name, description, event_date, venue, max_seats, category)
         VALUES (...);
    """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'status': 'success', 'message': 'Event created successfully', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'status': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
def event_update(request, event_id):
    """
    PUT /api/events/<id>/update/
    Update an existing event.

    SQL: UPDATE events SET name=..., description=... WHERE id = <event_id>;
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'status': 'success', 'message': 'Event updated successfully', 'data': serializer.data}
        )
    return Response(
        {'status': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def event_delete(request, event_id):
    """
    DELETE /api/events/<id>/delete/
    Delete an event from the database.

    SQL: DELETE FROM events WHERE id = <event_id>;
    (This also cascades to delete related registrations)
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    event_name = event.name
    event.delete()
    return Response(
        {'status': 'success', 'message': f'Event "{event_name}" deleted successfully'},
        status=status.HTTP_200_OK
    )


# ============================================================
# REGISTRATION (Core: Frontend → Backend → Database)
# ============================================================

@api_view(['POST'])
def register_for_event(request):
    """
    POST /api/register/
    Register a participant for an event.

    This endpoint demonstrates the full flow:
      1. Frontend sends JSON data via fetch()
      2. Backend validates the data
      3. Backend executes INSERT queries on MySQL
      4. Backend returns JSON response to frontend

    SQL Operations:
      - SELECT * FROM participants WHERE email = '...';   (check existing)
      - INSERT INTO participants (...) VALUES (...);       (if new)
      - INSERT INTO registrations (event_id, participant_id) VALUES (...);
    """
    serializer = EventRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            registration = serializer.save()
            return Response({
                'status': 'success',
                'message': f'Successfully registered for {registration.event.name}!',
                'data': {
                    'registration_id': registration.id,
                    'event': registration.event.name,
                    'participant': registration.participant.name,
                    'seats_left': registration.event.seats_left,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(
        {'status': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


# ============================================================
# REGISTRATION LIST (JOIN Query)
# ============================================================

@api_view(['GET'])
def event_registrations(request, event_id):
    """
    GET /api/events/<id>/registrations/
    Get all registrations for a specific event with participant details.

    SQL: SELECT r.*, p.name, p.email
         FROM registrations r
         JOIN participants p ON r.participant_id = p.id
         WHERE r.event_id = <event_id>;
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    registrations = Registration.objects.filter(event=event).select_related('participant')
    serializer = RegistrationSerializer(registrations, many=True)

    return Response({
        'status': 'success',
        'event': event.name,
        'total_registrations': registrations.count(),
        'seats_left': event.seats_left,
        'data': serializer.data
    })


# ============================================================
# DASHBOARD STATISTICS (Aggregate Queries)
# ============================================================

@api_view(['GET'])
def dashboard_stats(request):
    """
    GET /api/dashboard/
    Get aggregate statistics for the dashboard.

    SQL:
      - SELECT COUNT(*) FROM events WHERE is_active = 1;
      - SELECT COUNT(*) FROM participants;
      - SELECT COUNT(*) FROM registrations;
      - SELECT SUM(max_seats) FROM events WHERE is_active = 1;
    """
    total_events = Event.objects.filter(is_active=True).count()
    total_participants = Participant.objects.count()
    total_registrations = Registration.objects.count()
    total_seats = Event.objects.filter(is_active=True).aggregate(
        total=Sum('max_seats')
    )['total'] or 0

    # Events with most registrations (GROUP BY + ORDER BY)
    popular_events = Event.objects.filter(is_active=True).annotate(
        reg_count=Count('registrations')
    ).order_by('-reg_count')[:5]

    popular_data = [
        {
            'id': e.id,
            'name': e.name,
            'category': e.category,
            'registrations': e.reg_count,
            'max_seats': e.max_seats,
            'seats_left': e.seats_left,
        }
        for e in popular_events
    ]

    return Response({
        'status': 'success',
        'data': {
            'total_events': total_events,
            'total_participants': total_participants,
            'total_registrations': total_registrations,
            'total_seats': total_seats,
            'popular_events': popular_data,
        }
    })


# ============================================================
# SEARCH (WHERE + LIKE Query)
# ============================================================

@api_view(['GET'])
def search_events(request):
    """
    GET /api/events/search/?q=python
    Search events by name, description, or venue.

    SQL: SELECT * FROM events
         WHERE (name LIKE '%python%' OR description LIKE '%python%' OR venue LIKE '%python%')
         AND is_active = 1;
    """
    query = request.query_params.get('q', '')
    if not query:
        return Response(
            {'status': 'error', 'message': 'Please provide a search query (?q=...)'},
            status=status.HTTP_400_BAD_REQUEST
        )

    events = Event.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(venue__icontains=query),
        is_active=True
    )

    serializer = EventSerializer(events, many=True)
    return Response({
        'status': 'success',
        'query': query,
        'count': events.count(),
        'data': serializer.data
    })


# ============================================================
# ALL PARTICIPANTS LIST
# ============================================================

@api_view(['GET'])
def participant_list(request):
    """
    GET /api/participants/
    List all registered participants.

    SQL: SELECT * FROM participants ORDER BY name;
    """
    participants = Participant.objects.all()
    serializer = ParticipantSerializer(participants, many=True)
    return Response({
        'status': 'success',
        'count': participants.count(),
        'data': serializer.data
    })


@api_view(['PUT'])
def participant_update(request, participant_id):
    """
    PUT /api/participants/<id>/update/
    Update participant details.

    SQL: UPDATE participants SET name=..., email=..., phone=..., college=... WHERE id = <participant_id>;
    """
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Participant not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ParticipantSerializer(participant, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Participant updated successfully',
            'data': serializer.data
        })
    return Response(
        {'status': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def participant_delete(request, participant_id):
    """
    DELETE /api/participants/<id>/delete/
    Delete a participant from the database.

    SQL: DELETE FROM participants WHERE id = <participant_id>;
    """
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Participant not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    participant_name = participant.name
    participant.delete()
    return Response({
        'status': 'success',
        'message': f'Participant "{participant_name}" deleted successfully'
    }, status=status.HTTP_200_OK)

