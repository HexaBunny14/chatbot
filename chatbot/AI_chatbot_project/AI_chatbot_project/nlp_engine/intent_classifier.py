import re
import json
import os
import random

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

INTENT_PATTERNS = {
    "greetings": r'\b(hi|hello|hey|greetings|howdy|morning|afternoon|evening|namaste|pranam|kya haal|kaise ho)\b',
    "movie_recommendations": r'\b(movie|movies|film|films|watch|cinema|recommend a movie|picture|dekha|dekhu|dekhna)\b',
    "jokes": r'\b(joke|jokes|funny|laugh|humor|chutkula|hasna|hasi|mazak)\b',
    "music_suggestions": r'\b(music|song|songs|listen|playlist|track|artist|gana|gaane|sangeet|sunna|sunao)\b',
    "trending_topics": r'\b(trending|trend|news|latest|topics|popular|happening|kya chal raha|naya kya)\b',
    "fun_facts": r'\b(fact|facts|trivia|did you know|fun fact|interesting|kuch naya|kuch rochak|rochak|jankari)\b',
    "laughter": r'\b(haha+|lol|lmao|hehe+|rofl)\b',
    "agreement": r'\b(ok|okay|okayy|okkay|cool|nice|awesome|great|good|yes|yeah|yep|badhiya|sahi|achha|hmm|hmmm)\b',
    "gratitude": r'\b(thanks|thank you|thx|shukriya|dhanyawad|thankyou)\b',
    "follow_up": r'\b(another|one more|aur ek|ek aur|another one|more|ek aur)\b'
}

def detect_context(user_input):
    """Detects language and region context from user input."""
    input_lower = user_input.lower()
    
    # 1. Language Detection
    language = "en"
    # Check for Devanagari script (Hindi characters)
    if re.search(r'[\u0900-\u097F]', user_input):
        language = "hi"
    else:
        # Check for common Hinglish words
        hinglish_keywords = r'\b(hai|kya|kaise|batao|mujhe|mera|karo|nahi|haan|kaun|kab|kaha|sunao|dekha)\b'
        if re.search(hinglish_keywords, input_lower):
            language = "hi"  # Treat Hinglish as Hindi preference for responses
            
    # 2. Region Detection
    region = "mixed"
    indian_keywords = r'\b(bollywood|tollywood|kollywood|indian|desi|hindi movie|south indian)\b'
    international_keywords = r'\b(hollywood|english movie|international|american|british|foreign)\b'
    
    has_indian = re.search(indian_keywords, input_lower)
    has_intl = re.search(international_keywords, input_lower)
    
    if has_indian and not has_intl:
        region = "indian"
    elif has_intl and not has_indian:
        region = "international"
    elif language == "hi" and not has_intl:
        # Default to Indian if language is Hindi and no explicit international request
        region = "indian"
        
    return language, region

def classify_intent(user_input, last_intent=None):
    """Classifies user input into a predefined intent using regex."""
    user_input = user_input.lower()
    
    # Check for follow-up first
    if re.search(INTENT_PATTERNS["follow_up"], user_input) and last_intent:
        return last_intent
        
    for intent, pattern in INTENT_PATTERNS.items():
        if intent == "follow_up":
            continue
        if re.search(pattern, user_input):
            return intent
    return "unknown"

def get_predefined_response(intent, language, region):
    """Returns a random response for the matched intent based on language and region."""
    if intent in knowledge_base:
        lang_responses = knowledge_base[intent].get(language) or knowledge_base[intent].get("en")
        if not lang_responses:
            return None
            
        region_responses = lang_responses.get(region)
        
        # Fallbacks for region if not found
        if not region_responses:
            region_responses = lang_responses.get("mixed")
        if not region_responses:
            # Pick any available region if even mixed is missing
            region_responses = list(lang_responses.values())[0]
            
        return random.choice(region_responses) if region_responses else None
    return None
