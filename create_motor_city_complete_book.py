#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
كتاب موتور سيتي الكامل - PDF احترافي
Motor City Complete Professional Book
"""

from fpdf import FPDF
import os
import urllib.request
import tempfile

# الألوان
COLORS = {
    'primary': (220, 31, 39),
    'secondary': (15, 23, 42),
    'accent': (251, 191, 36),
    'emerald': (16, 185, 129),
    'cyan': (6, 182, 212),
    'purple': (139, 92, 246),
    'dark': (30, 41, 59),
    'white': (255, 255, 255),
    'gray': (100, 116, 139),
    'lightgray': (148, 163, 184),
}

def download_font():
    """تحميل الخط العربي"""
    temp_dir = tempfile.gettempdir()
    font_dir = os.path.join(temp_dir, "arabic_fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    fonts = {
        'Regular': 'https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf',
        'Bold': 'https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf',
    }
    
    paths = {}
    for name, url in fonts.items():
        path = os.path.join(font_dir, f"NotoSansArabic-{name}.ttf")
        if not os.path.exists(path):
            print(f"📥 تحميل {name}...")
            urllib.request.urlretrieve(url, path)
        paths[name] = path
    return paths


class MotorCityBook(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=20)
        fonts = download_font()
        self.add_font('Arabic', '', fonts['Regular'])
        self.add_font('Arabic', 'B', fonts['Bold'])
        self.set_text_shaping(True)
    
    def gradient_bg(self, c1, c2):
        """خلفية متدرجة"""
        r1, g1, b1 = COLORS[c1]
        r2, g2, b2 = COLORS[c2]
        for i in range(60):
            ratio = i / 60
            self.set_fill_color(int(r1+(r2-r1)*ratio), int(g1+(g2-g1)*ratio), int(b1+(b2-b1)*ratio))
            self.rect(0, i*5, 210, 6, 'F')
    
    def header_bar(self, text, color='secondary'):
        """شريط علوي"""
        self.set_fill_color(*COLORS[color])
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Arabic', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 5)
        self.cell(0, 8, text, align='C')
    
    def section_title(self, title, subtitle='', icon_color='primary'):
        """عنوان قسم"""
        self.set_font('Arabic', 'B', 18)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(20, self.get_y() + 5)
        self.cell(170, 10, title, align='R')
        if subtitle:
            self.set_font('Arabic', '', 10)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(20, self.get_y() + 10)
            self.cell(170, 6, subtitle, align='R')
        # خط تحت العنوان
        self.set_draw_color(*COLORS[icon_color])
        self.set_line_width(1.5)
        self.line(145, self.get_y() + 18, 190, self.get_y() + 18)
        self.set_y(self.get_y() + 25)
    
    def info_box(self, label, value, color='primary'):
        """مربع معلومة"""
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*COLORS[color])
        self.set_draw_color(*COLORS[color])
        self.rect(x, y, 50, 35, 'D')
        self.set_font('Arabic', 'B', 14)
        self.set_text_color(*COLORS[color])
        self.set_xy(x, y + 8)
        self.cell(50, 8, value, align='C')
        self.set_font('Arabic', '', 8)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(x, y + 20)
        self.cell(50, 6, label, align='C')
    
    def bullet_item(self, text, color='primary'):
        """عنصر نقطي"""
        self.set_fill_color(*COLORS[color])
        self.ellipse(185, self.get_y() + 3, 4, 4, 'F')
        self.set_font('Arabic', '', 10)
        self.set_text_color(*COLORS['dark'])
        self.set_x(20)
        self.multi_cell(160, 7, text, align='R')
        self.set_y(self.get_y() + 2)
    
    def data_row(self, label, value):
        """صف بيانات"""
        y = self.get_y()
        self.set_fill_color(248, 250, 252)
        self.rect(20, y, 170, 12, 'F')
        self.set_font('Arabic', 'B', 10)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(100, y + 3)
        self.cell(90, 6, value, align='R')
        self.set_font('Arabic', '', 10)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, y + 3)
        self.cell(80, 6, label, align='R')
        self.set_y(y + 14)
    
    def stat_card(self, value, label, color='emerald'):
        """بطاقة إحصائية"""
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*COLORS[color])
        self.rect(x, y, 40, 28, 'F')
        self.set_font('Arabic', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(x, y + 5)
        self.cell(40, 8, value, align='C')
        self.set_font('Arabic', '', 7)
        self.set_xy(x, y + 16)
        self.cell(40, 6, label, align='C')
    
    def page_number(self):
        """رقم الصفحة"""
        self.set_font('Arabic', '', 9)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 285)
        self.cell(0, 8, str(self.page_no()), align='C')

    # ═══════════════════════════════════════════════════════════════
    # صفحات الكتاب
    # ═══════════════════════════════════════════════════════════════
    
    def front_cover(self):
        """الغلاف الأمامي"""
        self.add_page()
        self.gradient_bg('secondary', 'dark')
        
        # شريط أحمر
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 0, 210, 8, 'F')
        self.set_fill_color(*COLORS['accent'])
        self.rect(0, 8, 210, 2, 'F')
        
        # الشعار
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 25)
        self.cell(0, 10, 'NOBLES REAL ESTATE', align='C')
        
        self.set_font('Arabic', 'B', 14)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 38)
        self.cell(0, 10, 'نوبلز العقارية', align='C')
        
        # العنوان
        self.set_font('helvetica', 'B', 48)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 100)
        self.cell(0, 20, 'MOTOR CITY', align='C')
        
        self.set_font('Arabic', 'B', 36)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 125)
        self.cell(0, 15, 'موتور سيتي', align='C')
        
        # خط زخرفي
        self.set_draw_color(*COLORS['accent'])
        self.set_line_width(0.5)
        self.line(75, 148, 135, 148)
        
        # العنوان الفرعي
        self.set_font('Arabic', '', 14)
        self.set_text_color(*COLORS['lightgray'])
        self.set_xy(0, 160)
        self.cell(0, 8, 'الخطة الاستراتيجية للاتصال والعلاقات العامة', align='C')
        
        # معلومات
        info = ['منطقة أحد، شرق عمان، الأردن', '210,000 متر مربع', '757 معرض سيارات']
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['accent'])
        y = 190
        for i in info:
            self.set_xy(0, y)
            self.cell(0, 7, i, align='C')
            y += 9
        
        # التاريخ
        self.set_font('Arabic', '', 10)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 270)
        self.cell(0, 8, 'يناير 2026', align='C')
        
        # شريط سفلي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 289, 210, 8, 'F')
    
    def title_page(self):
        """صفحة العنوان"""
        self.add_page()
        
        # إطار
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(1)
        self.rect(15, 15, 180, 267, 'D')
        
        # العنوان
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(0, 60)
        self.cell(0, 15, 'MOTOR CITY', align='C')
        
        self.set_font('Arabic', 'B', 26)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(0, 80)
        self.cell(0, 12, 'موتور سيتي', align='C')
        
        # العنوان الفرعي
        self.set_font('Arabic', '', 14)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(0, 115)
        self.cell(0, 8, 'الخطة الاستراتيجية المتكاملة للاتصال والعلاقات العامة', align='C')
        
        # معلومات النشر
        info = ['إعداد: منصة 24°45°', 'لصالح: نوبلز العقارية', 'الإصدار: 1.0', 'التاريخ: يناير 2026']
        self.set_font('Arabic', '', 11)
        y = 160
        for i in info:
            self.set_xy(0, y)
            self.cell(0, 10, i, align='C')
            y += 12
        
        # حقوق النشر
        self.set_font('Arabic', '', 9)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 260)
        self.cell(0, 8, 'جميع الحقوق محفوظة © نوبلز العقارية 2026', align='C')
    
    def toc_page(self):
        """فهرس المحتويات"""
        self.add_page()
        
        self.set_font('Arabic', 'B', 24)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(0, 30)
        self.cell(0, 12, 'فهرس المحتويات', align='C')
        
        self.set_draw_color(*COLORS['primary'])
        self.line(75, 48, 135, 48)
        
        items = [
            ('المقدمة', '4'),
            ('القسم الأول: نظرة عامة على المشروع', '6'),
            ('القسم الثاني: الوضع الراهن لسوق السيارات', '12'),
            ('القسم الثالث: المقارنات المعيارية الدولية', '22'),
            ('القسم الرابع: الخطة الاستراتيجية', '32'),
        ]
        
        y = 70
        for i, (title, page) in enumerate(items, 1):
            # رقم
            self.set_fill_color(*COLORS['primary'])
            self.ellipse(25, y, 8, 8, 'F')
            self.set_font('helvetica', 'B', 10)
            self.set_text_color(255, 255, 255)
            self.set_xy(25, y + 1)
            self.cell(8, 6, str(i), align='C')
            
            # العنوان
            self.set_font('Arabic', 'B', 12)
            self.set_text_color(*COLORS['secondary'])
            self.set_xy(40, y)
            self.cell(120, 8, title, align='L')
            
            # رقم الصفحة
            self.set_font('helvetica', 'B', 12)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(175, y)
            self.cell(15, 8, page, align='R')
            
            y += 25
    
    def section_divider(self, num, title_ar, title_en, color='primary'):
        """فاصل قسم"""
        self.add_page()
        self.gradient_bg('secondary', 'dark')
        
        # دائرة
        self.set_fill_color(30, 58, 95)
        self.ellipse(35, 78, 140, 140, 'F')
        self.set_draw_color(*COLORS[color])
        self.set_line_width(2)
        self.ellipse(50, 93, 110, 110, 'D')
        
        # الرقم
        self.set_font('helvetica', 'B', 72)
        self.set_text_color(*COLORS[color])
        self.set_xy(0, 120)
        self.cell(0, 30, str(num), align='C')
        
        # العناوين
        self.set_font('Arabic', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 165)
        self.cell(0, 12, title_ar, align='C')
        
        self.set_font('helvetica', '', 16)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 182)
        self.cell(0, 10, title_en, align='C')
    
    def introduction(self):
        """المقدمة"""
        self.add_page()
        self.header_bar('المقدمة')
        self.set_y(30)
        self.section_title('مقدمة', 'Introduction')
        
        text = """يمثل مشروع موتور سيتي نقلة نوعية في قطاع معارض السيارات في الأردن، حيث يهدف إلى إنشاء أول مدينة متكاملة ومتخصصة لمعارض السيارات في المملكة.

