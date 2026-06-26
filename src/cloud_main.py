#!/usr/bin/env python3
import sys
import time
import json
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from session import get_session_manager
from logger import get_logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = get_logger("cloud")

class CloudAutomation:
    def __init__(self):
        self.config = get_config()
        self.session_mgr = get_session_manager()
        self.driver = None
        self.stats = {"total": 0, "success": 0, "failed": 0, "skipped": 0}
        logger.info("🚀 بدء تشغيل نظام الأتمتة السحابي")

    def setup_driver(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("✅ المتصفح جاهز")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إعداد المتصفح: {e}")
            return False

    def load_accounts(self):
        return self.config.get('accounts', [])

    def login(self, email: str, password: str) -> bool:
        try:
            logger.info(f"🔑 محاولة تسجيل الدخول: {email}")
            self.driver.get("https://app.neilpatel.com/en/login")
            time.sleep(3)
            
            email_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.clear()
            email_input.send_keys(email)
            
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(password)
            
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)
            
            if "dashboard" in self.driver.current_url or "app" in self.driver.current_url:
                logger.info(f"✅ تسجيل الدخول ناجح: {email}")
                cookies = self.driver.get_cookies()
                self.session_mgr.save_session(email, cookies)
                return True
            else:
                logger.warning(f"⚠️ فشل تسجيل الدخول: {email}")
                return False
        except Exception as e:
            logger.error(f"❌ خطأ في تسجيل الدخول {email}: {e}")
            return False

    def run(self):
        if not self.setup_driver():
            return
        
        try:
            accounts = self.load_accounts()
            self.stats['total'] = len(accounts)
            
            for idx, account in enumerate(accounts, 1):
                email = account.get('email')
                password = account.get('password')
                
                if not email or not password or not account.get('enabled', True):
                    self.stats['skipped'] += 1
                    continue
                
                logger.info(f"📌 معالجة الحساب {idx}/{len(accounts)}")
                
                if self.session_mgr.is_valid(email):
                    logger.info(f"♻️ جلسة صالحة لـ {email}")
                    self.stats['success'] += 1
                else:
                    if self.login(email, password):
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                
                time.sleep(5)
            
        finally:
            if self.driver:
                self.driver.quit()
        
        logger.info("=" * 50)
        logger.info("📊 الإحصائيات:")
        logger.info(f"   ✅ نجح: {self.stats['success']}")
        logger.info(f"   ❌ فشل: {self.stats['failed']}")
        logger.info(f"   ⏭️ متخطي: {self.stats['skipped']}")
        logger.info(f"   📌 المجموع: {self.stats['total']}")

if __name__ == "__main__":
    CloudAutomation().run()
