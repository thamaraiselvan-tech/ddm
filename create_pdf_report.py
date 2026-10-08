import os
import subprocess
import fitz

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Eventify — DBMS Project Report</title>
    <style>
        @page {
            size: A4;
            margin: 18mm 16mm 18mm 16mm;
            @bottom-right {
                content: counter(page);
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }
        
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }

        /* --- TITLE PAGE --- */
        .title-page {
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
            padding: 40px 20px;
        }

        .university-header {
            font-size: 13pt;
            font-weight: 700;
            letter-spacing: 2px;
            color: #475569;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .course-title {
            font-size: 16pt;
            font-weight: 600;
            color: #2563eb;
            margin-bottom: 40px;
        }

        .project-badge {
            display: inline-block;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1d4ed8;
            font-size: 10pt;
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 20px;
        }

        .main-title {
            font-size: 34pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0 0 10px 0;
            line-height: 1.15;
            letter-spacing: -0.5px;
        }

        .sub-title {
            font-size: 13pt;
            font-weight: 400;
            color: #64748b;
            max-width: 550px;
            margin: 0 auto 50px auto;
        }

        .metadata-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px 32px;
            width: 100%;
            max-width: 500px;
            text-align: left;
            margin-top: auto;
        }

        .metadata-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px dashed #e2e8f0;
            font-size: 10pt;
        }

        .metadata-row:last-child {
            border-bottom: none;
        }

        .metadata-label {
            font-weight: 600;
            color: #475569;
        }

        .metadata-value {
            color: #0f172a;
            font-weight: 500;
        }

        /* --- HEADINGS & SECTIONS --- */
        h1 {
            font-size: 16pt;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 5px;
            margin-top: 24px;
            margin-bottom: 14px;
            page-break-after: avoid;
        }

        h2 {
            font-size: 12pt;
            font-weight: 700;
            color: #1e3a8a;
            margin-top: 18px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }

        h3 {
            font-size: 10.5pt;
            font-weight: 600;
            color: #334155;
            margin-top: 12px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }

        p {
            margin-top: 0;
            margin-bottom: 10px;
            text-align: justify;
        }

        ul, ol {
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 20px;
        }

        li {
            margin-bottom: 3px;
        }

        /* --- TABLES --- */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            margin-bottom: 16px;
            font-size: 9pt;
            page-break-inside: avoid;
        }

        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            text-align: left;
            padding: 7px 9px;
            border: 1px solid #cbd5e1;
        }

        td {
            padding: 6px 9px;
            border: 1px solid #cbd5e1;
            vertical-align: top;
        }

        tr:nth-child(even) td {
            background-color: #f8fafc;
        }

        .pk-badge {
            background: #dbeafe;
            color: #1e40af;
            font-size: 7pt;
            font-weight: 700;
            padding: 2px 4px;
            border-radius: 4px;
        }

        .fk-badge {
            background: #fef3c7;
            color: #92400e;
            font-size: 7pt;
            font-weight: 700;
            padding: 2px 4px;
            border-radius: 4px;
        }

        /* --- CODE BLOCKS --- */
        pre {
            background-color: #0f172a;
            color: #f8fafc;
            padding: 10px 14px;
            border-radius: 6px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 8pt;
            line-height: 1.4;
            overflow-x: auto;
            margin-top: 8px;
            margin-bottom: 14px;
            page-break-inside: avoid;
            white-space: pre-wrap;
            word-break: break-all;
        }

        code {
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 4px;
            border-radius: 4px;
        }

        /* --- CALLOUT BOXES --- */
        .callout {
            background-color: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 10px 14px;
            border-radius: 0 6px 6px 0;
            margin-top: 12px;
            margin-bottom: 14px;
            font-size: 9.5pt;
        }

        .callout-title {
            font-weight: 700;
            color: #1e40af;
            margin-bottom: 4px;
        }

        /* --- PAGE BREAK UTILITY --- */
        .page-break {
            page-break-before: always;
        }

        .figure-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 14px;
            text-align: center;
            page-break-inside: avoid;
        }

        .figure-caption {
            font-size: 8.5pt;
            font-weight: 600;
            color: #475569;
            margin-top: 5px;
        }
    </style>
