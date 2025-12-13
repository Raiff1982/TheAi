#!/usr/bin/env python3
"""
Codette Web Interface
Flask-based web server for the Codette AI framework
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Import main application
from main import get_app, CodetteWebApplication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
web_app = Flask(__name__)
web_app.secret_key = "codette_secret_key_2025"
CORS(web_app)

# Global Codette application instance
codette_app: CodetteWebApplication = None

@web_app.before_first_request
def initialize_codette():
    """Initialize Codette systems before first request"""
    global codette_app
    try:
        codette_app = get_app()
        logger.info("Codette systems initialized for web interface")
    except Exception as e:
        logger.error(f"Failed to initialize Codette: {e}")

@web_app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@web_app.route('/api/query', methods=['POST'])
def api_query():
    """API endpoint for processing queries"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'web_user')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Process query asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                codette_app.process_query(query, user_id)
            )
            return jsonify(response)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        return jsonify({"error": str(e)}), 500

@web_app.route('/api/quantum-simulation', methods=['POST'])
def api_quantum_simulation():
    """API endpoint for running quantum simulations"""
    try:
        data = request.get_json()
        cores = data.get('cores', 4)
        
        if cores > 16:  # Safety limit
            cores = 16
        
        results = codette_app.run_quantum_simulation(cores)
        
        return jsonify({
            "status": "success",
            "cores_used": cores,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Quantum simulation error: {e}")
        return jsonify({"error": str(e)}), 500

@web_app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            health = loop.run_until_complete(
                codette_app.health_monitor.check_status()
            )
            return jsonify({
                "status": "healthy",
                "metrics": health,
                "timestamp": datetime.now().isoformat()
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({"error": str(e)}), 500

@web_app.route('/api/analyze-identity', methods=['POST'])
def api_analyze_identity():
    """API endpoint for fractal identity analysis"""
    try:
        data = request.get_json()
        
        # Default example data if not provided
        micro_generations = data.get('micro_generations', [
            {"update": "Initial state", "timestamp": "2025-01-01T00:00:00Z"},
            {"update": "State change 1", "timestamp": "2025-01-02T00:00:00Z"}
        ])
        
        informational_states = data.get('informational_states', [
            {"state_id": "state_1", "data": "Sample data 1"},
            {"state_id": "state_2", "data": "Sample data 2"}
        ])
        
        perspectives = data.get('perspectives', ["Quantum", "Classical", "Ethical"])
        
        results = codette_app.analyze_identity_fractal(
            micro_generations,
            informational_states,
            perspectives
        )
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Identity analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@web_app.route('/dashboard')
def dashboard():
    """Codette dashboard page"""
    return render_template('dashboard.html')

@web_app.route('/quantum')
def quantum():
    """Quantum simulation interface"""
    return render_template('quantum.html')

@web_app.route('/cognitive')
def cognitive():
    """Cognitive processing interface"""
    return render_template('cognitive.html')

if __name__ == "__main__":
    # Initialize Codette systems
    initialize_codette()
    
    # Run the web application
    web_app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )