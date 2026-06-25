"""
WebDroid Client - التحكم في متصفح WebDroid عبر HTTP API
"""

import requests
import json
from typing import Optional, Dict, Any
from src.config import get_config

class WebDroidClient:
    """عميل للتحكم في WebDroid"""
    
    def __init__(self, host: str = None, port: int = None):
        config = get_config()
        self.host = host or config.get('webdroid.host', '127.0.0.1')
        self.port = port or config.get('webdroid.port', 8765)
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = config.get('webdroid.timeout', 30)
    
    def _request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Optional[Dict]:
        """إرسال طلب إلى WebDroid"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            if method.upper() == 'GET':
                resp = requests.get(url, timeout=self.timeout)
            elif method.upper() == 'POST':
                resp = requests.post(url, json=data, timeout=self.timeout)
            else:
                return None
            
            if resp.status_code == 200:
                return resp.json()
            return None
        except:
            return None
    
    def ping(self) -> bool:
        """التحقق من أن WebDroid شغال"""
        result = self._request('ping')
        return result is not None
    
    def navigate(self, url: str) -> bool:
        """توجيه المتصفح إلى رابط"""
        result = self._request('navigate', 'POST', {'url': url})
        return result is not None
    
    def get_html(self) -> Optional[str]:
        """الحصول على HTML الصفحة الحالية"""
        result = self._request('html')
        return result.get('html') if result else None
    
    def screenshot(self) -> Optional[str]:
        """التقاط لقطة شاشة (ترجع base64)"""
        result = self._request('screenshot')
        return result.get('screenshot') if result else None

def get_webdroid() -> WebDroidClient:
    return WebDroidClient()
