"""
إدارة ملف التكوين config.yaml
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional

class ConfigManager:
    """مدير التكوين - يقرأ ويوفر الوصول لإعدادات المشروع"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._config = {}
        self.config_path = Path("config/config.yaml")
        self._load()
    
    def _load(self):
        """تحميل التكوين من ملف YAML"""
        if not self.config_path.exists():
            print(f"⚠️ ملف التكوين غير موجود: {self.config_path}")
            self._config = self._get_default_config()
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ خطأ في قراءة ملف التكوين: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """إعدادات افتراضية"""
        return {
            "project": {"name": "Ubersuggest Automation", "version": "1.0.0"},
            "webdroid": {"host": "127.0.0.1", "port": 8765, "timeout": 30},
            "ubersuggest": {"base_url": "https://app.neilpatel.com", "timeout": 30, "max_retries": 3},
            "rate_limiting": {"enabled": True, "requests_per_minute": 5},
            "accounts": []
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """الحصول على قيمة من التكوين باستخدام مفتاح نقطي (مثل: webdroid.host)"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """تحديث قيمة في التكوين"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def reload(self):
        """إعادة تحميل التكوين من الملف"""
        self._load()
    
    @property
    def all(self) -> dict:
        """جميع إعدادات التكوين"""
        return self._config

# دالة مساعدة
def get_config() -> ConfigManager:
    return ConfigManager()
