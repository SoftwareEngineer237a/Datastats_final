"""
app/api/chat_domain.py

Simple rule-based domain answerer for Datastats-specific questions.

This module inspects the user message for keywords defined in
`app.api.chat_config.ALLOWED_KEYWORDS` and returns a canned answer from
`APP_ANSWERS` when applicable. It is intentionally lightweight and local so
the chat API can answer many product-related queries without calling the
external LLM.
"""
from typing import Optional
from app.api import chat_config


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def get_app_answer(message: str) -> Optional[str]:
    """Return a canned answer about Datastats if the message matches any
    known app-related keywords. Otherwise return None.

    Args:
        message: the raw user message

    Returns:
        A string answer when a match is found, else None.
    """
    if not message:
        return None

    normalized = _normalize(message)

    for domain, keywords in chat_config.ALLOWED_KEYWORDS.items():
        for kw in keywords:
            if kw in normalized:
                # If we have a canned answer for this domain, return it
                return chat_config.APP_ANSWERS.get(domain)

    # Fallback: if the message contains the product name 'datastats' anywhere
    # return the app answer. This covers short variations like "what is datastats app".
    if 'datastats' in normalized:
        return chat_config.APP_ANSWERS.get('datastats_app')

    return None
