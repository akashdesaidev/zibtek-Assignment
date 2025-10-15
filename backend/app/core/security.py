import re
from typing import Tuple


class PromptInjectionDetector:
    """Detect and prevent prompt injection attempts"""
    
    # Common prompt injection patterns
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|prior)\s+instructions",
        r"you\s+are\s+now",
        r"new\s+instructions",
        r"system\s*:",
        r"assistant\s*:",
        r"forget\s+(everything|all|previous)",
        r"disregard\s+(previous|all|prior)",
        r"override\s+instructions",
        r"your\s+new\s+role",
        r"act\s+as\s+(?!a\s+helpful)",
        r"pretend\s+to\s+be",
        r"simulate\s+being",
        r"hypothetically",
        r"in\s+this\s+scenario",
        r"jailbreak",
        r"DAN\s+mode",
    ]
    
    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.INJECTION_PATTERNS]
    
    def detect(self, user_input: str) -> Tuple[bool, str]:
        """
        Detect if user input contains prompt injection attempts
        
        Args:
            user_input: The user's message
            
        Returns:
            Tuple of (is_injection, message)
        """
        for pattern in self.patterns:
            if pattern.search(user_input):
                return True, "I apologize, but I can only answer questions related to Zibtek. Please rephrase your question."
        
        return False, ""
    
    def sanitize(self, user_input: str) -> str:
        """
        Sanitize user input by removing potentially harmful patterns
        
        Args:
            user_input: The user's message
            
        Returns:
            Sanitized input
        """
        # Remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', user_input).strip()
        
        # Remove special characters that might be used for injection
        sanitized = re.sub(r'[<>{}]', '', sanitized)
        
        return sanitized


# Global instance
prompt_injection_detector = PromptInjectionDetector()


