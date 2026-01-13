#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
كتاب موتور سيتي - PDF احترافي
Motor City Professional PDF Book
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY
import os

# ═══════════════════════════════════════════════════════════════
# الألوان الرئيسية
# ═══════════════════════════════════════════════════════════════
COLORS = {
    'primary': HexColor('#dc1f27'),      # أحمر نوبلز
    'secondary': HexColor('#0f172a'),    # كحلي داكن
    'accent': HexColor('#fbbf24'),       # ذهبي
    'emerald': HexColor('#10b981'),      # أخضر زمردي
    'cyan': HexColor('#06b6d4'),         # سماوي
    'purple': HexColor('#8b5cf6'),       # بنفسجي
    'dark': HexColor('#1e293b'),         # رمادي داكن
    'light': HexColor('#f8fafc'),        # رمادي فاتح
    'gold': HexColor('#d4af37'),         # ذهبي كلاسيكي
}

# ═══════════════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 2 * cm

class MotorCityBook:
    def __init__(self, filename="motor_city_book.pdf"):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.page_num = 0
        self.setup_fonts()
        
    def setup_fonts(self):
        """تسجيل الخطوط العربية"""
        # استخدام خط Helvetica كبديل (متوفر افتراضياً)
        # يمكن استبداله بخط عربي مثل Tajawal إذا كان متوفراً
        pass
    
    def draw_gradient_rect(self, x, y, width, height, color1, color2, vertical=True):
        """رسم مستطيل متدرج"""
        steps = 50
        if vertical:
            step_height = height / steps
            for i in range(steps):
                ratio = i / steps
                r = color1.red + (color2.red - color1.red) * ratio
                g = color1.green + (color2.green - color1.green) * ratio
                b = color1.blue + (color2.blue - color1.blue) * ratio
                self.c.setFillColorRGB(r, g, b)
                self.c.rect(x, y + i * step_height, width, step_height + 1, fill=1, stroke=0)
        else:
            step_width = width / steps
            for i in range(steps):
                ratio = i / steps
                r = color1.red + (color2.red - color1.red) * ratio
                g = color1.green + (color2.green - color1.green) * ratio
                b = color1.blue + (color2.blue - color1.blue) * ratio
                self.c.setFillColorRGB(r, g, b)
                self.c.rect(x + i * step_width, y, step_width + 1, height, fill=1, stroke=0)

    def draw_decorative_line(self, y, color=None):
        """خط زخرفي"""
        if color is None:
            color = COLORS['accent']
        self.c.setStrokeColor(color)
        self.c.setLineWidth(2)
        center = PAGE_WIDTH / 2
        self.c.line(center - 3*cm, y, center + 3*cm, y)
        # ماسة في المنتصف
        self.c.setFillColor(color)
        self.c.circle(center, y, 4, fill=1, stroke=0)

    # ═══════════════════════════════════════════════════════════════
    # الغلاف الأمامي
    # ═══════════════════════════════════════════════════════════════
    def create_front_cover(self):
        """إنشاء الغلاف الأمامي"""
        self.page_num += 1
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, 
                               COLORS['secondary'], COLORS['dark'])
        
        # شريط أحمر علوي
        self.c.setFillColor(COLORS['primary'])
        self.c.rect(0, PAGE_HEIGHT - 8*mm, PAGE_WIDTH, 8*mm, fill=1, stroke=0)
        
        # شريط ذهبي
        self.c.setFillColor(COLORS['accent'])
        self.c.rect(0, PAGE_HEIGHT - 10*mm, PAGE_WIDTH, 2*mm, fill=1, stroke=0)
        
        # الشعار العلوي
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3*cm, "NOBLES REAL ESTATE")
        
        self.c.setFont("Helvetica", 10)
        self.c.setFillColor(COLORS['accent'])
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3.6*cm, "نوبلز العقارية")
        
        # العنوان الرئيسي
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 42)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 3*cm, "MOTOR CITY")
        
        self.c.setFont("Helvetica-Bold", 36)
        self.c.setFillColor(COLORS['accent'])
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 1.5*cm, "موتور سيتي")
        
        # الخط الزخرفي
        self.draw_decorative_line(PAGE_HEIGHT/2 + 0.5*cm)
        
        # العنوان الفرعي
        self.c.setFillColor(HexColor('#94a3b8'))
        self.c.setFont("Helvetica", 16)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 1*cm, 
                                 "الخطة الاستراتيجية للاتصال والعلاقات العامة")
        
        self.c.setFont("Helvetica", 14)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 1.8*cm,
                                 "Strategic Communication & PR Plan")
        
        # معلومات المشروع
        y_info = PAGE_HEIGHT/2 - 4*cm
        info_items = [
            ("الموقع", "منطقة أحد، شرق عمان، الأردن"),
            ("المساحة", "210,000 متر مربع"),
            ("الوحدات", "757 معرض سيارات"),
        ]
        
        self.c.setFont("Helvetica", 11)
        for label, value in info_items:
            self.c.setFillColor(COLORS['accent'])
            self.c.drawCentredString(PAGE_WIDTH/2, y_info, f"{label}: {value}")
            y_info -= 0.7*cm
        
        # التاريخ في الأسفل
        self.c.setFillColor(HexColor('#64748b'))
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(PAGE_WIDTH/2, 3*cm, "يناير 2026")
        
        # شريط سفلي
        self.c.setFillColor(COLORS['primary'])
        self.c.rect(0, 0, PAGE_WIDTH, 8*mm, fill=1, stroke=0)
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # صفحة العنوان
    # ═══════════════════════════════════════════════════════════════
    def create_title_page(self):
        """صفحة العنوان الداخلية"""
        self.page_num += 1
        
        # خلفية بيضاء
        self.c.setFillColor(white)
        self.c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # إطار زخرفي
        self.c.setStrokeColor(COLORS['primary'])
        self.c.setLineWidth(2)
        self.c.rect(1.5*cm, 1.5*cm, PAGE_WIDTH - 3*cm, PAGE_HEIGHT - 3*cm, fill=0, stroke=1)
        
        self.c.setStrokeColor(COLORS['accent'])
        self.c.setLineWidth(0.5)
        self.c.rect(1.7*cm, 1.7*cm, PAGE_WIDTH - 3.4*cm, PAGE_HEIGHT - 3.4*cm, fill=0, stroke=1)
        
        # العنوان
        self.c.setFillColor(COLORS['secondary'])
        self.c.setFont("Helvetica-Bold", 28)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 6*cm, "MOTOR CITY")
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(COLORS['primary'])
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 7.5*cm, "موتور سيتي")
        
        # خط فاصل
        self.draw_decorative_line(PAGE_HEIGHT - 9*cm, COLORS['primary'])
        
        # العنوان الفرعي
        self.c.setFillColor(COLORS['dark'])
        self.c.setFont("Helvetica", 14)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 11*cm,
                                 "الخطة الاستراتيجية المتكاملة")
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 12*cm,
                                 "للاتصال والعلاقات العامة")
        
        # معلومات النشر
        self.c.setFont("Helvetica", 11)
        self.c.setFillColor(COLORS['dark'])
        
        publish_info = [
            "إعداد: منصة 24°45°",
            "لصالح: نوبلز العقارية",
            "الإصدار: 1.0",
            "التاريخ: يناير 2026",
        ]
        
        y = PAGE_HEIGHT/2 - 2*cm
        for info in publish_info:
            self.c.drawCentredString(PAGE_WIDTH/2, y, info)
            y -= 0.8*cm
        
        # حقوق النشر
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor('#64748b'))
        self.c.drawCentredString(PAGE_WIDTH/2, 4*cm, 
                                 "جميع الحقوق محفوظة © نوبلز العقارية 2026")
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # فهرس المحتويات
    # ═══════════════════════════════════════════════════════════════
    def create_table_of_contents(self):
        """فهرس المحتويات"""
        self.page_num += 1
        
        self.c.setFillColor(white)
        self.c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # العنوان
        self.c.setFillColor(COLORS['secondary'])
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 4*cm, "فهرس المحتويات")
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(COLORS['primary'])
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 5*cm, "Table of Contents")
        
        self.draw_decorative_line(PAGE_HEIGHT - 6*cm, COLORS['primary'])
        
        # عناصر الفهرس
        toc_items = [
            ("التمهيد والمقدمة", "Introduction", "5"),
            ("القسم الأول: نظرة عامة", "Overview", "7"),
            ("القسم الثاني: الوضع الراهن", "Current Status", "15"),
            ("القسم الثالث: المقارنات المعيارية", "Benchmarks", "25"),
            ("القسم الرابع: الخطة الاستراتيجية", "Strategic Plan", "45"),
        ]
        
        y = PAGE_HEIGHT - 8*cm
        
        for i, (title_ar, title_en, page) in enumerate(toc_items, 1):
            # رقم القسم
            self.c.setFillColor(COLORS['primary'])
            self.c.circle(MARGIN + 0.5*cm, y + 0.2*cm, 12, fill=1, stroke=0)
            self.c.setFillColor(white)
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawCentredString(MARGIN + 0.5*cm, y, str(i))
            
            # العنوان العربي
            self.c.setFillColor(COLORS['secondary'])
            self.c.setFont("Helvetica-Bold", 13)
            self.c.drawString(MARGIN + 1.5*cm, y, title_ar)
            
            # العنوان الإنجليزي
            self.c.setFillColor(HexColor('#64748b'))
            self.c.setFont("Helvetica", 10)
            self.c.drawString(MARGIN + 1.5*cm, y - 0.5*cm, title_en)
            
            # خط منقط
            self.c.setStrokeColor(HexColor('#cbd5e1'))
            self.c.setDash(2, 2)
            dots_start = MARGIN + 8*cm
            dots_end = PAGE_WIDTH - MARGIN - 1.5*cm
            self.c.line(dots_start, y - 0.2*cm, dots_end, y - 0.2*cm)
            self.c.setDash()
            
            # رقم الصفحة
            self.c.setFillColor(COLORS['primary'])
            self.c.setFont("Helvetica-Bold", 12)
            self.c.drawRightString(PAGE_WIDTH - MARGIN, y - 0.2*cm, page)
            
            y -= 2.5*cm
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # صفحة التمهيد
    # ═══════════════════════════════════════════════════════════════
    def create_introduction(self):
        """التمهيد والمقدمة"""
        self.page_num += 1
        
        self.c.setFillColor(white)
        self.c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # شريط علوي
        self.c.setFillColor(COLORS['secondary'])
        self.c.rect(0, PAGE_HEIGHT - 2*cm, PAGE_WIDTH, 2*cm, fill=1, stroke=0)
        
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 1.3*cm, "التمهيد والمقدمة")
        
        # العنوان
        self.c.setFillColor(COLORS['secondary'])
        self.c.setFont("Helvetica-Bold", 22)
        self.c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 4.5*cm, "مقدمة")
        
        self.c.setFillColor(COLORS['primary'])
        self.c.setFont("Helvetica", 14)
        self.c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 5.3*cm, "Introduction")
        
        # المحتوى
        intro_text = """
يمثل مشروع موتور سيتي نقلة نوعية في قطاع معارض السيارات في الأردن، حيث يهدف إلى إنشاء أول مدينة متكاملة ومتخصصة لمعارض السيارات في المملكة.

يقع المشروع في منطقة أحد شرق عمان على مساحة إجمالية تبلغ 210,000 متر مربع، ويضم 757 معرضاً للسيارات مع كافة الخدمات المساندة.

تم إعداد هذه الخطة الاستراتيجية للاتصال والعلاقات العامة لتحقيق الأهداف التالية:

• بناء الوعي بالمشروع وترسيخ مكانته كوجهة رئيسية
• جذب المستأجرين والمستثمرين المحتملين
• تعزيز السمعة المؤسسية لنوبلز العقارية
• إدارة التوقعات والتواصل الفعال مع أصحاب المصلحة

تستند هذه الخطة إلى دراسة معيارية شاملة لأفضل الممارسات العالمية في مدن السيارات، بالإضافة إلى دراسة ميدانية للسوق المحلي شملت أكثر من 350 معرضاً في عمان.
        """
        
        # رسم النص
        self.c.setFillColor(COLORS['dark'])
        self.c.setFont("Helvetica", 11)
        
        y = PAGE_HEIGHT - 7*cm
        for line in intro_text.strip().split('\n'):
            if line.strip():
                if line.startswith('•'):
                    self.c.setFillColor(COLORS['primary'])
                    self.c.drawString(PAGE_WIDTH - MARGIN - 0.5*cm, y, '●')
                    self.c.setFillColor(COLORS['dark'])
                    self.c.drawRightString(PAGE_WIDTH - MARGIN - 1*cm, y, line[1:].strip())
                else:
                    self.c.drawRightString(PAGE_WIDTH - MARGIN, y, line.strip())
            y -= 0.6*cm
        
        # رقم الصفحة
        self.c.setFillColor(COLORS['primary'])
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(PAGE_WIDTH/2, 1.5*cm, str(self.page_num))
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # فاصل الأقسام
    # ═══════════════════════════════════════════════════════════════
    def create_section_divider(self, section_num, title_ar, title_en, color=None):
        """فاصل بين الأقسام"""
        self.page_num += 1
        
        if color is None:
            color = COLORS['primary']
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, 
                               COLORS['secondary'], COLORS['dark'])
        
        # دائرة زخرفية كبيرة
        self.c.setFillColor(HexColor('#1e3a5f'))
        self.c.circle(PAGE_WIDTH/2, PAGE_HEIGHT/2, 8*cm, fill=1, stroke=0)
        
        self.c.setStrokeColor(color)
        self.c.setLineWidth(3)
        self.c.circle(PAGE_WIDTH/2, PAGE_HEIGHT/2, 6*cm, fill=0, stroke=1)
        
        self.c.setStrokeColor(COLORS['accent'])
        self.c.setLineWidth(1)
        self.c.circle(PAGE_WIDTH/2, PAGE_HEIGHT/2, 5.5*cm, fill=0, stroke=1)
        
        # رقم القسم
        self.c.setFillColor(color)
        self.c.setFont("Helvetica-Bold", 72)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 1.5*cm, str(section_num))
        
        # العنوان العربي
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 1*cm, title_ar)
        
        # العنوان الإنجليزي
        self.c.setFillColor(COLORS['accent'])
        self.c.setFont("Helvetica", 16)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 2*cm, title_en)
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # صفحة محتوى عامة
    # ═══════════════════════════════════════════════════════════════
    def create_content_page(self, section_title, content_title, content_items):
        """صفحة محتوى عامة"""
        self.page_num += 1
        
        self.c.setFillColor(white)
        self.c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        
        # شريط علوي
        self.c.setFillColor(COLORS['secondary'])
        self.c.rect(0, PAGE_HEIGHT - 1.5*cm, PAGE_WIDTH, 1.5*cm, fill=1, stroke=0)
        
        self.c.setFillColor(white)
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 1*cm, section_title)
        
        # العنوان
        self.c.setFillColor(COLORS['secondary'])
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 3.5*cm, content_title)
        
        # خط تحت العنوان
        self.c.setStrokeColor(COLORS['primary'])
        self.c.setLineWidth(3)
        self.c.line(PAGE_WIDTH - MARGIN - 5*cm, PAGE_HEIGHT - 4*cm, 
                   PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 4*cm)
        
        # المحتوى
        y = PAGE_HEIGHT - 5.5*cm
        
        for item in content_items:
            if isinstance(item, tuple):
                # عنوان فرعي + محتوى
                subtitle, text = item
                self.c.setFillColor(COLORS['primary'])
                self.c.setFont("Helvetica-Bold", 12)
                self.c.drawRightString(PAGE_WIDTH - MARGIN, y, subtitle)
                y -= 0.7*cm
                
                self.c.setFillColor(COLORS['dark'])
                self.c.setFont("Helvetica", 10)
                self.c.drawRightString(PAGE_WIDTH - MARGIN, y, text)
                y -= 1.2*cm
            else:
                # نص عادي
                self.c.setFillColor(COLORS['dark'])
                self.c.setFont("Helvetica", 10)
                self.c.drawRightString(PAGE_WIDTH - MARGIN, y, item)
                y -= 0.6*cm
        
        # رقم الصفحة
        self.c.setFillColor(COLORS['primary'])
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(PAGE_WIDTH/2, 1.5*cm, str(self.page_num))
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # الغلاف الخلفي
    # ═══════════════════════════════════════════════════════════════
    def create_back_cover(self):
        """الغلاف الخلفي"""
        self.page_num += 1
        
        # خلفية متدرجة
        self.draw_gradient_rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, 
                               COLORS['dark'], COLORS['secondary'])
        
        # شريط أحمر علوي
        self.c.setFillColor(COLORS['primary'])
        self.c.rect(0, PAGE_HEIGHT - 8*mm, PAGE_WIDTH, 8*mm, fill=1, stroke=0)
        
        # الشعار
        self.c.setFillColor(white)
        self.c.setFont("Helvetica-Bold", 28)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 3*cm, "NOBLES")
        
        self.c.setFont("Helvetica", 18)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 2*cm, "REAL ESTATE")
        
        self.c.setFillColor(COLORS['accent'])
        self.c.setFont("Helvetica", 16)
        self.c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + 0.8*cm, "نوبلز العقارية")
        
        # خط زخرفي
        self.draw_decorative_line(PAGE_HEIGHT/2 - 0.5*cm)
        
        # معلومات التواصل
        contact_info = [
            "www.nobles.jo",
            "info@nobles.jo",
            "+962 6 XXX XXXX",
        ]
        
        self.c.setFillColor(HexColor('#94a3b8'))
        self.c.setFont("Helvetica", 11)
        
        y = PAGE_HEIGHT/2 - 2*cm
        for info in contact_info:
            self.c.drawCentredString(PAGE_WIDTH/2, y, info)
            y -= 0.7*cm
        
        # حقوق النشر
        self.c.setFillColor(HexColor('#64748b'))
        self.c.setFont("Helvetica", 9)
        self.c.drawCentredString(PAGE_WIDTH/2, 3*cm, 
                                 "© 2026 Nobles Real Estate. All Rights Reserved.")
        
        # شريط سفلي
        self.c.setFillColor(COLORS['primary'])
        self.c.rect(0, 0, PAGE_WIDTH, 8*mm, fill=1, stroke=0)
        
        self.c.showPage()

    # ═══════════════════════════════════════════════════════════════
    # بناء الكتاب الكامل
    # ═══════════════════════════════════════════════════════════════
    def build(self):
        """بناء الكتاب الكامل"""
        print("🚀 بدء إنشاء كتاب موتور سيتي...")
        
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
        
        # القسم الأول: نظرة عامة
        print("  📊 إنشاء قسم نظرة عامة...")
        self.create_section_divider(1, "نظرة عامة", "Overview", COLORS['emerald'])
        self.create_content_page(
            "القسم الأول: نظرة عامة",
            "معلومات المشروع الأساسية",
            [
                ("اسم المشروع", "موتور سيتي - Motor City"),
                ("الموقع", "منطقة أحد، شرق عمان، الأردن"),
                ("المساحة الإجمالية", "210,000 متر مربع"),
                ("عدد الوحدات", "757 معرض سيارات"),
                ("نوع المشروع", "مدينة سيارات متكاملة"),
                ("تاريخ التسليم المتوقع", "2027"),
            ]
        )
        
        # القسم الثاني: الوضع الراهن
        print("  📈 إنشاء قسم الوضع الراهن...")
        self.create_section_divider(2, "الوضع الراهن", "Current Status", COLORS['cyan'])
        self.create_content_page(
            "القسم الثاني: الوضع الراهن",
            "تحليل سوق معارض السيارات في عمان",
            [
                ("عدد المعارض المستطلعة", "352 معرض"),
                ("معدل الاستجابة", "97%"),
                ("التحدي الأكبر", "البائعون غير المنظمين (31.9%)"),
                ("الرضا عن الموقع الحالي", "87.5%"),
                ("المهتمون بالانتقال", "32.4%"),
            ]
        )
        
        # القسم الثالث: المقارنات المعيارية
        print("  🌍 إنشاء قسم المقارنات المعيارية...")
        self.create_section_divider(3, "المقارنات المعيارية", "Benchmarks", COLORS['purple'])
        self.create_content_page(
            "القسم الثالث: المقارنات المعيارية",
            "التجارب العالمية في مدن السيارات",
            [
                ("Motor World Abu Dhabi", "الإمارات - نموذج ترفيهي متكامل"),
                ("Dubai Auto Zone", "الإمارات - منطقة حرة متخصصة"),
                ("Autostadt Wolfsburg", "ألمانيا - تجربة العلامة التجارية"),
                ("Autopia Istanbul", "تركيا - مدينة سيارات شاملة"),
                ("معارض القادسية", "السعودية - تجربة إقليمية"),
            ]
        )
        
        # القسم الرابع: الخطة الاستراتيجية
        print("  🎯 إنشاء قسم الخطة الاستراتيجية...")
        self.create_section_divider(4, "الخطة الاستراتيجية", "Strategic Plan", COLORS['primary'])
        self.create_content_page(
            "القسم الرابع: الخطة الاستراتيجية",
            "محاور الخطة الاتصالية",
            [
                ("الهدف الرئيسي", "تموضع موتور سيتي كوجهة رئيسية لقطاع السيارات في الأردن"),
                ("الجمهور المستهدف", "أصحاب المعارض، المستثمرون، الجهات الحكومية"),
                ("الرسالة المركزية", "من التشتت إلى التكامل - مدينة السيارات الأولى"),
                ("القنوات الرئيسية", "العلاقات العامة، الإعلام، وسائل التواصل الاجتماعي"),
            ]
        )
        
        # الغلاف الخلفي
        print("  📕 إنشاء الغلاف الخلفي...")
        self.create_back_cover()
        
        # حفظ الملف
        self.c.save()
        print(f"\n✅ تم إنشاء الكتاب بنجاح: {self.filename}")
        print(f"   عدد الصفحات: {self.page_num}")


# ═══════════════════════════════════════════════════════════════
# التشغيل الرئيسي
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # إنشاء الكتاب
    book = MotorCityBook("motor_city_book.pdf")
    book.build()
    
    print("\n📂 يمكنك فتح الملف من:")
    print(f"   {os.path.abspath('motor_city_book.pdf')}")
