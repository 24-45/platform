#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
24°45° Pitch Deck & MVP Document Generator
مولد عرض تقديمي للمستثمرين ووثيقة MVP
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

# ═══════════════════════════════════════════════════════════════════════════════
# Color Palette - 24°45° Brand Colors
# ═══════════════════════════════════════════════════════════════════════════════
COLORS = {
    'primary': HexColor('#1a5f7a'),       # Teal Blue
    'primary_dark': HexColor('#0d2137'),  # Dark Navy
    'accent': HexColor('#f9a825'),         # Golden Yellow
    'accent_green': HexColor('#10b981'),   # Emerald
    'accent_red': HexColor('#ef4444'),     # Red
    'accent_purple': HexColor('#8b5cf6'),  # Purple
    'accent_blue': HexColor('#3b82f6'),    # Blue
    'text_white': HexColor('#ffffff'),
    'text_light': HexColor('#e2e8f0'),
    'text_muted': HexColor('#94a3b8'),
    'bg_dark': HexColor('#0f172a'),
    'bg_card': HexColor('#1e293b'),
}

# ═══════════════════════════════════════════════════════════════════════════════
# Arabic Text Processing
# ═══════════════════════════════════════════════════════════════════════════════
def arabic(text):
    """Process Arabic text for proper RTL display"""
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

