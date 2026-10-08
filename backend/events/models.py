"""
Database Models for Eventify - Event Registration System.

This module defines three core tables that demonstrate relational database design:
  1. Event       - Stores event details (name, date, venue, max_seats, etc.)
  2. Participant - Stores participant information (name, email, phone)
  3. Registration - Links participants to events (many-to-many with metadata)

Key Database Concepts Demonstrated:
  - Primary Keys (auto-generated BigAutoField)
  - Foreign Keys (Registration → Event, Registration → Participant)
  - Unique Constraints (one registration per participant per event)
  - Data Types (CharField, TextField, DateTimeField, IntegerField, EmailField)
  - Indexes (for faster lookups)
"""

from django.db import models
from django.core.validators import MinValueValidator


class Event(models.Model):
    """
    Event table - Stores information about each event/hackathon.

    SQL Equivalent:
        CREATE TABLE events_event (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            event_date DATETIME NOT NULL,
            venue VARCHAR(300) NOT NULL,
            max_seats INT NOT NULL CHECK (max_seats >= 1),
            category VARCHAR(50) NOT NULL,
            image_url VARCHAR(500),
            is_active TINYINT(1) DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """

    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathon'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('webinar', 'Webinar'),
        ('conference', 'Conference'),
        ('meetup', 'Meetup'),
        ('competition', 'Competition'),
    ]

    name = models.CharField(max_length=200, help_text="Name of the event")
    description = models.TextField(help_text="Detailed description of the event")
    event_date = models.DateTimeField(help_text="Date and time of the event")
    venue = models.CharField(max_length=300, help_text="Location/venue of the event")
    max_seats = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Maximum number of seats available"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='hackathon',
        help_text="Category of the event"
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL for event banner image"
    )
    is_active = models.BooleanField(default=True, help_text="Whether the event is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        ordering = ['event_date']
        indexes = [
            models.Index(fields=['event_date'], name='idx_event_date'),
            models.Index(fields=['category'], name='idx_event_category'),
            models.Index(fields=['is_active'], name='idx_event_active'),
        ]

    def __str__(self):
        return f"{self.name} ({self.event_date.strftime('%Y-%m-%d')})"

    @property
    def registered_count(self):
        """Count of registrations for this event (uses COUNT query)."""
        return self.registrations.count()

    @property
    def seats_left(self):
        """Calculate remaining seats (max_seats - registered_count)."""
        return max(0, self.max_seats - self.registered_count)

    @property
    def is_full(self):
        """Check if event has no seats left."""
        return self.seats_left == 0


class Participant(models.Model):
    """
    Participant table - Stores information about registered participants.

    SQL Equivalent:
        CREATE TABLE participants (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE,
            phone VARCHAR(15),
            college VARCHAR(200),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """

    name = models.CharField(max_length=200, help_text="Full name of the participant")
    email = models.EmailField(unique=True, help_text="Email address (unique identifier)")
    phone = models.CharField(max_length=15, blank=True, help_text="Phone number")
    college = models.CharField(max_length=200, blank=True, help_text="College/University name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participants'
        ordering = ['name']
        indexes = [
            models.Index(fields=['email'], name='idx_participant_email'),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"


class Registration(models.Model):
    """
    Registration table - Junction/bridge table linking Participants to Events.
    This demonstrates a Many-to-Many relationship with additional metadata.

    SQL Equivalent:
        CREATE TABLE registrations (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            event_id BIGINT NOT NULL,
            participant_id BIGINT NOT NULL,
            registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
            UNIQUE KEY unique_registration (event_id, participant_id)
        );
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="Foreign Key → Event table"
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="Foreign Key → Participant table"
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registrations'
        # Unique constraint: one person can register for an event only once
        unique_together = ['event', 'participant']
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['event', 'participant'], name='idx_reg_event_participant'),
        ]

    def __str__(self):
        return f"{self.participant.name} → {self.event.name}"
