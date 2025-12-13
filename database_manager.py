"""
Database manager for Codette AI
Handles persistence and data management
"""
import sqlite3
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
import threading

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manager for SQLite database with Codette data"""
    
    def __init__(self, db_path: str = "codette_data.db"):
        """Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Conversations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Messages table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id INTEGER NOT NULL,
                        user_message TEXT NOT NULL,
                        ai_response TEXT NOT NULL,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                    )
                ''')
                
                # Memory table for Codette's long-term memory
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
                
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            # For in-memory databases that might not support certain operations,
            # we still want to log but not fail completely
            if ":memory:" not in self.db_path:
                raise
    
    def create_user(self, username: str, password_hash: str, metadata: Optional[Dict] = None) -> int:
        """Create a new user
        
        Args:
            username: Username
            password_hash: Hashed password
            metadata: Optional user metadata
            
        Returns:
            User ID
        """
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                        (username, password_hash)
                    )
                    conn.commit()
                    logger.info(f"User created: {username}")
                    return cursor.lastrowid
        except sqlite3.IntegrityError:
            logger.warning(f"User already exists: {username}")
            raise ValueError(f"User {username} already exists")
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username
        
        Args:
            username: Username to look up
            
        Returns:
            User dict or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    def save_message(self, conversation_id: int, user_message: str, ai_response: str,
                    metadata: Optional[Dict] = None) -> int:
        """Save a conversation message
        
        Args:
            conversation_id: ID of conversation
            user_message: User's message
            ai_response: AI's response
            metadata: Optional message metadata
            
        Returns:
            Message ID
        """
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    metadata_json = json.dumps(metadata or {})
                    cursor.execute('''
                        INSERT INTO messages (conversation_id, user_message, ai_response, metadata)
                        VALUES (?, ?, ?, ?)
                    ''', (conversation_id, user_message, ai_response, metadata_json))
                    conn.commit()
                    return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error saving message: {e}")
            raise
    
    def get_conversation_history(self, conversation_id: int, limit: int = 50) -> List[Dict]:
        """Get conversation history
        
        Args:
            conversation_id: ID of conversation
            limit: Max messages to retrieve
            
        Returns:
            List of message dicts
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE conversation_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (conversation_id, limit))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Error retrieving history: {e}")
            return []
    
    def create_conversation(self, user_id: int, title: Optional[str] = None) -> int:
        """Create a new conversation
        
        Args:
            user_id: ID of user
            title: Optional conversation title
            
        Returns:
            Conversation ID
        """
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'INSERT INTO conversations (user_id, title) VALUES (?, ?)',
                        (user_id, title)
                    )
                    conn.commit()
                    return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error creating conversation: {e}")
            raise
    
    def save_memory(self, key: str, value: Any) -> None:
        """Save item to Codette's memory
        
        Args:
            key: Memory key
            value: Memory value
        """
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    value_json = json.dumps(value)
                    cursor.execute('''
                        INSERT OR REPLACE INTO memory (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    ''', (key, value_json))
                    conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error saving memory: {e}")
            raise
    
    def load_memory(self, key: str) -> Optional[Any]:
        """Load item from Codette's memory
        
        Args:
            key: Memory key
            
        Returns:
            Memory value or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM memory WHERE key = ?', (key,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None
        except sqlite3.Error as e:
            logger.error(f"Error loading memory: {e}")
            return None
    
    def get_all_memory(self) -> Dict[str, Any]:
        """Get all memory items
        
        Returns:
            Dictionary of all memory
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT key, value FROM memory')
                rows = cursor.fetchall()
                return {key: json.loads(value) for key, value in rows}
        except sqlite3.Error as e:
            logger.error(f"Error loading all memory: {e}")
            return {}
    
    def clear_memory(self) -> None:
        """Clear all memory"""
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM memory')
                    conn.commit()
                    logger.info("Memory cleared")
        except sqlite3.Error as e:
            logger.error(f"Error clearing memory: {e}")
    
    def export_user_data(self, user_id: int) -> Dict[str, Any]:
        """Export all data for a user
        
        Args:
            user_id: ID of user
            
        Returns:
            Dictionary of user data
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get user info
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                user = dict(cursor.fetchone() or {})
                
                # Get conversations
                cursor.execute('SELECT * FROM conversations WHERE user_id = ?', (user_id,))
                conversations = [dict(row) for row in cursor.fetchall()]
                
                # Get all messages for user's conversations
                messages = []
                for conv in conversations:
                    cursor.execute('SELECT * FROM messages WHERE conversation_id = ?', (conv['id'],))
                    messages.extend([dict(row) for row in cursor.fetchall()])
                
                return {
                    'user': user,
                    'conversations': conversations,
                    'messages': messages
                }
        except sqlite3.Error as e:
            logger.error(f"Error exporting user data: {e}")
            return {}


# Convenience functions
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(db_path: str = "codette_data.db") -> DatabaseManager:
    """Get or create database manager singleton
    
    Args:
        db_path: Path to database file
        
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager


if __name__ == "__main__":
    # Test the database manager
    logging.basicConfig(level=logging.INFO)
    
    db = DatabaseManager("test_codette.db")
    
    # Create test user
    try:
        user_id = db.create_user("test_user", "hashed_password_123")
        print(f"Created user with ID: {user_id}")
    except ValueError as e:
        print(f"User already exists: {e}")
        user = db.get_user("test_user")
        user_id = user['id']
    
    # Create conversation
    conv_id = db.create_conversation(user_id, "Test Conversation")
    print(f"Created conversation with ID: {conv_id}")
    
    # Save messages
    msg_id = db.save_message(conv_id, "Hello Codette", "Hi there!")
    print(f"Saved message with ID: {msg_id}")
    
    # Save memory
    db.save_memory("test_key", {"data": "test_value"})
    memory = db.load_memory("test_key")
    print(f"Loaded memory: {memory}")
    
    # Get history
    history = db.get_conversation_history(conv_id)
    print(f"Conversation history: {history}")

