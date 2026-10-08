/**
 * ============================================================
 *  EVENTIFY - Frontend JavaScript Application
 * ============================================================
 * 
 *  This file handles ALL frontend-to-backend communication.
 *  Every function that talks to the database goes through:
 * 
 *    Frontend (fetch API)  →  Backend (Django REST API)  →  MySQL Database
 *    
 *  Key Concepts Demonstrated:
 *    - fetch() API for HTTP requests (GET, POST, PUT, DELETE)
 *    - Async/Await for handling asynchronous operations
 *    - JSON data exchange between frontend and backend
 *    - Dynamic DOM manipulation based on database responses
 *    - Error handling for network/server errors
 * ============================================================
 */

// ============================================================
// CONFIGURATION
// ============================================================
// Automatically detects whether running locally or live on GitHub Pages
const API_BASE_URL = window.API_BASE_URL || (
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/api'
        : 'https://ddm-eventify-backend.onrender.com/api'
);

// Category emoji mapping
const CATEGORY_ICONS = {
    hackathon: '🏆',
    workshop: '🔧',
    seminar: '🎤',
    webinar: '💻',
    conference: '🌐',
    meetup: '🤝',
    competition: '⚡',
};

// Store all events for client-side filtering
let allEvents = [];
let currentFilter = 'all';


// ============================================================
// API HELPER — Central function for all HTTP requests
// ============================================================
/**
 * Makes an HTTP request to the Django backend.
 * This is the CORE function that connects frontend to backend.
 * 
 * @param {string} endpoint - API endpoint (e.g., '/events/')
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} body - Request body for POST/PUT requests
 * @returns {object} - JSON response from the backend
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    console.log(`📡 [API ${method}] ${url}`, body || '');

    try {
        const response = await fetch(url, options);
        const data = await response.json();
        
        console.log(`✅ [Response]`, data);

        if (!response.ok) {
            throw { status: response.status, data: data };
        }

        return data;
    } catch (error) {
        if (error.data) throw error;
        console.error(`❌ [API Error]`, error);
        throw { status: 0, data: { message: 'Cannot connect to backend. Is the Django server running?' } };
    }
}


// ============================================================
// DATABASE CONNECTION STATUS
// ============================================================
/**
 * Check if the backend (and therefore MySQL) is reachable.
 * Calls the dashboard endpoint as a health check.
 */
async function checkDatabaseConnection() {
    const statusEl = document.getElementById('dbStatus');
    const statusText = document.getElementById('dbStatusText');

    try {
        await apiRequest('/dashboard/');
        statusEl.className = 'db-status connected';
        statusText.textContent = 'Database Connected';
    } catch (error) {
        statusEl.className = 'db-status disconnected';
        statusText.textContent = 'DB Disconnected';
    }
}


