"""
Rate Limiting - التحكم في عدد الطلبات لكل وحدة زمنية
"""

import time
from datetime import datetime, timedelta
from collections import deque
from typing import Optional

class RateLimiter:
    """محدد معدل الطلبات"""
    
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        """
        max_requests: عدد الطلبات المسموح بها في النافذة الزمنية
        time_window: النافذة الزمنية بالثواني (افتراضي 60 ثانية = دقيقة)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def can_make_request(self) -> bool:
        """التحقق من إمكانية إرسال طلب"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        
        # إزالة الطلبات القديمة
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()
        
        return len(self.requests) < self.max_requests
    
    def wait_if_needed(self) -> Optional[float]:
        """
        انتظار إذا كان الحد قد تجاوز
        ترجع وقت الانتظار بالثواني، أو None إذا كان مسموح بالطلب
        """
        if self.can_make_request():
            return None
        
        # حساب وقت الانتظار
        now = datetime.now()
        oldest = self.requests[0] if self.requests else now
        wait_time = (oldest + timedelta(seconds=self.time_window) - now).total_seconds()
        return max(0, wait_time)
    
    def record_request(self):
        """تسجيل طلب جديد"""
        self.requests.append(datetime.now())
    
    def get_remaining(self) -> int:
        """عدد الطلبات المتبقية في النافذة الحالية"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()
        
        return max(0, self.max_requests - len(self.requests))

def get_rate_limiter() -> RateLimiter:
    return RateLimiter()
