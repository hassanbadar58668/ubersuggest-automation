#!/usr/bin/env python3
"""
Ubersuggest Automation - Main Entry Point
"""

import sys
from pathlib import Path

# إضافة مجلد src إلى مسار Python
sys.path.insert(0, str(Path(__file__).parent))

from config import ConfigManager, get_config
from session import SessionManager, get_session_manager
from simple_crypto import SimpleCrypto, get_crypto

def main():
    print("=" * 50)
    print("🚀 Ubersuggest Automation System")
    print("=" * 50)
    
    # 1. تحميل التكوين
    config = get_config()
    print(f"📁 Project: {config.get('project.name')} v{config.get('project.version')}")
    print(f"🌐 WebDroid: {config.get('webdroid.host')}:{config.get('webdroid.port')}")
    
    # 2. إدارة الجلسات
    session_mgr = get_session_manager()
    print(f"📂 Sessions Dir: {session_mgr.sessions_dir}")
    
    # 3. التشفير
    crypto = get_crypto()
    test_email = "test@example.com"
    encrypted = crypto.encrypt(test_email)
    decrypted = crypto.decrypt(encrypted)
    print(f"🔐 Encryption Test: {test_email} → {encrypted} → {decrypted}")
    
    # 4. تحميل الحسابات من التكوين
    accounts = config.get('accounts', [])
    print(f"👥 Total Accounts: {len(accounts)}")
    
    for acc in accounts:
        print(f"  - {acc.get('email')} (enabled: {acc.get('enabled', True)})")
    
    print("=" * 50)
    print("✅ System ready!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
