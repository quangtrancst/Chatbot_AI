from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import generate_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('chatbot_server.log'),
                        logging.StreamHandler()
                    ])

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Validate JSON input
        if not request.is_json:
            logging.error("Invalid request: Not a JSON")
            return jsonify({"error": "Invalid request. JSON required."}), 400
        
        data = request.get_json()
        user_input = data.get("message", "").strip()
        
        # Validate message
        if not user_input:
            logging.warning("No message provided")
            return jsonify({"error": "No message provided"}), 400

        # Generate response
        logging.info(f"Received input: {user_input}")
        response = generate_response(user_input)
        
        logging.info(f"Sent response: {response}")
        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == "__main__":
    logging.info("Server starting on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)