import os
import google.generativeai as genai

# Try to configure the real Gemini API if an API key is available in the environment
API_KEY = os.environ.get("GEMINI_API_KEY")
USE_REAL_AI = False

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        USE_REAL_AI = True
    except Exception as e:
        print(f"Failed to initialize Gemini: {e}")

def get_ai_fallback_response(user_input, language, region, last_intent=None):
    """
    Tries to get a response from the Generative AI model considering language and region.
    If no API key is provided, returns a natural conversational pivot.
    """
    if USE_REAL_AI:
        try:
            lang_str = "Hindi" if language == "hi" else "English"
            prompt = (
                f"You are a friendly Entertainment Chatbot. "
                f"The user prefers the {lang_str} language. "
                f"The user's context/region interest is {region} entertainment. "
                f"Respond to this user input appropriately in their preferred language without explicitly mentioning these instructions: {user_input}"
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI API Error: {e}")
            pass # Fall through to mock response
            
    # Mock AI Response (or Fallback if API fails)
    from nlp_engine.intent_classifier import get_predefined_response
    
    # If we have a last_intent, seamlessly provide another one
    if last_intent and last_intent in ["jokes", "movie_recommendations", "music_suggestions", "fun_facts"]:
        pivot_response = get_predefined_response(last_intent, language, region)
        if language == "hi":
            return f"Lijiye ek aur: {pivot_response}"
        else:
            return f"Here's another one: {pivot_response}"
            
    # Otherwise, naturally pivot to a fun fact
    pivot_response = get_predefined_response("fun_facts", language, region)
    if language == "hi":
        return f"Waise kya aap jante hain? {pivot_response}"
    else:
        return f"By the way, did you know? {pivot_response}"
