from flask import Flask, request, jsonify, send_from_directory
import os
from nlp_engine.intent_classifier import classify_intent, detect_context, get_predefined_response
from nlp_engine.ai_fallback import get_ai_fallback_response

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Serve the main index.html file
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

# Chat API endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data['message']
    last_intent = data.get('last_intent')
    
    # 1. Classify the intent and detect context (language, region)
    intent = classify_intent(user_message, last_intent)
    language, region = detect_context(user_message)
    
    # 2. Try to get a predefined response
    if intent != "unknown":
        response_text = get_predefined_response(intent, language, region)
        source = "rule_based"
    else:
        # 3. Fallback to AI if unknown
        response_text = get_ai_fallback_response(user_message, language, region, last_intent)
        source = "ai_fallback"

    return jsonify({
        'response': response_text,
        'intent': intent,
        'language': language,
        'region': region,
        'source': source
    })

if __name__ == '__main__':
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    app.run(debug=True, port=5000)
