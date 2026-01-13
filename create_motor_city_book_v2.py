#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
كتاب موتور سيتي - PDF احترافي مع دعم كامل للعربية باستخدام FPDF2
Motor City Professional PDF Book with Full Arabic Support using FPDF2
"""

from fpdf import FPDF
import os
import urllib.request
import tempfile

# ═══════════════════════════════════════════════════════════════
# الألوان الرئيسية (RGB)
# ═══════════════════════════════════════════════════════════════
COLORS = {
    'primary': (220, 31, 39),       # أحمر نوبلز
    'secondary': (15, 23, 42),      # كحلي داكن
    'accent': (251, 191, 36),       # ذهبي
    'emerald': (16, 185, 129),      # أخضر زمردي
    'cyan': (6, 182, 212),          # سماوي
    'purple': (139, 92, 246),       # بنفسجي
    'dark': (30, 41, 59),           # رمادي داكن
    'light': (248, 250, 252),       # رمادي فاتح
    'gold': (212, 175, 55),         # ذهبي كلاسيكي
    'gray': (100, 116, 139),        # رمادي
    'lightgray': (148, 163, 184),   # رمادي فاتح
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}


def download_arabic_font():
    """تحميل خط عربي يدعم العرض الصحيح"""
    temp_dir = tempfile.gettempdir()
    font_dir = os.path.join(temp_dir, "arabic_fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    # خط Noto Sans Arabic من Google
    fonts = {
        'NotoSansArabic-Regular': 'https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf',
        'NotoSansArabic-Bold': 'https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf',
    }
    
    font_paths = {}
    for name, url in fonts.items():
        path = os.path.join(font_dir, f"{name}.ttf")
        if not os.path.exists(path):
            print(f"📥 جاري تحميل الخط {name}...")
            try:
                urllib.request.urlretrieve(url, path)
                print(f"✅ تم تحميل {name}")
            except Exception as e:
                print(f"⚠️ فشل تحميل {name}: {e}")
                # البحث عن خط عربي في النظام
                system_fonts = [
                    "/System/Library/Fonts/Supplemental/AlBayan.ttc",
                    "/System/Library/Fonts/GeezaPro.ttc",
                ]
                for sf in system_fonts:
                    if os.path.exists(sf):
                        path = sf
                        break
        font_paths[name] = path
    
    return font_paths


class MotorCityPDF(FPDF):
    """كلاس PDF مخصص لكتاب موتور سيتي"""
    
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.page_width = 210
        self.page_height = 297
        self.margin = 20
        self.setup_fonts()
        
    def setup_fonts(self):
        """إعداد الخطوط العربية"""
        font_paths = download_arabic_font()
        
        # تسجيل الخطوط
        regular_path = font_paths.get('NotoSansArabic-Regular', '')
        bold_path = font_paths.get('NotoSansArabic-Bold', '')
        
        if regular_path and os.path.exists(regular_path) and regular_path.endswith('.ttf'):
            try:
                self.add_font('Arabic', '', regular_path)
                self.add_font('Arabic', 'B', bold_path if bold_path and os.path.exists(bold_path) else regular_path)
                self.arabic_font = 'Arabic'
                print("✅ تم تسجيل خط NotoSansArabic")
            except Exception as e:
                print(f"⚠️ خطأ: {e}")
                self.arabic_font = 'helvetica'
        else:
            self.arabic_font = 'helvetica'
            print("⚠️ استخدام خط افتراضي")
    
    def set_color(self, color_name, fill=True):
        """تعيين اللون"""
        r, g, b = COLORS.get(color_name, COLORS['black'])
        if fill:
            self.set_fill_color(r, g, b)
        else:
            self.set_draw_color(r, g, b)
        self.set_text_color(r, g, b)
    
    def draw_gradient_rect(self, x, y, w, h, color1, color2, steps=50):
        """رسم مستطيل متدرج"""
        r1, g1, b1 = COLORS[color1]
        r2, g2, b2 = COLORS[color2]
        step_h = h / steps
        
        for i in range(steps):
            ratio = i / steps
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            self.set_fill_color(r, g, b)
            self.rect(x, y + i * step_h, w, step_h + 0.5, 'F')
    
    def arabic_text(self, x, y, text, size=12, style='', color='white', align='C'):
        """كتابة نص عربي"""
        self.set_font(self.arabic_font, style, size)
        r, g, b = COLORS.get(color, COLORS['black'])
        self.set_text_color(r, g, b)
        
        # FPDF2 يدعم النص العربي تلقائياً مع text_shaping
        self.set_xy(x, y)
        if align == 'C':
            self.cell(0, 10, text, align='C')
        elif align == 'R':
            self.cell(0, 10, text, align='R')
        else:
            self.cell(0, 10, text, align='L')

    # ═══════════════════════════════════════════════════════════════
    # الغلاف الأمامي
    # ═══════════════════════════════════════════════════════════════
    def create_front_cover(self):
        """إنشاء الغلاف الأمامي"""
        self.add_page()
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, 210, 297, 'secondary', 'dark')
        
        # شريط أحمر علوي
        self.set_color('primary')
        self.rect(0, 0, 210, 8, 'F')
        
        # شريط ذهبي
        self.set_color('accent')
        self.rect(0, 8, 210, 2, 'F')
        
        # الشعار
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 25)
        self.cell(0, 10, 'NOBLES REAL ESTATE', align='C')
        
        self.set_font(self.arabic_font, 'B', 14)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 35)
        self.cell(0, 10, 'نوبلز العقارية', align='C')
        
        # العنوان الرئيسي
        self.set_font('helvetica', 'B', 48)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 100)
        self.cell(0, 20, 'MOTOR CITY', align='C')
        
        self.set_font(self.arabic_font, 'B', 36)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 125)
        self.cell(0, 15, 'موتور سيتي', align='C')
        
        # خط زخرفي
        self.set_draw_color(*COLORS['accent'])
        self.set_line_width(0.5)
        self.line(75, 145, 135, 145)
        self.set_fill_color(*COLORS['accent'])
        self.ellipse(102, 143, 6, 6, 'F')
        
        # العنوان الفرعي
        self.set_font(self.arabic_font, '', 14)
        self.set_text_color(*COLORS['lightgray'])
        self.set_xy(0, 155)
        self.cell(0, 8, 'الخطة الاستراتيجية للاتصال والعلاقات العامة', align='C')
        
        self.set_font('helvetica', '', 12)
        self.set_xy(0, 165)
        self.cell(0, 8, 'Strategic Communication & PR Plan', align='C')
        
        # معلومات المشروع
        info_items = [
            'منطقة أحد، شرق عمان، الأردن',
            '210,000 متر مربع',
            '757 معرض سيارات',
        ]
        
        y = 190
        self.set_font(self.arabic_font, '', 11)
        self.set_text_color(*COLORS['accent'])
        for item in info_items:
            self.set_xy(0, y)
            self.cell(0, 7, item, align='C')
            y += 8
        
        # التاريخ
        self.set_font(self.arabic_font, '', 10)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 270)
        self.cell(0, 8, 'يناير 2026', align='C')
        
        # شريط سفلي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 289, 210, 8, 'F')

    # ═══════════════════════════════════════════════════════════════
    # صفحة العنوان
    # ═══════════════════════════════════════════════════════════════
    def create_title_page(self):
        """صفحة العنوان الداخلية"""
        self.add_page()
        
        # خلفية بيضاء
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 297, 'F')
        
        # إطار زخرفي
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(1)
        self.rect(15, 15, 180, 267, 'D')
        
        self.set_draw_color(*COLORS['accent'])
        self.set_line_width(0.3)
        self.rect(17, 17, 176, 263, 'D')
        
        # العنوان
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(0, 60)
        self.cell(0, 15, 'MOTOR CITY', align='C')
        
        self.set_font(self.arabic_font, 'B', 26)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(0, 80)
        self.cell(0, 12, 'موتور سيتي', align='C')
        
        # خط فاصل
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(0.5)
        self.line(75, 100, 135, 100)
        self.set_fill_color(*COLORS['primary'])
        self.ellipse(102, 98, 6, 6, 'F')
        
        # العنوان الفرعي
        self.set_font(self.arabic_font, '', 14)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(0, 115)
        self.cell(0, 8, 'الخطة الاستراتيجية المتكاملة', align='C')
        self.set_xy(0, 125)
        self.cell(0, 8, 'للاتصال والعلاقات العامة', align='C')
        
        # معلومات النشر
        publish_info = [
            'إعداد: منصة 24°45°',
            'لصالح: نوبلز العقارية',
            'الإصدار: 1.0',
            'التاريخ: يناير 2026',
        ]
        
        y = 160
        self.set_font(self.arabic_font, '', 11)
        self.set_text_color(*COLORS['dark'])
        for info in publish_info:
            self.set_xy(0, y)
            self.cell(0, 8, info, align='C')
            y += 10
        
        # حقوق النشر
        self.set_font(self.arabic_font, '', 9)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 260)
        self.cell(0, 8, 'جميع الحقوق محفوظة © نوبلز العقارية 2026', align='C')

    # ═══════════════════════════════════════════════════════════════
    # فهرس المحتويات
    # ═══════════════════════════════════════════════════════════════
    def create_table_of_contents(self):
        """فهرس المحتويات"""
        self.add_page()
        
        # العنوان
        self.set_font(self.arabic_font, 'B', 24)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(0, 30)
        self.cell(0, 12, 'فهرس المحتويات', align='C')
        
        self.set_font('helvetica', '', 14)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(0, 45)
        self.cell(0, 8, 'Table of Contents', align='C')
        
        # خط فاصل
        self.set_draw_color(*COLORS['primary'])
        self.line(75, 58, 135, 58)
        
        # عناصر الفهرس
        toc_items = [
            ('التمهيد والمقدمة', 'Introduction', '5'),
            ('القسم الأول: نظرة عامة', 'Overview', '7'),
            ('القسم الثاني: الوضع الراهن', 'Current Status', '15'),
            ('القسم الثالث: المقارنات المعيارية', 'Benchmarks', '25'),
            ('القسم الرابع: الخطة الاستراتيجية', 'Strategic Plan', '45'),
        ]
        
        y = 75
        for i, (title_ar, title_en, page) in enumerate(toc_items, 1):
            # رقم
            self.set_fill_color(*COLORS['primary'])
            self.ellipse(25, y, 8, 8, 'F')
            self.set_font('helvetica', 'B', 10)
            self.set_text_color(255, 255, 255)
            self.set_xy(25, y + 1)
            self.cell(8, 6, str(i), align='C')
            
            # العنوان العربي
            self.set_font(self.arabic_font, 'B', 13)
            self.set_text_color(*COLORS['secondary'])
            self.set_xy(40, y)
            self.cell(100, 8, title_ar, align='L')
            
            # العنوان الإنجليزي
            self.set_font('helvetica', '', 10)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(40, y + 8)
            self.cell(100, 6, title_en, align='L')
            
            # خط منقط
            self.set_draw_color(*COLORS['lightgray'])
            self.set_dash_pattern(dash=2, gap=2)
            self.line(145, y + 5, 175, y + 5)
            self.set_dash_pattern()
            
            # رقم الصفحة
            self.set_font('helvetica', 'B', 12)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(175, y)
            self.cell(15, 8, page, align='R')
            
            y += 30

    # ═══════════════════════════════════════════════════════════════
    # صفحة التمهيد
    # ═══════════════════════════════════════════════════════════════
    def create_introduction(self):
        """التمهيد والمقدمة"""
        self.add_page()
        
        # شريط علوي
        self.set_fill_color(*COLORS['secondary'])
        self.rect(0, 0, 210, 20, 'F')
        
        self.set_font(self.arabic_font, 'B', 11)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 6)
        self.cell(0, 8, 'التمهيد والمقدمة', align='C')
        
        # العنوان
        self.set_font(self.arabic_font, 'B', 22)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(20, 35)
        self.cell(170, 12, 'مقدمة', align='R')
        
        self.set_font('helvetica', '', 14)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(20, 48)
        self.cell(170, 8, 'Introduction', align='R')
        
        # المحتوى
        intro_text = """يمثل مشروع موتور سيتي نقلة نوعية في قطاع معارض السيارات في الأردن، حيث يهدف إلى إنشاء أول مدينة متكاملة ومتخصصة لمعارض السيارات في المملكة.

