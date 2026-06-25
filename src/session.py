"""
إدارة الجلسات - تخزين واسترجاع Cookies و Tokens
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SessionManager:
    """مدير الجلسات - يخزن ويسترجع بيانات الجلسة لكل حساب"""
    
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def get_session_file(self, email: str) -> Path:
        """مسار ملف الجلسة للحساب"""
        # ننظف الإيميل عشان يبقى اسم ملف صالح
        safe_email = email.replace("@", "_at_").replace(".", "_")
        return self.sessions_dir / f"{safe_email}.json"
    
    def save_session(self, email: str, cookies: Dict, headers: Dict = None, extra: Dict = None):
        """حفظ جلسة الحساب"""
        session_file = self.get_session_file(email)
        
        session_data = {
            "email": email,
            "cookies": cookies,
            "headers": headers or {},
            "extra": extra or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return session_data
    
    def load_session(self, email: str) -> Optional[Dict]:
        """تحميل جلسة الحساب"""
        session_file = self.get_session_file(email)
        
        if not session_file.exists():
            return None
        
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def is_valid(self, email: str, max_age_hours: int = 24) -> bool:
        """التحقق من صلاحية الجلسة"""
        session = self.load_session(email)
        if not session:
            return False
        
        created_at = datetime.fromisoformat(session.get("created_at", "2000-01-01T00:00:00"))
        age = datetime.now() - created_at
        
        return age < timedelta(hours=max_age_hours)
    
    def delete_session(self, email: str) -> bool:
        """حذف جلسة الحساب"""
        session_file = self.get_session_file(email)
        if session_file.exists():
            session_file.unlink()
            return True
        return False
    
    def list_sessions(self) -> list:
        """قائمة بجميع الجلسات المحفوظة"""
        sessions = []
        for file in self.sessions_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        "email": data.get("email", file.stem),
                        "created_at": data.get("created_at"),
                        "file": file.name
                    })
            except:
                pass
        return sessions

# دالة مساعدة للحصول على مدير الجلسات
def get_session_manager() -> SessionManager:
    return SessionManager()
