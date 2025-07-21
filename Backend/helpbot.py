from flask import Flask, request, jsonify, session
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import uuid
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# === Configuration ===
SESSION_TIMEOUT = 30 * 60  # 30 minutes in seconds
MAX_HISTORY_PER_USER = 50  # Maximum chat history per user

# === Thread-safe data structures ===
class UserManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.users = {}  # user_id -> user_data
        self.last_activity = {}  # user_id -> timestamp
        
    def get_or_create_user(self, user_id=None):
        with self.lock:
            if not user_id:
                user_id = str(uuid.uuid4())
            
            if user_id not in self.users:
                self.users[user_id] = {
                    'id': user_id,
                    'chat_history': [],
                    'created_at': datetime.now(),
                    'message_count': 0
                }
                print(f"[UserManager] Created new user: {user_id}")
            
            self.last_activity[user_id] = time.time()
            return user_id, self.users[user_id]
    
    def update_user_activity(self, user_id):
        with self.lock:
            if user_id in self.users:
                self.last_activity[user_id] = time.time()
    
    def add_to_history(self, user_id, question, response):
        with self.lock:
            if user_id in self.users:
                user_data = self.users[user_id]
                user_data['chat_history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'question': question,
                    'response': response
                })
                user_data['message_count'] += 1
                
                # Keep only the last MAX_HISTORY_PER_USER messages
                if len(user_data['chat_history']) > MAX_HISTORY_PER_USER:
                    user_data['chat_history'] = user_data['chat_history'][-MAX_HISTORY_PER_USER:]
    
    def get_user_stats(self, user_id):
        with self.lock:
            if user_id in self.users:
                user_data = self.users[user_id]
                return {
                    'user_id': user_id,
                    'message_count': user_data['message_count'],
                    'created_at': user_data['created_at'].isoformat(),
                    'last_activity': datetime.fromtimestamp(self.last_activity[user_id]).isoformat(),
                    'history_length': len(user_data['chat_history'])
                }
            return None
    
    def cleanup_inactive_users(self):
        """Remove users who have been inactive for more than SESSION_TIMEOUT"""
        current_time = time.time()
        with self.lock:
            inactive_users = [
                user_id for user_id, last_active in self.last_activity.items()
                if current_time - last_active > SESSION_TIMEOUT
            ]
            
            for user_id in inactive_users:
                del self.users[user_id]
                del self.last_activity[user_id]
                print(f"[UserManager] Cleaned up inactive user: {user_id}")
            
            return len(inactive_users)
    
    def get_active_users_count(self):
        with self.lock:
            return len(self.users)

# === Initialize components ===
user_manager = UserManager()

# Initialize LLM with error handling
try:
    model = OllamaLLM(model="qwen2.5-coder:3b")
    print("[Server] LLM initialized successfully")
except Exception as e:
    print(f"[Server] Error initializing LLM: {e}")
    model = None

