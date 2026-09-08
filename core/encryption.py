class CaesarCipher:
    """Simple Caesar cipher for educational purposes"""
    
    @staticmethod
    def encrypt(text: str, shift: int = 3) -> str:
        """Encrypt text using Caesar cipher with given shift"""
        result = []
        for char in text:
            if char.isalpha():
                shift_amount = shift % 26
                ascii_offset = 65 if char.isupper() else 97
                shifted = ord(char) + shift_amount
                if shifted > ascii_offset + 25:
                    shifted -= 26
                result.append(chr(shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decrypt(text: str, shift: int = 3) -> str:
        """Decrypt text using Caesar cipher with given shift"""
        return CaesarCipher.encrypt(text, -shift)
    
    @staticmethod
    def brute_force(text: str) -> list:
        """Attempt all 25 possible shifts to decrypt"""
        results = []
        for shift in range(1, 26):
            results.append({
                'shift': shift,
                'text': CaesarCipher.encrypt(text, -shift)
            })
        return results 