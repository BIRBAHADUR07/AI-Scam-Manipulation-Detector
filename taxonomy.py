from enum import Enum

class ScamType(Enum):
    OTP_PHISHING = "OTP_PHISHING"
    INVESTMENT_SCAM = "INVESTMENT_SCAM"
    ROMANCE_SCAM = "ROMANCE_SCAM"
    URGENCY_MANIPULATION = "URGENCY_MANIPULATION"
    AUTHORITY_IMPERSONATION = "AUTHORITY_IMPERSONATION"
    LINK_PHISHING = "LINK_PHISHING"
    EMOTIONAL_COERCION = "EMOTIONAL_COERCION"
    NORMAL = "NORMAL"

def classify_taxonomy_rule_based(message: str) -> str:
    message = message.lower()
    if any(word in message for word in ["otp", "verify account", "verification code"]):
        return ScamType.OTP_PHISHING.value
    if any(word in message for word in ["invest", "return", "crypto", "profit", "2x"]):
        return ScamType.INVESTMENT_SCAM.value
    if any(word in message for word in ["care about me", "love", "gift card", "baby"]):
        if "money" in message or "gift" in message:
            return ScamType.ROMANCE_SCAM.value
    
    # Emotional Coercion / Guilt Tripping
    if any(word in message for word in ["if you are so", "why not you", "do it yourself", "you don't care"]):
        return ScamType.EMOTIONAL_COERCION.value
    if any(word in message for word in ["lost my", "need money", "buy lunch", "some money please", "help me out"]):
        return ScamType.EMOTIONAL_COERCION.value

    if any(word in message for word in ["urgent", "emergency", "immediately", "quick"]):
        if "money" in message or "send" in message:
            return ScamType.URGENCY_MANIPULATION.value
    if any(word in message for word in ["police", "bank", "irs", "tax", "arrest", "suspend"]):
        return ScamType.AUTHORITY_IMPERSONATION.value
    if any(word in message for word in ["click this link", "http", "www", "log in here"]):
        return ScamType.LINK_PHISHING.value
    
    return ScamType.NORMAL.value
