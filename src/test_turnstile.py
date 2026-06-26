from seleniumbase import SB
import time
import yaml
import os

def test_turnstile_with_proxy():
    print("🚀 بدء اختبار Turnstile مع بروكسي سكني...")
    
    try:
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        proxy_list = config.get("proxy", {}).get("list", [])
        if not proxy_list:
            print("❌ لا توجد بروكسيات في config")
            with open("test_result.txt", "w") as f:
                f.write("FAILED: No proxies in config")
            return False
        
        proxy = proxy_list[0]
        print(f"🔗 استخدام بروكسي: {proxy}")
        
        # استخدام الصيغة الصحيحة لـ xvfb_metrics
        with SB(uc=True, xvfb=True, xvfb_metrics="1920,1080") as sb:
            sb.activate_cdp_mode(
                "https://app.neilpatel.com/en/login",
                proxy=proxy
            )
            print("✅ تم تحميل الصفحة عبر البروكسي")
            
            time.sleep(5)
            
            if sb.uc_gui_click_captcha():
                print("✅ تم النقر على Turnstile!")
            else:
                print("⚠️ لم يتم العثور على Turnstile")
            
            time.sleep(5)
            
            sb.save_screenshot("turnstile_test.png")
            print("📸 تم حفظ لقطة الشاشة")
            
            with open("debug_page.html", "w") as f:
                f.write(sb.get_page_source())
            print("📄 تم حفظ HTML")
            
            with open("test_result.txt", "w") as f:
                f.write("SUCCESS: Turnstile test completed")
            
            print(f"🔗 URL الحالي: {sb.get_current_url()}")
            return True
            
    except Exception as e:
        print(f"❌ فشل الاختبار: {e}")
        with open("test_result.txt", "w") as f:
            f.write(f"FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_turnstile_with_proxy()
