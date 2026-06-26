#!/usr/bin/env python3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from session import get_session_manager
from logger import get_logger
import undetected_chromedriver as uc

logger = get_logger("cloud")

class CloudAutomation:
    def __init__(self):
        self.config = get_config()
        self.session_mgr = get_session_manager()
        self.driver = None
        self.stats = {"total": 0, "success": 0, "failed": 0, "skipped": 0}
        logger.info("🚀 بدء التشغيل")

    def setup_driver(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = uc.Chrome(options=options)
            logger.info("✅ المتصفح جاهز")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إعداد المتصفح: {e}")
            return False

    def run(self):
        if not self.setup_driver():
            return
        logger.info("✅ النظام شغال")
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    CloudAutomation().run()
