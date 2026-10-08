"""
URL routing for the Events API.

Each URL maps to a view function that performs database operations.
All routes are prefixed with /api/ (configured in eventify/urls.py).
"""

from django.urls import path
from . import views

urlpatterns = [
    # ---- Event CRUD ----
    path('events/', views.event_list, name='event-list'),                          # GET    → SELECT all
    path('events/<int:event_id>/', views.event_detail, name='event-detail'),       # GET    → SELECT one
    path('events/create/', views.event_create, name='event-create'),               # POST   → INSERT
    path('events/<int:event_id>/update/', views.event_update, name='event-update'),# PUT    → UPDATE
    path('events/<int:event_id>/delete/', views.event_delete, name='event-delete'),# DELETE → DELETE

    # ---- Registration ----
    path('register/', views.register_for_event, name='register'),                  # POST   → INSERT (with FK)

    # ---- Registrations List (JOIN) ----
    path('events/<int:event_id>/registrations/', views.event_registrations, name='event-registrations'),

    # ---- Dashboard (Aggregates) ----
    path('dashboard/', views.dashboard_stats, name='dashboard'),                   # GET → COUNT, SUM

    # ---- Search (WHERE + LIKE) ----
    path('events/search/', views.search_events, name='search-events'),             # GET → WHERE LIKE

    # ---- Participants ----
    path('participants/', views.participant_list, name='participant-list'),         # GET    → SELECT all
    path('participants/<int:participant_id>/update/', views.participant_update, name='participant-update'), # PUT → UPDATE
    path('participants/<int:participant_id>/delete/', views.participant_delete, name='participant-delete'), # DELETE → DELETE
]