</head>
<body>

    <!-- TITLE PAGE -->
    <div class="title-page">
        <div class="university-header">Database Design & Management System</div>
        <div class="course-title">Academic Capstone DBMS Project Report</div>
        
        <div class="project-badge">🎯 Full-Stack System Integration</div>
        <h1 class="main-title">EVENTIFY</h1>
        <div class="sub-title">A Full-Stack Event Registration & Management System Demonstrating Frontend-Backend-Database Connectivity</div>
        
        <div class="metadata-box">
            <div class="metadata-row">
                <span class="metadata-label">Subject</span>
                <span class="metadata-value">Database Design and Management</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Frontend</span>
                <span class="metadata-value">HTML5, CSS3, Vanilla JavaScript</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Backend Engine</span>
                <span class="metadata-value">Django REST Framework (Python)</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Database</span>
                <span class="metadata-value">MySQL / SQLite Relational DB</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Architecture</span>
                <span class="metadata-value">RESTful API / 3-Tier Client-Server</span>
            </div>
            <div class="metadata-row">
                <span class="metadata-label">Date</span>
                <span class="metadata-value">Academic Term 2026</span>
            </div>
        </div>
    </div>

    <!-- 1. INTRODUCTION -->
    <h1>1. Introduction & Project Overview</h1>
    <p>
        <strong>Eventify</strong> is a complete web-based Event Registration System developed as an academic project for the course <strong>Database Design and Management</strong>. The principal objective of this project is to demonstrate real-time, 3-tier database connectivity between a modern web user interface, a Python backend REST API server, and a relational database management system (RDBMS).
    </p>
    <p>
        In modern web applications, user actions in the browser must be seamlessly translated into structured SQL queries in the database engine, and database query outputs must be transformed into dynamic UI updates. Eventify models a real-world event host platform where visitors can browse technical events, filter by categories, register with instant seat management, view participant lists, and manage events through an admin dashboard.
    </p>

    <div class="callout">
        <div class="callout-title">Core DBMS Learning Objectives Demonstrated:</div>
        <ul>
            <li>Designing 3rd Normal Form (3NF) relational tables with primary key and foreign key constraints.</li>
            <li>Resolving Many-to-Many (M:N) relationships using junction/bridge tables (<code>registrations</code>).</li>
            <li>Executing relational <code>JOIN</code> operations to retrieve participant and event details simultaneously.</li>
            <li>Performing relational aggregation functions (<code>COUNT</code>, <code>SUM</code>) for real-time analytics.</li>
            <li>Handling database integrity, unique key constraints, and transactional seat updates.</li>
        </ul>
    </div>

    <!-- 2. CONCEPTUAL MODEL & ER DIAGRAM -->
    <div class="page-break"></div>
    <h1>2. Conceptual Database Design (ER Model)</h1>
    <p>
        The conceptual design of Eventify centers around three major entity sets: <strong>EVENTS</strong>, <strong>PARTICIPANTS</strong>, and <strong>REGISTRATIONS</strong>.
    </p>

    <h2>2.1 Entity Descriptions</h2>
    <ul>
        <li><strong>EVENT:</strong> Represents a workshop, hackathon, seminar, or competition hosted on the platform. It tracks maximum seat capacity, event dates, category, and venue.</li>
        <li><strong>PARTICIPANT:</strong> Represents an individual registrant identified uniquely by their email address, storing name, phone number, and institution details.</li>
        <li><strong>REGISTRATION:</strong> Represents an instance of a participant signing up for an event. It stores the timestamp of registration.</li>
    </ul>

    <h2>2.2 Entity Relationship Diagram (ERD)</h2>
    <p>
        A single <code>EVENT</code> can be attended by multiple <code>PARTICIPANTS</code>, and a single <code>PARTICIPANT</code> can register for multiple <code>EVENTS</code>. This creates a <strong>Many-to-Many (M:N)</strong> relationship between <code>EVENTS</code> and <code>PARTICIPANTS</code>.
    </p>
    <p>
        The M:N relationship is decomposed into two <strong>One-to-Many (1:N)</strong> relationships using an associative junction entity named <strong>REGISTRATION</strong>:
    </p>

    <!-- VISUAL VECTOR ER DIAGRAM SVG -->
    <div class="figure-box">
        <svg viewBox="0 0 800 310" width="100%" height="300" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="eventGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#2563eb"/>
                    <stop offset="100%" stop-color="#1e40af"/>
                </linearGradient>
                <linearGradient id="regGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#d97706"/>
                    <stop offset="100%" stop-color="#b45309"/>
                </linearGradient>
                <linearGradient id="partGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#059669"/>
                    <stop offset="100%" stop-color="#047857"/>
                </linearGradient>
                <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
                    <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.12"/>
                </filter>
            </defs>

            <!-- CONNECTING LINES -->
            <line x1="220" y1="150" x2="310" y2="150" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5,4"/>
            <line x1="490" y1="150" x2="580" y2="150" stroke="#64748b" stroke-width="2.5" stroke-dasharray="5,4"/>

            <!-- CARDINALITY BADGES -->
            <rect x="230" y="132" width="22" height="22" rx="4" fill="#dbeafe"/>
            <text x="241" y="148" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">1</text>

            <rect x="278" y="132" width="22" height="22" rx="4" fill="#fef3c7"/>
            <text x="289" y="148" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#b45309" text-anchor="middle">N</text>

            <rect x="500" y="132" width="22" height="22" rx="4" fill="#fef3c7"/>
            <text x="511" y="148" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#b45309" text-anchor="middle">N</text>

            <rect x="548" y="132" width="22" height="22" rx="4" fill="#d1fae5"/>
            <text x="559" y="148" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" fill="#047857" text-anchor="middle">1</text>

            <!-- ENTITY 1: EVENT -->
            <g filter="url(#shadow)">
                <rect x="30" y="30" width="190" height="250" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect x="30" y="30" width="190" height="40" rx="8" fill="url(#eventGrad)"/>
                <rect x="30" y="55" width="190" height="15" fill="url(#eventGrad)"/>
                <text x="125" y="56" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">EVENTS</text>

                <text x="45" y="90" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#1e40af">🔑 id (PK)</text>
                <text x="45" y="112" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• name</text>
                <text x="45" y="134" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• description</text>
                <text x="45" y="156" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• event_date</text>
                <text x="45" y="178" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• venue</text>
                <text x="45" y="200" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• max_seats</text>
                <text x="45" y="222" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• category</text>
                <text x="45" y="244" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• is_active</text>
                <text x="45" y="266" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• created_at</text>
            </g>

            <!-- ENTITY 2: REGISTRATION (JUNCTION) -->
            <g filter="url(#shadow)">
                <rect x="310" y="55" width="180" height="190" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="2"/>
                <rect x="310" y="55" width="180" height="40" rx="8" fill="url(#regGrad)"/>
                <rect x="310" y="80" width="180" height="15" fill="url(#regGrad)"/>
                <text x="400" y="81" font-family="Segoe UI, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">REGISTRATIONS</text>

                <text x="325" y="118" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#d97706">🔑 id (PK)</text>
                <text x="325" y="144" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#b45309">🔗 event_id (FK)</text>
                <text x="325" y="170" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#b45309">🔗 participant_id (FK)</text>
                <text x="325" y="196" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• registered_at</text>
                <line x1="320" y1="215" x2="480" y2="215" stroke="#e2e8f0" stroke-width="1"/>
                <text x="400" y="232" font-family="Segoe UI, sans-serif" font-size="9" font-style="italic" fill="#64748b" text-anchor="middle">UNIQUE(event_id, participant_id)</text>
            </g>

            <!-- ENTITY 3: PARTICIPANT -->
            <g filter="url(#shadow)">
                <rect x="580" y="55" width="190" height="190" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect x="580" y="55" width="190" height="40" rx="8" fill="url(#partGrad)"/>
                <rect x="580" y="80" width="190" height="15" fill="url(#partGrad)"/>
                <text x="675" y="81" font-family="Segoe UI, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">PARTICIPANTS</text>

                <text x="595" y="118" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#059669">🔑 id (PK)</text>
                <text x="595" y="144" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• name</text>
                <text x="595" y="170" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#047857">⭐ email (UNIQUE)</text>
                <text x="595" y="196" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• phone</text>
                <text x="595" y="222" font-family="Segoe UI, sans-serif" font-size="10.5" fill="#334155">• college</text>
            </g>
        </svg>
        <div class="figure-caption">Figure 2.1: Entity-Relationship Diagram (ERD) with Primary/Foreign Keys & Cardinality Mapping</div>
    </div>

    <!-- 3. RELATIONAL SCHEMAS & TABLES -->
    <h1>3. Relational Schema & Data Structures</h1>
    <p>
        The conceptual ER model is mapped into three normalized relational tables in Third Normal Form (3NF). All tables utilize surrogate auto-increment primary keys and foreign keys to enforce referential integrity.
    </p>

    <h2>3.1 Relational Schema Definitions</h2>
    <ul>
        <li><code>events (id, name, description, event_date, venue, max_seats, category, image_url, is_active, created_at)</code></li>
        <li><code>participants (id, name, email, phone, college, created_at)</code></li>
        <li><code>registrations (id, event_id, participant_id, registered_at)</code></li>
    </ul>

    <h2>3.2 Data Dictionary & Column Specifications</h2>
    
    <h3>Table: events</h3>
    <table>
        <thead>
            <tr>
                <th>Column Name</th>
                <th>Data Type</th>
                <th>Constraints</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>id</code></td>
                <td>INT / INTEGER</td>
                <td><span class="pk-badge">PRIMARY KEY</span> AUTO_INCREMENT</td>
                <td>Unique surrogate identifier for the event</td>
            </tr>
            <tr>
                <td><code>name</code></td>
                <td>VARCHAR(200)</td>
                <td>NOT NULL</td>
                <td>Name/Title of the event</td>
            </tr>
            <tr>
                <td><code>description</code></td>
                <td>TEXT</td>
                <td>NOT NULL</td>
                <td>Detailed breakdown of event activities</td>
            </tr>
            <tr>
                <td><code>event_date</code></td>
                <td>DATETIME</td>
                <td>NOT NULL</td>
                <td>Date and starting time of the event</td>
            </tr>
            <tr>
                <td><code>venue</code></td>
                <td>VARCHAR(250)</td>
                <td>NOT NULL</td>
                <td>Physical room/hall location or meeting URL</td>
            </tr>
            <tr>
                <td><code>max_seats</code></td>
                <td>INT</td>
                <td>NOT NULL</td>
                <td>Maximum available seating capacity</td>
            </tr>
            <tr>
                <td><code>category</code></td>
                <td>VARCHAR(50)</td>
                <td>NOT NULL DEFAULT 'workshop'</td>
                <td>Category tag (hackathon, seminar, etc.)</td>
            </tr>
        </tbody>
    </table>

    <h3>Table: participants</h3>
    <table>
        <thead>
            <tr>
                <th>Column Name</th>
                <th>Data Type</th>
                <th>Constraints</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>id</code></td>
                <td>INT / INTEGER</td>
                <td><span class="pk-badge">PRIMARY KEY</span> AUTO_INCREMENT</td>
                <td>Unique participant ID</td>
            </tr>
            <tr>
                <td><code>name</code></td>
                <td>VARCHAR(150)</td>
                <td>NOT NULL</td>
                <td>Full legal name of participant</td>
            </tr>
            <tr>
                <td><code>email</code></td>
                <td>VARCHAR(254)</td>
                <td>NOT NULL, <span class="pk-badge">UNIQUE</span></td>
                <td>Unique email address (login/contact key)</td>
            </tr>
            <tr>
                <td><code>college</code></td>
                <td>VARCHAR(200)</td>
                <td>NULL / DEFAULT ''</td>
                <td>Institution / University affiliation</td>
            </tr>
        </tbody>
    </table>

    <h3>Table: registrations (Junction Table)</h3>
    <table>
        <thead>
            <tr>
                <th>Column Name</th>
                <th>Data Type</th>
                <th>Constraints</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>id</code></td>
                <td>INT / INTEGER</td>
                <td><span class="pk-badge">PRIMARY KEY</span> AUTO_INCREMENT</td>
                <td>Unique registration transaction ID</td>
            </tr>
            <tr>
                <td><code>event_id</code></td>
                <td>INT</td>
                <td><span class="fk-badge">FOREIGN KEY</span> REFERENCES events(id) ON DELETE CASCADE</td>
                <td>References the registered event</td>
            </tr>
            <tr>
                <td><code>participant_id</code></td>
                <td>INT</td>
                <td><span class="fk-badge">FOREIGN KEY</span> REFERENCES participants(id) ON DELETE CASCADE</td>
                <td>References the registrant participant</td>
            </tr>
            <tr>
                <td><code>registered_at</code></td>
                <td>DATETIME</td>
                <td>DEFAULT CURRENT_TIMESTAMP</td>
                <td>Registration timestamp</td>
            </tr>
        </tbody>
    </table>

    <div class="page-break"></div>
    <h2>3.3 Active Database State (Sample Data Rows)</h2>
    <p>Below is a snapshot of the actual records populated in the database engine during demonstration:</p>

    <h3>Sample Records: events</h3>
    <table>
        <thead>
            <tr>
                <th>id</th>
                <th>name</th>
                <th>category</th>
                <th>event_date</th>
                <th>venue</th>
                <th>max_seats</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>HackFusion 2024</td>
                <td>hackathon</td>
                <td>2026-10-25 09:00:00</td>
                <td>Main Auditorium, Block A</td>
                <td>50</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Full-Stack Web Dev Workshop</td>
                <td>workshop</td>
                <td>2026-10-28 14:00:00</td>
                <td>Computer Lab 3, IT Building</td>
                <td>40</td>
            </tr>
            <tr>
                <td>3</td>
                <td>AI & Future Tech Seminar</td>
                <td>seminar</td>
                <td>2026-11-02 10:30:00</td>
                <td>Mini Seminar Hall 2</td>
                <td>100</td>
            </tr>
            <tr>
                <td>4</td>
                <td>UI/UX Design Masterclass</td>
                <td>workshop</td>
                <td>2026-11-10 11:00:00</td>
                <td>Design Studio, 4th Floor</td>
                <td>30</td>
            </tr>
        </tbody>
    </table>

    <h3>Sample Records: participants</h3>
    <table>
        <thead>
            <tr>
                <th>id</th>
                <th>name</th>
                <th>email</th>
                <th>phone</th>
                <th>college</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Aarav Sharma</td>
                <td>aarav.sharma@example.com</td>
                <td>9876543210</td>
                <td>IIT Madras</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Ananya Sen</td>
                <td>ananya.sen@example.com</td>
                <td>9876543211</td>
                <td>NIT Trichy</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Rohan Verma</td>
                <td>rohan.verma@example.com</td>
                <td>9876543212</td>
                <td>Anna University</td>
            </tr>
        </tbody>
    </table>

    <!-- 4. SOURCE CODE & SQL QUERIES -->
    <h1>4. Source Code & SQL Implementation</h1>

    <h2>4.1 Data Definition Language (DDL) Script</h2>
    <p>The standard ANSI/MySQL DDL script used to initialize the database tables is as follows:</p>
