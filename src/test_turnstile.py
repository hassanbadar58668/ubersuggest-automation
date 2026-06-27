import requests
import yaml
import json

def test_login():
    print("🚀 بدء اختبار تسجيل الدخول عبر API...")

    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    accounts = config.get('accounts', [])
    if not accounts:
        print("❌ مفيش حسابات")
        return

    account = accounts[0]
    email = account.get('email', '').strip()
    password = account.get('password', '').strip()

    print(f"📧 {email}")
    print(f"🔑 {password}")

    url = "https://app.neilpatel.com/api/login"

    payload = {
        "email": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📦 Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if data.get('user'):
                print("✅ تسجيل الدخول ناجح!")
                # حفظ النتيجة
                with open("login_result.json", "w") as f:
                    json.dump(data, f, indent=2)
            else:
                print("❌ فشل تسجيل الدخول: بيانات غير صحيحة أو مرفوضة")
        else:
            print(f"❌ فشل الطلب: {response.status_code}")

    except Exception as e:
        print(f"💥 خطأ: {e}")

if __name__ == "__main__":
    test_login()
