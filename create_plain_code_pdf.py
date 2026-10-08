import os
import subprocess
import html
import fitz

# Read source code files directly
def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return f"/* File {filepath} not found */"

sql_code = read_file(r"d:\New folder (5)\backend\eventify_database.sql")
models_code = read_file(r"d:\New folder (5)\backend\events\models.py")
views_code = read_file(r"d:\New folder (5)\backend\events\views.py")
html_code = read_file(r"d:\New folder (5)\frontend\index.html")
css_code = read_file(r"d:\New folder (5)\frontend\css\style.css")
js_code = read_file(r"d:\New folder (5)\frontend\js\app.js")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Eventify — DBMS Project Report</title>
    <style>
        @page {{
            size: A4;
            margin: 18mm 16mm 18mm 16mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                color: #444;
            }}
        }}
        
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: Arial, Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #111111;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        /* COVER PAGE */
        .cover-page {{
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
            padding: 40px 20px;
        }}

        .academic-header {{
            font-size: 12pt;
            font-weight: bold;
            letter-spacing: 1.5px;
            color: #333;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .course-title {{
            font-size: 14pt;
            font-weight: bold;
            color: #1a56db;
            margin-bottom: 50px;
        }}

        .main-title {{
            font-size: 32pt;
            font-weight: bold;
            color: #000000;
            margin: 0 0 10px 0;
            line-height: 1.1;
        }}

        .sub-title {{
            font-size: 13pt;
            color: #444444;
            max-width: 550px;
            margin: 0 auto 60px auto;
        }}

        .meta-table {{
            width: 100%;
            max-width: 480px;
            margin-top: auto;
            border-collapse: collapse;
            font-size: 9.5pt;
        }}

        .meta-table td {{
            padding: 6px 10px;
            border: 1px solid #ccc;
        }}

        .meta-table td.label {{
            font-weight: bold;
            background-color: #f2f2f2;
            width: 35%;
        }}

        /* HEADINGS */
        h1 {{
            font-size: 15pt;
            font-weight: bold;
            color: #000;
            border-bottom: 2px solid #333;
            padding-bottom: 4px;
            margin-top: 22px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 12pt;
            font-weight: bold;
            color: #1a56db;
            margin-top: 16px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 10.5pt;
            font-weight: bold;
            color: #222;
            margin-top: 14px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
            text-align: justify;
        }}

        /* DATA TABLES */
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
            margin-bottom: 14px;
            font-size: 9pt;
            page-break-inside: avoid;
        }}

        table.data-table th {{
            background-color: #eaeaea;
            color: #000;
            font-weight: bold;
            text-align: left;
            padding: 6px 8px;
            border: 1px solid #999;
        }}

        table.data-table td {{
            padding: 5px 8px;
            border: 1px solid #aaa;
            vertical-align: top;
        }}

        /* PLAIN TEXT CODE BLOCKS */
        pre.code-block {{
            background-color: #f8f9fa;
            color: #111111;
            border: 1px solid #cccccc;
            padding: 10px 12px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 8pt;
            line-height: 1.35;
            white-space: pre-wrap;
            word-break: break-all;
            margin-top: 6px;
            margin-bottom: 16px;
            page-break-inside: auto;
        }}

        .page-break {{
            page-break-before: always;
        }}

        .diagram-box {{
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 14px;
            text-align: center;
            background: #fafafa;
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>

    <!-- COVER PAGE -->
    <div class="cover-page">
        <div class="academic-header">Database Design & Management System</div>
        <div class="course-title">Academic Capstone DBMS Project Report</div>
        
        <h1 class="main-title">EVENTIFY</h1>
        <div class="sub-title">A Full-Stack Event Registration System Demonstrating Frontend ↔ Backend ↔ Database Connectivity</div>
        
        <table class="meta-table">
            <tr>
                <td class="label">Subject</td>
                <td>Database Design and Management</td>
            </tr>
            <tr>
                <td class="label">Frontend</td>
                <td>HTML5, CSS3, Vanilla JavaScript</td>
            </tr>
            <tr>
                <td class="label">Backend</td>
                <td>Django REST Framework (Python)</td>
            </tr>
            <tr>
                <td class="label">Database</td>
                <td>MySQL / SQLite Relational DB</td>
            </tr>
            <tr>
                <td class="label">Architecture</td>
                <td>3-Tier Client-Server REST API</td>
            </tr>
        </table>
    </div>

    <!-- 1. INTRODUCTION -->
    <h1>1. Introduction & System Overview</h1>
    <p>
        <strong>Eventify</strong> is a web-based Event Registration System developed for the subject <strong>Database Design and Management</strong>. The goal of this project is to demonstrate real-time database connectivity between a Frontend user interface (HTML/CSS/JS), a Backend REST API (Django), and a Relational Database engine (MySQL/SQLite).
    </p>
    <p>
        All event details, participant profiles, and event registrations are stored in normalized relational database tables. Actions taken by users on the website trigger HTTP API calls, which execute SQL queries against the database and update the interface dynamically.
    </p>

    <!-- 2. CONCEPTUAL MODEL & RELATIONAL SCHEMA -->
    <div class="page-break"></div>
    <h1>2. Database Design & Relational Tables</h1>
    <p>
        The relational database consists of three primary tables in 3rd Normal Form (3NF). The Many-to-Many relationship between <code>events</code> and <code>participants</code> is resolved using the <code>registrations</code> junction table.
    </p>

    <h2>2.1 Entity Relationship Diagram</h2>
    <div class="diagram-box">
        <svg viewBox="0 0 800 280" width="100%" height="260" xmlns="http://www.w3.org/2000/svg">
            <!-- LINES -->
            <line x1="220" y1="140" x2="310" y2="140" stroke="#333" stroke-width="2" stroke-dasharray="4,4"/>
            <line x1="490" y1="140" x2="580" y2="140" stroke="#333" stroke-width="2" stroke-dasharray="4,4"/>

            <text x="240" y="132" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1a56db">1</text>
            <text x="285" y="132" font-family="sans-serif" font-size="12" font-weight="bold" fill="#d97706">N</text>
            <text x="505" y="132" font-family="sans-serif" font-size="12" font-weight="bold" fill="#d97706">N</text>
            <text x="555" y="132" font-family="sans-serif" font-size="12" font-weight="bold" fill="#059669">1</text>

            <!-- EVENTS -->
            <rect x="30" y="30" width="190" height="220" rx="4" fill="#fff" stroke="#1a56db" stroke-width="2"/>
            <rect x="30" y="30" width="190" height="36" rx="4" fill="#1a56db"/>
            <text x="125" y="53" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">EVENTS</text>
            <text x="45" y="85" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#1a56db">id (PK)</text>
            <text x="45" y="105" font-family="sans-serif" font-size="10.5" fill="#333">name</text>
            <text x="45" y="125" font-family="sans-serif" font-size="10.5" fill="#333">description</text>
            <text x="45" y="145" font-family="sans-serif" font-size="10.5" fill="#333">event_date</text>
            <text x="45" y="165" font-family="sans-serif" font-size="10.5" fill="#333">venue</text>
            <text x="45" y="185" font-family="sans-serif" font-size="10.5" fill="#333">max_seats</text>
            <text x="45" y="205" font-family="sans-serif" font-size="10.5" fill="#333">category</text>
            <text x="45" y="225" font-family="sans-serif" font-size="10.5" fill="#333">is_active</text>

            <!-- REGISTRATIONS -->
            <rect x="310" y="50" width="180" height="180" rx="4" fill="#fff" stroke="#d97706" stroke-width="2"/>
            <rect x="310" y="50" width="180" height="36" rx="4" fill="#d97706"/>
            <text x="400" y="73" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">REGISTRATIONS</text>
            <text x="325" y="105" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#d97706">id (PK)</text>
            <text x="325" y="130" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#b45309">event_id (FK)</text>
            <text x="325" y="155" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#b45309">participant_id (FK)</text>
            <text x="325" y="180" font-family="sans-serif" font-size="10.5" fill="#333">registered_at</text>

            <!-- PARTICIPANTS -->
            <rect x="580" y="50" width="190" height="180" rx="4" fill="#fff" stroke="#059669" stroke-width="2"/>
            <rect x="580" y="50" width="190" height="36" rx="4" fill="#059669"/>
            <text x="675" y="73" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">PARTICIPANTS</text>
            <text x="595" y="105" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#059669">id (PK)</text>
            <text x="595" y="130" font-family="sans-serif" font-size="10.5" fill="#333">name</text>
            <text x="595" y="155" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#047857">email (UNIQUE)</text>
            <text x="595" y="180" font-family="sans-serif" font-size="10.5" fill="#333">phone</text>
            <text x="595" y="205" font-family="sans-serif" font-size="10.5" fill="#333">college</text>
        </svg>
    </div>

    <h2>2.2 Data Dictionary</h2>
    <h3>Table: events</h3>
    <table class="data-table">
        <tr><th>Column Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr>
        <tr><td>id</td><td>INT</td><td>PRIMARY KEY AUTO_INCREMENT</td><td>Unique event identifier</td></tr>
        <tr><td>name</td><td>VARCHAR(200)</td><td>NOT NULL</td><td>Event title</td></tr>
        <tr><td>description</td><td>TEXT</td><td>NOT NULL</td><td>Event summary</td></tr>
        <tr><td>event_date</td><td>DATETIME</td><td>NOT NULL</td><td>Event date & time</td></tr>
        <tr><td>venue</td><td>VARCHAR(250)</td><td>NOT NULL</td><td>Hall / Online link</td></tr>
        <tr><td>max_seats</td><td>INT</td><td>NOT NULL</td><td>Capacity limit</td></tr>
        <tr><td>category</td><td>VARCHAR(50)</td><td>NOT NULL</td><td>Category tag</td></tr>
    </table>

    <h3>Table: participants</h3>
    <table class="data-table">
        <tr><th>Column Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr>
        <tr><td>id</td><td>INT</td><td>PRIMARY KEY AUTO_INCREMENT</td><td>Unique participant ID</td></tr>
        <tr><td>name</td><td>VARCHAR(150)</td><td>NOT NULL</td><td>Participant name</td></tr>
        <tr><td>email</td><td>VARCHAR(254)</td><td>NOT NULL UNIQUE</td><td>Unique contact email</td></tr>
        <tr><td>college</td><td>VARCHAR(200)</td><td>DEFAULT ''</td><td>Institution name</td></tr>
    </table>

    <h3>Table: registrations</h3>
    <table class="data-table">
        <tr><th>Column Name</th><th>Data Type</th><th>Constraints</th><th>Description</th></tr>
        <tr><td>id</td><td>INT</td><td>PRIMARY KEY AUTO_INCREMENT</td><td>Registration transaction ID</td></tr>
        <tr><td>event_id</td><td>INT</td><td>FOREIGN KEY → events(id)</td><td>References event</td></tr>
        <tr><td>participant_id</td><td>INT</td><td>FOREIGN KEY → participants(id)</td><td>References participant</td></tr>
        <tr><td>registered_at</td><td>DATETIME</td><td>DEFAULT CURRENT_TIMESTAMP</td><td>Registration timestamp</td></tr>
    </table>


    <!-- 3. SOURCE CODE -->
    <div class="page-break"></div>
    <h1>3. Source Code Plain Text Listings</h1>

    <h2>3.1 Database DDL Schema (schema.sql / eventify_database.sql)</h2>
    <pre class="code-block">{html.escape(sql_code)}</pre>

    <div class="page-break"></div>
    <h2>3.2 Backend Models (backend/events/models.py)</h2>
    <pre class="code-block">{html.escape(models_code)}</pre>

    <div class="page-break"></div>
    <h2>3.3 Backend API Controller Views (backend/events/views.py)</h2>
    <pre class="code-block">{html.escape(views_code)}</pre>

    <div class="page-break"></div>
    <h2>3.4 Frontend User Interface Markup (frontend/index.html)</h2>
    <pre class="code-block">{html.escape(html_code)}</pre>

    <div class="page-break"></div>
    <h2>3.5 Frontend Styling System (frontend/css/style.css)</h2>
    <pre class="code-block">{html.escape(css_code)}</pre>

    <div class="page-break"></div>
    <h2>3.6 Frontend Application Logic (frontend/js/app.js)</h2>
    <pre class="code-block">{html.escape(js_code)}</pre>

    <!-- 4. CONCLUSION -->
    <div class="page-break"></div>
    <h1>4. Conclusion</h1>
    <p>
        The <strong>Eventify</strong> project demonstrates complete frontend to backend to relational database connectivity. By using normalized tables (3NF), foreign key constraints, and REST API controllers, the system handles real-time seat tracking, participant management, and event listing efficiently without data redundancy.
    </p>

</body>
</html>
"""

html_path = r"d:\New folder (5)\report.html"
pdf_path = r"d:\New folder (5)\Eventify_Project_Report.pdf"
main_pdf_path = r"d:\New folder (5)\Eventify_DBMS_Project_Report.pdf"
artifact_pdf_path = r"C:\Users\THAMARAI SELVAN\.gemini\antigravity-ide\brain\4cfc0d0b-95de-497f-9bee-91a775480f2e\Eventify_DBMS_Project_Report.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML report written to:", html_path)

# Try removing previous PDF file if exists
if os.path.exists(pdf_path):
    try:
        os.remove(pdf_path)
    except Exception as e:
        print("Notice:", e)

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
    
    # Try updating main PDF path as well
    try:
        with open(main_pdf_path, "wb") as dst, open(pdf_path, "rb") as src:
            dst.write(src.read())
        print("Updated main_pdf_path successfully!")
    except Exception as e:
        print("Notice updating main_pdf_path:", e)

    # Copy to artifact path
    try:
        with open(artifact_pdf_path, "wb") as dst, open(pdf_path, "rb") as src:
            dst.write(src.read())
        print("PDF copied to artifact path:", artifact_pdf_path)
    except Exception as e:
        print("Notice updating artifact:", e)

    doc = fitz.open(pdf_path)
    print("Total PDF Page Count:", len(doc))
else:
    print("PDF compilation failed.")
