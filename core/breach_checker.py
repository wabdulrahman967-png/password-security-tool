import hashlib
import requests
from typing import Tuple, Optional, Dict
from datetime import datetime

class BreachChecker:
    """Check passwords against Have I Been Pwned database"""
    
    def __init__(self):
        self.api_url = "https://api.pwnedpasswords.com/range/"
        self.timeout = 10
        self.cache = {}  # Simple cache for performance
    
    def check_password(self, password: str) -> Tuple[Optional[bool], Optional[int]]:
        """
        Check if password has been breached using k-Anonymity
        
        Returns:
            (is_breached, count) or (None, error_message)
        """
        # Check cache first
        if password in self.cache:
            return self.cache[password]
        
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        try:
            response = requests.get(
                f"{self.api_url}{prefix}",
                timeout=self.timeout,
                headers={'User-Agent': 'PasswordSecurityTool/1.0'}
            )
            
            if response.status_code == 200:
                hashes = (line.split(':') for line in response.text.splitlines())
                for h, count in hashes:
                    if h == suffix:
                        result = (True, int(count))
                        self.cache[password] = result
                        return result
                result = (False, 0)
                self.cache[password] = result
                return result
            else:
                return (None, f"API Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            return (None, f"Connection Error: {str(e)}")
    
    def get_breach_details(self, email: str) -> Dict:
        """
        Get detailed breach information for an email
        Requires: API key from haveibeenpwned.com
        """
        # Note: Full implementation would require API key
        # This is a placeholder for the feature
        return {
            'available': False,
            'message': 'This feature requires an API key. Visit haveibeenpwned.com'
        }