// ============================================================
// NAVIGATION
// ============================================================
function navigateTo(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show target page
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.page === page);
    });

    // Close mobile nav
    document.getElementById('navbarNav').classList.remove('open');

    // Load data for the page
    switch (page) {
        case 'home':
            loadDashboardStats();
            loadFeaturedEvents();
            break;
        case 'events':
            loadAllEvents();
            break;
        case 'registrations':
            loadEventSelector();
            break;
        case 'participants':
            loadParticipants();
            break;
        case 'admin':
            loadAdminEvents();
            break;
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleMobileNav() {
    document.getElementById('navbarNav').classList.toggle('open');
}


// ============================================================
// DASHBOARD STATS (Aggregate Queries: COUNT, SUM)
// ============================================================
/**
 * Load dashboard statistics from the backend.
 * 
 * Backend SQL:
 *   SELECT COUNT(*) FROM events;
 *   SELECT COUNT(*) FROM participants;
 *   SELECT COUNT(*) FROM registrations;
 *   SELECT SUM(max_seats) FROM events;
 */
async function loadDashboardStats() {
    try {
        const response = await apiRequest('/dashboard/');
        const stats = response.data;

        // Animate counter
        animateCounter('statEvents', stats.total_events);
        animateCounter('statParticipants', stats.total_participants);
        animateCounter('statRegistrations', stats.total_registrations);
        animateCounter('statSeats', stats.total_seats);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function animateCounter(elementId, target) {
    const el = document.getElementById(elementId);
    const duration = 1200;
    const start = parseInt(el.textContent) || 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (target - start) * eased);
        
        el.textContent = current.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}


// ============================================================
// LOAD EVENTS (SELECT Query)
// ============================================================
/**
 * Load featured events (first 4) for the home page.
 * 
 * Backend SQL: SELECT * FROM events WHERE is_active = 1 ORDER BY event_date LIMIT 4;
 */
async function loadFeaturedEvents() {
    const grid = document.getElementById('featuredEventsGrid');

    try {
        const response = await apiRequest('/events/');
        allEvents = response.data;

        const featured = allEvents.slice(0, 4);
        grid.innerHTML = featured.map(event => createEventCard(event)).join('');
    } catch (error) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-icon">⚠️</div>
                <h3>Cannot Connect to Backend</h3>
                <p>Make sure the Django server is running at ${API_BASE_URL}</p>
                <p style="margin-top: var(--space-md); color: var(--text-tertiary); font-size: 0.8rem;">
                    Run: <code style="color: var(--accent-400);">python manage.py runserver</code>
                </p>
            </div>
        `;
    }
}

/**
 * Load all events with optional category filtering.
 * 
 * Backend SQL: SELECT * FROM events WHERE is_active = 1 AND category = '...' ORDER BY event_date;
 */
async function loadAllEvents() {
    const grid = document.getElementById('allEventsGrid');
    grid.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

    try {
        let endpoint = '/events/';
        if (currentFilter !== 'all') {
            endpoint += `?category=${currentFilter}`;
        }

        const response = await apiRequest(endpoint);
        allEvents = response.data;

        if (allEvents.length === 0) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1/-1;">
                    <div class="empty-icon">📅</div>
                    <h3>No Events Found</h3>
                    <p>No events match the current filter. Try a different category.</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = allEvents.map((event, i) => 
            createEventCard(event, i * 0.05)
        ).join('');
    } catch (error) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-icon">⚠️</div>
                <h3>Cannot Load Events</h3>
                <p>Backend server might be down. Please try again.</p>
            </div>
        `;
    }
}


// ============================================================
// EVENT CARD COMPONENT
// ============================================================
function createEventCard(event, delay = 0) {
    const date = new Date(event.event_date);
    const formattedDate = date.toLocaleDateString('en-IN', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
    const formattedTime = date.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit',
    });

    const percentFilled = ((event.registered_count / event.max_seats) * 100).toFixed(0);
    let seatsClass = 'seats-available';
    let progressClass = '';
    if (event.is_full) {
        seatsClass = 'seats-full';
        progressClass = 'high';
    } else if (event.seats_left <= event.max_seats * 0.2) {
        seatsClass = 'seats-limited';
        progressClass = 'medium';
    }

    const categoryIcon = CATEGORY_ICONS[event.category] || '📅';
    const imageUrl = event.image_url || `https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800`;

    return `
        <div class="event-card" style="animation-delay: ${delay}s;">
            <div class="event-card-image-wrapper">
                <img 
                    src="${imageUrl}" 
                    alt="${event.name}" 
                    class="event-card-image"
                    onerror="this.src='https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800'"
                    loading="lazy"
                >
                <span class="event-card-category">${categoryIcon} ${event.category}</span>
                <span class="event-card-seats-badge ${seatsClass}">
                    ${event.is_full ? '🚫 Full' : `${event.seats_left} seats left`}
                </span>
            </div>
            <div class="event-card-body">
                <h3 class="event-card-title">${event.name}</h3>
                <p class="event-card-desc">${event.description}</p>
                <div class="event-card-meta">
                    <div class="meta-item">
                        <span class="icon">📅</span>
                        ${formattedDate} at ${formattedTime}
                    </div>
                    <div class="meta-item">
                        <span class="icon">📍</span>
                        ${event.venue}
                    </div>
                </div>
                <div class="seats-progress">
                    <div class="seats-info">
                        <span class="seats-count">${event.registered_count} / ${event.max_seats} registered</span>
                        <span class="seats-left" style="color: ${event.is_full ? 'var(--error-500)' : 'var(--success-500)'}">
                            ${event.is_full ? 'Full' : `${event.seats_left} left`}
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill ${progressClass}" style="width: ${Math.min(percentFilled, 100)}%"></div>
                    </div>
                </div>
                <div class="event-card-footer">
                    <button class="btn btn-primary btn-sm" onclick="openRegisterModal(${event.id}, '${event.name.replace(/'/g, "\\'")}')" ${event.is_full ? 'disabled style="opacity:0.5;cursor:not-allowed;"' : ''}>
                        ${event.is_full ? '🚫 Full' : '✅ Register'}
                    </button>
                    <button class="btn btn-outline btn-sm" onclick="viewEventDetails(${event.id})">
                        👁️ Details
                    </button>
                </div>
            </div>
        </div>
    `;
}


