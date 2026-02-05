#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
منصة 24°45° - أداة إنشاء مشروع جديد
Platform 24-45 - New Project Creator

هذا الملف يحتوي على قالب وأداة لإنشاء مشروع عرض تقديمي تفاعلي جديد
"""

import os
import json
from pathlib import Path
from datetime import datetime

# ========================================
# إعدادات المشروع - قم بتعديلها
# ========================================

PROJECT_CONFIG = {
    # معلومات المشروع الأساسية
    "project_slug": "new_project",           # اسم المشروع بالإنجليزية (بدون مسافات)
    "client_name_ar": "اسم العميل",           # اسم العميل بالعربي
    "client_name_en": "Client Name",          # اسم العميل بالإنجليزي
    "project_description": "وصف المشروع",     # وصف المشروع
    
    # ألوان الهوية البصرية
    "colors": {
        "primary": "#8B1538",                 # اللون الرئيسي
        "primary_dark": "#6A1029",            # اللون الرئيسي الداكن
        "secondary": "#D4AF37",               # اللون الثانوي (ذهبي)
        "secondary_light": "#E5C76B",         # اللون الثانوي الفاتح
        "accent": "#ffffff",                  # لون التمييز
        "bg_primary": "#5D0E26",              # لون الخلفية الرئيسي
        "bg_dark": "#3D0616",                 # لون الخلفية الداكن
    }
}

# ========================================
# مقاسات الشرائح (ثابتة)
# ========================================

SLIDE_DIMENSIONS = {
    "width": "33.87cm",
    "height": "19.05cm",
    "aspect_ratio": "16:9",
    "safe_margins": {
        "top": "15mm",
        "right": "25mm",
        "bottom": "18mm",
        "left": "25mm"
    }
}

# ========================================
# العناصر التفاعلية
# ========================================

INTERACTIVE_ELEMENTS = [
    {"id": "slide-nav-minimal", "name": "شريط التنقل الجانبي", "position": "left"},
    {"id": "interactive-toolbar", "name": "شريط الأدوات", "position": "top-right"},
    {"id": "searchModal", "name": "نافذة البحث", "shortcut": "Ctrl+F"},
    {"id": "notesPanel", "name": "لوحة الملاحظات"},
    {"id": "bookmarksPanel", "name": "لوحة الإشارات المرجعية"},
    {"id": "gridView", "name": "عرض الشبكة"},
    {"id": "presentation-mode", "name": "وضع العرض التقديمي"},
    {"id": "tocModal", "name": "نافذة الفهرس"},
    {"id": "progressBar", "name": "شريط التقدم"},
]

# ========================================
# الملفات المصدرية للنسخ
# ========================================

SOURCE_FILES = {
    "base_template": "templates/tenant/qatar_sports/base.html",
    "index_template": "templates/tenant/qatar_sports/index.html",
    "client_css": "static/css/tenants/qatar_sports/client.css",
    "slides_css": "static/css/tenants/qatar_sports/slides.css",
    "platform_css": "static/css/slides-platform.css"
}

# ========================================
# هيكل الشرائح
# ========================================

SLIDES_STRUCTURE = [
    {"type": "slide-cover", "name": "شريحة الغلاف", "order": 1},
    {"type": "slide-intro", "name": "شريحة المقدمة", "order": 2},
    {"type": "slide-toc", "name": "شريحة الفهرس", "order": 3},
    {"type": "slide-content", "name": "شرائح المحتوى", "order": 4},
    {"type": "slide-closing", "name": "شريحة الختام", "order": -1},
]

# ========================================
# الأمر الكامل للذكاء الاصطناعي
# ========================================

def generate_ai_prompt(config: dict) -> str:
    """توليد الأمر الكامل للذكاء الاصطناعي"""
    
    prompt = f"""
أنشئ مشروع عرض تقديمي تفاعلي جديد لعميل {config['client_name_ar']} باسم {config['project_slug']}
بنفس نظام منصة 24°45° في مشروع qatar_sports

