"""
نظام التسجيل المتقدم
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

class LoggerManager:
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
        
        # إنشاء مجلد logs
        Path("logs").mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("ubersuggest")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # معالج الطرفية
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))
        self.logger.addHandler(console)
        
        # معالج الملف
        file_handler = logging.FileHandler(
            f"logs/ubersuggest_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
    
    def get_logger(self, name: str = None):
        if name:
            return self.logger.getChild(name)
        return self.logger

def get_logger(name: str = None):
    return LoggerManager().get_logger(name)
