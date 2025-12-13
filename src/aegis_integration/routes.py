
from flask import jsonify, request
from typing import Dict, Any

def register_aegis_endpoints(app, aegis_bridge):
    @app.route('/api/aegis/analyze', methods=['POST'])
    def analyze_with_aegis():
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({"error": "Missing text parameter"}), 400
                
            analysis = aegis_bridge.enhance_response(
                data.get('prompt', ''),
                data['text']
            )
            return jsonify(analysis)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/aegis/memory', methods=['GET'])
    def get_aegis_memory():
        try:
            memory_state = aegis_bridge.get_memory_state()
            return jsonify(memory_state)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/aegis/graphs', methods=['GET'])
    def get_aegis_graphs():
        try:
            graphs = aegis_bridge.get_analysis_graphs()
            return jsonify(graphs)
        except Exception as e:

            return jsonify({"error": str(e)}), 500