import re
import math
import string
from typing import Dict


class PasswordStrengthChecker:
    """Advanced password strength analyzer with entropy calculation"""

    def __init__(self):
        self.common_passwords = self._load_common_passwords()

    def _load_common_passwords(self) -> set:
        """Load list of common passwords"""
        return {
            'password', '123456', '123456789', '12345678', '1234567',
            'password1', '12345', '1234567890', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            'sunshine', 'password12', 'iloveyou', 'princess', 'admin123',
            '123123', 'qwertyuiop', 'password1234', 'dragon', 'football',
            'baseball', 'trustno1', 'master', '123321', 'shadow'
        }

    def _calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits (log2 of the true keyspace)"""
        if not password:
            return 0.0

        pool = 0
        if any(c.islower() for c in password):
            pool += 26
        if any(c.isupper() for c in password):
            pool += 26
        if any(c.isdigit() for c in password):
            pool += 10
        special_chars = set(string.punctuation)
        if any(c in special_chars for c in password):
            pool += len(special_chars)
        if any(c not in string.printable for c in password):
            pool += 26

        if pool == 0:
            return 0.0

        return round(len(password) * math.log2(pool), 2)

    def _estimate_crack_time(self, entropy: float) -> str:
        """Rough estimate of offline brute-force crack time, assuming
        ~10 billion guesses/sec on modern GPU hardware."""
        guesses_per_second = 10_000_000_000
        seconds = (2 ** entropy) / guesses_per_second

        periods = [
            ("second", 60),
            ("minute", 60),
            ("hour", 24),
            ("day", 365),
            ("year", 100),
        ]
        value = seconds
        for name, size in periods:
            if value < size:
                return f"{value:.1f} {name}s"
            value /= size
        return "centuries"

    def check_strength(self, password: str) -> Dict:
        """Evaluate password strength with detailed analysis"""
        criteria = {
            'length': False,
            'uppercase': False,
            'lowercase': False,
            'digits': False,
            'special': False,
            'no_common': False,
            'no_repeating': False,
        }
        feedback = []
        score = 0
        entropy = self._calculate_entropy(password)

        if len(password) >= 12:
            criteria['length'] = True
            score += 2
        elif len(password) >= 8:
            criteria['length'] = True
            score += 1
        else:
            feedback.append("❌ Password must be at least 8 characters (12+ recommended)")

        if any(c.isupper() for c in password):
            criteria['uppercase'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one uppercase letter")

        if any(c.islower() for c in password):
            criteria['lowercase'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one lowercase letter")

        if any(c.isdigit() for c in password):
            criteria['digits'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one number")

        special_chars = set(string.punctuation)
        if any(c in special_chars for c in password):
            criteria['special'] = True
            score += 1
        else:
            feedback.append("❌ Include at least one special character (!@#$%...)")

        if password.lower() not in self.common_passwords:
            criteria['no_common'] = True
            score += 1
        else:
            feedback.append("⚠️ This is a commonly used password")

        if not re.search(r'(.)\1{2,}', password):
            criteria['no_repeating'] = True
            score += 1
        else:
            feedback.append("⚠️ Avoid repeated characters (e.g., 'aaa')")

        if score <= 3:
            strength, color = "Weak 🔴", "#f38ba8"
        elif score <= 5:
            strength, color = "Medium 🟡", "#f9e2af"
        elif score <= 7:
            strength, color = "Strong 🟢", "#a6e3a1"
        else:
            strength, color = "Very Strong 💪", "#89b4fa"

        return {
            'score': score,
            'max_score': 8,
            'strength': strength,
            'strength_color': color,
            'entropy': entropy,
            'crack_time': self._estimate_crack_time(entropy),
            'criteria': criteria,
            'feedback': feedback,
            'is_common': password.lower() in self.common_passwords,
        }