<pre>
-- ============================================================
-- EVENTIFY DATABASE CREATION SCRIPT
-- ============================================================
CREATE DATABASE IF NOT EXISTS eventify_db;
USE eventify_db;

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    event_date DATETIME NOT NULL,
    venue VARCHAR(250) NOT NULL,
    max_seats INT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'workshop',
    image_url VARCHAR(500) NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    phone VARCHAR(20) DEFAULT '',
    college VARCHAR(200) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    participant_id INT NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reg_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT fk_reg_participant FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
    CONSTRAINT unique_event_participant UNIQUE (event_id, participant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
</pre>

    <div class="page-break"></div>
    <h2>4.2 Feature-to-SQL Query Mapping</h2>
    <p>
        Every user action triggered in the frontend corresponds to a specific SQL query executed by the database engine through Django REST Framework:
    </p>

    <h3>1. Dashboard Aggregations (Analytics Counter)</h3>
    <pre>
-- Calculate total active events, participants, registrations, and total seat capacity
SELECT COUNT(*) FROM events WHERE is_active = 1;
SELECT COUNT(*) FROM participants;
SELECT COUNT(*) FROM registrations;
SELECT SUM(max_seats) FROM events WHERE is_active = 1;
    </pre>

    <h3>2. Relational JOIN Query (View Event Registrations)</h3>
    <pre>
-- Fetch participant details registered for a specific event (e.g. event_id = 1)
SELECT 
    r.id AS registration_id,
    p.name AS participant_name,
    p.email AS participant_email,
    p.college,
    r.registered_at
FROM registrations r
INNER JOIN participants p ON r.participant_id = p.id
WHERE r.event_id = 1
ORDER BY r.registered_at DESC;
    </pre>

    <h3>3. Search & Pattern Matching (LIKE Operator)</h3>
    <pre>
-- Search events by substring keyword across name, description, or venue
SELECT * FROM events 
WHERE is_active = 1 
  AND (name LIKE '%hackathon%' OR description LIKE '%hackathon%' OR venue LIKE '%hackathon%')
ORDER BY event_date ASC;
    </pre>

    <h3>4. Transactional Event Registration (INSERT with Duplicate Protection)</h3>
    <pre>
-- Step A: Get or insert participant record
INSERT INTO participants (name, email, phone, college)
VALUES ('Rohan Verma', 'rohan.verma@example.com', '9876543212', 'Anna University')
ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id);

