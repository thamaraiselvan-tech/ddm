"""
Seed script to populate the database with sample event data.

Run this after migrations:
    python manage.py shell < seed_data.py
    
Or:
    python manage.py shell
    >>> exec(open('seed_data.py').read())
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventify.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from events.models import Event, Participant, Registration

print("=" * 60)
print("🌱 Seeding Database with Sample Data...")
print("=" * 60)

# ---- Create Sample Events ----
events_data = [
    {
        'name': 'HackFusion 2024',
        'description': 'A 48-hour hackathon where teams build innovative solutions to real-world problems. Prizes worth ₹50,000! Join us for an exciting journey of coding, collaboration, and creativity.',
        'event_date': timezone.now() + timedelta(days=15),
        'venue': 'Main Auditorium, Block A',
        'max_seats': 100,
        'category': 'hackathon',
        'image_url': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800',
    },
    {
        'name': 'Python for Data Science Workshop',
        'description': 'Hands-on workshop covering Pandas, NumPy, Matplotlib, and Scikit-learn. Build your first ML model in just 3 hours! Laptops required.',
        'event_date': timezone.now() + timedelta(days=7),
        'venue': 'Computer Lab 3, IT Block',
        'max_seats': 50,
        'category': 'workshop',
        'image_url': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800',
    },
    {
        'name': 'AI & Future of Tech Seminar',
        'description': 'Distinguished speakers from Google and Microsoft discuss the future of Artificial Intelligence, Machine Learning, and their impact on society.',
        'event_date': timezone.now() + timedelta(days=20),
        'venue': 'Seminar Hall, Admin Block',
        'max_seats': 200,
        'category': 'seminar',
        'image_url': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
    },
    {
        'name': 'Web Development Bootcamp',
        'description': 'Learn HTML, CSS, JavaScript, and React in this intensive 2-day bootcamp. Perfect for beginners who want to start their web development journey.',
        'event_date': timezone.now() + timedelta(days=10),
        'venue': 'Smart Classroom 1, CS Block',
        'max_seats': 60,
        'category': 'workshop',
        'image_url': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800',
    },
    {
        'name': 'Cloud Computing Conference',
        'description': 'Annual conference on cloud technologies featuring AWS, Azure, and GCP. Networking opportunities with industry professionals.',
        'event_date': timezone.now() + timedelta(days=30),
        'venue': 'Convention Center, Main Campus',
        'max_seats': 150,
        'category': 'conference',
        'image_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800',
    },
    {
        'name': 'Competitive Programming Meetup',
        'description': 'Weekly competitive programming session. Solve problems from Codeforces, LeetCode, and HackerRank together. All skill levels welcome!',
        'event_date': timezone.now() + timedelta(days=3),
        'venue': 'Lab 5, CS Block',
        'max_seats': 40,
        'category': 'meetup',
        'image_url': 'https://images.unsplash.com/photo-1515879218367-8466d910auj7?w=800',
    },
    {
        'name': 'CodeSprint Challenge',
        'description': 'Speed coding competition with 5 progressively harder problems. Top 3 winners get internship referrals and cash prizes!',
        'event_date': timezone.now() + timedelta(days=12),
        'venue': 'CS Lab 1, IT Block',
        'max_seats': 80,
        'category': 'competition',
        'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
    },
    {
        'name': 'Cybersecurity Webinar',
        'description': 'Online webinar on ethical hacking, penetration testing, and cybersecurity best practices. Guest speaker from CrowdStrike.',
        'event_date': timezone.now() + timedelta(days=5),
        'venue': 'Online (Zoom)',
        'max_seats': 300,
        'category': 'webinar',
        'image_url': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800',
    },
]

created_events = []
for event_data in events_data:
    event, created = Event.objects.get_or_create(
        name=event_data['name'],
        defaults=event_data
    )
    created_events.append(event)
    status_text = "✅ Created" if created else "⏭️  Already exists"
    print(f"  {status_text}: {event.name}")

# ---- Create Sample Participants ----
participants_data = [
    {'name': 'Aarav Sharma', 'email': 'aarav.sharma@email.com', 'phone': '9876543210', 'college': 'IIT Madras'},
    {'name': 'Priya Patel', 'email': 'priya.patel@email.com', 'phone': '9876543211', 'college': 'NIT Trichy'},
    {'name': 'Rahul Kumar', 'email': 'rahul.kumar@email.com', 'phone': '9876543212', 'college': 'VIT Vellore'},
    {'name': 'Sneha Reddy', 'email': 'sneha.reddy@email.com', 'phone': '9876543213', 'college': 'SRM University'},
    {'name': 'Vikram Singh', 'email': 'vikram.singh@email.com', 'phone': '9876543214', 'college': 'Anna University'},
    {'name': 'Anjali Nair', 'email': 'anjali.nair@email.com', 'phone': '9876543215', 'college': 'IIT Madras'},
    {'name': 'Karthik Rajan', 'email': 'karthik.rajan@email.com', 'phone': '9876543216', 'college': 'NIT Trichy'},
    {'name': 'Deepa Menon', 'email': 'deepa.menon@email.com', 'phone': '9876543217', 'college': 'VIT Vellore'},
]

created_participants = []
for p_data in participants_data:
    participant, created = Participant.objects.get_or_create(
        email=p_data['email'],
        defaults=p_data
    )
    created_participants.append(participant)
    status_text = "✅ Created" if created else "⏭️  Already exists"
    print(f"  {status_text}: {participant.name}")

# ---- Create Sample Registrations ----
registration_pairs = [
    (0, 0), (0, 1), (0, 2), (0, 3),  # HackFusion: 4 registrations
    (1, 1), (1, 2), (1, 4),          # Python Workshop: 3 registrations
    (2, 0), (2, 3), (2, 5), (2, 6),  # AI Seminar: 4 registrations
    (3, 2), (3, 4), (3, 7),          # Web Dev Bootcamp: 3 registrations
    (4, 0), (4, 5),                   # Cloud Conference: 2 registrations
    (5, 1), (5, 6),                   # CP Meetup: 2 registrations
    (6, 3), (6, 4), (6, 7),          # CodeSprint: 3 registrations
    (7, 0), (7, 2), (7, 5), (7, 7),  # Cybersecurity: 4 registrations
]

for event_idx, participant_idx in registration_pairs:
    if event_idx < len(created_events) and participant_idx < len(created_participants):
        reg, created = Registration.objects.get_or_create(
            event=created_events[event_idx],
            participant=created_participants[participant_idx]
        )
        if created:
            print(f"  ✅ Registered: {reg.participant.name} → {reg.event.name}")

print("\n" + "=" * 60)
print("🎉 Database seeding complete!")
print(f"   Events: {Event.objects.count()}")
print(f"   Participants: {Participant.objects.count()}")
print(f"   Registrations: {Registration.objects.count()}")
print("=" * 60)
