from seleniumbase import SB
import time
import yaml

def test_login():
    print("🚀 بدء اختبار تسجيل الدخول...")
    
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    proxy = config.get("proxy", {}).get("list", [None])[0]
    
    # استخدم SB مع xvfb=True (شاشة وهمية) و headless2=True (تخفي أفضل)
    with SB(uc=True, xvfb=True, headless2=True) as sb:
        sb.activate_cdp_mode("https://app.neilpatel.com/en/login", proxy=proxy)
        print("✅ تم تحميل الصفحة")
        
        time.sleep(3)
        
        # حاول تسجيل الدخول
        sb.type('input[name="email"]', "ezz1yn0vb7@ruutukf.com")
        sb.type('input[name="password"]', "*tW4kEI5hj2aRJP&")
        sb.click('button[type="submit"]')
        print("✅ تم الضغط على تسجيل الدخول")
        
        time.sleep(5)
        sb.save_screenshot("login_result.png")
        print(f"🔗 URL: {sb.get_current_url()}")

if __name__ == "__main__":
    test_login()