# Updated prompt template for better context handling
template = """
You are a professional electronic engineer and expert assistant specializing in EDA tools including eSim, KiCad, and NgSPICE simulation. 

Use the following knowledge base information to provide accurate and helpful answers:
{context}

Previous conversation context (if any):
{history}

Current question: {question}

Instructions:
- Provide practical, actionable advice
- Include specific commands, syntax, or examples when relevant
- Keep responses concise but comprehensive (maximum 200 words)
- If the question is about debugging, provide step-by-step troubleshooting steps
- Reference specific parameters or options when applicable
- If you're not certain about something, say so clearly

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# === Cleanup thread ===
def cleanup_thread():
    """Background thread to cleanup inactive users"""
    while True:
        try:
            time.sleep(300)  # Run every 5 minutes
            cleaned_count = user_manager.cleanup_inactive_users()
            if cleaned_count > 0:
                print(f"[Cleanup] Removed {cleaned_count} inactive users")
        except Exception as e:
            print(f"[Cleanup] Error during cleanup: {e}")

# Start cleanup thread
cleanup_worker = threading.Thread(target=cleanup_thread, daemon=True)
cleanup_worker.start()

# === API Routes ===

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get or create user session
        user_id = request.json.get("user_id") or session.get('user_id')
        user_id, user_data = user_manager.get_or_create_user(user_id)
        session['user_id'] = user_id
        
        question = request.json.get("prompt", "").strip()
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        print(f"[API] User {user_id[:8]}... asked: {question}")
        
        # Check if LLM is available
        if model is None:
            return jsonify({"error": "LLM not available"}), 503
        
        # 1. Retrieve relevant documents
        context = ""
        try:
            docs = retriever.invoke(question)
            if isinstance(docs, list) and docs:
                # Format context with more structure
                context_parts = []
                for i, doc in enumerate(docs[:5], 1):  # Limit to top 5 results
                    if hasattr(doc, 'page_content') and hasattr(doc, 'metadata'):
                        content = doc.page_content
                        metadata = doc.metadata
                        
                        # Add command information if available
                        cmd_info = f"[{i}] "
                        if metadata.get('command'):
                            cmd_info += f"Command: {metadata['command']} | "
                        if metadata.get('category'):
                            cmd_info += f"Category: {metadata['category']} | "
                        
                        cmd_info += content
                        context_parts.append(cmd_info)
                
                context = "\n\n".join(context_parts)
            elif hasattr(docs, "page_content"):
                context = docs.page_content
            else:
                context = str(docs) if docs else ""
                
        except Exception as e:
            print(f"[API] Retriever error for user {user_id[:8]}...: {e}")
            context = ""
        
        # 2. Get recent chat history for context
        history = ""
        if user_data['chat_history']:
            recent_history = user_data['chat_history'][-3:]  # Last 3 exchanges
            history_parts = []
            for h in recent_history:
                history_parts.append(f"Previous Q: {h['question']}")
                history_parts.append(f"Previous A: {h['response'][:100]}...")  # Truncate long responses
            history = "\n".join(history_parts)
        
        # 3. Run LLM
        try:
            chain = prompt | model
            output = chain.invoke({
                "context": context,
                "history": history,
                "question": question
            })
            response = str(output).strip()
            
            # Store in user's chat history
            user_manager.add_to_history(user_id, question, response)
            
            return jsonify({
                "response": response,
                "user_id": user_id,
                "message_count": user_data['message_count'] + 1,
                "context_found": bool(context.strip())
            })
            
        except Exception as e:
            print(f"[API] LLM error for user {user_id[:8]}...: {e}")
            return jsonify({"error": f"LLM processing error: {str(e)}"}), 500
    
    except Exception as e:
        print(f"[API] Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/search", methods=["POST"])
def search_knowledge():
    """Search the knowledge base directly"""
    try:
        query = request.json.get("query", "").strip()
        if not query:
            return jsonify({"error": "No search query provided"}), 400
        
        # Retrieve relevant documents
        docs = retriever.invoke(query)
        results = []
        
        if isinstance(docs, list):
            for doc in docs[:10]:  # Return top 10 results
                if hasattr(doc, 'page_content') and hasattr(doc, 'metadata'):
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "command": doc.metadata.get('command', ''),
                        "category": doc.metadata.get('category', ''),
                        "description": doc.metadata.get('description', '')
                    })
        
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/new_session", methods=["POST"])
def new_session():
    """Create a new user session"""
    try:
        user_id, user_data = user_manager.get_or_create_user()
        session['user_id'] = user_id
        
        return jsonify({
            "user_id": user_id,
            "message": "New session created",
            "created_at": user_data['created_at'].isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history():
    """Get chat history for current user"""
    try:
        user_id = request.args.get("user_id") or session.get('user_id')
        if not user_id:
            return jsonify({"error": "No user session found"}), 400
        
        user_id, user_data = user_manager.get_or_create_user(user_id)
        user_manager.update_user_activity(user_id)
        
        limit = int(request.args.get("limit", 10))
        history = user_data['chat_history'][-limit:] if limit > 0 else user_data['chat_history']
        
        return jsonify({
            "history": history,
            "total_messages": user_data['message_count'],
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear_history", methods=["POST"])
def clear_history():
    """Clear chat history for current user"""
    try:
        user_id = request.json.get("user_id") or session.get('user_id')
        if not user_id:
            return jsonify({"error": "No user session found"}), 400
        
        user_id, user_data = user_manager.get_or_create_user(user_id)
        user_data['chat_history'] = []
        user_manager.update_user_activity(user_id)
        
        return jsonify({"message": "History cleared", "user_id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stats", methods=["GET"])
def get_stats():
    """Get user statistics"""
    try:
        user_id = request.args.get("user_id") or session.get('user_id')
        if user_id:
            user_stats = user_manager.get_user_stats(user_id)
            if user_stats:
                user_manager.update_user_activity(user_id)
                return jsonify(user_stats)
        
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/server_stats", methods=["GET"])
def get_server_stats():
    """Get server statistics (admin endpoint)"""
    try:
        return jsonify({
            "active_users": user_manager.get_active_users_count(),
            "server_uptime": "Running",
            "llm_status": "Available" if model else "Unavailable",
            "vector_db_status": "Available"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": user_manager.get_active_users_count(),
        "components": {
            "llm": "Available" if model else "Unavailable",
            "vector_db": "Available",
            "user_manager": "Available"
        }
    })

# === Error handlers ===
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("\n" + "="*50)
    print("[Server] Starting NgSPICE ChatBot Server...")
    print("="*50)
    print(f"[Server] Session timeout: {SESSION_TIMEOUT // 60} minutes")
    print(f"[Server] Max history per user: {MAX_HISTORY_PER_USER}")
    print(f"[Server] LLM Model: {'qwen2.5-coder:3b' if model else 'Not Available'}")
    print("="*50)
    
    # Run with threading support for multiple users
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,  # Set to False for production
        threaded=True  # Enable threading for concurrent requests
    )