يقع المشروع في منطقة أحد شرق عمان على مساحة إجمالية تبلغ 210,000 متر مربع، ويضم 757 معرضاً للسيارات مع كافة الخدمات المساندة.

تم إعداد هذه الخطة الاستراتيجية للاتصال والعلاقات العامة لتحقيق الأهداف التالية:

• بناء الوعي بالمشروع وترسيخ مكانته كوجهة رئيسية
• جذب المستأجرين والمستثمرين المحتملين
• تعزيز السمعة المؤسسية لنوبلز العقارية
• إدارة التوقعات والتواصل الفعال مع أصحاب المصلحة

تستند هذه الخطة إلى دراسة معيارية شاملة لأفضل الممارسات العالمية في مدن السيارات، بالإضافة إلى دراسة ميدانية للسوق المحلي شملت أكثر من 350 معرضاً في عمان."""
        
        self.set_font(self.arabic_font, '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, 65)
        self.multi_cell(170, 8, intro_text, align='R')
        
        # رقم الصفحة
        self.set_font('helvetica', '', 10)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(0, 285)
        self.cell(0, 8, str(self.page_no()), align='C')

    # ═══════════════════════════════════════════════════════════════
    # فاصل الأقسام
    # ═══════════════════════════════════════════════════════════════
    def create_section_divider(self, section_num, title_ar, title_en, color_name='primary'):
        """فاصل بين الأقسام"""
        self.add_page()
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, 210, 297, 'secondary', 'dark')
        
        # دائرة زخرفية
        self.set_fill_color(30, 58, 95)
        self.ellipse(25, 68, 160, 160, 'F')
        
        self.set_draw_color(*COLORS[color_name])
        self.set_line_width(2)
        self.ellipse(45, 88, 120, 120, 'D')
        
        self.set_draw_color(*COLORS['accent'])
        self.set_line_width(0.5)
        self.ellipse(50, 93, 110, 110, 'D')
        
        # رقم القسم
        self.set_font('helvetica', 'B', 72)
        self.set_text_color(*COLORS[color_name])
        self.set_xy(0, 115)
        self.cell(0, 30, str(section_num), align='C')
        
        # العنوان العربي
        self.set_font(self.arabic_font, 'B', 24)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 160)
        self.cell(0, 12, title_ar, align='C')
        
        # العنوان الإنجليزي
        self.set_font('helvetica', '', 16)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 175)
        self.cell(0, 10, title_en, align='C')

    # ═══════════════════════════════════════════════════════════════
    # صفحة محتوى
    # ═══════════════════════════════════════════════════════════════
    def create_content_page(self, section_title, content_title, content_items):
        """صفحة محتوى"""
        self.add_page()
        
        # شريط علوي
        self.set_fill_color(*COLORS['secondary'])
        self.rect(0, 0, 210, 15, 'F')
        
        self.set_font(self.arabic_font, '', 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 4)
        self.cell(0, 8, section_title, align='C')
        
        # العنوان
        self.set_font(self.arabic_font, 'B', 18)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(20, 25)
        self.cell(170, 10, content_title, align='R')
        
        # خط تحت العنوان
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(2)
        self.line(140, 38, 190, 38)
        
        # المحتوى
        y = 50
        self.set_font(self.arabic_font, '', 11)
        
        for item in content_items:
            if isinstance(item, tuple):
                subtitle, text = item
                # عنوان فرعي
                self.set_font(self.arabic_font, 'B', 12)
                self.set_text_color(*COLORS['primary'])
                self.set_xy(20, y)
                self.cell(170, 8, subtitle, align='R')
                y += 10
                
                # النص
                self.set_font(self.arabic_font, '', 10)
                self.set_text_color(*COLORS['dark'])
                self.set_xy(20, y)
                self.cell(170, 7, text, align='R')
                y += 15
            else:
                self.set_font(self.arabic_font, '', 10)
                self.set_text_color(*COLORS['dark'])
                self.set_xy(20, y)
                self.cell(170, 7, item, align='R')
                y += 8
        
        # رقم الصفحة
        self.set_font('helvetica', '', 10)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(0, 285)
        self.cell(0, 8, str(self.page_no()), align='C')

    # ═══════════════════════════════════════════════════════════════
    # الغلاف الخلفي
    # ═══════════════════════════════════════════════════════════════
    def create_back_cover(self):
        """الغلاف الخلفي"""
        self.add_page()
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, 210, 297, 'dark', 'secondary')
        
        # شريط أحمر علوي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 0, 210, 8, 'F')
        
        # الشعار
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 110)
        self.cell(0, 15, 'NOBLES', align='C')
        
        self.set_font('helvetica', '', 18)
        self.set_xy(0, 125)
        self.cell(0, 12, 'REAL ESTATE', align='C')
        
        self.set_font(self.arabic_font, 'B', 16)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 140)
        self.cell(0, 10, 'نوبلز العقارية', align='C')
        
        # خط زخرفي
        self.set_draw_color(*COLORS['accent'])
        self.set_line_width(0.5)
        self.line(75, 155, 135, 155)
        
        # معلومات التواصل
        contact_info = [
            'www.nobles.jo',
            'info@nobles.jo',
            '+962 6 XXX XXXX',
        ]
        
        y = 170
        self.set_font('helvetica', '', 11)
        self.set_text_color(*COLORS['lightgray'])
        for info in contact_info:
            self.set_xy(0, y)
            self.cell(0, 8, info, align='C')
            y += 10
        
        # حقوق النشر
        self.set_font('helvetica', '', 9)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 260)
        self.cell(0, 8, '© 2026 Nobles Real Estate. All Rights Reserved.', align='C')
        
        # شريط سفلي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 289, 210, 8, 'F')

    # ═══════════════════════════════════════════════════════════════
    # بناء الكتاب
    # ═══════════════════════════════════════════════════════════════
    def build(self, filename='motor_city_book_arabic.pdf'):
        """بناء الكتاب الكامل"""
        print("🚀 بدء إنشاء كتاب موتور سيتي...")
        
        # تفعيل دعم النص العربي
        self.set_text_shaping(True)
        
        # الغلاف الأمامي
        print("  📖 إنشاء الغلاف الأمامي...")
        self.create_front_cover()
        
        # صفحة العنوان
        print("  📄 إنشاء صفحة العنوان...")
        self.create_title_page()
        
        # فهرس المحتويات
        print("  📑 إنشاء فهرس المحتويات...")
        self.create_table_of_contents()
        
        # التمهيد
        print("  📝 إنشاء صفحة التمهيد...")
        self.create_introduction()
        
        # القسم الأول
        print("  📊 إنشاء قسم نظرة عامة...")
        self.create_section_divider(1, 'نظرة عامة', 'Overview', 'emerald')
        self.create_content_page(
            'القسم الأول: نظرة عامة',
            'معلومات المشروع الأساسية',
            [
                ('اسم المشروع', 'موتور سيتي - Motor City'),
                ('الموقع', 'منطقة أحد، شرق عمان، الأردن'),
                ('المساحة الإجمالية', '210,000 متر مربع'),
                ('عدد الوحدات', '757 معرض سيارات'),
                ('نوع المشروع', 'مدينة سيارات متكاملة'),
                ('تاريخ التسليم المتوقع', '2027'),
            ]
        )
        
        # القسم الثاني
        print("  📈 إنشاء قسم الوضع الراهن...")
        self.create_section_divider(2, 'الوضع الراهن', 'Current Status', 'cyan')
        self.create_content_page(
            'القسم الثاني: الوضع الراهن',
            'تحليل سوق معارض السيارات في عمان',
            [
                ('عدد المعارض المستطلعة', '352 معرض'),
                ('معدل الاستجابة', '97%'),
                ('التحدي الأكبر', 'البائعون غير المنظمين (31.9%)'),
                ('الرضا عن الموقع الحالي', '87.5%'),
                ('المهتمون بالانتقال', '32.4%'),
            ]
        )
        
        # القسم الثالث
        print("  🌍 إنشاء قسم المقارنات المعيارية...")
        self.create_section_divider(3, 'المقارنات المعيارية', 'Benchmarks', 'purple')
        self.create_content_page(
            'القسم الثالث: المقارنات المعيارية',
            'التجارب العالمية في مدن السيارات',
            [
                ('Motor World Abu Dhabi', 'الإمارات - نموذج ترفيهي متكامل'),
                ('Dubai Auto Zone', 'الإمارات - منطقة حرة متخصصة'),
                ('Autostadt Wolfsburg', 'ألمانيا - تجربة العلامة التجارية'),
                ('Autopia Istanbul', 'تركيا - مدينة سيارات شاملة'),
                ('معارض القادسية', 'السعودية - تجربة إقليمية'),
            ]
        )
        
        # القسم الرابع
        print("  🎯 إنشاء قسم الخطة الاستراتيجية...")
        self.create_section_divider(4, 'الخطة الاستراتيجية', 'Strategic Plan', 'primary')
        self.create_content_page(
            'القسم الرابع: الخطة الاستراتيجية',
            'محاور الخطة الاتصالية',
            [
                ('الهدف الرئيسي', 'تموضع موتور سيتي كوجهة رئيسية لقطاع السيارات في الأردن'),
                ('الجمهور المستهدف', 'أصحاب المعارض، المستثمرون، الجهات الحكومية'),
                ('الرسالة المركزية', 'من التشتت إلى التكامل - مدينة السيارات الأولى'),
                ('القنوات الرئيسية', 'العلاقات العامة، الإعلام، وسائل التواصل الاجتماعي'),
            ]
        )
        
        # الغلاف الخلفي
        print("  📕 إنشاء الغلاف الخلفي...")
        self.create_back_cover()
        
        # حفظ الملف
        self.output(filename)
        print(f"\n✅ تم إنشاء الكتاب بنجاح: {filename}")
        print(f"   عدد الصفحات: {self.page_no()}")
        
        return filename


# ═══════════════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pdf = MotorCityPDF()
    output_file = pdf.build('motor_city_book_arabic.pdf')
    
    print(f"\n📂 الملف في: {os.path.abspath(output_file)}")
