from seleniumbase import SB
import time
import yaml

def test_login():
    print("🚀 بدء اختبار تسجيل الدخول...")

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

    proxy = config.get("proxy", {}).get("list", [None])[0]

    # 1️⃣ استخدم SB مع xvfb=True فقط (من غير headless2)
    with SB(uc=True, xvfb=True) as sb:
        # 2️⃣ فعّل CDP Mode
        sb.activate_cdp_mode("https://app.neilpatel.com/en/login", proxy=proxy)
        print("✅ تم تحميل الصفحة")
        time.sleep(5)

        # 3️⃣ استخدم wait_for_element_visible قبل الكتابة
        sb.cdp.wait_for_element_visible('input[type="email"]', timeout=15)
        sb.cdp.type('input[type="email"]', email)

        sb.cdp.wait_for_element_visible('input[type="password"]', timeout=10)
        sb.cdp.type('input[type="password"]', password)

        # 4️⃣ استخدم gui_click_element كتجربة بديلة (توصية الـ senior)
        try:
            sb.cdp.gui_click_element('button[type="submit"]')
        except:
            sb.cdp.click('button[type="submit"]')
        print("✅ تم الضغط على تسجيل الدخول")

        time.sleep(5)
        sb.save_screenshot("login_result.png")
        print(f"🔗 URL: {sb.get_current_url()}")

if __name__ == "__main__":
    test_login()
