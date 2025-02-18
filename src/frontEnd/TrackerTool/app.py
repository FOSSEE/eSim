from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
import os
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# Database connection helper
def connect_db():
    return psycopg2.connect(
        dbname="esim_tracker",
        user="esim_tracker_user",
        password="iusEtWgeL6xXkpYVOkC532tFenmaik2x",
        host="dpg-cu6tr3l6l47c73c3snh0-a.oregon-postgres.render.com",
        port="5432"
    )

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
# API Endpoint: Get all sessions
@app.route('/sessions', methods=['GET'])
def get_sessions():
    user_filter = request.args.get('user')  # Get user filter from query parameter
    conn = connect_db()
    cursor = conn.cursor()

    if user_filter:
        cursor.execute("SELECT * FROM sessions WHERE user_id = %s", (user_filter,))
    else:
        cursor.execute("SELECT * FROM sessions")

    sessions = cursor.fetchall()

    # Format session data for easier handling in frontend
    formatted_sessions = []
    for session in sessions:
        session_data = {
            'session_id': session[0],
            'user_id': session[1],
            'session_start': session[2].strftime('%Y-%m-%d %H:%M:%S'),
            'session_end': session[3].strftime('%Y-%m-%d %H:%M:%S') if session[3] else '',
            'total_duration': str(session[4]) if session[4] else 'N/A'
        }
        formatted_sessions.append(session_data)

    conn.close()
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
@app.route('/add-session', methods=['POST'])
def add_session():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()

    # Ensure total_duration is in INTERVAL format (in hours)
    total_duration_interval = f"{data['total_duration']} hours"

    try:
        # Insert session with correct type casting for total_duration
        cursor.execute('''
            INSERT INTO sessions (user_id, session_start, session_end, total_duration)
            VALUES (%s, %s, %s, %s::INTERVAL)
        ''', (data['user_id'], data['session_start'], data['session_end'], total_duration_interval))
        conn.commit()
        conn.close()
        return jsonify({"message": "Session added successfully"})
    
    except Exception as e:
        return jsonify({"error": f"Error occurred: {str(e)}"}), 50


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
        cursor.execute("SELECT user_id, session_start, session_end, total_duration FROM sessions")

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
                "total_duration": r[3].total_seconds() if r[3] is not None else 0  # Convert timedelta to seconds
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
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