// ============================================================
// SEARCH EVENTS (WHERE + LIKE Query)
// ============================================================
let searchTimeout;

/**
 * Search events by name/description/venue.
 * 
 * Backend SQL: SELECT * FROM events WHERE name LIKE '%query%' OR description LIKE '%query%';
 */
function handleSearch() {
    clearTimeout(searchTimeout);
    const query = document.getElementById('searchInput').value.trim();

    searchTimeout = setTimeout(async () => {
        if (!query) {
            loadAllEvents();
            return;
        }

        const grid = document.getElementById('allEventsGrid');
        grid.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

        try {
            const response = await apiRequest(`/events/search/?q=${encodeURIComponent(query)}`);
            const events = response.data;

            if (events.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state" style="grid-column: 1/-1;">
                        <div class="empty-icon">🔍</div>
                        <h3>No Results</h3>
                        <p>No events found for "${query}". Try a different search term.</p>
                    </div>
                `;
                return;
            }

            grid.innerHTML = events.map((event, i) => createEventCard(event, i * 0.05)).join('');
        } catch (error) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1/-1;">
                    <div class="empty-icon">⚠️</div>
                    <h3>Search Failed</h3>
                    <p>Could not perform search. Please try again.</p>
                </div>
            `;
        }
    }, 300);
}


// ============================================================
// FILTER BY CATEGORY
// ============================================================
function filterByCategory(category, buttonEl) {
    currentFilter = category;
    
    // Update pill states
    document.querySelectorAll('.filter-pill').forEach(pill => pill.classList.remove('active'));
    buttonEl.classList.add('active');

    loadAllEvents();
}


// ============================================================
// REGISTRATION (INSERT with Foreign Keys)
// ============================================================
/**
 * Open registration modal for a specific event.
 */
function openRegisterModal(eventId, eventName) {
    document.getElementById('registerEventId').value = eventId;
    document.getElementById('registerEventName').textContent = eventName;
    document.getElementById('registerForm').reset();
    document.getElementById('registerEventId').value = eventId;
    openModal('registerModal');
}

/**
 * Handle registration form submission.
 * 
 * Frontend sends JSON via POST → Backend executes:
 *   1. SELECT/INSERT INTO participants (get_or_create)
 *   2. INSERT INTO registrations (event_id, participant_id)
 */
async function handleRegistration(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('registerSubmitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Registering...';

    const data = {
        event_id: parseInt(document.getElementById('registerEventId').value),
        name: document.getElementById('regName').value,
        email: document.getElementById('regEmail').value,
        phone: document.getElementById('regPhone').value,
        college: document.getElementById('regCollege').value,
    };

    try {
        const response = await apiRequest('/register/', 'POST', data);
        
        closeModal('registerModal');
        showToast('success', response.message || 'Registration successful!');
        
        // Refresh data to show updated seat counts
        loadDashboardStats();
        loadFeaturedEvents();
        loadAllEvents();
    } catch (error) {
        const errorMsg = error.data?.errors?.event_id?.[0] 
            || error.data?.errors?.detail?.[0] 
            || error.data?.message 
            || 'Registration failed. Please try again.';
        showToast('error', errorMsg);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '✅ Register Now';
    }
}


// ============================================================
// VIEW EVENT DETAILS
// ============================================================
async function viewEventDetails(eventId) {
    try {
        const response = await apiRequest(`/events/${eventId}/`);
        const event = response.data;

        const date = new Date(event.event_date);
        const formattedDate = date.toLocaleDateString('en-IN', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });

        const categoryIcon = CATEGORY_ICONS[event.category] || '📅';

        // Show details in a modal-like alert (simple approach)
        const detailHTML = `
            <div style="text-align: left;">
                <h2 style="font-family: var(--font-display); margin-bottom: var(--space-md);">${event.name}</h2>
                <p style="color: var(--text-secondary); margin-bottom: var(--space-lg); line-height: 1.6;">${event.description}</p>
                <div style="display: grid; gap: var(--space-md);">
                    <div class="meta-item"><span class="icon">${categoryIcon}</span> ${event.category.charAt(0).toUpperCase() + event.category.slice(1)}</div>
                    <div class="meta-item"><span class="icon">📅</span> ${formattedDate}</div>
                    <div class="meta-item"><span class="icon">📍</span> ${event.venue}</div>
                    <div class="meta-item"><span class="icon">💺</span> ${event.seats_left} / ${event.max_seats} seats available</div>
                    <div class="meta-item"><span class="icon">✅</span> ${event.registered_count} registrations</div>
                </div>
            </div>
        `;

        // Reuse registerModal structure for detail view
        document.getElementById('registerModal').querySelector('.modal-title').textContent = '📅 Event Details';
        document.getElementById('registerModal').querySelector('.modal-body').innerHTML = detailHTML + `
            <div style="margin-top: var(--space-xl); display: flex; gap: var(--space-sm); justify-content: flex-end;">
                <button class="btn btn-outline" onclick="closeModal('registerModal')">Close</button>
                ${!event.is_full ? `<button class="btn btn-primary" onclick="closeModal('registerModal'); openRegisterModal(${event.id}, '${event.name.replace(/'/g, "\\'")}')">✅ Register</button>` : ''}
            </div>
        `;
        openModal('registerModal');
    } catch (error) {
        showToast('error', 'Could not load event details.');
    }
}


// ============================================================
// REGISTRATIONS LIST (JOIN Query)
// ============================================================
/**
 * Load event selector for registrations page.
 */
async function loadEventSelector() {
    const container = document.getElementById('eventSelectorCards');

    try {
        const response = await apiRequest('/events/');
        const events = response.data;

        container.innerHTML = events.map(event => `
            <div class="event-selector-card" onclick="loadRegistrationsForEvent(${event.id}, '${event.name.replace(/'/g, "\\'")}')">
                <div class="event-selector-header">
                    <div class="event-selector-icon">${CATEGORY_ICONS[event.category] || '📅'}</div>
                    <div class="event-selector-title">
                        <h4>${event.name}</h4>
                        <span class="event-selector-category">${event.category}</span>
                    </div>
                </div>
                <div class="event-selector-footer">
                    <span class="badge badge-reg">📋 ${event.registered_count} Registered</span>
                    <span class="badge badge-seats">${event.seats_left} Seats Left</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-icon">⚠️</div>
                <h3>Cannot Load Events</h3>
                <p>Please check if the backend is running.</p>
            </div>
        `;
    }
}

/**
 * Load registrations for a specific event.
 * 
 * Backend SQL:
 *   SELECT r.*, p.name, p.email 
 *   FROM registrations r
 *   JOIN participants p ON r.participant_id = p.id
 *   WHERE r.event_id = ?;
 */
async function loadRegistrationsForEvent(eventId, eventName) {
    const container = document.getElementById('registrationsContent');
    container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

    try {
        const response = await apiRequest(`/events/${eventId}/registrations/`);
        const registrations = response.data;

        if (registrations.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📋</div>
                    <h3>No Registrations Yet</h3>
                    <p>No one has registered for "${eventName}" yet.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div style="margin-bottom: var(--space-md); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-md);">
                <div>
                    <h3 style="font-family: var(--font-display); font-size: 1.1rem;">${eventName}</h3>
                    <p style="color: var(--text-tertiary); font-size: 0.85rem;">${response.total_registrations} registered • ${response.seats_left} seats left</p>
                </div>
                <span class="db-status connected">
                    <span class="dot"></span>
                    SELECT ... FROM registrations JOIN participants
                </span>
            </div>
            <div class="table-wrapper">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Registered At</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${registrations.map((reg, i) => `
                            <tr>
                                <td>${i + 1}</td>
                                <td><strong>${reg.participant_name}</strong></td>
                                <td class="email-cell">${reg.participant_email}</td>
                                <td>${new Date(reg.registered_at).toLocaleString('en-IN')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <h3>Failed to Load</h3>
                <p>Could not load registrations. Please try again.</p>
            </div>
        `;
    }
}


// ============================================================
// PARTICIPANTS (SELECT * FROM participants)
// ============================================================
/**
 * Load all participants from the database.
 * 
 * Backend SQL: SELECT * FROM participants ORDER BY name;
 */
let allParticipants = [];
let participantViewMode = 'grid';

function setParticipantView(mode) {
    participantViewMode = mode;
    renderParticipants();
}

function filterParticipantsList() {
    renderParticipants();
}

async function loadParticipants() {
    const container = document.getElementById('participantsContent');
    container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

    try {
        const response = await apiRequest('/participants/');
        allParticipants = response.data || [];
        renderParticipants();
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <h3>Cannot Load Participants</h3>
                <p>Please check backend connectivity.</p>
            </div>
        `;
    }
}

