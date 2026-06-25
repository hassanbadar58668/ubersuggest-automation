"""
نظام معالجة الأخطاء المتكامل
"""

class UbersuggestError(Exception):
    """الخطأ الأساسي"""
    def __init__(self, message: str, code: str = "UNKNOWN", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

class AuthenticationError(UbersuggestError):
    """أخطاء تسجيل الدخول"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "AUTH_ERROR", details)

class InvalidCredentialsError(AuthenticationError):
    """بيانات دخول غير صحيحة"""
    def __init__(self, email: str):
        super().__init__(
            f"بيانات الدخول غير صحيحة: {email}",
            {"email": email}
        )
        self.code = "INVALID_CREDENTIALS"

class SessionExpiredError(AuthenticationError):
    """انتهت صلاحية الجلسة"""
    def __init__(self, email: str):
        super().__init__(
            f"انتهت صلاحية الجلسة: {email}",
            {"email": email}
        )
        self.code = "SESSION_EXPIRED"

class NetworkError(UbersuggestError):
    """أخطاء الشبكة"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "NETWORK_ERROR", details)

class RateLimitError(NetworkError):
    """تجاوز حد الطلبات"""
    def __init__(self, retry_after: int = None):
        super().__init__(
            "تم تجاوز حد الطلبات",
            {"retry_after": retry_after}
        )
        self.code = "RATE_LIMIT"

class WebDroidError(UbersuggestError):
    """أخطاء WebDroid"""
    def __init__(self, message: str):
        super().__init__(f"خطأ في WebDroid: {message}", "WEB_DROID_ERROR")

def handle_error(error: UbersuggestError) -> dict:
    """معالجة موحدة للأخطاء"""
    result = {
        "should_retry": False,
        "should_skip": False,
        "should_stop": False,
        "message": error.message
    }
    
    if isinstance(error, InvalidCredentialsError):
        result["should_skip"] = True
    elif isinstance(error, SessionExpiredError):
        result["should_retry"] = True
    elif isinstance(error, RateLimitError):
        result["should_retry"] = True
    elif isinstance(error, NetworkError):
        result["should_retry"] = True
    elif isinstance(error, WebDroidError):
        result["should_stop"] = True
    else:
        result["should_stop"] = True
    
    return result