يقع المشروع في منطقة أحد شرق عمان على مساحة إجمالية تبلغ 210,000 متر مربع، ويضم 757 معرضاً للسيارات مع كافة الخدمات المساندة والبنية التحتية المتكاملة.

تم إعداد هذه الخطة الاستراتيجية للاتصال والعلاقات العامة لتحقيق الأهداف التالية:"""
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y())
        self.multi_cell(170, 8, text, align='R')
        
        self.set_y(self.get_y() + 10)
        objectives = [
            'بناء الوعي بالمشروع وترسيخ مكانته كوجهة رئيسية لقطاع السيارات',
            'جذب المستأجرين والمستثمرين المحتملين من أصحاب المعارض',
            'تعزيز السمعة المؤسسية لشركة نوبلز العقارية في السوق الأردني',
            'إدارة التوقعات والتواصل الفعال مع جميع أصحاب المصلحة',
        ]
        for obj in objectives:
            self.bullet_item(obj)
        
        self.set_y(self.get_y() + 10)
        text2 = """تستند هذه الخطة إلى دراسة معيارية شاملة لأفضل الممارسات العالمية في مدن السيارات، بالإضافة إلى دراسة ميدانية للسوق المحلي شملت أكثر من 350 معرضاً في عمان."""
        
        self.set_font('Arabic', '', 11)
        self.set_xy(20, self.get_y())
        self.multi_cell(170, 8, text2, align='R')
        self.page_number()
    
    def overview_section(self):
        """قسم نظرة عامة"""
        self.section_divider(1, 'نظرة عامة', 'Overview', 'emerald')
        
        # صفحة معلومات المشروع
        self.add_page()
        self.header_bar('القسم الأول: نظرة عامة')
        self.set_y(30)
        self.section_title('معلومات المشروع الأساسية', 'Project Information', 'emerald')
        
        data = [
            ('اسم المشروع', 'موتور سيتي - Motor City'),
            ('الموقع', 'منطقة أحد، شرق عمان، الأردن'),
            ('المساحة الإجمالية', '210,000 متر مربع'),
            ('عدد المعارض', '757 معرض سيارات'),
            ('نوع المشروع', 'مدينة سيارات متكاملة'),
            ('المطور', 'شركة نوبلز العقارية'),
            ('تاريخ التسليم المتوقع', '2027'),
        ]
        for label, value in data:
            self.data_row(label, value)
        self.page_number()
        
        # صفحة الرؤية والرسالة
        self.add_page()
        self.header_bar('القسم الأول: نظرة عامة')
        self.set_y(30)
        self.section_title('الرؤية والرسالة', 'Vision & Mission', 'emerald')
        
        self.set_font('Arabic', 'B', 12)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(20, self.get_y())
        self.cell(170, 8, 'الرؤية', align='R')
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y() + 10)
        self.multi_cell(170, 8, 'أن تصبح موتور سيتي الوجهة الأولى والمرجعية الرائدة لقطاع السيارات في الأردن والمنطقة، ونموذجاً يحتذى به في التخطيط العمراني المتخصص.', align='R')
        
        self.set_y(self.get_y() + 15)
        self.set_font('Arabic', 'B', 12)
        self.set_text_color(*COLORS['cyan'])
        self.set_xy(20, self.get_y())
        self.cell(170, 8, 'الرسالة', align='R')
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y() + 10)
        self.multi_cell(170, 8, 'توفير بيئة متكاملة ومتطورة لعرض وبيع وصيانة السيارات، تجمع بين الكفاءة التشغيلية والتجربة المميزة للعملاء، مع الالتزام بأعلى معايير الجودة والاستدامة.', align='R')
        self.page_number()
        
        # صفحة المزايا التنافسية
        self.add_page()
        self.header_bar('القسم الأول: نظرة عامة')
        self.set_y(30)
        self.section_title('المزايا التنافسية', 'Competitive Advantages', 'emerald')
        
        advantages = [
            'أول مدينة متكاملة ومتخصصة لمعارض السيارات في الأردن',
            'موقع استراتيجي على طريق عمان-الزرقاء السريع',
            'بنية تحتية متكاملة وحديثة (كهرباء، مياه، اتصالات، طرق)',
            'مساحات متنوعة تناسب جميع احتياجات المعارض',
            'خدمات مساندة شاملة (صيانة، تمويل، تأمين، ترخيص)',
            'أمن وحماية على مدار الساعة',
            'مواقف سيارات واسعة للزوار والعملاء',
            'سهولة الوصول من جميع مناطق عمان',
        ]
        for adv in advantages:
            self.bullet_item(adv, 'emerald')
        self.page_number()
        
        # صفحة القطاعات المستهدفة
        self.add_page()
        self.header_bar('القسم الأول: نظرة عامة')
        self.set_y(30)
        self.section_title('القطاعات المستهدفة', 'Target Sectors', 'emerald')
        
        sectors = [
            'معارض السيارات الجديدة (وكالات رسمية)',
            'معارض السيارات المستعملة',
            'مراكز صيانة وخدمة السيارات',
            'محلات قطع الغيار والإكسسوارات',
            'شركات تأجير السيارات',
            'شركات التأمين على السيارات',
            'البنوك وشركات التمويل',
            'مراكز الفحص الفني والترخيص',
        ]
        for sec in sectors:
            self.bullet_item(sec, 'purple')
        self.page_number()
    
    def current_status_section(self):
        """قسم الوضع الراهن"""
        self.section_divider(2, 'الوضع الراهن', 'Current Status', 'cyan')
        
        # صفحة منهجية الدراسة
        self.add_page()
        self.header_bar('القسم الثاني: الوضع الراهن')
        self.set_y(30)
        self.section_title('منهجية جمع البيانات', 'Data Collection Methodology', 'cyan')
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y())
        self.multi_cell(170, 8, 'تم إجراء دراسة ميدانية شاملة لسوق معارض السيارات في عمان خلال الفترة من 12 إلى 18 مارس 2025، بمشاركة فريق من 8 باحثين ميدانيين تحت إشراف مشرفين متخصصين.', align='R')
        
        # إحصائيات الدراسة
        self.set_y(self.get_y() + 15)
        self.set_x(25)
        self.stat_card('352', 'معرض مستطلع', 'primary')
        self.set_xy(70, self.get_y() - 28)
        self.stat_card('8', 'باحثين ميدانيين', 'emerald')
        self.set_xy(115, self.get_y() - 28)
        self.stat_card('7', 'أيام بحث', 'cyan')
        self.set_xy(160, self.get_y() - 28)
        self.stat_card('97%', 'معدل الاستجابة', 'accent')
        
        self.set_y(self.get_y() + 45)
        self.set_font('Arabic', 'B', 12)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(20, self.get_y())
        self.cell(170, 8, 'النطاق الجغرافي', align='R')
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y() + 10)
        self.multi_cell(170, 8, 'شمل المسح جميع مناطق عمان الرئيسية: شمال عمان، شرق عمان، غرب عمان، وجنوب عمان. تم زيارة 363 معرضاً، أكمل 352 منهم المقابلات بنجاح.', align='R')
        self.page_number()
        
        # صفحة التوزيع الجغرافي
        self.add_page()
        self.header_bar('القسم الثاني: الوضع الراهن')
        self.set_y(30)
        self.section_title('التوزيع الجغرافي للمعارض', 'Geographic Distribution', 'cyan')
        
        geo_data = [
            ('شمال عمان', '112 معرض', '31.8%'),
            ('شرق عمان', '98 معرض', '27.8%'),
            ('غرب عمان', '87 معرض', '24.7%'),
            ('جنوب عمان', '55 معرض', '15.7%'),
        ]
        
        for region, count, percent in geo_data:
            y = self.get_y()
            self.set_fill_color(248, 250, 252)
            self.rect(20, y, 170, 18, 'F')
            
            self.set_font('Arabic', 'B', 11)
            self.set_text_color(*COLORS['secondary'])
            self.set_xy(130, y + 5)
            self.cell(60, 8, region, align='R')
            
            self.set_font('Arabic', '', 10)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(70, y + 5)
            self.cell(50, 8, count, align='C')
            
            self.set_font('Arabic', 'B', 11)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(20, y + 5)
            self.cell(40, 8, percent, align='C')
            
            self.set_y(y + 22)
        self.page_number()
        
        # صفحة تحديات السوق
        self.add_page()
        self.header_bar('القسم الثاني: الوضع الراهن')
        self.set_y(30)
        self.section_title('تحديات السوق الرئيسية', 'Market Challenges', 'cyan')
        
        challenges = [
            ('البائعون غير المنظمين', '31.9%', 'يعتبرونهم أكبر تحدٍ يواجه السوق'),
            ('التحديات الاقتصادية', '24.1%', 'ارتفاع أسعار الوقود وضعف القدرة الشرائية'),
            ('الرسوم الجمركية', '11.2%', 'ارتفاع الضرائب والرسوم على السيارات'),
            ('المنافسة الشديدة', '9.5%', 'زيادة عدد المعارض وحدة المنافسة'),
            ('صعوبة التمويل', '8.2%', 'شروط البنوك وارتفاع الفوائد'),
        ]
        
        for challenge, percent, desc in challenges:
            y = self.get_y()
            self.set_fill_color(254, 242, 242)
            self.rect(20, y, 170, 22, 'F')
            
            self.set_font('Arabic', 'B', 11)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(130, y + 3)
            self.cell(60, 8, challenge, align='R')
            
            self.set_font('Arabic', 'B', 14)
            self.set_xy(20, y + 3)
            self.cell(40, 8, percent, align='C')
            
            self.set_font('Arabic', '', 9)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(60, y + 12)
            self.cell(130, 6, desc, align='R')
            
            self.set_y(y + 26)
        self.page_number()
        
        # صفحة مؤشرات التشغيل
        self.add_page()
        self.header_bar('القسم الثاني: الوضع الراهن')
        self.set_y(30)
        self.section_title('مؤشرات التشغيل', 'Operating Indicators', 'cyan')
        
        indicators = [
            ('المساحة الداخلية', '53.7% أقل من 50 م²'),
            ('المساحة الخارجية', '48.9% بين 10-100 م²'),
            ('السيارات المعروضة', '56.8% عشر سيارات أو أقل'),
            ('المبيعات الشهرية', '80.1% أقل من 5 سيارات'),
            ('الإيجار الشهري', '51.4% أقل من 500 دينار'),
            ('عدد الموظفين', '68.5% موظفين أو أقل'),
        ]
        
        for label, value in indicators:
            self.data_row(label, value)
        
        self.set_y(self.get_y() + 15)
        self.set_font('Arabic', 'B', 12)
        self.set_text_color(*COLORS['emerald'])
        self.set_xy(20, self.get_y())
        self.cell(170, 8, 'التطلعات المستقبلية', align='R')
        
        aspirations = [
            ('الرضا عن الموقع الحالي', '87.5%'),
            ('المهتمون بالانتقال لموقع جديد', '32.4%'),
            ('يفضلون موقعاً متكاملاً', '78.2%'),
        ]
        self.set_y(self.get_y() + 10)
        for label, value in aspirations:
            self.data_row(label, value)
        self.page_number()
    
    def benchmarks_section(self):
        """قسم المقارنات المعيارية"""
        self.section_divider(3, 'المقارنات المعيارية', 'Benchmarks', 'purple')
        
        # صفحة مقدمة المقارنات
        self.add_page()
        self.header_bar('القسم الثالث: المقارنات المعيارية')
        self.set_y(30)
        self.section_title('التجارب العالمية في مدن السيارات', 'Global Car City Experiences', 'purple')
        
        self.set_font('Arabic', '', 11)
        self.set_text_color(*COLORS['dark'])
        self.set_xy(20, self.get_y())
        self.multi_cell(170, 8, 'تم دراسة 6 تجارب عالمية وإقليمية ناجحة في مجال مدن ومجمعات السيارات المتكاملة، لاستخلاص أفضل الممارسات والدروس المستفادة التي يمكن تطبيقها في مشروع موتور سيتي.', align='R')
        
        benchmarks = [
            ('Autostadt Wolfsburg', 'Germany', '25 hectares - 2.5M visitors/year'),
            ('Autopia Istanbul', 'Turkey', 'Largest in Europe - 3,000 showrooms'),
            ('Motor World Abu Dhabi', 'UAE', 'Luxury automotive complex'),
            ('Dubai Auto Zone', 'UAE', 'Free zone for car trade'),
            ('Al-Qadisiya Showrooms', 'KSA', 'Largest car hub in Riyadh'),
            ('Zarqa Free Zone', 'Jordan', 'Local free zone experience'),
        ]
        
        self.set_y(self.get_y() + 10)
        for name, country, desc in benchmarks:
            y = self.get_y()
            self.set_fill_color(245, 243, 255)
            self.rect(20, y, 170, 24, 'F')
            
            self.set_font('helvetica', 'B', 11)
            self.set_text_color(*COLORS['purple'])
            self.set_xy(100, y + 3)
            self.cell(90, 8, name, align='R')
            
            self.set_font('helvetica', '', 9)
            self.set_text_color(*COLORS['accent'])
            self.set_xy(20, y + 3)
            self.cell(40, 8, country, align='C')
            
            self.set_font('helvetica', '', 9)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(20, y + 14)
            self.cell(170, 6, desc, align='R')
            
            self.set_y(y + 28)
        self.page_number()
        
        # صفحة الدروس المستفادة
        self.add_page()
        self.header_bar('القسم الثالث: المقارنات المعيارية')
        self.set_y(30)
        self.section_title('الدروس المستفادة', 'Key Learnings', 'purple')
        
        lessons = [
            'التكامل بين البيع والخدمات والترفيه عامل نجاح رئيسي',
            'الموقع الاستراتيجي وسهولة الوصول من أهم عوامل الجذب',
            'تنوع المساحات يلبي احتياجات مختلف المستأجرين',
            'الخدمات المساندة (تمويل، تأمين، ترخيص) تضيف قيمة كبيرة',
            'العلامة التجارية القوية تجذب الزوار والمستأجرين',
            'التقنية والرقمنة تحسن تجربة العملاء',
            'الفعاليات والأحداث تزيد من حركة الزوار',
            'الشراكات مع الوكالات الرسمية تعزز المصداقية',
        ]
        for lesson in lessons:
            self.bullet_item(lesson, 'purple')
        self.page_number()
    
    def strategic_plan_section(self):
        """قسم الخطة الاستراتيجية"""
        self.section_divider(4, 'الخطة الاستراتيجية', 'Strategic Plan', 'primary')
        
        # صفحة الأهداف
        self.add_page()
        self.header_bar('القسم الرابع: الخطة الاستراتيجية')
        self.set_y(30)
        self.section_title('الأهداف الاستراتيجية', 'Strategic Objectives', 'primary')
        
        objectives = [
            'بناء الوعي بموتور سيتي كوجهة رئيسية لقطاع السيارات في الأردن',
            'جذب 70% من المعارض المستهدفة للاستئجار خلال السنة الأولى',
            'تحقيق تغطية إعلامية واسعة في وسائل الإعلام المحلية والإقليمية',
            'بناء قاعدة بيانات تضم 500 عميل محتمل مؤهل',
            'تعزيز سمعة نوبلز العقارية كمطور موثوق في السوق الأردني',
        ]
        for obj in objectives:
            self.bullet_item(obj, 'primary')
        self.page_number()
        
        # صفحة الجمهور المستهدف
        self.add_page()
        self.header_bar('القسم الرابع: الخطة الاستراتيجية')
        self.set_y(30)
        self.section_title('الجمهور المستهدف', 'Target Audience', 'primary')
        
        audiences = [
            ('الجمهور الأساسي', 'أصحاب معارض السيارات الحاليين في عمان'),
            ('الجمهور الثانوي', 'المستثمرون في قطاع السيارات'),
            ('صناع القرار', 'الجهات الحكومية والتنظيمية'),
            ('المؤثرون', 'وسائل الإعلام والصحفيون المتخصصون'),
        ]
        
        for title, desc in audiences:
            y = self.get_y()
            self.set_font('Arabic', 'B', 11)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(20, y)
            self.cell(170, 8, title, align='R')
            
            self.set_font('Arabic', '', 10)
            self.set_text_color(*COLORS['dark'])
            self.set_xy(20, y + 10)
            self.cell(170, 6, desc, align='R')
            self.set_y(y + 22)
        self.page_number()
        
        # صفحة الرسائل الرئيسية
        self.add_page()
        self.header_bar('القسم الرابع: الخطة الاستراتيجية')
        self.set_y(30)
        self.section_title('الرسائل الرئيسية', 'Key Messages', 'primary')
        
        # الرسالة المركزية
        self.set_fill_color(254, 242, 242)
        self.rect(20, self.get_y(), 170, 35, 'F')
        self.set_font('Arabic', 'B', 10)
        self.set_text_color(*COLORS['primary'])
        self.set_xy(20, self.get_y() + 5)
        self.cell(170, 8, 'الرسالة المركزية', align='C')
        self.set_font('Arabic', 'B', 12)
        self.set_text_color(*COLORS['secondary'])
        self.set_xy(20, self.get_y() + 15)
        self.cell(170, 10, 'موتور سيتي: من التشتت إلى التكامل - مدينة السيارات الأولى في الأردن', align='C')
        
        self.set_y(self.get_y() + 45)
        messages = [
            'موقع استراتيجي يجمع كل ما يحتاجه قطاع السيارات في مكان واحد',
            'بنية تحتية متكاملة بمعايير عالمية',
            'فرصة استثمارية واعدة في سوق متنامٍ',
            'شريك موثوق بخبرة عالمية (نوبلز العقارية)',
        ]
        for msg in messages:
            self.bullet_item(msg, 'primary')
        self.page_number()
        
        # صفحة القنوات الاتصالية
        self.add_page()
        self.header_bar('القسم الرابع: الخطة الاستراتيجية')
        self.set_y(30)
        self.section_title('القنوات الاتصالية', 'Communication Channels', 'primary')
        
        channels = [
            ('العلاقات العامة', 'مؤتمرات صحفية، بيانات إعلامية، مقابلات حصرية'),
            ('الإعلام الرقمي', 'الموقع الإلكتروني، وسائل التواصل الاجتماعي'),
            ('التسويق المباشر', 'زيارات ميدانية، عروض تقديمية، اتصالات مباشرة'),
            ('الفعاليات', 'معارض متخصصة، أيام مفتوحة، جولات للمستثمرين'),
            ('الشراكات', 'تعاون مع غرفة التجارة، جمعيات تجار السيارات'),
        ]
        
        for channel, desc in channels:
            y = self.get_y()
            self.set_fill_color(248, 250, 252)
            self.rect(20, y, 170, 20, 'F')
            
            self.set_font('Arabic', 'B', 11)
            self.set_text_color(*COLORS['primary'])
            self.set_xy(130, y + 3)
            self.cell(60, 8, channel, align='R')
            
            self.set_font('Arabic', '', 9)
            self.set_text_color(*COLORS['gray'])
            self.set_xy(20, y + 10)
            self.cell(170, 6, desc, align='R')
            
            self.set_y(y + 24)
        self.page_number()
    
    def back_cover(self):
        """الغلاف الخلفي"""
        self.add_page()
        self.gradient_bg('dark', 'secondary')
        
        # شريط علوي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 0, 210, 8, 'F')
        
        # الشعار
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 110)
        self.cell(0, 15, 'NOBLES', align='C')
        
        self.set_font('helvetica', '', 18)
        self.set_xy(0, 128)
        self.cell(0, 12, 'REAL ESTATE', align='C')
        
        self.set_font('Arabic', 'B', 16)
        self.set_text_color(*COLORS['accent'])
        self.set_xy(0, 145)
        self.cell(0, 10, 'نوبلز العقارية', align='C')
        
        # خط زخرفي
        self.set_draw_color(*COLORS['accent'])
        self.line(75, 162, 135, 162)
        
        # معلومات التواصل
        contact = ['www.nobles.jo', 'info@nobles.jo', '+962 6 XXX XXXX']
        self.set_font('helvetica', '', 11)
        self.set_text_color(*COLORS['lightgray'])
        y = 175
        for c in contact:
            self.set_xy(0, y)
            self.cell(0, 8, c, align='C')
            y += 12
        
        # حقوق النشر
        self.set_font('helvetica', '', 9)
        self.set_text_color(*COLORS['gray'])
        self.set_xy(0, 260)
        self.cell(0, 8, '© 2026 Nobles Real Estate. All Rights Reserved.', align='C')
        
        # شريط سفلي
        self.set_fill_color(*COLORS['primary'])
        self.rect(0, 289, 210, 8, 'F')
    
    def build(self, filename='motor_city_complete.pdf'):
        """بناء الكتاب الكامل"""
        print("🚀 بدء إنشاء كتاب موتور سيتي الكامل...")
        
        print("  📖 الغلاف الأمامي...")
        self.front_cover()
        
        print("  📄 صفحة العنوان...")
        self.title_page()
        
        print("  📑 فهرس المحتويات...")
        self.toc_page()
        
        print("  📝 المقدمة...")
        self.introduction()
        
        print("  📊 قسم نظرة عامة...")
        self.overview_section()
        
        print("  📈 قسم الوضع الراهن...")
        self.current_status_section()
        
        print("  🌍 قسم المقارنات المعيارية...")
        self.benchmarks_section()
        
        print("  🎯 قسم الخطة الاستراتيجية...")
        self.strategic_plan_section()
        
        print("  📕 الغلاف الخلفي...")
        self.back_cover()
        
        self.output(filename)
        print(f"\n✅ تم إنشاء الكتاب: {filename}")
        print(f"   عدد الصفحات: {self.page_no()}")
        return filename


if __name__ == "__main__":
    book = MotorCityBook()
    book.build('motor_city_complete.pdf')
