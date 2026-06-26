from seleniumbase import SB
import time

def test_turnstile_with_proxy():
    print("🚀 بدء اختبار Turnstile مع بروكسي سكني...")
    
    # قراءة البروكسي من config
    import yaml
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    proxy_list = config.get("proxy", {}).get("list", [])
    if not proxy_list:
        print("❌ لا توجد بروكسيات في config")
        return False
    
    proxy = proxy_list[0]  # استخدم أول بروكسي
    print(f"🔗 استخدام بروكسي: {proxy}")
    
    try:
        # استخدام SB مع xvfb=True و CDP mode
        with SB(uc=True, xvfb=True, xvfb_metrics="1920x1080") as sb:
            # إعداد البروكسي
            sb.activate_cdp_mode(
                "https://app.neilpatel.com/en/login",
                proxy=proxy
            )
            print("✅ تم تحميل الصفحة عبر البروكسي")
            
            # انتظار تحميل Turnstile
            time.sleep(5)
            
            # محاولة حل التحدي
            if sb.uc_gui_click_captcha():
                print("✅ تم النقر على Turnstile!")
            else:
                print("⚠️ لم يتم العثور على Turnstile، محاولة بديلة...")
                try:
                    sb.cdp.gui_click_element("ngx-turnstile div")
                    print("✅ تم النقر بديلاً!")
                except:
                    print("❌ فشل النقر على Turnstile")
            
            time.sleep(5)
            
            # محاولة ملء النموذج
            try:
                sb.cdp.wait_for_element("#email", timeout=10)
                sb.cdp.type("#email", "test@example.com")
                sb.cdp.type("#password", "testpass")
                sb.cdp.click("#login-button")
                print("✅ تم ملء النموذج!")
            except Exception as e:
                print(f"⚠️ فشل ملء النموذج: {e}")
                # محاولة باستخدام selectors بديلة
                try:
                    sb.type('input[type="email"]', "test@example.com")
                    sb.type('input[type="password"]', "testpass")
                    sb.click('button[type="submit"]')
                    print("✅ تم ملء النموذج (باستخدام selectors بديلة)!")
                except Exception as e2:
                    print(f"❌ فشل ملء النموذج تماماً: {e2}")
            
            time.sleep(3)
            
            # حفظ لقطة شاشة
            sb.save_screenshot("turnstile_test.png")
            print("📸 تم حفظ لقطة الشاشة")
            
            print(f"🔗 URL الحالي: {sb.get_current_url()}")
            
            return True
            
    except Exception as e:
        print(f"❌ فشل الاختبار: {e}")
        return False

if __name__ == "__main__":
    test_turnstile_with_proxy()
