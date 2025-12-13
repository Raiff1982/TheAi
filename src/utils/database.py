import sqlite3
from typing import Optional, List, Dict, Any
import logging
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class Database:
    """Database manager for Codette"""
    def __init__(self, db_path: str = "codette.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.connection = None
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database and create tables if they don't exist"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

            # Create tables
            with self.connection:
                # Users table
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Interactions table
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        query TEXT NOT NULL,
                        response TEXT NOT NULL,
                        feedback TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')

                # Quantum states table
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS quantum_states (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        interaction_id INTEGER NOT NULL,
                        state_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (interaction_id) REFERENCES interactions(id)
                    )
                ''')

                # User profiles table
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS user_profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE NOT NULL,
                        preferences TEXT,
                        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')

            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            return dict(user) if user else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None

    def create_user(self, username: str) -> Optional[int]:
        """Create a new user"""
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    def log_interaction(self, user_id: int, query: str, response: str):
        """Log a user interaction"""
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO interactions (user_id, query, response) VALUES (?, ?, ?)",
                    (user_id, query, response)
                )
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
            return None

    def get_latest_feedback(self, user_id: int) -> Optional[str]:
        """Get the most recent feedback for a user"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT feedback
                FROM interactions
                WHERE user_id = ? AND feedback IS NOT NULL
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (user_id,)
            )
            result = cursor.fetchone()
            return result['feedback'] if result else None
        except Exception as e:
            logger.error(f"Error getting feedback: {e}")
            return None

    def save_quantum_state(self, interaction_id: int, state_data: Dict[str, Any]):
        """Save quantum state data"""
        try:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO quantum_states (interaction_id, state_data) VALUES (?, ?)",
                    (interaction_id, json.dumps(state_data))
                )
        except Exception as e:
            logger.error(f"Error saving quantum state: {e}")

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile data"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
            profile = cursor.fetchone()
            if profile:
                profile_dict = dict(profile)
                profile_dict['preferences'] = json.loads(profile_dict['preferences'])
                return profile_dict
            return None
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None

    def update_user_profile(self, user_id: int, preferences: Dict[str, Any]):
        """Update user profile preferences"""
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO user_profiles (user_id, preferences)
                    VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        preferences = excluded.preferences,
                        last_active = CURRENT_TIMESTAMP
                    """,
                    (user_id, json.dumps(preferences))
                )
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()