import secrets
import string


class PasswordGenerator:
    """Cryptographically secure password generator"""

    AMBIGUOUS = set("il1Lo0O")

    @staticmethod
    def generate(
        length: int = 16,
        use_upper: bool = True,
        use_lower: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        avoid_ambiguous: bool = False,
    ) -> str:
        pool = ""
        if use_lower:
            pool += string.ascii_lowercase
        if use_upper:
            pool += string.ascii_uppercase
        if use_digits:
            pool += string.digits
        if use_special:
            pool += string.punctuation

        if not pool:
            raise ValueError("Select at least one character type")

        if avoid_ambiguous:
            pool = "".join(c for c in pool if c not in PasswordGenerator.AMBIGUOUS)

        # Guarantee at least one char from each selected category
        password_chars = []
        categories = []
        if use_lower:
            categories.append(string.ascii_lowercase)
        if use_upper:
            categories.append(string.ascii_uppercase)
        if use_digits:
            categories.append(string.digits)
        if use_special:
            categories.append(string.punctuation)

        for cat in categories:
            if avoid_ambiguous:
                cat = "".join(c for c in cat if c not in PasswordGenerator.AMBIGUOUS)
            if cat:
                password_chars.append(secrets.choice(cat))

        remaining = max(length - len(password_chars), 0)
        password_chars += [secrets.choice(pool) for _ in range(remaining)]

        secrets.SystemRandom().shuffle(password_chars)
        return "".join(password_chars[:length])
