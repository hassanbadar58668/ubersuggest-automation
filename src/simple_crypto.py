"""
تشفير بسيط باستخدام base64 (بديل عن cryptography للمعالج 32-bit)
"""

import base64
import json

class SimpleCrypto:
    @staticmethod
    def encrypt(text: str) -> str:
        """تشفير بسيط"""
        return base64.b64encode(text.encode()).decode()
    
    @staticmethod
    def decrypt(encoded: str) -> str:
        """فك تشفير بسيط"""
        return base64.b64decode(encoded.encode()).decode()
    
    @staticmethod
    def encrypt_account(email: str, password: str) -> dict:
        return {
            "email": SimpleCrypto.encrypt(email),
            "password": SimpleCrypto.encrypt(password)
        }
    
    @staticmethod
    def decrypt_account(data: dict) -> tuple:
        return (
            SimpleCrypto.decrypt(data["email"]),
            SimpleCrypto.decrypt(data["password"])
        )

# دالة مساعدة
def get_crypto():
    return SimpleCrypto()