-- Step B: Insert registration link
INSERT INTO registrations (event_id, participant_id, registered_at)
VALUES (1, LAST_INSERT_ID(), NOW());
    </pre>

    <!-- 5. SYSTEM ARCHITECTURE & CONNECTIVITY -->
    <div class="page-break"></div>
    <h1>5. System Architecture & Database Connectivity</h1>
    
    <h2>5.1 3-Tier Architecture Flow</h2>
    <p>The application follows a clean 3-tier client-server architecture:</p>
    <ol>
        <li><strong>Presentation Tier (Frontend):</strong> Standard Vanilla HTML5, CSS3, and JavaScript. Makes asynchronous HTTP requests using the <code>fetch()</code> API to API endpoints.</li>
        <li><strong>Application Tier (Backend API):</strong> Python Django REST Framework running on <code>http://localhost:8000</code>. Validates JSON payload, checks capacity limits, and orchestrates database transactions.</li>
        <li><strong>Data Tier (Relational DB):</strong> MySQL / SQLite storage engine executing normalized query plans and maintaining foreign key constraints.</li>
    </ol>

    <div class="figure-box">
        <pre style="background:#0f172a; color:#38bdf8; text-align:left; padding:15px; border-radius:8px;">
 [ FRONTEND ]                      [ BACKEND API ]                  [ DATABASE ENGINE ]
  Browser UI   ----(HTTP POST)----&gt;  Django REST   ----(SQL INSERT)--&gt;  MySQL / SQLite
 (HTML/CSS/JS) &lt;---(JSON Status)---  Python Engine &lt;---(Result Sets)--  Relational Tables
        </pre>
        <div class="figure-caption">Figure 5.1: Asynchronous Request-Response Data Flow</div>
    </div>

    <h2>5.2 Backend API Views (Python Source Code)</h2>
    <p>Below is an excerpt from <code>backend/events/views.py</code> illustrating API query execution:</p>