## المتطلبات التقنية:

### 1. هيكل الملفات:
templates/tenant/{config['project_slug']}/
  - base.html (القالب الأساسي)
  - index.html (الشرائح)

static/css/tenants/{config['project_slug']}/
  - client.css (الهوية والألوان)
  - slides.css (أنماط الشرائح)

static/images/tenants/{config['project_slug']}/
  - logo.svg
  - favicon.svg

### 2. مقاس الشرائح (للطباعة PDF):
- العرض: {SLIDE_DIMENSIONS['width']}
- الارتفاع: {SLIDE_DIMENSIONS['height']}
- نسبة: {SLIDE_DIMENSIONS['aspect_ratio']}
- هوامش آمنة: {SLIDE_DIMENSIONS['safe_margins']['top']} أعلى، {SLIDE_DIMENSIONS['safe_margins']['right']} يمين/يسار، {SLIDE_DIMENSIONS['safe_margins']['bottom']} أسفل

### 3. الألوان:
- اللون الرئيسي: {config['colors']['primary']}
- اللون الرئيسي الداكن: {config['colors']['primary_dark']}
- اللون الثانوي: {config['colors']['secondary']}
- لون الخلفية: {config['colors']['bg_primary']}

### 4. العناصر التفاعلية المطلوبة:
- شريط التنقل الجانبي (slide-nav-minimal)
- شريط الأدوات (interactive-toolbar)
- نافذة البحث (searchModal)
- لوحة الملاحظات (notesPanel)
- لوحة الإشارات المرجعية (bookmarksPanel)
- عرض الشبكة (gridView)
- وضع العرض التقديمي (presentation-mode)
- نافذة الفهرس (tocModal)
- شريط التقدم (progressBar)

### 5. انسخ من الملفات التالية:
- templates/tenant/qatar_sports/base.html
- templates/tenant/qatar_sports/index.html
- static/css/tenants/qatar_sports/client.css
- static/css/tenants/qatar_sports/slides.css

### 6. أضف route جديد في app.py:
@app.route('/{config['project_slug']}')
def {config['project_slug']}_page():
    tenant = get_tenant_by_slug('{config['project_slug']}')
    return render_template('tenant/{config['project_slug']}/index.html', tenant=tenant)
"""
    return prompt


def generate_css_variables(config: dict) -> str:
    """توليد متغيرات CSS"""
    
    css = f"""
:root {{
    /* ألوان العميل */
    --client-primary: {config['colors']['primary']};
    --client-primary-dark: {config['colors']['primary_dark']};
    --client-secondary: {config['colors']['secondary']};
    --client-secondary-light: {config['colors']['secondary_light']};
    --client-accent: {config['colors']['accent']};
    --client-text: #ffffff;
    --client-text-dark: #1A1A1A;
    
    /* ألوان الخلفية */
    --bg-primary: {config['colors']['bg_primary']};
    --bg-dark: {config['colors']['bg_dark']};
    --accent-gold: {config['colors']['secondary']};
    --text-white: #FFFFFF;
    
    /* مقاسات الشرائح */
    --slide-w: {SLIDE_DIMENSIONS['width']};
    --slide-h: {SLIDE_DIMENSIONS['height']};
    --safe-margin-top: {SLIDE_DIMENSIONS['safe_margins']['top']};
    --safe-margin-right: {SLIDE_DIMENSIONS['safe_margins']['right']};
    --safe-margin-bottom: {SLIDE_DIMENSIONS['safe_margins']['bottom']};
    --safe-margin-left: {SLIDE_DIMENSIONS['safe_margins']['left']};
    
    /* ألوان المنصة */
    --platform-black: #0a0a0a;
    --platform-white: #ffffff;
    --platform-green: #00d46a;
    --platform-font: 'Tajawal', 'Cairo', sans-serif;
    --slide-aspect-ratio: 16 / 9;
}}
"""
    return css


def generate_app_route(config: dict) -> str:
    """توليد كود Route لـ Flask"""
    
    route = f"""
