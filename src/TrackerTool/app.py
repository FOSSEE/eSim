from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
import os
from datetime import timedelta
from psycopg2.extras import Json
import traceback
from threading import Thread
import hashlib

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# Database connection helper

#def connect_db():
#    return psycopg2.connect(
#        dbname="esim_tracker",
#        user="esim_tracker_user",
#        password="iusEtWgeL6xXkpYVOkC532tFenmaik2x",
#        host="dpg-cu6tr3l6l47c73c3snh0-a.oregon-postgres.render.com",
 #       port="5432"
  #  )

import os
import requests

def send_crash_email_to_admin(crash: dict):
    api_key = os.getenv("RESEND_API_KEY")
    admin_email = os.getenv("ADMIN_EMAIL")
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

    print("[EMAIL] Attempting Resend...", flush=True)

    if not api_key:
        print("[EMAIL] Missing RESEND_API_KEY", flush=True)
        return

    if not admin_email:
        print("[EMAIL] Missing ADMIN_EMAIL", flush=True)
        return

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "from": from_email,
        "to": [admin_email],
        "subject": f"[eSim] Crash — {crash.get('user_id')}",
        "text": f"""
🚨 eSim Crash Alert

User: {crash.get('user_id')}
Crash Time: {crash.get('crash_time')}
Session Start: {crash.get('session_start')}
Session End: {crash.get('session_end')}
Provider: {crash.get('provider')}
Event ID: {crash.get('event_id')}
Exception: {crash.get('exception_code')}
Faulting Module: {crash.get('faulting_module')}

Message:
{(crash.get('message') or '')[:4000]}
"""
    }

    try:
        r = requests.post(url, json=body, headers=headers, timeout=15)

        if r.status_code >= 400:
            print("[EMAIL] Resend failed:", r.status_code, r.text, flush=True)
        else:
            print("[EMAIL] Resend sent OK", flush=True)

    except Exception as e:
        print("[EMAIL] Resend exception:", repr(e), flush=True)


from dotenv import load_dotenv
load_dotenv()

def connect_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set")
    # ensure sslmode=require even if missing
    if "sslmode=" not in db_url:
        sep = "&" if "?" in db_url else "?"
        db_url = db_url + f"{sep}sslmode=require"
    return psycopg2.connect(db_url, connect_timeout=10)


# -------------------------
# ✅ DB helper functions
# -------------------------

def exec_sql(sql, params=()):
    """INSERT / UPDATE / DELETE"""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

import os
import psycopg2

def qall(sql, params=()):
    """SELECT many rows (returns list of tuples)"""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def q1(sql, params=()):
    """SELECT single row (returns one tuple or None)"""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()
    finally:
        conn.close()

@app.route("/debug/counts", methods=["GET"])
def debug_counts():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("select current_database(), current_user;")
            who = cur.fetchone()

            cur.execute("select count(*) from public.sessions;")
            sessions = cur.fetchone()[0]
            cur.execute("select count(*) from public.logs;")
            logs = cur.fetchone()[0]
            cur.execute("select count(*) from public.crashes;")
            crashes = cur.fetchone()[0]

    return jsonify({
        "db": who[0],
        "user": who[1],
        "counts": {"sessions": sessions, "logs": logs, "crashes": crashes}
    })
# Serve the front-end (index.html)
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')  # Ensure your index.html is in a 'static' folder

@app.route('/statstics', methods=['GET'])
def get_stats():
    conn = connect_db()
    cursor = conn.cursor()

    user_id = request.args.get("user")  # Fetch user filter from API request

    if user_id:
        # Fetch stats for a specific user (Fixed: use %s instead of ?)
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE user_id = %s", (user_id,))
        total_sessions = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(total_duration) FROM sessions WHERE user_id = %s", (user_id,))
        total_hours = cursor.fetchone()[0] or 0

        cursor.execute("SELECT AVG(total_duration) FROM sessions WHERE user_id = %s", (user_id,))
        avg_duration = cursor.fetchone()[0] or 0

    else:
        # Fetch overall stats (all users)
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM sessions")
        active_users = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(total_duration) FROM sessions")
        total_hours = cursor.fetchone()[0] or 0

        cursor.execute("SELECT AVG(total_duration) FROM sessions")
        avg_duration = cursor.fetchone()[0] or 0

    conn.close()

    # Convert `total_hours` and `avg_duration` from timedelta if needed
    if isinstance(avg_duration, timedelta):
        avg_duration = avg_duration.total_seconds() / 3600  # Convert to hours

    if isinstance(total_hours, timedelta):
        total_hours = total_hours.total_seconds() / 3600  # Convert to hours

    return jsonify({
        "total_sessions": total_sessions,
        "active_users": active_users if not user_id else 1,  # Show active user count only for all users
        "total_hours": float(total_hours),  # Convert to numeric format
        "avg_duration": float(avg_duration),  # Convert to numeric format
    })

