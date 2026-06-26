from seleniumbase import SB
import time

def test_turnstile_solution():
    print("🚀 بدء اختبار تجاوز Turnstile...")
    
    try:
        with SB(uc=True, xvfb=True, headless2=True) as sb:
            # 1. فتح الصفحة
            sb.activate_cdp_mode("https://app.neilpatel.com/en/login")
            print("✅ تم تحميل الصفحة")
            time.sleep(5)
            
            # 2. محاولة حل Turnstile
            if sb.uc_gui_click_captcha():
                print("✅ تم النقر على Turnstile!")
            else:
                print("⚠️ لم يتم العثور على Turnstile")
            
            time.sleep(3)
            
            # 3. محاولة ملء نموذج تسجيل الدخول
            try:
                sb.type('input[type="email"]', "test@example.com")
                sb.type('input[type="password"]', "testpass")
                sb.click('button[type="submit"]')
                print("✅ تم ملء النموذج")
            except Exception as e:
                print(f"⚠️ فشل ملء النموذج: {e}")
            
            time.sleep(5)
            
            # 4. حفظ لقطة شاشة
            sb.save_screenshot("turnstile_test.png")
            print("📸 تم حفظ لقطة الشاشة")
            
    except Exception as e:
        print(f"❌ فشل الاختبار: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_turnstile_solution()
