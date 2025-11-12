import os
from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI
from dotenv import load_dotenv
from app.api.chat_config import (
    ALLOWED_KEYWORDS, 
    CLASSIFICATION_PROMPT, 
    RESTRICTION_MESSAGE,
    ENHANCED_SYSTEM_CONTEXT
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create Blueprint
chat_bp = Blueprint("chat", __name__)

# Rate limiter (basic protection)
limiter = Limiter(get_remote_address, default_limits=["10 per minute", "100 per day"])


class DomainValidator:
    """Class to handle domain validation logic"""
    
    @staticmethod
    def contains_allowed_keywords(message):
        """Quick keyword-based check for allowed domains"""
        message_lower = message.lower()
        
        for domain, keywords in ALLOWED_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return True
        return False
    
    @staticmethod
    def classify_with_openai(message):
        """Use OpenAI to classify question domain"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CLASSIFICATION_PROMPT},
                    {"role": "user", "content": message}
                ],
                max_tokens=10,
                temperature=0.1  # Low temperature for consistent classification
            )
            
            classification = response.choices[0].message.content.strip().upper()
            return classification == "ALLOWED"
            
        except Exception as e:
            current_app.logger.error(f"Classification error: {e}")
            # If classification fails, fall back to keyword check
            return DomainValidator.contains_allowed_keywords(message)
    
    @classmethod
    def is_question_allowed(cls, message):
        """Main validation function combining both methods"""
        # First, try quick keyword check
        if cls.contains_allowed_keywords(message):
            return True
        
        # If no keywords found, use OpenAI classification
        return cls.classify_with_openai(message)


@chat_bp.route("/api/chat", methods=["POST"])
@limiter.limit("5 per minute")  # each user: max 5 messages/min
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()
        context = data.get("context", ENHANCED_SYSTEM_CONTEXT)

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Validate if question is within allowed domains
        if not DomainValidator.is_question_allowed(user_message):
            return jsonify({"reply": RESTRICTION_MESSAGE})

        # Build the conversation prompt with enhanced context
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content

        return jsonify({"reply": ai_reply})

    except Exception as e:
        current_app.logger.error(f"Chat API error: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500