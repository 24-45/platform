#!/usr/bin/env python3
"""
سكريبت تصدير العرض التقديمي إلى PDF
بمقاس مخصص: 33.87cm × 19.05cm
"""

import asyncio
import os
import sys
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("جاري تثبيت playwright...")
    os.system(f"{sys.executable} -m pip install playwright")
    os.system(f"{sys.executable} -m playwright install chromium")
    from playwright.async_api import async_playwright


async def export_to_pdf(url: str, output_path: str = None):
    """
    تصدير العرض التقديمي إلى PDF
    
    المقاس: 33.87cm × 19.05cm (العرض × الطول)
    """
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"qatar_sports_presentation_{timestamp}.pdf"
    
    # تحويل السنتيمترات إلى بكسل (96 DPI)
    # 33.87cm = 338.7mm = 1280px تقريباً
    # 19.05cm = 190.5mm = 720px تقريباً
    width_px = 1280
    height_px = 720
    
    print(f"🚀 جاري تصدير PDF...")
    print(f"📐 المقاس: 33.87cm × 19.05cm")
    print(f"🔗 الرابط: {url}")
    
    async with async_playwright() as p:
        # تشغيل المتصفح
        browser = await p.chromium.launch(headless=True)
        
        # إنشاء صفحة بالمقاس المطلوب
        page = await browser.new_page(
            viewport={'width': width_px, 'height': height_px}
        )
        
        # فتح الصفحة
        await page.goto(url, wait_until='networkidle')
        
        # انتظار تحميل الشرائح
        await page.wait_for_selector('.slide', timeout=10000)
        
        # إخفاء عناصر التنقل
        await page.evaluate('''
            () => {
                const hide = document.querySelectorAll('.toc-container, .slides-nav, .fab-container, .grid-view-overlay');
                hide.forEach(el => el.style.display = 'none');
            }
        ''')
        
        # تصدير PDF
        await page.pdf(
            path=output_path,
            width='33.87cm',
            height='19.05cm',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        
        await browser.close()
    
    print(f"✅ تم التصدير بنجاح!")
    print(f"📄 الملف: {output_path}")
    
    return output_path


def main():
    """نقطة الدخول الرئيسية"""
    
    # الرابط الافتراضي
    url = "http://127.0.0.1:5001/qatar_sports/"
    
    # التحقق من وجود رابط مخصص
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    # اسم الملف
    output = None
    if len(sys.argv) > 2:
        output = sys.argv[2]
    
    # تشغيل التصدير
    asyncio.run(export_to_pdf(url, output))


if __name__ == "__main__":
    main()