@app.route("/health/db", methods=["GET"])
def health_db():
    try:
        with connect_db() as conn:
            dsn = conn.get_dsn_parameters()
            with conn.cursor() as cur:
                cur.execute("select current_database(), current_user;")
                dbname, dbuser = cur.fetchone()

        # ✅ Don't leak password. This is safe.
        return jsonify({
            "ok": True,
            "current_database": dbname,
            "current_user": dbuser,
            "dsn_host": dsn.get("host"),
            "dsn_dbname": dsn.get("dbname"),
            "dsn_user": dsn.get("user"),
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    

# API Endpoint: Get all sessions
@app.route('/sessions', methods=['GET'])
def get_sessions():
    user_filter = request.args.get('user')
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
        SELECT session_id, user_id, session_start, session_end, total_duration, location
        FROM sessions
    """
    params = ()
    if user_filter:
        sql += " WHERE user_id = %s"
        params = (user_filter,)
    sql += " ORDER BY session_id DESC"

    cursor.execute(sql, params)
    sessions = cursor.fetchall()
    conn.close()

    formatted_sessions = []
    for s in sessions:
        formatted_sessions.append({
            'session_id': s[0],
            'user_id': s[1],
            'session_start': s[2].strftime('%Y-%m-%d %H:%M:%S'),
            'session_end': s[3].strftime('%Y-%m-%d %H:%M:%S') if s[3] else '',
            'total_duration': str(s[4]) if s[4] else 'N/A',
            'location': s[5]  # NEW
        })

    return jsonify(formatted_sessions)

@app.route('/logs', methods=['GET'])
def get_logs():
    """Fetch logs only for the requested user."""
    user_filter = request.args.get('user')  # Get user filter from query parameter

    conn = connect_db()
    cursor = conn.cursor()

    if user_filter:
        cursor.execute("SELECT log_id, user_id, log_timestamp, log_content FROM logs WHERE user_id = %s", (user_filter,))
    else:
        cursor.execute("SELECT log_id, user_id, log_timestamp, log_content FROM logs")

    logs = cursor.fetchall()
    conn.close()

    # Format log data for JSON response
    formatted_logs = [
        {
            "log_id": log[0],
            "user_id": log[1],
            "log_timestamp": log[2].strftime('%Y-%m-%d %H:%M:%S'),
            "log_content": log[3]
        }
        for log in logs
    ]

    return jsonify(formatted_logs)

@app.route("/get_users", methods=["GET"])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM sessions;")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route("/get_summary", methods=["GET"])
def get_summary():
    user = request.args.get("user", "All Users")
    conn = connect_db()
    cursor = conn.cursor()
    
    if user == "All Users":
        cursor.execute("SELECT COUNT(*), SUM(total_duration) FROM sessions;")
    else:
        cursor.execute("SELECT COUNT(*), SUM(total_duration) FROM sessions WHERE user_id=%s;", (user,))
    
    result = cursor.fetchone()
    conn.close()
    
    summary = {
        "total_sessions": result[0] if result else 0,
        "total_duration": str(result[1]) if result[1] else "0:00:00"
    }
    return jsonify(summary)

import re
from datetime import datetime, timezone

def parse_dt_flexible(v):
    """
    Accept:
    - datetime already
    - 'YYYY-MM-DD HH:MM:SS'
    - ISO 'YYYY-MM-DDTHH:MM:SS'
    - Windows '/Date(1771270797069)/'  (ms since epoch)
    """
    if v is None:
        return None

    if isinstance(v, datetime):
        return v

    s = str(v).strip()
    if not s:
        return None

    # Windows /Date( ... )/
    m = re.match(r"^/Date\((\d+)\)/$", s)
    if m:
        ms = int(m.group(1))
        return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).replace(tzinfo=None)

    # Replace T with space, try ISO
    s2 = s.replace("T", " ")
    try:
        return datetime.fromisoformat(s2)
    except Exception:
        pass

    # Last resort common format
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s2, fmt)
        except Exception:
            continue

    return None

from datetime import datetime
from psycopg2.extras import Json

def parse_dt(v):
    if v is None:
        return None
    s = str(v).strip().replace("T", " ")
    return datetime.fromisoformat(s)

@app.route('/add-session', methods=['POST'])
def add_session():
    data = request.get_json(silent=True) or {}

    required = ["user_id", "session_start", "session_end"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Prefer seconds
    if data.get("total_duration_seconds") is not None:
        try:
            secs = float(data["total_duration_seconds"])
        except Exception:
            return jsonify({"error": "total_duration_seconds must be numeric"}), 400
    elif data.get("total_duration") is not None:
        try:
            hours = float(data["total_duration"])
        except Exception:
            return jsonify({"error": "total_duration must be numeric hours OR provide total_duration_seconds"}), 400
        secs = hours * 3600.0
    else:
        return jsonify({"error": "Missing total_duration_seconds or total_duration"}), 400

    location = data.get("location")

    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sessions (user_id, session_start, session_end, total_duration, location)
                    VALUES (%s, %s, %s, make_interval(secs => %s), %s)
                    ON CONFLICT (user_id, session_start, session_end)
                    DO UPDATE SET
                        total_duration = EXCLUDED.total_duration,
                        location = COALESCE(EXCLUDED.location, sessions.location);
                """, (
                    data["user_id"],
                    parse_dt(data["session_start"]),
                    parse_dt(data["session_end"]),
                    secs,
                    Json(location) if location else None
                ))
        return jsonify({"message": "Session upserted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# API Endpoint: Add a log
@app.route('/add-log', methods=['POST'])
def add_log():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO logs (user_id, log_timestamp, log_content)
                      VALUES (%s, %s, %s)''',
                   (data['user_id'], data['log_timestamp'], data['log_content']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Log added successfully"})

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        user_filter = request.args.get('user')
        conn = connect_db()
        cursor = conn.cursor()

        # Total active users
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM sessions")
        active_users = cursor.fetchone()[0]

        # Total hours logged (Handle timedelta conversion)
        cursor.execute("SELECT SUM(total_duration) FROM sessions")  # duration should be timedelta
        total_duration = cursor.fetchone()[0] or timedelta(0)  # Handle null or empty result

        # Convert total_duration to hours
        total_hours = total_duration.total_seconds() / 3600  # Convert to hours

        # Average time spent per session (Handle timedelta conversion)
        cursor.execute("SELECT AVG(total_duration) FROM sessions")  # duration should be timedelta
        avg_time = cursor.fetchone()[0] or timedelta(0)  # Handle null or empty result

        # Convert avg_time to hours
        avg_duration = avg_time.total_seconds() / 3600  # Convert to hours

        conn.close()

        # Return as JSON
        return jsonify({
            "active-users": active_users,
            "total-hours": round(total_hours, 2),
            "avg-duration": round(avg_duration, 2)
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "There was a problem with the database query.", "details": str(e)}), 500


@app.route('/export-data', methods=['GET'])
def export_data():
    """Fetches session data for export."""
    user_filter = request.args.get("user_filter")  
    conn = connect_db()
    cursor = conn.cursor()

    if user_filter and user_filter != "All Users":
        cursor.execute("SELECT user_id, session_start, session_end, total_duration FROM sessions WHERE user_id = %s", (user_filter,))
    else:
        cursor.execute("SELECT user_id, session_start, session_end, total_duration, location FROM sessions")


    records = cursor.fetchall()
    conn.close()

    if not records:
        return jsonify({"error": "No data found"}), 404  # Return error if no data

    try:
        data = [
            {
                "user_id": r[0] if r[0] is not None else "Unknown",
                "session_start": r[1].isoformat() if r[1] is not None else "N/A",
                "session_end": r[2].isoformat() if r[2] is not None else "N/A",
                "total_duration": r[3].total_seconds() if r[3] is not None else 0,
                "location": r[4]  # ✅ NEW
            }
            for r in records
        ]

        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to serialize data"}), 500

@app.route('/delete-session', methods=['DELETE'])
def delete_session():
    """Deletes a session based on user and start time."""
    data = request.json
    user_id = data.get("user")  # Fix: Ensure correct key name
    session_start = data.get("session_start")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sessions WHERE user_id = %s AND session_start = %s", (user_id, session_start))
    conn.commit()

    if cursor.rowcount == 0:  # No rows deleted (session not found)
        conn.close()
        return jsonify({"error": "Session not found or already deleted"}), 404

    conn.close()
    return jsonify({"message": f"Session for {user_id} at {session_start} deleted successfully."})

from psycopg2.extras import Json

@app.route('/add-crash', methods=['POST'])
def add_crash():
    data = request.get_json(silent=True) or {}

    if "user_id" not in data:
        return jsonify({"error": "Missing fields: ['user_id']"}), 400

    try:
        crash_time = parse_dt_flexible(data.get("crash_time"))
        sess_start = parse_dt_flexible(data.get("session_start"))
        sess_end   = parse_dt_flexible(data.get("session_end"))

        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO crashes (
                        user_id, session_start, session_end, crash_time,
                        event_id, provider, exception_code, faulting_module, message,
                        location
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    data.get("user_id"),
                    sess_start,
                    sess_end,
                    crash_time,
                    int(data.get("event_id") or 0),
                    data.get("provider", ""),
                    data.get("exception_code", ""),
                    data.get("faulting_module", ""),
                    data.get("message", ""),
                    Json(data.get("location")) if data.get("location") else None
                ))

        # ✅ Build a safe payload for email (strings only)
        email_payload = {
            **data,
            "crash_time": crash_time.strftime("%Y-%m-%d %H:%M:%S") if crash_time else data.get("crash_time"),
            "session_start": sess_start.strftime("%Y-%m-%d %H:%M:%S") if sess_start else data.get("session_start"),
            "session_end": sess_end.strftime("%Y-%m-%d %H:%M:%S") if sess_end else data.get("session_end"),
        }

        print("[EMAIL] Queuing crash email...", flush=True)

        # ✅ Send email in background so request returns fast
        Thread(target=send_crash_email_to_admin, args=(email_payload,), daemon=True).start()

        return jsonify({"message": "Crash recorded successfully"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/crashes', methods=['GET'])
def get_crashes():
    user_filter = request.args.get('user')
    since_id = request.args.get('since_id')

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
      SELECT crash_id, user_id, session_start, session_end, crash_time,
             event_id, provider, exception_code, faulting_module, message,
             location
      FROM crashes
    """
    params = []
    clauses = []

    if user_filter:
        clauses.append("user_id = %s")
        params.append(user_filter)

    if since_id:
        clauses.append("crash_id > %s")
        params.append(int(since_id))

    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY crash_id DESC LIMIT 200"

    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    def fmt_dt(x):
        return x.strftime('%Y-%m-%d %H:%M:%S') if x else ""

    out = []
    for r in rows:
        out.append({
            "crash_id": r[0],
            "user_id": r[1],
            "session_start": fmt_dt(r[2]),
            "session_end": fmt_dt(r[3]),
            "crash_time": fmt_dt(r[4]),
            "event_id": r[5],
            "provider": r[6],
            "exception_code": r[7],
            "faulting_module": r[8],
            "message": r[9],
            "location": r[10],  # ✅ NEW
        })

    return jsonify(out)



# =========================
# TASKS (expanded) + dependencies + comments
# =========================

# =========================
# TASKS (expanded) + dependencies + comments + ✅ linked releases
# =========================

@app.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    category = request.args.get("category")
    platform = request.args.get("platform")
    component = request.args.get("component")

    base = """
        SELECT
            t.task_id,
            t.title,
            COALESCE(t.description,''),
            t.category,
            t.component,
            t.platform,
            t.status,
            t.priority,
            t.severity,
            t.assignee,
            t.created_at,
            t.updated_at,

            -- list of release ids
            COALESCE(array_agg(r.release_id ORDER BY r.release_id)
                     FILTER (WHERE r.release_id IS NOT NULL), '{}') AS release_ids,

            -- list of release labels like "v2.3 (Planned)"
            COALESCE(array_agg((r.version || ' (' || r.status || ')') ORDER BY r.release_id)
                     FILTER (WHERE r.release_id IS NOT NULL), '{}') AS release_labels

        FROM tasks t
        LEFT JOIN release_items ri ON ri.task_id = t.task_id
        LEFT JOIN releases r ON r.release_id = ri.release_id
    """

    clauses = []
    params = []

    if status:
        clauses.append("t.status=%s"); params.append(status)
    if category:
        clauses.append("t.category=%s"); params.append(category)
    if platform:
        clauses.append("t.platform=%s"); params.append(platform)
    if component:
        clauses.append("t.component=%s"); params.append(component)

    if clauses:
        base += " WHERE " + " AND ".join(clauses)

    base += """
        GROUP BY
            t.task_id, t.title, t.description, t.category, t.component, t.platform,
            t.status, t.priority, t.severity, t.assignee, t.created_at, t.updated_at
        ORDER BY t.created_at DESC
    """

    rows = qall(base, tuple(params))

    return jsonify([{
        "task_id": r[0],
        "title": r[1],
        "description": r[2],

        # backward compatibility
        "task_type": r[3],
        "category": r[3],

        "component": r[4],
        "platform": r[5],
        "status": r[6],
        "priority": r[7],
        "severity": r[8],
        "assignee": r[9] or "Unassigned",
        "created_at": r[10].strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": r[11].strftime("%Y-%m-%d %H:%M:%S"),

        # NEW
        "release_ids": list(r[12]) if r[12] else [],
        "release_labels": list(r[13]) if r[13] else [],
    } for r in rows])




@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json

    # ✅ UI sends task_type; DB stores it as category
    task_type = data.get("task_type", data.get("category", "Feature"))

    exec_sql("""
        INSERT INTO tasks (title,description,category,component,platform,status,priority,severity,assignee)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["title"],
        data.get("description",""),
        task_type,
        data.get("component","General"),
        data.get("platform","All"),
        data.get("status","Backlog"),
        data.get("priority","Medium"),
        data.get("severity", None),
        data.get("assignee","Unassigned")
    ))
    return jsonify({"message": "Task added"})


@app.route("/update-task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    # ✅ UI sends task_type; DB stores it as category
    task_type = data.get("task_type", data.get("category", "Feature"))

    exec_sql("""
        UPDATE tasks
        SET title=%s,
            description=%s,
            category=%s,
            component=%s,
            platform=%s,
            status=%s,
            priority=%s,
            severity=%s,
            assignee=%s,
            updated_at=NOW()
        WHERE task_id=%s
    """, (
        data["title"],
        data.get("description",""),
        task_type,
        data.get("component","General"),
        data.get("platform","All"),
        data.get("status","Backlog"),
        data.get("priority","Medium"),
        data.get("severity", None),
        data.get("assignee","Unassigned"),
        task_id
    ))
    return jsonify({"message": "Task updated"})


@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    exec_sql("DELETE FROM tasks WHERE task_id=%s", (task_id,))
    return jsonify({"message": "Task deleted"})



@app.route("/tasks/<int:task_id>/deps", methods=["GET"])
def get_task_deps(task_id):
    rows = qall("""
        SELECT depends_on_task_id
        FROM task_dependencies
        WHERE task_id=%s
    """, (task_id,))
    return jsonify({"task_id": task_id, "depends_on": [r[0] for r in rows]})


@app.route("/tasks/<int:task_id>/deps", methods=["POST"])
def add_task_dep(task_id):
    data = request.json
    depends_on = int(data["depends_on_task_id"])
    exec_sql("""
        INSERT INTO task_dependencies (task_id, depends_on_task_id)
        VALUES (%s,%s)
        ON CONFLICT DO NOTHING
    """, (task_id, depends_on))
    return jsonify({"message": "Dependency added"})


@app.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_task_comments(task_id):
    rows = qall("""
        SELECT comment_id,author,comment,created_at
        FROM task_comments
        WHERE task_id=%s
        ORDER BY created_at DESC
    """, (task_id,))
    return jsonify([{
        "comment_id": r[0],
        "author": r[1],
        "comment": r[2],
        "created_at": r[3].strftime("%Y-%m-%d %H:%M:%S")
    } for r in rows])


@app.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_task_comment(task_id):
    data = request.json
    exec_sql("""
        INSERT INTO task_comments (task_id,author,comment)
        VALUES (%s,%s,%s)
    """, (task_id, data.get("author","Unknown"), data["comment"]))
    return jsonify({"message": "Comment added"})


# =========================
# RELEASES + linking tasks to releases
# =========================

@app.route("/releases", methods=["GET"])
def get_releases():
    rows = qall("SELECT release_id,version,status,target_date,release_date,notes FROM releases ORDER BY COALESCE(release_date, target_date) DESC NULLS LAST")
    return jsonify([{
        "release_id": r[0],
        "version": r[1],
        "status": r[2],
        "target_date": str(r[3]) if r[3] else None,
        "release_date": str(r[4]) if r[4] else None,
        "notes": r[5] or ""
    } for r in rows])


@app.route("/releases", methods=["POST"])
def add_release():
    data = request.json
    exec_sql("""
        INSERT INTO releases (version,status,target_date,release_date,notes)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data["version"],
        data.get("status","Planned"),
        data.get("target_date", None),
        data.get("release_date", None),
        data.get("notes","")
    ))
    return jsonify({"message": "Release added"})


@app.route("/releases/<int:release_id>/items", methods=["POST"])
def add_release_item(release_id):
    data = request.json
    task_id = int(data["task_id"])
    exec_sql("""
        INSERT INTO release_items (release_id, task_id)
        VALUES (%s,%s)
        ON CONFLICT DO NOTHING
    """, (release_id, task_id))
    return jsonify({"message": "Task attached to release"})


@app.route("/releases/<int:release_id>/items", methods=["GET"])
def get_release_items(release_id):
    rows = qall("""
        SELECT t.task_id, t.title, t.status, t.category, t.component, t.platform, t.priority, t.assignee
        FROM release_items ri
        JOIN tasks t ON t.task_id = ri.task_id
        WHERE ri.release_id=%s
        ORDER BY t.priority DESC, t.updated_at DESC
    """, (release_id,))
    return jsonify([{
        "task_id": r[0],
        "title": r[1],
        "status": r[2],
        "category": r[3],
        "component": r[4],
        "platform": r[5],
        "priority": r[6],
        "assignee": r[7],
    } for r in rows])


@app.route("/releases/<int:release_id>/progress", methods=["GET"])
def release_progress(release_id):
    rows = qall("""
        SELECT status, COUNT(*)
        FROM release_items ri
        JOIN tasks t ON t.task_id = ri.task_id
        WHERE ri.release_id=%s
        GROUP BY status
    """, (release_id,))
    stats = {r[0]: r[1] for r in rows}
    return jsonify({"release_id": release_id, "by_status": stats})

from psycopg2.extras import Json

@app.route("/add-env-snapshot", methods=["POST"])
def add_env_snapshot():
    data = request.get_json(silent=True) or {}

    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO env_snapshots (
                      snapshot_id, user_id, session_id, timestamp,
                      os_name, os_release, os_version, machine, processor,
                      cpu_count_logical, cpu_count_physical, total_ram_gb, toolchain
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (snapshot_id) DO NOTHING
                """, (
                    data.get("snapshot_id"),
                    data.get("user_id"),
                    data.get("session_id"),
                    data.get("timestamp"),
                    data.get("os_name"),
                    data.get("os_release"),
                    data.get("os_version"),
                    data.get("machine"),
                    data.get("processor"),
                    data.get("cpu_count_logical"),
                    data.get("cpu_count_physical"),
                    data.get("total_ram_gb"),
                    Json(data.get("toolchain")) if data.get("toolchain") else None
                ))

        return jsonify({"message": "env snapshot stored"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)

