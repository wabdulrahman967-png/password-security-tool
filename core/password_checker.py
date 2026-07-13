import re
import string
from typing import Dict, List, Tuple

class PasswordStrengthChecker:
    """Advanced password strength analyzer with entropy calculation"""
    
    def __init__(self):
        self.criteria = {
            'length': False,
            'uppercase': False,
            'lowercase': False,
            'digits': False,
            'special': False,
            'no_common': False,
            'no_repeating': False
        }
        self.common_passwords = self._load_common_passwords()
    
    def _load_common_passwords(self) -> set:
        """Load list of common passwords (top 100)"""
        return {
            'password', '123456', '123456789', '12345678', '1234567',
            'password1', '12345', '1234567890', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            'sunshine', 'password12', '123456789', 'iloveyou',
            'princess', 'admin123', '123123', 'qwertyuiop', 'password1234'
        }
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits"""
        char_sets = 0
        if any(c.islower() for c in password):
            char_sets += 26
        if any(c.isupper() for c in password):
            char_sets += 26
        if any(c.isdigit() for c in password):
            char_sets += 10
        special_chars = set(string.punctuation)
        if any(c in special_chars for c in password):
            char_sets += len(special_chars)
        
        if char_sets == 0:
            return 0.0
        
        return len(password) * (char_sets.bit_length() - 1)
    
    def check_strength(self, password: str) -> Dict:
        """Evaluate password strength with detailed analysis"""
        feedback = []
        score = 0
        entropy = self._calculate_entropy(password)
        
        # Criteria 1: Length (minimum 12 chars for strong)
        if len(password) >= 12:
            self.criteria['length'] = True
            score += 2
        elif len(password) >= 8:
            self.criteria['length'] = True
            score += 1
        else:
            feedback.append("❌ Password must be at least 8 characters (12+ recommended)")
        
        # Criteria 2: Uppercase letters
        if any(c.isupper() for c in password):
            self.criteria['uppercase'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one uppercase letter")
        
        # Criteria 3: Lowercase letters
        if any(c.islower() for c in password):
            self.criteria['lowercase'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one lowercase letter")
        
        # Criteria 4: Digits
        if any(c.isdigit() for c in password):
            self.criteria['digits'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one number")
        
        # Criteria 5: Special characters
        special_chars = set(string.punctuation)
        if any(c in special_chars for c in password):
            self.criteria['special'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one special character (!@#$%...)")
        
        # Criteria 6: Not common
        if password.lower() not in self.common_passwords:
            self.criteria['no_common'] = True
            score += 1
        else:
            feedback.append("⚠️ This is a commonly used password")
        
        # Criteria 7: No repeating patterns
        if not re.search(r'(.)\1{2,}', password):  # No 3+ repeated chars
            self.criteria['no_repeating'] = True
            score += 1
        else:
            feedback.append("⚠️ Avoid repeated characters (e.g., 'aaa')")
        
        # Determine strength level
        if score <= 3:
            strength = "Weak 🔴"
            color = "#f38ba8"
        elif score <= 5:
            strength = "Medium 🟡"
            color = "#f9e2af"
        elif score <= 7:
            strength = "Strong 🟢"
            color = "#a6e3a1"
        else:
            strength = "Very Strong 💪"
            color = "#89b4fa"
        
        return {
            'score': score,
            'max_score': 8,
            'strength': strength,
            'strength_color': color,
            'entropy': round(entropy, 2),
            'criteria': self.criteria,
            'feedback': feedback,
            'is_common': password.lower() in self.common_passwords
        }