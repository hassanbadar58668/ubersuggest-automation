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
    
    proxy = config.get("proxy", {}).get("list", [None])[0]
    
    with SB(uc=True, xvfb=True, headless2=True) as sb:
        sb.activate_cdp_mode("https://app.neilpatel.com/en/login", proxy=proxy)
        print("✅ تم تحميل الصفحة")
        time.sleep(3)
        
        sb.cdp.type('#email', email)
        sb.cdp.type('#password', password)
        sb.cdp.click('button[type="submit"]')
        print("✅ تم الضغط على تسجيل الدخول")
        
        time.sleep(5)
        sb.save_screenshot("login_result.png")
        print(f"🔗 URL: {sb.get_current_url()}")

if __name__ == "__main__":
    test_login()