# ═══════════════════════════════════════════════════════════════════════════════
# Pitch Deck Generator Class
# ═══════════════════════════════════════════════════════════════════════════════
class PitchDeckPDF:
    def __init__(self, output_path="24-45_Pitch_Deck.pdf"):
        self.output_path = output_path
        # Landscape A4
        self.width, self.height = landscape(A4)
        self.margin = 1.5 * cm
        self.setup_fonts()
        self.pdf = canvas.Canvas(output_path, pagesize=landscape(A4))
        self.page_number = 0
        
    def setup_fonts(self):
        """Register Arabic-compatible fonts"""
        font_paths = [
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            '/Library/Fonts/Arial Unicode.ttf',
        ]
        self.arabic_font = 'Helvetica'
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ArabicFont', font_path))
                    self.arabic_font = 'ArabicFont'
                    break
                except:
                    continue

    def draw_background(self):
        """Draw dark gradient background"""
        self.pdf.setFillColor(COLORS['bg_dark'])
        self.pdf.rect(0, 0, self.width, self.height, fill=True, stroke=False)
        
        # Decorative elements
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.setFillAlpha(0.1)
        self.pdf.circle(self.width + 50, self.height - 50, 200, fill=True, stroke=False)
        self.pdf.circle(-50, 50, 150, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)

    def draw_page_number(self):
        """Draw page number"""
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(self.width / 2, 0.8 * cm, f"{self.page_number}")

    def new_page(self):
        """Start a new page"""
        if self.page_number > 0:
            self.draw_page_number()
            self.pdf.showPage()
        self.page_number += 1
        self.draw_background()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 1: Cover
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_cover(self):
        """Cover slide"""
        self.new_page()
        
        # Logo area
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.roundRect(self.width/2 - 3*cm, self.height - 5*cm, 6*cm, 3*cm, 15, fill=True, stroke=False)
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 32)
        self.pdf.drawCentredString(self.width/2, self.height - 3.8*cm, "24°45°")
        
        # Main title
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 42)
        self.pdf.drawCentredString(self.width/2, self.height - 9*cm, arabic("مساحة العمل الإبداعية"))
        
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.drawCentredString(self.width/2, self.height - 11*cm, arabic("لفرق التواصل المؤسسي"))
        
        # Subtitle
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 18)
        self.pdf.drawCentredString(self.width/2, self.height - 14*cm, 
            "Creative Workspace for Communication Teams")
        
        # Tagline box
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFillAlpha(0.2)
        self.pdf.roundRect(self.width/2 - 6*cm, 3*cm, 12*cm, 2*cm, 10, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
        
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, 3.7*cm, arabic("الرزنامة الذكية + البطاقات التفاعلية + العصف الذهني مع AI"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 2: Problem
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_problem(self):
        """Problem slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_red'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("المشكلة"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "The Problem")
        
        # Problem boxes
        problems = [
            (arabic("التشتت"), arabic("5 أدوات مختلفة للتخطيط"), "Miro + Trello + Excel + WhatsApp + Hootsuite"),
            (arabic("النسيان"), arabic("المناسبات تمر بدون استعداد"), arabic("فاتنا اليوم الوطني!")),
            (arabic("ضعف التعاون"), arabic("الأفكار تضيع في المحادثات"), arabic("الفريق لا يعمل كوحدة واحدة")),
            (arabic("لا إبداع"), arabic("لا أداة تساعد على العصف الذهني"), arabic("كل واحد يعمل لوحده")),
        ]
        
        box_width = 5.5*cm
        box_height = 4.5*cm
        start_x = (self.width - 4*box_width - 1.5*cm) / 2
        y = self.height - 10*cm
        
        colors = [COLORS['accent_red'], COLORS['accent'], COLORS['accent_purple'], COLORS['accent_blue']]
        
        for i, (title, desc, detail) in enumerate(problems):
            x = start_x + i * (box_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(colors[i])
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - box_height, box_width, box_height, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Top border
            self.pdf.setFillColor(colors[i])
            self.pdf.rect(x, y - 0.2*cm, box_width, 0.3*cm, fill=True, stroke=False)
            
            # Content
            self.pdf.setFillColor(colors[i])
            self.pdf.setFont(self.arabic_font, 18)
            self.pdf.drawCentredString(x + box_width/2, y - 1.2*cm, title)
            
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 11)
            self.pdf.drawCentredString(x + box_width/2, y - 2.2*cm, desc)
            
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 9)
            self.pdf.drawCentredString(x + box_width/2, y - 3.2*cm, detail)
        
        # Quote
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 3*cm, 
            arabic("\"80% من فرق التواصل تستخدم أدوات غير متخصصة\""))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 3: Solution
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_solution(self):
        """Solution slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_green'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("الحل"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Our Solution")
        
        # Main solution
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 24)
        self.pdf.drawCentredString(self.width/2, self.height - 6.5*cm, 
            arabic("مساحة عمل واحدة متكاملة لفرق التواصل"))
        
        # Three pillars
        pillars = [
            (arabic("الرزنامة الذكية"), arabic("500+ مناسبة عربية وعالمية"), COLORS['accent_blue'], "📅"),
            (arabic("البطاقة التفاعلية"), arabic("كل شيء في مكان واحد"), COLORS['accent_green'], "🃏"),
            (arabic("العصف الذهني مع AI"), arabic("طور أفكارك قبل مشاركتها"), COLORS['accent_purple'], "🧠"),
        ]
        
        pillar_width = 7*cm
        pillar_height = 5*cm
        start_x = (self.width - 3*pillar_width - 1*cm) / 2
        y = self.height - 13*cm
        
        for i, (title, desc, color, icon) in enumerate(pillars):
            x = start_x + i * (pillar_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - pillar_height, pillar_width, pillar_height, 15, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Border
            self.pdf.setStrokeColor(color)
            self.pdf.setLineWidth(2)
            self.pdf.roundRect(x, y - pillar_height, pillar_width, pillar_height, 15, fill=False, stroke=True)
            
            # Content
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 16)
            self.pdf.drawCentredString(x + pillar_width/2, y - 1.5*cm, title)
            
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 11)
            self.pdf.drawCentredString(x + pillar_width/2, y - 2.5*cm, desc)
        
        # Bottom tagline
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 2.5*cm, 
            arabic("نتكامل مع أدوات النشر، لا ننافسها"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 4: The Magic Card
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_magic_card(self):
        """The magic card slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("السر: البطاقة التفاعلية"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "The Magic: Interactive Card")
        
        # Card visualization
        card_x = self.width/2 - 8*cm
        card_y = self.height - 14*cm
        card_width = 16*cm
        card_height = 8*cm
        
        # Card background
        self.pdf.setFillColor(COLORS['bg_card'])
        self.pdf.roundRect(card_x, card_y, card_width, card_height, 15, fill=True, stroke=False)
        
        # Card header
        self.pdf.setFillColor(COLORS['accent_green'])
        self.pdf.roundRect(card_x, card_y + card_height - 1.5*cm, card_width, 1.5*cm, 15, fill=True, stroke=False)
        self.pdf.rect(card_x, card_y + card_height - 1.5*cm, card_width, 0.75*cm, fill=True, stroke=False)
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(card_x + card_width/2, card_y + card_height - 1*cm, 
            arabic("حملة إطلاق ALIC"))
        
        # Card tabs
        tabs = [
            (arabic("الوصف"), COLORS['accent_blue']),
            (arabic("الأفكار"), COLORS['accent_purple']),
            (arabic("النشر"), COLORS['accent_green']),
            (arabic("المؤثرين"), COLORS['accent']),
            (arabic("التتبع"), COLORS['text_muted']),
        ]
        
        tab_width = card_width / 5
        for i, (tab_name, color) in enumerate(tabs):
            tx = card_x + i * tab_width
            
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.3 if i > 0 else 1)
            self.pdf.rect(tx, card_y + card_height - 2.5*cm, tab_width, 0.8*cm, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            self.pdf.setFillColor(COLORS['text_white'] if i == 0 else color)
            self.pdf.setFont(self.arabic_font, 9)
            self.pdf.drawCentredString(tx + tab_width/2, card_y + card_height - 2.2*cm, tab_name)
        
        # Card content sample
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 10)
        content_y = card_y + card_height - 3.5*cm
        
        lines = [
            arabic("الهدف: إطلاق حملة تشويقية قبل المؤتمر الصحفي"),
            arabic("الجمهور: المستثمرين في القطاع الصناعي"),
            arabic("المدة: 15-17 يناير 2026"),
            arabic("الفريق: أحمد، سارة، نورة، خالد"),
        ]
        
        for line in lines:
            self.pdf.drawRightString(card_x + card_width - 0.5*cm, content_y, line)
            content_y -= 0.7*cm
        
        # Features below card
        features = [
            (arabic("كل شيء في بطاقة واحدة"), COLORS['accent_blue']),
            (arabic("تمتد ليوم أو أسبوع"), COLORS['accent_green']),
            (arabic("تعاون الفريق داخلها"), COLORS['accent_purple']),
            (arabic("عصف ذهني مدمج"), COLORS['accent']),
        ]
        
        feat_y = 2.5*cm
        feat_start = (self.width - 4*5*cm) / 2
        
        for i, (feat, color) in enumerate(features):
            fx = feat_start + i * 5.5*cm
            
            self.pdf.setFillColor(color)
            self.pdf.circle(fx, feat_y, 0.3*cm, fill=True, stroke=False)
            
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawString(fx + 0.5*cm, feat_y - 0.1*cm, feat)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 5: Market
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_market(self):
        """Market slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_blue'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("السوق"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Market Opportunity")
        
        # TAM SAM SOM
        circles = [
            ("TAM", "$2B", arabic("سوق أدوات التواصل - MENA"), 8*cm, COLORS['accent_blue']),
            ("SAM", "$200M", arabic("فرق التواصل المؤسسي"), 5.5*cm, COLORS['accent_green']),
            ("SOM", "$5M", arabic("السنوات 3 الأولى"), 3*cm, COLORS['accent']),
        ]
        
        center_x = self.width / 3
        center_y = self.height / 2
        
        for name, value, desc, radius, color in circles:
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.2)
            self.pdf.circle(center_x, center_y, radius, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            self.pdf.setStrokeColor(color)
            self.pdf.setLineWidth(2)
            self.pdf.circle(center_x, center_y, radius, fill=False, stroke=True)
        
        # Labels
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 24)
        self.pdf.drawCentredString(center_x, center_y + 0.3*cm, "$5M")
        
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(center_x, center_y - 0.5*cm, "SOM")
        
        # Right side - target segments
        right_x = self.width * 0.65
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 18)
        self.pdf.drawRightString(self.width - self.margin, self.height - 6*cm, arabic("الشرائح المستهدفة:"))
        
        segments = [
            (arabic("القطاع الحكومي"), "2,000+", "40%"),
            (arabic("القطاع الخاص"), "1,500+", "35%"),
            (arabic("القطاع الثالث"), "1,000+", "25%"),
        ]
        
        seg_y = self.height - 8*cm
        for seg_name, count, percent in segments:
            self.pdf.setFillColor(COLORS['primary'])
            self.pdf.setFillAlpha(0.2)
            self.pdf.roundRect(right_x, seg_y - 1.2*cm, 8*cm, 1.4*cm, 8, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            self.pdf.setFillColor(COLORS['text_white'])
            self.pdf.setFont(self.arabic_font, 12)
            self.pdf.drawRightString(right_x + 7.5*cm, seg_y - 0.7*cm, seg_name)
            
            self.pdf.setFillColor(COLORS['accent'])
            self.pdf.drawString(right_x + 0.3*cm, seg_y - 0.7*cm, f"{count} {arabic('جهة')}")
            
            seg_y -= 1.8*cm
        
        # Key insight
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 2.5*cm, 
            arabic("لا يوجد منافس عربي مباشر في هذا المجال"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 6: Competition
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_competition(self):
        """Competition slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_purple'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("المنافسة"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Competitive Landscape")
        
        # Competition matrix
        matrix_x = 3*cm
        matrix_y = 2.5*cm
        matrix_width = self.width - 6*cm
        matrix_height = self.height - 9*cm
        
        # Axes
        self.pdf.setStrokeColor(COLORS['text_muted'])
        self.pdf.setLineWidth(2)
        self.pdf.line(matrix_x, matrix_y, matrix_x, matrix_y + matrix_height)  # Y axis
        self.pdf.line(matrix_x, matrix_y, matrix_x + matrix_width, matrix_y)  # X axis
        
        # Labels
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(matrix_x + matrix_width/2, matrix_y - 0.8*cm, arabic("عربي ←――――――――――――――――――――→ إنجليزي"))
        
        # Save and rotate for vertical text
        self.pdf.saveState()
        self.pdf.translate(matrix_x - 0.8*cm, matrix_y + matrix_height/2)
        self.pdf.rotate(90)
        self.pdf.drawCentredString(0, 0, arabic("متخصص للتواصل ←――――――→ أداة عامة"))
        self.pdf.restoreState()
        
        # Competitors
        competitors = [
            ("Notion", 0.8, 0.3, COLORS['text_muted'], 1.2*cm),
            ("Trello", 0.75, 0.25, COLORS['text_muted'], 1*cm),
            ("Monday", 0.7, 0.4, COLORS['text_muted'], 1.1*cm),
            ("Hootsuite", 0.85, 0.7, COLORS['accent_blue'], 1.2*cm),
            ("Sprout", 0.9, 0.75, COLORS['accent_blue'], 1*cm),
            ("Loomly", 0.8, 0.65, COLORS['accent_blue'], 0.9*cm),
            ("24°45°", 0.15, 0.85, COLORS['accent'], 1.5*cm),
        ]
        
        for name, x_pos, y_pos, color, size in competitors:
            cx = matrix_x + x_pos * matrix_width
            cy = matrix_y + y_pos * matrix_height
            
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.3)
            self.pdf.circle(cx, cy, size, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            self.pdf.setFillColor(COLORS['text_white'] if name == "24°45°" else color)
            self.pdf.setFont(self.arabic_font, 10 if name != "24°45°" else 14)
            self.pdf.drawCentredString(cx, cy - 0.1*cm, name)
        
        # Our advantage box
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFillAlpha(0.1)
        self.pdf.roundRect(matrix_x, matrix_y + matrix_height * 0.6, matrix_width * 0.35, matrix_height * 0.35, 10, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
        
        self.pdf.setStrokeColor(COLORS['accent'])
        self.pdf.setLineWidth(2)
        self.pdf.setDash(5, 3)
        self.pdf.roundRect(matrix_x, matrix_y + matrix_height * 0.6, matrix_width * 0.35, matrix_height * 0.35, 10, fill=False, stroke=True)
        self.pdf.setDash()
        
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(matrix_x + matrix_width * 0.17, matrix_y + matrix_height * 0.55, 
            arabic("الفرصة: لا منافس هنا!"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 7: Business Model
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_business_model(self):
        """Business model slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_green'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("نموذج العمل"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Business Model")
        
        # Pricing tiers
        tiers = [
            (arabic("مجاني"), "$0", [arabic("مستخدم 1"), arabic("مشروع 1"), arabic("10 بطاقات")], COLORS['text_muted']),
            (arabic("احترافي"), "$49/"+arabic("شهر"), [arabic("5 مستخدمين"), arabic("10 مشاريع"), arabic("50 جلسة AI")], COLORS['accent_blue']),
            (arabic("مؤسسي"), "$149/"+arabic("شهر"), [arabic("20 مستخدم"), arabic("غير محدود"), arabic("AI غير محدود")], COLORS['accent_green']),
        ]
        
        tier_width = 6.5*cm
        tier_height = 7*cm
        start_x = (self.width - 3*tier_width - 1*cm) / 2
        y = self.height - 12*cm
        
        for i, (name, price, features, color) in enumerate(tiers):
            x = start_x + i * (tier_width + 0.5*cm)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(x, y - tier_height, tier_width, tier_height, 15, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            if i == 1:  # Popular
                self.pdf.setFillColor(COLORS['accent'])
                self.pdf.roundRect(x + tier_width/2 - 1.5*cm, y + 0.2*cm, 3*cm, 0.6*cm, 5, fill=True, stroke=False)
                self.pdf.setFillColor(COLORS['bg_dark'])
                self.pdf.setFont(self.arabic_font, 8)
                self.pdf.drawCentredString(x + tier_width/2, y + 0.4*cm, arabic("الأكثر شعبية"))
            
            # Border
            self.pdf.setStrokeColor(color)
            self.pdf.setLineWidth(2)
            self.pdf.roundRect(x, y - tier_height, tier_width, tier_height, 15, fill=False, stroke=True)
            
            # Content
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 16)
            self.pdf.drawCentredString(x + tier_width/2, y - 1*cm, name)
            
            self.pdf.setFillColor(COLORS['text_white'])
            self.pdf.setFont(self.arabic_font, 24)
            self.pdf.drawCentredString(x + tier_width/2, y - 2.2*cm, price)
            
            # Features
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 10)
            feat_y = y - 3.5*cm
            for feat in features:
                self.pdf.drawCentredString(x + tier_width/2, feat_y, "✓ " + feat)
                feat_y -= 0.7*cm
        
        # Revenue projection
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 2.5*cm, 
            arabic("السنة 3: 1,000 عميل × $80 = $960,000 سنوياً"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 8: MVP
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_mvp(self):
        """MVP slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, "MVP")
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Minimum Viable Product")
        
        # MVP Features
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 18)
        self.pdf.drawRightString(self.width - self.margin, self.height - 6*cm, arabic("ما سنبنيه أولاً:"))
        
        mvp_features = [
            (arabic("الرزنامة التفاعلية"), arabic("عرض شهري/أسبوعي مع سحب وإفلات"), "✅"),
            (arabic("قاعدة المناسبات"), arabic("500+ مناسبة عربية وعالمية وإسلامية"), "✅"),
            (arabic("البطاقات الأساسية"), arabic("وصف + أفكار + تعليقات الفريق"), "✅"),
            (arabic("إدارة المشاريع"), arabic("مشاريع متعددة بألوان مختلفة"), "✅"),
            (arabic("مشاركة الفريق"), arabic("دعوة أعضاء وصلاحيات"), "✅"),
        ]
        
        feat_y = self.height - 8*cm
        for title, desc, status in mvp_features:
            # Box
            self.pdf.setFillColor(COLORS['accent_green'])
            self.pdf.setFillAlpha(0.1)
            self.pdf.roundRect(self.width/2, feat_y - 1.2*cm, 12*cm, 1.4*cm, 8, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Status
            self.pdf.setFillColor(COLORS['accent_green'])
            self.pdf.setFont(self.arabic_font, 14)
            self.pdf.drawString(self.width/2 + 0.3*cm, feat_y - 0.8*cm, status)
            
            # Title
            self.pdf.setFillColor(COLORS['text_white'])
            self.pdf.setFont(self.arabic_font, 12)
            self.pdf.drawRightString(self.width/2 + 11.5*cm, feat_y - 0.6*cm, title)
            
            # Desc
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 9)
            self.pdf.drawRightString(self.width/2 + 11.5*cm, feat_y - 1*cm, desc)
            
            feat_y -= 1.8*cm
        
        # NOT in MVP
        self.pdf.setFillColor(COLORS['accent_red'])
        self.pdf.setFont(self.arabic_font, 14)
        not_y = self.height - 8*cm
        self.pdf.drawString(self.margin, not_y, arabic("ليس في MVP:"))
        
        not_mvp = [
            arabic("العصف الذهني مع AI"),
            arabic("النشر التلقائي"),
            arabic("قاعدة المؤثرين"),
            arabic("التقارير المتقدمة"),
        ]
        
        not_y -= 0.8*cm
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        for item in not_mvp:
            self.pdf.drawString(self.margin + 0.5*cm, not_y, "○ " + item)
            not_y -= 0.6*cm
        
        # Timeline
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 2.5*cm, 
            arabic("المدة: 6 أسابيع للـ MVP"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 9: Roadmap
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_roadmap(self):
        """Roadmap slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("خارطة الطريق"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Roadmap")
        
        # Timeline
        phases = [
            ("Q1 2026", arabic("MVP"), [arabic("الرزنامة"), arabic("البطاقات"), arabic("المناسبات")], COLORS['accent_green']),
            ("Q2 2026", arabic("النمو"), [arabic("العصف الذهني AI"), arabic("التكاملات")], COLORS['accent_blue']),
            ("Q3 2026", arabic("التوسع"), [arabic("قاعدة المؤثرين"), arabic("التقارير")], COLORS['accent_purple']),
            ("Q4 2026", arabic("Scale"), [arabic("API"), arabic("Enterprise")], COLORS['accent']),
        ]
        
        phase_width = 5.5*cm
        phase_height = 5*cm
        start_x = (self.width - 4*phase_width - 1.5*cm) / 2
        y = self.height - 10*cm
        
        # Connection line
        self.pdf.setStrokeColor(COLORS['text_muted'])
        self.pdf.setLineWidth(3)
        self.pdf.line(start_x, y - phase_height/2, start_x + 4*phase_width + 1*cm, y - phase_height/2)
        
        for i, (quarter, name, items, color) in enumerate(phases):
            x = start_x + i * (phase_width + 0.5*cm)
            
            # Circle on line
            self.pdf.setFillColor(color)
            self.pdf.circle(x + phase_width/2, y - phase_height/2, 0.4*cm, fill=True, stroke=False)
            
            # Box
            self.pdf.setFillColor(color)
            self.pdf.setFillAlpha(0.15)
            self.pdf.roundRect(x, y - phase_height, phase_width, phase_height - 1*cm, 10, fill=True, stroke=False)
            self.pdf.setFillAlpha(1)
            
            # Quarter
            self.pdf.setFillColor(color)
            self.pdf.setFont(self.arabic_font, 12)
            self.pdf.drawCentredString(x + phase_width/2, y - 0.5*cm, quarter)
            
            # Name
            self.pdf.setFillColor(COLORS['text_white'])
            self.pdf.setFont(self.arabic_font, 14)
            self.pdf.drawCentredString(x + phase_width/2, y - 1.8*cm, name)
            
            # Items
            self.pdf.setFillColor(COLORS['text_light'])
            self.pdf.setFont(self.arabic_font, 9)
            item_y = y - 2.8*cm
            for item in items:
                self.pdf.drawCentredString(x + phase_width/2, item_y, "• " + item)
                item_y -= 0.6*cm
        
        # KPIs
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 3.5*cm, arabic("الأهداف:"))
        
        kpis = [
            ("Q1", "50", arabic("عميل")),
            ("Q2", "150", arabic("عميل")),
            ("Q3", "350", arabic("عميل")),
            ("Q4", "600", arabic("عميل")),
        ]
        
        kpi_start = (self.width - 4*4*cm) / 2
        for i, (q, num, label) in enumerate(kpis):
            kx = kpi_start + i * 5*cm
            self.pdf.setFillColor(COLORS['accent'])
            self.pdf.setFont(self.arabic_font, 18)
            self.pdf.drawCentredString(kx, 2.5*cm, num)
            self.pdf.setFillColor(COLORS['text_muted'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(kx, 2*cm, label)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 10: Team (Optional)
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_team(self):
        """Team slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent_purple'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("الفريق"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "Team")
        
        # Founder
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.circle(self.width/2, self.height - 8*cm, 2*cm, fill=True, stroke=False)
        
        self.pdf.setFillColor(COLORS['bg_dark'])
        self.pdf.setFont(self.arabic_font, 20)
        self.pdf.drawCentredString(self.width/2, self.height - 8.2*cm, arabic("طاهر"))
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 18)
        self.pdf.drawCentredString(self.width/2, self.height - 10.5*cm, arabic("طاهر إرشيد"))
        
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, self.height - 11.5*cm, arabic("المؤسس والرئيس التنفيذي"))
        
        # Experience
        exp_items = [
            arabic("خبرة 15+ سنة في العلاقات العامة"),
            arabic("عمل مع 50+ جهة حكومية وخاصة"),
            arabic("مؤسس 24-45 للاستشارات"),
        ]
        
        exp_y = self.height - 13*cm
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 12)
        for item in exp_items:
            self.pdf.drawCentredString(self.width/2, exp_y, "• " + item)
            exp_y -= 0.8*cm
        
        # Looking for
        self.pdf.setFillColor(COLORS['accent_blue'])
        self.pdf.setFillAlpha(0.2)
        self.pdf.roundRect(self.width/2 - 8*cm, 2*cm, 16*cm, 2.5*cm, 10, fill=True, stroke=False)
        self.pdf.setFillAlpha(1)
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 3.5*cm, arabic("نبحث عن: مطور Full-Stack + مصمم UX"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 11: Ask
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_ask(self):
        """The ask slide"""
        self.new_page()
        
        # Title
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 36)
        self.pdf.drawCentredString(self.width/2, self.height - 3*cm, arabic("ماذا نحتاج؟"))
        
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 4*cm, "The Ask")
        
        # Investment ask
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 60)
        self.pdf.drawCentredString(self.width/2, self.height - 8*cm, "$150K")
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 18)
        self.pdf.drawCentredString(self.width/2, self.height - 9.5*cm, arabic("استثمار أولي (Pre-Seed)"))
        
        # Use of funds
        funds = [
            (arabic("التطوير"), "50%", COLORS['accent_blue']),
            (arabic("التسويق"), "25%", COLORS['accent_green']),
            (arabic("التشغيل"), "15%", COLORS['accent_purple']),
            (arabic("احتياطي"), "10%", COLORS['text_muted']),
        ]
        
        fund_y = self.height - 12*cm
        fund_width = 18*cm
        fund_x = (self.width - fund_width) / 2
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, fund_y, arabic("توزيع الاستثمار:"))
        
        # Progress bar
        bar_y = fund_y - 1.5*cm
        bar_height = 1*cm
        current_x = fund_x
        
        for name, percent, color in funds:
            pct = int(percent.replace('%', '')) / 100
            bar_width = fund_width * pct
            
            self.pdf.setFillColor(color)
            self.pdf.rect(current_x, bar_y, bar_width, bar_height, fill=True, stroke=False)
            
            self.pdf.setFillColor(COLORS['text_white'])
            self.pdf.setFont(self.arabic_font, 10)
            self.pdf.drawCentredString(current_x + bar_width/2, bar_y + 0.3*cm, f"{name} {percent}")
            
            current_x += bar_width
        
        # What we offer
        self.pdf.setFillColor(COLORS['accent_green'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, 4.5*cm, arabic("مقابل: 15% حصة"))
        
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 12)
        self.pdf.drawCentredString(self.width/2, 3.5*cm, 
            arabic("التقييم: $1M Pre-money"))
        
        # Milestones
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(self.width/2, 2.5*cm, 
            arabic("الهدف: 100 عميل مدفوع خلال 12 شهر"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Slide 12: Contact
    # ═══════════════════════════════════════════════════════════════════════════════
    def slide_contact(self):
        """Contact slide"""
        self.new_page()
        
        # Logo
        self.pdf.setFillColor(COLORS['primary'])
        self.pdf.roundRect(self.width/2 - 3*cm, self.height - 6*cm, 6*cm, 3*cm, 15, fill=True, stroke=False)
        
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 32)
        self.pdf.drawCentredString(self.width/2, self.height - 4.8*cm, "24°45°")
        
        # Tagline
        self.pdf.setFillColor(COLORS['text_white'])
        self.pdf.setFont(self.arabic_font, 24)
        self.pdf.drawCentredString(self.width/2, self.height - 9*cm, arabic("مساحة العمل الإبداعية لفرق التواصل"))
        
        # Contact info
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, self.height - 12*cm, "www.24-45.com")
        
        self.pdf.setFillColor(COLORS['text_light'])
        self.pdf.setFont(self.arabic_font, 14)
        self.pdf.drawCentredString(self.width/2, self.height - 13*cm, "taher@24-45.com")
        
        # CTA
        self.pdf.setFillColor(COLORS['accent'])
        self.pdf.roundRect(self.width/2 - 4*cm, 4*cm, 8*cm, 2*cm, 10, fill=True, stroke=False)
        
        self.pdf.setFillColor(COLORS['bg_dark'])
        self.pdf.setFont(self.arabic_font, 16)
        self.pdf.drawCentredString(self.width/2, 4.7*cm, arabic("لنبني المستقبل معاً"))
        
        # Date
        self.pdf.setFillColor(COLORS['text_muted'])
        self.pdf.setFont(self.arabic_font, 10)
        self.pdf.drawCentredString(self.width/2, 2*cm, datetime.now().strftime("%B %Y"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # Generate Complete Deck
    # ═══════════════════════════════════════════════════════════════════════════════
    def generate(self):
        """Generate the complete pitch deck"""
        print("جاري إنشاء Pitch Deck...")
        
        self.slide_cover()
        self.slide_problem()
        self.slide_solution()
        self.slide_magic_card()
        self.slide_market()
        self.slide_competition()
        self.slide_business_model()
        self.slide_mvp()
        self.slide_roadmap()
        self.slide_team()
        self.slide_ask()
        self.slide_contact()
        
        self.draw_page_number()
        self.pdf.save()
        
        print(f"\n✅ تم إنشاء الملف: {self.output_path}")
        print(f"📄 عدد الشرائح: {self.page_number}")
        return self.output_path


# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "24-45_Pitch_Deck.pdf")
    
    deck = PitchDeckPDF(output_path)
    deck.generate()
    
    print(f"\n{'='*60}")
    print("تم إنشاء Pitch Deck بنجاح!")
    print(f"{'='*60}")