<pre>
@api_view(['POST'])
def register_for_event(request):
    event_id = request.data.get('event_id')
    email = request.data.get('email', '').strip().lower()
    name = request.data.get('name', '').strip()
    
    event = get_object_or_404(Event, id=event_id)
    
    # Check seating availability constraint
    if event.seats_left &lt;= 0:
        return Response({'message': 'Event is full!'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Get or create participant
    participant, _ = Participant.objects.get_or_create(
        email=email,
        defaults={'name': name, 'phone': request.data.get('phone', ''), 'college': request.data.get('college', '')}
    )
    
    # Create registration junction record
    Registration.objects.create(event=event, participant=participant)
    
    return Response({'message': 'Successfully registered!'}, status=status.HTTP_201_CREATED)
</pre>

    <!-- 6. CONCLUSION -->
    <div class="page-break"></div>
    <h1>6. Conclusion & Future Enhancements</h1>
    
    <h2>6.1 Summary of Project Outcomes</h2>
    <p>
        The <strong>Eventify</strong> system successfully demonstrates end-to-end database connectivity across all application layers. By decomposing the Many-to-Many relationship between events and participants into normalized tables, the application preserves data integrity, avoids redundant storage, and enables efficient relational queries.
    </p>
    <p>
        Key academic milestones achieved include:
    </p>
    <ul>
        <li>Implementation of 3rd Normal Form (3NF) tables with cascade deletion constraints.</li>
        <li>Demonstration of relational JOIN queries and aggregate calculations in a real-time web UI.</li>
        <li>Construction of a robust backend REST API bridging web clients to database storage engines.</li>
    </ul>

    <h2>6.2 Future System Enhancements</h2>
    <ul>
        <li><strong>Role-Based Authentication:</strong> Adding user login tables (<code>users</code>, <code>roles</code>) for separate organizer and student permissions.</li>
        <li><strong>Automated QR Code Generation:</strong> Storing unique ticket hashes in the <code>registrations</code> table for instant venue check-in.</li>
        <li><strong>Waitlist Database Queue:</strong> Implementing database triggers for automatic seat allocation upon cancellation.</li>
    </ul>

    <div style="margin-top: 50px; border-top: 1px solid #cbd5e1; padding-top: 20px; text-align: center; color: #64748b; font-size: 9pt;">
        Eventify DBMS Academic Project Report • Generated for Database Design & Management Submission
    </div>

</body>
</html>
"""

html_path = r"d:\New folder (5)\report.html"
pdf_path = r"d:\New folder (5)\Eventify_DBMS_Project_Report.pdf"
artifact_pdf_path = r"C:\Users\THAMARAI SELVAN\.gemini\antigravity-ide\brain\4cfc0d0b-95de-497f-9bee-91a775480f2e\Eventify_DBMS_Project_Report.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML report written to:", html_path)

edge_cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path.replace('\\', '/')}"
]

res = subprocess.run(edge_cmd, capture_output=True, text=True)
print("Edge compilation result code:", res.returncode)

if os.path.exists(pdf_path):
    print("PDF compiled successfully! File size:", os.path.getsize(pdf_path), "bytes")
    
    # Also copy to artifact path
    with open(artifact_pdf_path, "wb") as dst, open(pdf_path, "rb") as src:
        dst.write(src.read())
    print("PDF copied to artifact path:", artifact_pdf_path)

    doc = fitz.open(pdf_path)
    print("Total PDF Page Count:", len(doc))
else:
    print("PDF compilation failed.")