@app.route('/{config['project_slug']}')
@app.route('/{config['project_slug']}/')
def {config['project_slug']}_page():
    \"\"\"صفحة {config['client_name_ar']}\"\"\"
    tenant = get_tenant_by_slug('{config['project_slug']}')
    return render_template('tenant/{config['project_slug']}/index.html', tenant=tenant)
"""
    return route


def generate_tenant_config(config: dict) -> dict:
    """توليد إعدادات Tenant"""
    
    return {
        "id": config['project_slug'],
        "slug": config['project_slug'],
        "name": config['client_name_ar'],
        "name_en": config['client_name_en'],
        "description": config['project_description'],
        "logo": f"/static/images/tenants/{config['project_slug']}/logo.svg",
        "favicon": f"/static/images/tenants/{config['project_slug']}/favicon.svg",
        "colors": {
            "primary": config['colors']['primary'],
            "secondary": config['colors']['secondary'],
            "accent": config['colors']['accent']
        },
        "active": True
    }


def print_checklist(config: dict):
    """طباعة قائمة التحقق"""
    
    checklist = [
        f"إنشاء مجلد templates/tenant/{config['project_slug']}/",
        "إنشاء ملف base.html",
        "إنشاء ملف index.html",
        f"إنشاء مجلد static/css/tenants/{config['project_slug']}/",
        "إنشاء ملف client.css",
        "إنشاء ملف slides.css",
        f"إنشاء مجلد static/images/tenants/{config['project_slug']}/",
        "إضافة الشعار والأيقونة",
        "تعديل الألوان في CSS",
        "إضافة Route في app.py",
        "إضافة Tenant في data/tenants.json",
        "اختبار العرض في المتصفح",
        "اختبار تصدير PDF",
        "اختبار العناصر التفاعلية"
    ]
    
    print("\n✅ قائمة التحقق:")
    print("=" * 50)
    for i, item in enumerate(checklist, 1):
        print(f"  [ ] {i}. {item}")
    print("=" * 50)


def main():
    """الدالة الرئيسية"""
    
    print("\n" + "=" * 60)
    print("🎯 منصة 24°45° - أداة إنشاء مشروع جديد")
    print("=" * 60)
    
    print(f"\n📋 معلومات المشروع:")
    print(f"   - الاسم: {PROJECT_CONFIG['project_slug']}")
    print(f"   - العميل: {PROJECT_CONFIG['client_name_ar']}")
    print(f"   - اللون الرئيسي: {PROJECT_CONFIG['colors']['primary']}")
    
    print(f"\n📐 مقاسات الشرائح:")
    print(f"   - العرض: {SLIDE_DIMENSIONS['width']}")
    print(f"   - الارتفاع: {SLIDE_DIMENSIONS['height']}")
    print(f"   - النسبة: {SLIDE_DIMENSIONS['aspect_ratio']}")
    
    print("\n" + "-" * 60)
    print("🤖 الأمر للذكاء الاصطناعي:")
    print("-" * 60)
    print(generate_ai_prompt(PROJECT_CONFIG))
    
    print("\n" + "-" * 60)
    print("🎨 متغيرات CSS:")
    print("-" * 60)
    print(generate_css_variables(PROJECT_CONFIG))
    
    print("\n" + "-" * 60)
    print("🔧 كود Route:")
    print("-" * 60)
    print(generate_app_route(PROJECT_CONFIG))
    
    print("\n" + "-" * 60)
    print("📄 إعدادات Tenant (JSON):")
    print("-" * 60)
    print(json.dumps(generate_tenant_config(PROJECT_CONFIG), indent=2, ensure_ascii=False))
    
    print_checklist(PROJECT_CONFIG)
    
    print(f"\n📅 تاريخ التوليد: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
