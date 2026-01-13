ما هو #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor City Strategic Plan PDF Generator
مولد ملف PDF للخطة الاستراتيجية لمشروع موتور سيتي

This script generates a professionally designed Arabic PDF book 
containing the Strategic Plan content for Motor City project.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display

# ═══════════════════════════════════════════════════════════════════════════════
# Color Palette - Motor City Brand Colors
# ═══════════════════════════════════════════════════════════════════════════════
COLORS = {
    'primary': HexColor('#dc1f27'),      # Motor City Red
    'primary_dark': HexColor('#b51920'),  # Dark Red
    'secondary': HexColor('#0f172a'),     # Dark Navy
    'accent': HexColor('#10b981'),        # Emerald Green
    'accent_blue': HexColor('#3b82f6'),   # Blue
    'accent_purple': HexColor('#8b5cf6'), # Purple
    'accent_orange': HexColor('#f59e0b'), # Orange
    'text_light': HexColor('#e2e8f0'),    # Light Gray
    'text_muted': HexColor('#94a3b8'),    # Muted Gray
    'bg_dark': HexColor('#1e293b'),       # Dark Background
    'white': HexColor('#ffffff'),
    'black': HexColor('#000000'),
}

# ═══════════════════════════════════════════════════════════════════════════════
# Arabic Text Processing
# ═══════════════════════════════════════════════════════════════════════════════
def arabic(text):
    """Process Arabic text for proper RTL display"""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ═══════════════════════════════════════════════════════════════════════════════
