"""
Playwright + Stealth bypass for Ubersuggest login
"""

import asyncio
import yaml
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def test_login():
    print("🚀 بدء اختبار تسجيل الدخول باستخدام Playwright + Stealth...")

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

    async with async_playwright() as p:
        # 1️⃣ تشغيل المتصفح (بدون headless عشان التخفي)
        browser = await p.chromium.launch(
            headless=False,  # مهم!
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # 2️⃣ تفعيل stealth mode
        await stealth_async(page)

        # 3️⃣ فتح صفحة تسجيل الدخول
        print("⏳ جاري تحميل الصفحة...")
        await page.goto("https://app.neilpatel.com/en/login", wait_until="networkidle")
        await page.wait_for_timeout(5000)  # انتظار 5 ثواني

        # 4️⃣ ملء الحقول
        await page.fill('input[type="email"]', email)
        await page.fill('input[type="password"]', password)

        # 5️⃣ الضغط على زر تسجيل الدخول
        await page.click('button[type="submit"]')
        print("✅ تم الضغط على تسجيل الدخول")

        # 6️⃣ انتظار التوجيه
        await page.wait_for_timeout(5000)

        # 7️⃣ التحقق من النتيجة
        current_url = page.url
        print(f"🔗 URL: {current_url}")

        if "dashboard" in current_url or "new-dashboard" in current_url:
            print("✅ تسجيل الدخول ناجح!")
            await page.screenshot(path="login_success.png")
        else:
            print("❌ فشل تسجيل الدخول")
            await page.screenshot(path="login_failed.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_login())