function renderParticipants() {
    const container = document.getElementById('participantsContent');
    const query = (document.getElementById('participantSearchInput')?.value || '').toLowerCase().trim();

    let filtered = allParticipants.filter(p => 
        p.name.toLowerCase().includes(query) ||
        p.email.toLowerCase().includes(query) ||
        (p.college && p.college.toLowerCase().includes(query)) ||
        (p.phone && p.phone.includes(query))
    );

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="participants-toolbar">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="form-input" id="participantSearchInput" placeholder="Filter by name, email, college..." value="${query}" oninput="filterParticipantsList()">
                </div>
                <div class="view-toggle-buttons">
                    <button class="btn btn-outline btn-sm ${participantViewMode === 'grid' ? 'active' : ''}" onclick="setParticipantView('grid')">🔲 Grid View</button>
                    <button class="btn btn-outline btn-sm ${participantViewMode === 'table' ? 'active' : ''}" onclick="setParticipantView('table')">📋 Table View</button>
                </div>
            </div>
            <div class="empty-state">
                <div class="empty-icon">👥</div>
                <h3>No Participants Match</h3>
                <p>No participants match "${query}".</p>
            </div>
        `;
        return;
    }

    const isTable = participantViewMode === 'table';

    let html = `
        <div class="participants-toolbar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" class="form-input" id="participantSearchInput" placeholder="Filter by name, email, college..." value="${query}" oninput="filterParticipantsList()">
            </div>
            <div class="view-toggle-buttons">
                <button class="btn btn-outline btn-sm ${!isTable ? 'active' : ''}" onclick="setParticipantView('grid')">🔲 Grid View</button>
                <button class="btn btn-outline btn-sm ${isTable ? 'active' : ''}" onclick="setParticipantView('table')">📋 Table View</button>
            </div>
        </div>
    `;

    if (isTable) {
        html += `
            <div class="table-wrapper">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Participant</th>
                            <th>Email Address</th>
                            <th>Phone Number</th>
                            <th>College / Institution</th>
                            <th style="text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filtered.map(p => {
                            const initials = p.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
                            const safeName = p.name.replace(/'/g, "\\'");
                            return `
                                <tr>
                                    <td>
                                        <div class="participant-table-user">
                                            <div class="participant-avatar-sm">${initials}</div>
                                            <span class="user-name">${p.name}</span>
                                        </div>
                                    </td>
                                    <td class="email-cell">${p.email}</td>
                                    <td>${p.phone || '—'}</td>
                                    <td><span class="badge badge-college">🎓 ${p.college || 'General'}</span></td>
                                    <td style="text-align: right;">
                                        <div class="table-actions">
                                            <button class="btn btn-outline btn-sm" onclick="editParticipant(${p.id}, '${safeName}', '${p.email.replace(/'/g, "\\'")}', '${(p.phone||'').replace(/'/g, "\\'")}', '${(p.college||'').replace(/'/g, "\\'")}')">✏️ Edit</button>
                                            <button class="btn btn-danger btn-sm" onclick="deleteParticipant(${p.id}, '${safeName}')">🗑️ Delete</button>
                                        </div>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } else {
        html += `
            <div class="participant-cards">
                ${filtered.map(p => {
                    const initials = p.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
                    const safeName = p.name.replace(/'/g, "\\'");
                    return `
                        <div class="participant-card">
                            <div class="participant-card-header">
                                <div class="participant-avatar">${initials}</div>
                                <div class="participant-header-text">
                                    <h4 class="participant-name">${p.name}</h4>
                                    <span class="participant-college-tag">🎓 ${p.college || 'General Participant'}</span>
                                </div>
                            </div>
                            <div class="participant-card-body">
                                <div class="info-row">
                                    <span class="info-icon">📧</span>
                                    <span class="info-text email">${p.email}</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-icon">📞</span>
                                    <span class="info-text">${p.phone || 'No phone provided'}</span>
                                </div>
                            </div>
                            <div class="participant-card-footer">
                                <button class="btn btn-outline btn-sm" onclick="editParticipant(${p.id}, '${safeName}', '${p.email.replace(/'/g, "\\'")}', '${(p.phone||'').replace(/'/g, "\\'")}', '${(p.college||'').replace(/'/g, "\\'")}')">✏️ Edit</button>
                                <button class="btn btn-danger btn-sm" onclick="deleteParticipant(${p.id}, '${safeName}')">🗑️ Delete</button>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    container.innerHTML = html;
}

/**
 * Delete participant from database.
 */
async function deleteParticipant(participantId, participantName) {
    if (!confirm(`⚠️ Are you sure you want to delete participant "${participantName}"?\n\nThis will also delete their event registrations.`)) {
        return;
    }

    try {
        await apiRequest(`/participants/${participantId}/delete/`, 'DELETE');
        showToast('success', `Participant "${participantName}" deleted successfully!`);
        loadParticipants();
        loadDashboardStats();
    } catch (error) {
        showToast('error', 'Failed to delete participant.');
    }
}

/**
 * Edit participant details.
 */
async function editParticipant(id, name, email, phone, college) {
    const newName = prompt("Edit Participant Name:", name);
    if (newName === null) return;

    const newEmail = prompt("Edit Email:", email);
    if (newEmail === null) return;

    const newPhone = prompt("Edit Phone:", phone);
    if (newPhone === null) return;

    const newCollege = prompt("Edit College:", college);
    if (newCollege === null) return;

    try {
        await apiRequest(`/participants/${id}/update/`, 'PUT', {
            name: newName,
            email: newEmail,
            phone: newPhone,
            college: newCollege
        });
        showToast('success', `Participant "${newName}" updated successfully!`);
        loadParticipants();
    } catch (error) {
        showToast('error', 'Failed to update participant.');
    }
}



// ============================================================
// ADMIN PANEL (Full CRUD)
// ============================================================
/**
 * Load all events in admin view with edit/delete actions.
 */
async function loadAdminEvents() {
    const container = document.getElementById('adminEventsContent');
    container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

    try {
        const response = await apiRequest('/events/');
        const events = response.data;

        if (events.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📅</div>
                    <h3>No Events</h3>
                    <p>Click "Create Event" to add your first event.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="admin-events-list">
                ${events.map(event => {
                    const date = new Date(event.event_date);
                    const formattedDate = date.toLocaleDateString('en-IN', {
                        year: 'numeric', month: 'short', day: 'numeric'
                    });
                    const icon = CATEGORY_ICONS[event.category] || '📅';

                    return `
                        <div class="admin-event-row">
                            <div class="admin-event-main">
                                <div class="admin-event-icon">${icon}</div>
                                <div class="admin-event-info">
                                    <h3>${event.name}</h3>
                                    <div class="meta">
                                        <span>📅 ${formattedDate}</span>
                                        <span>📍 ${event.venue}</span>
                                        <span>🏷️ ${event.category}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="admin-event-stats">
                                <div class="admin-event-stat">
                                    <div class="value">${event.registered_count}</div>
                                    <div class="label">Registered</div>
                                </div>
                                <div class="admin-event-stat">
                                    <div class="value">${event.seats_left}</div>
                                    <div class="label">Seats Left</div>
                                </div>
                                <div class="admin-event-stat">
                                    <div class="value">${event.max_seats}</div>
                                    <div class="label">Total</div>
                                </div>
                            </div>
                            <div class="admin-event-actions">
                                <button class="btn btn-outline btn-sm" onclick="openEditEventModal(${event.id})">✏️ Edit</button>
                                <button class="btn btn-danger btn-sm" onclick="deleteEvent(${event.id}, '${event.name.replace(/'/g, "\\'")}')">🗑️ Delete</button>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <h3>Cannot Load Events</h3>
                <p>Please check backend connectivity.</p>
            </div>
        `;
    }
}


// ============================================================
// CREATE EVENT (INSERT INTO events)
// ============================================================
function openCreateEventModal() {
    document.getElementById('eventModalTitle').textContent = '➕ Create New Event';
    document.getElementById('eventSubmitBtn').textContent = '✅ Create Event';
    document.getElementById('eventFormId').value = '';
    document.getElementById('eventForm').reset();
    openModal('eventModal');
}

/**
 * Handle event form submission (CREATE or UPDATE).
 * 
 * CREATE SQL: INSERT INTO events (name, description, ...) VALUES (...);
 * UPDATE SQL: UPDATE events SET name=..., description=... WHERE id = ?;
 */
async function handleEventSubmit(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('eventSubmitBtn');
    submitBtn.disabled = true;

    const eventId = document.getElementById('eventFormId').value;
    const isEdit = !!eventId;

    const data = {
        name: document.getElementById('eventName').value,
        description: document.getElementById('eventDesc').value,
        event_date: new Date(document.getElementById('eventDate').value).toISOString(),
        venue: document.getElementById('eventVenue').value,
        max_seats: parseInt(document.getElementById('eventMaxSeats').value),
        category: document.getElementById('eventCategory').value,
        image_url: document.getElementById('eventImageUrl').value || null,
    };

    try {
        let response;
        if (isEdit) {
            response = await apiRequest(`/events/${eventId}/update/`, 'PUT', data);
            showToast('success', `Event "${data.name}" updated successfully!`);
        } else {
            response = await apiRequest('/events/create/', 'POST', data);
            showToast('success', `Event "${data.name}" created successfully!`);
        }

        closeModal('eventModal');
        loadAdminEvents();
        loadDashboardStats();
    } catch (error) {
        const errorMsg = error.data?.errors 
            ? Object.values(error.data.errors).flat().join(', ')
            : 'Failed to save event.';
        showToast('error', errorMsg);
    } finally {
        submitBtn.disabled = false;
    }
}


// ============================================================
// EDIT EVENT (UPDATE query)
// ============================================================
/**
 * Open edit modal pre-filled with event data.
 * 
 * Backend SQL: SELECT * FROM events WHERE id = ?;
 */
async function openEditEventModal(eventId) {
    try {
        const response = await apiRequest(`/events/${eventId}/`);
        const event = response.data;

        document.getElementById('eventModalTitle').textContent = '✏️ Edit Event';
        document.getElementById('eventSubmitBtn').textContent = '💾 Save Changes';
        document.getElementById('eventFormId').value = event.id;
        document.getElementById('eventName').value = event.name;
        document.getElementById('eventDesc').value = event.description;
        
        // Format datetime for the input
        const date = new Date(event.event_date);
        const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
        document.getElementById('eventDate').value = localDate.toISOString().slice(0, 16);
        
        document.getElementById('eventVenue').value = event.venue;
        document.getElementById('eventMaxSeats').value = event.max_seats;
        document.getElementById('eventCategory').value = event.category;
        document.getElementById('eventImageUrl').value = event.image_url || '';

        openModal('eventModal');
    } catch (error) {
        showToast('error', 'Could not load event for editing.');
    }
}


// ============================================================
// DELETE EVENT (DELETE FROM events WHERE id = ?)
// ============================================================
async function deleteEvent(eventId, eventName) {
    if (!confirm(`⚠️ Are you sure you want to delete "${eventName}"?\n\nThis will also delete all registrations for this event (CASCADE DELETE).`)) {
        return;
    }

    try {
        await apiRequest(`/events/${eventId}/delete/`, 'DELETE');
        showToast('success', `Event "${eventName}" deleted successfully!`);
        loadAdminEvents();
        loadDashboardStats();
    } catch (error) {
        showToast('error', 'Failed to delete event.');
    }
}


// ============================================================
// MODAL HELPERS
// ============================================================
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    document.body.style.overflow = '';

    // Reset register modal to original state if it was used for details
    if (modalId === 'registerModal') {
        const modal = document.getElementById('registerModal');
        modal.querySelector('.modal-title').textContent = '📝 Register for Event';
        modal.querySelector('.modal-body').innerHTML = `
            <div class="form-group">
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: var(--space-md);">
                    Registering for: <strong id="registerEventName" style="color: var(--primary-300);"></strong>
                </p>
            </div>
            <form id="registerForm" onsubmit="handleRegistration(event)">
                <input type="hidden" id="registerEventId">
                <div class="form-group">
                    <label class="form-label">Full Name <span class="required">*</span></label>
                    <input type="text" class="form-input" id="regName" placeholder="Enter your full name" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Email <span class="required">*</span></label>
                        <input type="email" class="form-input" id="regEmail" placeholder="your@email.com" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Phone</label>
                        <input type="tel" class="form-input" id="regPhone" placeholder="9876543210">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">College / University</label>
                    <input type="text" class="form-input" id="regCollege" placeholder="Your college name">
                </div>
                <div class="modal-footer" style="padding: 0;">
                    <button type="button" class="btn btn-outline" onclick="closeModal('registerModal')">Cancel</button>
                    <button type="submit" class="btn btn-primary" id="registerSubmitBtn">
                        ✅ Register Now
                    </button>
                </div>
            </form>
        `;
    }
}

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeModal(overlay.id);
        }
    });
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
            closeModal(modal.id);
        });
    }
});


// ============================================================
// TOAST NOTIFICATIONS
// ============================================================
function showToast(type, message) {
    const container = document.getElementById('toastContainer');
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Remove after animation
    setTimeout(() => {
        toast.remove();
    }, 4000);
}


// ============================================================
// NAVBAR SCROLL EFFECT
// ============================================================
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});


// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 Eventify Frontend Loaded');
    console.log(`📡 API Base URL: ${API_BASE_URL}`);
    
    // Check database connection
    checkDatabaseConnection();

    // Load home page data
    loadDashboardStats();
    loadFeaturedEvents();
});