# PDF Document Class
# ═══════════════════════════════════════════════════════════════════════════════
class MotorCityStrategicPlanPDF:
    def __init__(self, output_path="motor_city_strategic_plan.pdf"):
        self.output_path = output_path
        self.width, self.height = A4
        self.margin = 2.5 * cm
        
        # Try to register Arabic fonts
        self.setup_fonts()
        
        # Create PDF canvas
        self.pdf = canvas.Canvas(output_path, pagesize=A4)
        self.page_number = 0
        
    def setup_fonts(self):
        """Register Arabic-compatible fonts"""
        # Try to find and register Arabic fonts
        font_paths = [
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            '/Library/Fonts/Arial Unicode.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/System/Library/Fonts/Geeza Pro.ttc',
        ]
        
        self.arabic_font = 'Helvetica'  # Fallback
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ArabicFont', font_path))
                    self.arabic_font = 'ArabicFont'
                    break
                except:
                    continue
    
    def draw_background_gradient(self, color1, color2):
        """Draw a gradient-like background"""
        self.pdf.setFillColor(color1)
        self.pdf.rect(0, 0, self.width, self.height, fill=True, stroke=False)
        
        # Add subtle gradient effect with rectangles
        for i in range(10):
            alpha = i / 10
            y = self.height * (1 - i / 10)
            self.pdf.setFillColor(color2)
            self.pdf.setFillAlpha(alpha * 0.3)
            self.pdf.rect(0, 0, self.width, y, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
    
    def draw_decorative_corner(self, x, y, size, color):
        """Draw decorative corner element"""
        self.pdf.setFillColor(color)
        self.pdf.setFillAlpha(0.1)
        self.pdf.circle(x, y, size, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
    
    def add_page_number(self):
        """Add page number to current page"""
        self.page_number += 1
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        page_text = arabic(f"صفحة {self.page_number}")
        self.pdf.drawCentredString(self.width / 2, 1.5 * cm, page_text)
    
    def new_page(self, with_bg=True, with_number=True):
        """Start a new page"""
        if self.page_number > 0:
            if with_number:
                self.add_page_number()
            self.pdf.showPage()
        
        if with_bg:
            self.draw_background_gradient(COLORS['secondary'], COLORS['bg_dark'])
            # Add decorative elements
            self.draw_decorative_corner(self.width, self.height, 200, COLORS['primary'])
            self.draw_decorative_corner(0, 0, 150, COLORS['accent'])
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Cover Page
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_cover_page(self):
        """Draw the cover page"""
        self.new_page(with_number=False)
        
        # Background
        self.draw_background_gradient(COLORS['secondary'], COLORS['bg_dark'])
        
        # Large decorative circles
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.setFillAlpha(0.1)
        self.pdf.circle(self.width + 100, self.height - 100, 300, fill=True, stroke=False)
        self.pdf.circle(-100, 100, 250, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
        
        # Motor City Logo area
        logo_y = self.height - 5 * cm
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.roundRect(self.width/2 - 4*cm, logo_y - 2*cm, 8*cm, 4*cm, 20, fill=True, stroke=False)
        
        # Logo text
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 28)
        self.pdf.drawCentredString(self.width/2, logo_y, "MOTOR CITY")
        
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, logo_y - 0.8*cm, arabic("موتور سيتي"))
        
        # Main title
        title_y = self.height - 11 * cm
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, title_y, arabic("الخطة الاستراتيجية"))
        
        # Subtitle
        self.pdf.setFont(self.arabic_font, 20)
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.drawCentredString(self.width/2, title_y - 1.5*cm, arabic("خطة الاتصال والعلاقات العامة"))
        
        # English subtitle
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.drawCentredString(self.width/2, title_y - 2.5*cm, "Strategic Communication & PR Plan")
        
        # Divider line
        self.pdf.setStrokeColor(COLORS['primary'])
        self.pdf.setLineWidth(3)
        self.pdf.line(self.width/4, title_y - 4*cm, 3*self.width/4, title_y - 4*cm)
        
        # Project description
        desc_y = title_y - 5.5*cm
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, desc_y, 
            arabic("أول مدينة سيارات متكاملة في الأردن والمشرق العربي"))
        
        # Key stats boxes
        stats_y = desc_y - 3*cm
        box_width = 4*cm
        box_height = 2.5*cm
        
        stats = [
            ("914", arabic("دونم")),
            ("3", arabic("مناطق")),
            ("2026", arabic("الإطلاق")),
        ]
        
        start_x = self.width/2 - 1.5*box_width - 1*cm
        
        for i, (number, label) in enumerate(stats):
            x = start_x + i * (box_width + 0.5*cm)
            
            # Box background
            self.pdf.setFillColor(COLORS['primary'])
            self.pdf.setFillAlpha(0.2)
            self.pdf.roundRect(x, stats_y - box_height, box_width, box_height, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Number
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 28)
            self.pdf.drawCentredString(x + box_width/2, stats_y - 1*cm, number)
            
            # Label
            self.pdf.setFont(self.arabic_font, 11)
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.drawCentredString(x + box_width/2, stats_y - 1.8*cm, label)
        
        # Footer
        footer_y = 3*cm
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 11)
        self.pdf.drawCentredString(self.width/2, footer_y, 
            arabic("إعداد: 24-45 للعلاقات العامة والاتصال"))
        
        # Date
        date_text = datetime.now().strftime("%Y/%m/%d")
        self.pdf.drawCentredString(self.width/2, footer_y - 0.7*cm, date_text)
        
        # Partners logos area
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(self.width/2, footer_y - 1.8*cm, 
            arabic("رؤية عمان  •  نوبلز  •  أمانة عمان الكبرى"))
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Table of Contents
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_table_of_contents(self):
        """Draw table of contents page"""
        self.new_page()
        
        # Title
        title_y = self.height - 4*cm
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.setFont(self.arabic_font, 28)
        self.pdf.drawCentredString(self.width/2, title_y, arabic("فهرس المحتويات"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, title_y - 1*cm, "Table of Contents")
        
        # Divider
        self.pdf.setStrokeColor(COLORS['primary'])
        self.pdf.setLineWidth(2)
        self.pdf.line(self.margin, title_y - 2*cm, self.width - self.margin, title_y - 2*cm)
        
        # Contents items
        contents = [
            (arabic("الدراسة التفصيلية - المقارنات المعيارية"), "1"),
            (arabic("  • النماذج العالمية (Autostadt, Autopia)"), ""),
            (arabic("  • النماذج الإقليمية (Motor World, Dubai Auto Zone)"), ""),
            (arabic("  • النماذج المحلية (معارض القادسية)"), ""),
            (arabic("لوحة التحليل الاتصالي"), "2"),
            (arabic("  • تحليل SWOT"), ""),
            (arabic("  • تحليل الفجوات الاتصالية"), ""),
            (arabic("  • خلاصة المقارنات المرجعية"), ""),
            (arabic("التوجه الاتصالي"), "3"),
            (arabic("  • مراحل الإعلام عن المشروع"), ""),
            (arabic("  • قضية الحملة وسيناريو الإعلان"), ""),
            (arabic("  • الأهداف الاتصالية"), ""),
            (arabic("منتجات الحملة الاتصالية"), "4"),
            (arabic("  • المرحلة الأولى: التهيئة"), ""),
            (arabic("  • المرحلة الثانية: الترسيخ"), ""),
            (arabic("  • المرحلة الثالثة: الزخم"), ""),
            (arabic("إدارة الأزمات الإعلامية"), "5"),
            (arabic("  • مصفوفة المخاطر"), ""),
            (arabic("  • خطة الاستجابة"), ""),
            (arabic("نظرة شاملة على الحملة"), "6"),
        ]
        
        y = title_y - 4*cm
        line_height = 0.8*cm
        
        for item, page_num in contents:
            if page_num:  # Main section
                self.pdf.setFillColor(COLORS['white'])
                self.pdf.setFont(self.arabic_font, 13)
            else:  # Sub-item
                self.pdf.setFillColor(COLORS['text_muted'])
                self.pdf.setFont(self.arabic_font, 11)
            
            # Draw text right-aligned
            self.pdf.drawRightString(self.width - self.margin, y, item)
            
            # Draw page number
            if page_num:
                self.pdf.setFillColor(COLORS['primary'])
                self.pdf.drawString(self.margin, y, page_num)
                
                # Dotted line
                self.pdf.setStrokeColor(COLORS['text_muted'])
                self.pdf.setLineWidth(0.5)
                self.pdf.setDash(2, 3)
                self.pdf.line(self.margin + 0.5*cm, y - 0.1*cm, 
                             self.width - self.margin - len(item)*0.15*cm, y - 0.1*cm)
                self.pdf.setDash()
            
            y -= line_height
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: Benchmark Study
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_benchmark_section(self):
        """Draw the benchmark study section"""
        self.new_page()
        
        # Section header
        self.draw_section_header(
            arabic("الدراسة التفصيلية"),
            "Detailed Benchmark Study",
            arabic("تحليل شامل للنماذج العالمية والإقليمية والمحلية"),
            COLORS['accent_blue']
        )
        
        y = self.height - 8*cm
        
        # Introduction text
        intro_text = arabic(
            "تتضمن هذه الدراسة تحليلاً معمقاً لأنجح النماذج العالمية والإقليمية في مجال مدن السيارات المتكاملة، "
            "بهدف استخلاص الدروس والممارسات الناجحة التي يمكن تطبيقها في مشروع موتور سيتي."
        )
        self.draw_paragraph(intro_text, self.margin, y, self.width - 2*self.margin)
        
        y -= 3*cm
        
        # Three levels overview
        levels = [
            (arabic("المستوى العالمي"), "🌍", COLORS['accent_blue'], 
             ["Autostadt - " + arabic("ألمانيا"), "Autopia Istanbul - " + arabic("تركيا")]),
            (arabic("المستوى الإقليمي"), "🌏", COLORS['accent'], 
             ["Motor World - " + arabic("أبوظبي"), "Dubai Auto Zone - " + arabic("دبي"), arabic("معارض القادسية - السعودية")]),
            (arabic("المستوى المحلي"), "🏠", COLORS['primary'], 
             [arabic("المنطقة الحرة - الزرقاء")]),
        ]
        
        box_width = (self.width - 2*self.margin - 1*cm) / 3
        
        for i, (title, icon, color, models) in enumerate(levels):
            x = self.margin + i * (box_width + 0.5*cm)
            
            # Box background
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - 5*cm, box_width, 5*cm, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Border
            self.pdf.setStrokeColor(color)
            self.pdf.setLineWidth(2)
            self.pdf.roundRect(x, y - 5*cm, box_width, 5*cm, 10, fill=False, stroke=True)
            
            # Title
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 14)
            self.pdf.drawCentredString(x + box_width/2, y - 0.8*cm, title)
            
            # Models list
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            model_y = y - 1.8*cm
            for model in models:
                self.pdf.drawCentredString(x + box_width/2, model_y, model)
                model_y -= 0.7*cm
    
    def draw_autostadt_case(self):
        """Draw Autostadt case study"""
        self.new_page()
        
        # Case study header
        self.draw_case_header(
            "Autostadt",
            arabic("ألمانيا"),
            COLORS['accent_blue'],
            "🇩🇪"
        )
        
        y = self.height - 9*cm
        
        # Key stats
        stats = [
            ("28", arabic("هكتار")),
            ("2M+", arabic("زائر سنوياً")),
            ("€430M", arabic("استثمار")),
        ]
        self.draw_stats_row(stats, y, COLORS['accent_blue'])
        
        y -= 4*cm
        
        # Description
        desc = arabic(
            "أوتوشتات (مدينة السيارات) في فولفسبورغ، ألمانيا، هي الوجهة السياحية الأولى في ألمانيا خارج برلين. "
            "تأسست عام 2000 كمتنزه ترفيهي تعليمي يجمع بين عرض السيارات والتجربة التفاعلية."
        )
        self.draw_paragraph(desc, self.margin, y, self.width - 2*self.margin)
        
        y -= 3*cm
        
        # Key learnings
        learnings = [
            arabic("التجربة الغامرة: تحويل شراء السيارة إلى رحلة عاطفية"),
            arabic("التكامل التقني: استخدام التكنولوجيا في كل نقطة تفاعل"),
            arabic("العلامة التجارية: ربط الزيارة بقيم Volkswagen"),
            arabic("الاستدامة: التركيز على السيارات الكهربائية والمستقبل"),
        ]
        self.draw_bullet_list(learnings, y, COLORS['accent_blue'])
    
    def draw_motor_world_case(self):
        """Draw Motor World Abu Dhabi case study"""
        self.new_page()
        
        self.draw_case_header(
            "Motor World",
            arabic("أبوظبي"),
            COLORS['accent'],
            "🇦🇪"
        )
        
        y = self.height - 9*cm
        
        stats = [
            ("250K", arabic("م² مغطاة")),
            ("50+", arabic("معرض")),
            ("100%", arabic("إشغال")),
        ]
        self.draw_stats_row(stats, y, COLORS['accent'])
        
        y -= 4*cm
        
        desc = arabic(
            "أكبر مجمع سيارات مغطى في الشرق الأوسط. يوفر بيئة متكاملة للتجار والمشترين "
            "مع تكييف كامل وخدمات شاملة تشمل التمويل والتأمين والترخيص."
        )
        self.draw_paragraph(desc, self.margin, y, self.width - 2*self.margin)
        
        y -= 3*cm
        
        learnings = [
            arabic("البنية التحتية المتميزة: تكييف كامل في صحراء الخليج"),
            arabic("الخدمات المتكاملة: كل ما يحتاجه المشتري في مكان واحد"),
            arabic("الحوافز الضريبية: إعفاءات ضريبية جذبت التجار"),
            arabic("التسويق الإقليمي: استهداف أسواق الخليج كاملة"),
        ]
        self.draw_bullet_list(learnings, y, COLORS['accent'])
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: SWOT Analysis
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_swot_section(self):
        """Draw SWOT analysis section"""
        self.new_page()
        
        self.draw_section_header(
            arabic("تحليل الموقف الاتصالي"),
            "SWOT Analysis",
            arabic("تحليل نقاط القوة والضعف والفرص والتهديدات"),
            COLORS['primary']
        )
        
        y = self.height - 9*cm
        box_height = 8*cm
        box_width = (self.width - 2*self.margin - 1*cm) / 2
        
        swot_data = [
            (arabic("نقاط القوة"), COLORS['accent'], [
                arabic("طلب سوقي مثبت من 352 معرض"),
                arabic("نماذج ناجحة عالمياً"),
                arabic("خبرة نوبلز في 7 مشاريع"),
                arabic("موقع استراتيجي متميز"),
            ]),
            (arabic("نقاط الضعف"), COLORS['primary'], [
                arabic("مشروع جديد لم يثبت نجاحه"),
                arabic("مقاومة التغيير من التجار"),
                arabic("تكاليف الانتقال المرتفعة"),
                arabic("ضعف الوعي بالمفهوم"),
            ]),
            (arabic("الفرص"), COLORS['accent_blue'], [
                arabic("فجوة سوقية - لا منافس مباشر"),
                arabic("دعم حكومي متوقع"),
                arabic("نمو سوق السيارات"),
                arabic("فرصة سياحة السيارات"),
            ]),
            (arabic("التهديدات"), COLORS['accent_orange'], [
                arabic("الوضع الاقتصادي الصعب"),
                arabic("مقاومة التجار المنظمة"),
                arabic("الرسوم الجمركية"),
                arabic("البيع الإلكتروني"),
            ]),
        ]
        
        for i, (title, color, items) in enumerate(swot_data):
            row = i // 2
            col = i % 2
            x = self.margin + col * (box_width + 0.5*cm)
            box_y = y - row * (box_height + 0.5*cm)
            
            # Box background
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(x, box_y - box_height, box_width, box_height, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Top border
            self.pdf.setStrokeColor(color)
            self.pdf.setLineWidth(4)
            self.pdf.line(x, box_y, x + box_width, box_y)
            
            # Title
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 14)
            self.pdf.drawRightString(x + box_width - 0.5*cm, box_y - 1*cm, title)
            
            # Items
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            item_y = box_y - 2*cm
            for item in items:
                self.pdf.drawRightString(x + box_width - 0.5*cm, item_y, "• " + item)
                item_y -= 0.7*cm
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: Communication Gaps
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_gaps_section(self):
        """Draw communication gaps section"""
        self.new_page()
        
        self.draw_section_header(
            arabic("تحليل الفجوات الاتصالية"),
            "Communication Gaps Analysis",
            arabic("الفجوات الرئيسية واستراتيجيات سدها"),
            COLORS['accent_purple']
        )
        
        y = self.height - 9*cm
        
        gaps = [
            (arabic("فجوة الوعي"), COLORS['primary'], arabic("حرجة"),
             arabic("مفهوم مدينة السيارات غير معروف في السوق الأردني")),
            (arabic("فجوة الثقة"), COLORS['accent_orange'], arabic("عالية"),
             arabic("31.9% من التجار متخوفون من البائعين غير المنظمين")),
            (arabic("فجوة المعلومات"), COLORS['accent_blue'], arabic("متوسطة"),
             arabic("التجار لا يعرفون قصص النجاح العالمية والعوائد المتوقعة")),
            (arabic("فجوة القيمة"), COLORS['accent'], arabic("متوسطة"),
             arabic("80% من المعارض تبيع أقل من 5 سيارات شهرياً لكن لا يربطون ذلك بالبيئة")),
        ]
        
        box_height = 2.5*cm
        
        for i, (title, color, severity, description) in enumerate(gaps):
            box_y = y - i * (box_height + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(self.margin, box_y - box_height, 
                              self.width - 2*self.margin, box_height, 10, 
                              fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Left border
            self.pdf.setFillColor(color)
            self.pdf.rect(self.margin, box_y - box_height, 0.3*cm, box_height, 
                         fill=True, stroke=False)
            
            # Title
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 13)
            self.pdf.drawRightString(self.width - self.margin - 0.5*cm, box_y - 0.8*cm, title)
            
            # Severity badge
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.3)
            self.pdf.roundRect(self.margin + 0.5*cm, box_y - 1.2*cm, 2*cm, 0.7*cm, 5, 
                              fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 9)
            self.pdf.drawCentredString(self.margin + 1.5*cm, box_y - 0.9*cm, severity)
            
            # Description
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawRightString(self.width - self.margin - 0.5*cm, box_y - 1.8*cm, description)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: Campaign Products
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_campaign_products_section(self):
        """Draw campaign products section"""
        self.new_page()
        
        self.draw_section_header(
            arabic("منتجات الحملة الاتصالية"),
            "Campaign Products",
            arabic("17 منتج اتصالي موزعة على 3 مراحل"),
            COLORS['accent']
        )
        
        y = self.height - 9*cm
        
        # Phase overview
        phases = [
            (arabic("المرحلة الأولى"), arabic("التهيئة"), "5", COLORS['primary']),
            (arabic("المرحلة الثانية"), arabic("الترسيخ"), "7", COLORS['accent_blue']),
            (arabic("المرحلة الثالثة"), arabic("الزخم"), "5", COLORS['accent']),
        ]
        
        box_width = (self.width - 2*self.margin - 1*cm) / 3
        
        for i, (phase, name, count, color) in enumerate(phases):
            x = self.margin + i * (box_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - 3.5*cm, box_width, 3.5*cm, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Phase name
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 12)
            self.pdf.drawCentredString(x + box_width/2, y - 0.8*cm, phase)
            
            # Phase title
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 16)
            self.pdf.drawCentredString(x + box_width/2, y - 1.6*cm, name)
            
            # Count
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 24)
            self.pdf.drawCentredString(x + box_width/2, y - 2.7*cm, count)
            
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(x + box_width/2, y - 3.2*cm, arabic("منتج"))
        
        y -= 5*cm
        
        # Phase 1 products detail
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawRightString(self.width - self.margin, y, arabic("منتجات المرحلة الأولى:"))
        
        y -= 1*cm
        
        phase1_products = [
            arabic("المؤتمر الصحفي الرسمي"),
            arabic("البيان الصحفي الرسمي"),
            arabic("ظهور متحدث رؤية عمان"),
            arabic("دعم كتاب الرأي والمؤثرين"),
            arabic("فيديو وثائقي للمشروع"),
        ]
        
        self.draw_bullet_list(phase1_products, y, COLORS['primary'])
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: Crisis Management
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_crisis_section(self):
        """Draw crisis management section"""
        self.new_page()
        
        self.draw_section_header(
            arabic("إدارة الأزمات الإعلامية"),
            "Crisis Management Plan",
            arabic("6 مخاطر محددة و3 مستويات تصعيد"),
            COLORS['primary']
        )
        
        y = self.height - 9*cm
        
        # Risk matrix intro
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 12)
        self.pdf.drawRightString(self.width - self.margin, y, 
            arabic("مصفوفة المخاطر (الاحتمالية × التأثير):"))
        
        y -= 1.5*cm
        
        risks = [
            (arabic("معارضة التجار"), "16", COLORS['primary']),
            (arabic("تغطية إعلامية سلبية"), "12", COLORS['accent_orange']),
            (arabic("حملات سوشيال ميديا"), "8", COLORS['accent_orange']),
            (arabic("شائعات ومعلومات مغلوطة"), "6", COLORS['accent_blue']),
            (arabic("ضغوط سياسية"), "4", COLORS['accent_blue']),
            (arabic("تأخر التنفيذ"), "4", COLORS['accent']),
        ]
        
        for i, (risk, score, color) in enumerate(risks):
            row = i // 2
            col = i % 2
            
            box_width = (self.width - 2*self.margin - 0.5*cm) / 2
            x = self.margin + col * (box_width + 0.5*cm)
            box_y = y - row * 1.5*cm
            
            # Background
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(x, box_y - 1.2*cm, box_width, 1.2*cm, 6, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Score circle
            self.pdf.setFillColor(color)
            self.pdf.circle(x + 0.8*cm, box_y - 0.6*cm, 0.4*cm, fill=True, stroke=False)
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 9)
            self.pdf.drawCentredString(x + 0.8*cm, box_y - 0.7*cm, score)
            
            # Risk name
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 11)
            self.pdf.drawRightString(x + box_width - 0.5*cm, box_y - 0.7*cm, risk)
        
        y -= 5.5*cm
        
        # Escalation levels
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawRightString(self.width - self.margin, y, arabic("مستويات التصعيد:"))
        
        y -= 1.5*cm
        
        levels = [
            (arabic("أخضر - عادي"), COLORS['accent'], arabic("الفريق الميداني")),
            (arabic("أصفر - متوسط"), COLORS['accent_orange'], arabic("المدير التنفيذي")),
            (arabic("أحمر - حرج"), COLORS['primary'], arabic("الرئيس التنفيذي")),
        ]
        
        level_width = (self.width - 2*self.margin - 1*cm) / 3
        
        for i, (level, color, handler) in enumerate(levels):
            x = self.margin + i * (level_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.2)
            self.pdf.roundRect(x, y - 2*cm, level_width, 2*cm, 8, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Level name
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 11)
            self.pdf.drawCentredString(x + level_width/2, y - 0.7*cm, level)
            
            # Handler
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(x + level_width/2, y - 1.5*cm, handler)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Section: Campaign Overview
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_overview_section(self):
        """Draw campaign overview section"""
        self.new_page()
        
        self.draw_section_header(
            arabic("نظرة شاملة على الحملة"),
            "Campaign Overview Dashboard",
            arabic("ملخص تنفيذي للخطة الاتصالية"),
            COLORS['accent_blue']
        )
        
        y = self.height - 9*cm
        
        # Key metrics
        metrics = [
            ("17", arabic("منتج اتصالي")),
            ("3", arabic("مراحل")),
            ("3", arabic("أشهر")),
            ("$35K", arabic("الميزانية")),
        ]
        
        box_width = (self.width - 2*self.margin - 1.5*cm) / 4
        
        for i, (value, label) in enumerate(metrics):
            x = self.margin + i * (box_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(COLORS['accent_blue'])
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - 2.5*cm, box_width, 2.5*cm, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Value
            self.pdf.setFillColor(COLORS['white'])
            self.pdf.setFont(self.arabic_font, 24)
            self.pdf.drawCentredString(x + box_width/2, y - 1*cm, value)
            
            # Label
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(x + box_width/2, y - 2*cm, label)
        
        y -= 4.5*cm
        
        # Timeline
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawRightString(self.width - self.margin, y, arabic("الجدول الزمني:"))
        
        y -= 1.5*cm
        
        timeline = [
            (arabic("مارس 2026"), arabic("التهيئة والإعلان")),
            (arabic("أبريل 2026"), arabic("الترسيخ والتوسع")),
            (arabic("مايو 2026"), arabic("بناء الزخم")),
        ]
        
        for month, activity in timeline:
            # Month box
            self.pdf.setFillColor(COLORS['primary'])
            self.pdf.setFillAlpha(0.2)
            self.pdf.roundRect(self.width - self.margin - 3*cm, y - 0.8*cm, 3*cm, 0.8*cm, 5, 
                              fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            self.pdf.setFillColor(COLORS['primary'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(self.width - self.margin - 1.5*cm, y - 0.5*cm, month)
            
            # Activity
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.drawRightString(self.width - self.margin - 3.5*cm, y - 0.5*cm, activity)
            
            y -= 1.2*cm
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════
    def draw_section_header(self, title_ar, title_en, subtitle, color):
        """Draw a section header"""
        y = self.height - 4*cm
        
        # Icon box
        self.pdf.setFillColor(color)
        self.pdf.roundRect(self.width/2 - 1.5*cm, y + 0.5*cm, 3*cm, 2*cm, 15, fill=True, stroke=False)
        
        # Title
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 26)
        self.pdf.drawCentredString(self.width/2, y - 2*cm, title_ar)
        
        # English title
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, y - 3*cm, title_en)
        
        # Subtitle
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 12)
        self.pdf.drawCentredString(self.width/2, y - 4*cm, subtitle)
        
        # Divider
        self.pdf.setStrokeColor(color)
        self.pdf.setLineWidth(2)
        self.pdf.line(self.margin, y - 5*cm, self.width - self.margin, y - 5*cm)
    
    def draw_case_header(self, name, country, color, flag):
        """Draw a case study header"""
        y = self.height - 4*cm
        
        # Background bar
        self.pdf.setFillColor(color)
        self.pdf.setFillAlpha(0.1)
        self.pdf.rect(0, y - 1*cm, self.width, 4*cm, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
        
        # Name
        self.pdf.setFillColor(COLORS['white'])
        self.pdf.setFont(self.arabic_font, 28)
        self.pdf.drawCentredString(self.width/2, y + 1*cm, name)
        
        # Country
        self.pdf.setFillColor(color)
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, y, country)
    
    def draw_stats_row(self, stats, y, color):
        """Draw a row of statistics"""
        box_width = (self.width - 2*self.margin - 1*cm) / len(stats)
        
        for i, (value, label) in enumerate(stats):
            x = self.margin + i * (box_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(x, y - 2*cm, box_width, 2*cm, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Value
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 22)
            self.pdf.drawCentredString(x + box_width/2, y - 0.8*cm, value)
            
            # Label
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(x + box_width/2, y - 1.5*cm, label)
    
    def draw_paragraph(self, text, x, y, width):
        """Draw a paragraph of text"""
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 11)
        
        # Simple word wrapping
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.pdf.stringWidth(test_line, self.arabic_font, 11) > width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        line_height = 0.6*cm
        for i, line in enumerate(lines):
            self.pdf.drawRightString(x + width, y - i * line_height, line)
    
    def draw_bullet_list(self, items, y, color):
        """Draw a bullet list"""
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 11)
        
        for i, item in enumerate(items):
            item_y = y - i * 0.7*cm
            
            # Bullet
            self.pdf.setFillColor(color)
            self.pdf.circle(self.width - self.margin - 0.2*cm, item_y + 0.1*cm, 0.1*cm, fill=True, stroke=False)
            
            # Text
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.drawRightString(self.width - self.margin - 0.5*cm, item_y, item)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Generate PDF
    # ═══════════════════════════════════════════════════════════════════════════════
    def generate(self):
        """Generate the complete PDF"""
        print(arabic("جاري إنشاء ملف PDF للخطة الاستراتيجية..."))
        
        # Cover page
        self.draw_cover_page()
        
        # Table of contents
        self.draw_table_of_contents()
        
        # Benchmark section
        self.draw_benchmark_section()
        self.draw_autostadt_case()
        self.draw_motor_world_case()
        
        # SWOT Analysis
        self.draw_swot_section()
        
        # Communication Gaps
        self.draw_gaps_section()
        
        # Campaign Products
        self.draw_campaign_products_section()
        
        # Crisis Management
        self.draw_crisis_section()
        
        # Campaign Overview
        self.draw_overview_section()
        
        # Final page number and save
        self.add_page_number()
        self.pdf.save()
        
        print(f"\n✅ تم إنشاء الملف بنجاح: {self.output_path}")
        print(f"📄 عدد الصفحات: {self.page_number}")
        return self.output_path


# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Output path
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Motor_City_Strategic_Plan.pdf")
    
    # Generate PDF
    pdf_generator = MotorCityStrategicPlanPDF(output_path)
    pdf_generator.generate()
    
    print(f"\n{'='*60}")
    print(arabic("تم إنشاء ملف PDF الخطة الاستراتيجية لمشروع موتور سيتي"))
    print(f"{'='*60}")
