# -*- coding: utf-8 -*-
"""
خطة الاتصال والعلاقات العامة - ALIC
PDF Generator with Nobles Branding using FPDF2
"""

from fpdf import FPDF
import os

class ArabicPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def add_arabic_font(self):
        # Use built-in fonts that support basic characters
        pass
        
    def header(self):
        pass
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def reverse_arabic(text):
    """Reverse Arabic text for display"""
    return text[::-1]

def create_pr_plan_pdf():
    """Create professional PR Plan PDF"""
    
    pdf = ArabicPDF()
    pdf.set_margins(20, 20, 20)
    
    # ===== Cover Page =====
    pdf.add_page()
    
    # Background gradient effect (dark blue)
    pdf.set_fill_color(15, 23, 42)  # Dark blue #0F172A
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Decorative circles
    pdf.set_fill_color(16, 185, 129)  # Green
    pdf.set_draw_color(16, 185, 129)
    
    # Logo box
    pdf.set_xy(75, 60)
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(75, 60, 60, 60, 'F')
    
    # ALIC text
    pdf.set_font('Helvetica', 'B', 36)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(75, 75)
    pdf.cell(60, 30, 'ALIC', align='C')
    
    # Main Title (English - RTL issues with Arabic)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(16, 185, 129)
    pdf.set_xy(20, 140)
    pdf.cell(170, 15, 'Communication & PR Plan', align='C')
    
    # Subtitle
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(245, 158, 11)
    pdf.set_xy(20, 160)
    pdf.cell(170, 12, 'Amman Logistics & Industrial City', align='C')
    
    # Divider line
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(1)
    pdf.line(60, 185, 150, 185)
    
    # Stats boxes
    stats = [
        ('20', 'Media Products'),
        ('3', 'Phases'),
        ('85%', 'Local Coverage')
    ]
    
    x_start = 35
    for i, (value, label) in enumerate(stats):
        x = x_start + (i * 50)
        
        # Box background
        pdf.set_fill_color(20, 60, 50)
        pdf.set_draw_color(16, 185, 129)
        pdf.rect(x, 200, 45, 40, 'D')
        
        # Value
        pdf.set_font('Helvetica', 'B', 24)
        pdf.set_text_color(16, 185, 129)
        pdf.set_xy(x, 205)
        pdf.cell(45, 15, value, align='C')
        
        # Label
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(148, 163, 184)
        pdf.set_xy(x, 220)
        pdf.cell(45, 10, label, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(20, 265)
    pdf.cell(170, 10, 'January 2026 | Nobles Properties', align='C')
    
    # ===== Executive Summary =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Section Header
    add_section_header(pdf, '1', 'Executive Summary')
    
    # Vision Card
    pdf.set_y(60)
    add_card(pdf, 'Strategic Vision', 
             'Position ALIC as the "Smart Growth Engine" for the Jordanian economy, '
             'transforming it from a startup project to a leading brand in the '
             'logistics and industrial sector in the region.')
    
    # KPI Grid
    pdf.set_y(120)
    add_kpi_grid(pdf, [
        ('85%', 'Local Coverage'),
        ('10%', 'Regional Coverage'),
        ('5%', 'International'),
        ('20', 'Media Products')
    ])
    
    # ===== SWOT Analysis =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '2', 'SWOT Analysis')
    
    # Strengths
    pdf.set_y(60)
    add_swot_card(pdf, 'Strengths', [
        'Strategic location at crossroads of 3 regional markets',
        '3 confirmed strategic partnerships',
        'Ready infrastructure and modern warehouses',
        'Strong Nobles reputation in real estate market'
    ], (16, 185, 129))
    
    # Weaknesses
    pdf.set_y(130)
    add_swot_card(pdf, 'Weaknesses', [
        'Limited ALIC brand awareness',
        'Pre-official launch phase',
        'No previous media coverage',
        'Need for strong visual identity'
    ], (239, 68, 68))
    
    # Opportunities
    pdf.set_y(200)
    add_swot_card(pdf, 'Opportunities', [
        'Market gap for integrated logistics cities',
        'E-commerce growth 25% annually',
        'Government support for economic modernization',
        'Growing demand for smart warehouses'
    ], (59, 130, 246))
    
    # ===== Strategic Objectives =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '3', 'Strategic Objectives')
    
    objectives = [
        ('Build Brand Awareness', 
         'Achieve 80% awareness of ALIC among target audience within 3 months of launch.'),
        ('Strengthen Competitive Position', 
         'Position ALIC as the largest and most modern logistics industrial city in Jordan.'),
        ('Link to National Vision', 
         'Confirm ALIC role as strategic partner in achieving Economic Modernization Vision 2033.')
    ]
    
    y_pos = 60
    for i, (title, desc) in enumerate(objectives, 1):
        add_objective_card(pdf, i, title, desc, y_pos)
        y_pos += 50
    
    # ===== Target Audiences =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '4', 'Target Audiences')
    
    # Primary Audiences
    pdf.set_y(60)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(245, 158, 11)
    pdf.cell(0, 10, 'Primary Audiences', ln=True)
    
    primary = [
        ('Industrial Companies', 'Local and regional manufacturers'),
        ('Regional Investors', 'Gulf businessmen and investors'),
        ('Logistics Companies', '3PL, distribution, and storage')
    ]
    
    y_pos = 75
    for name, desc in primary:
        add_audience_card(pdf, name, desc, y_pos)
        y_pos += 35
    
    # Secondary Audiences
    pdf.set_y(185)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(245, 158, 11)
    pdf.cell(0, 10, 'Secondary Audiences', ln=True)
    
    secondary = [
        ('Government Entities', 'Ministries and investment agencies'),
        ('Financial Institutions', 'Banks and investment funds'),
        ('Media', 'Journalists and economic influencers')
    ]
    
    y_pos = 200
    for name, desc in secondary:
        add_audience_card(pdf, name, desc, y_pos)
        y_pos += 35
    
    # ===== Implementation Phases =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '5', 'Implementation Phases')
    
    # Phase 1
    pdf.set_y(60)
    add_phase_card(pdf, '1', 'Foundation & Teasing', 'Jan 1-14, 2026', [
        'Visual identity development',
        'Website launch',
        'Social media teaser campaign',
        'Marketing materials preparation',
        'Teaser video production',
        'VIP invitations',
        'Strategic media leaks'
    ], (16, 185, 129))
    
    # Phase 2
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_y(20)
    add_phase_card(pdf, '2', 'Grand Launch', 'Jan 15-22, 2026', [
        'VIP Launch Event - 150 guests',
        '4K Cinematic Film',
        'TV Coverage - 5 channels',
        'LinkedIn Campaign - 10 posts',
        'Digital Ads Campaign - $3,000',
        'Podcast with Omar Ayesh',
        '5 Opinion Articles',
        'Media Tour - 25 journalists'
    ], (245, 158, 11))
    
    # Phase 3
    pdf.set_y(160)
    add_phase_card(pdf, '3', 'Consolidation', 'Jan 23-31, 2026', [
        'Radio Interview - Hosna FM',
        'Radio Tour - 5 stations',
        'YouTube Episode - Al Mukhbir',
        'TV Report - Business Program',
        'Partner Testimonials Campaign'
    ], (139, 92, 246))
    
    # ===== Media Products Table =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '6', 'Key Media Products')
    
    products = [
        ('1', 'Launch Event', 'VIP Event', 'Jan 15', '150 guests'),
        ('2', '4K Film', 'Video', 'Jan 15', '500K views'),
        ('3', 'TV Coverage', 'Television', 'Jan 15-17', '2M+ viewers'),
        ('4', 'LinkedIn Campaign', 'Social', 'Jan 13-22', '100K impr.'),
        ('5', 'Digital Ads', 'Paid', 'Jan 13-22', '50+ leads'),
        ('6', 'Podcast', 'Audio', 'Jan 18-20', '50K listens'),
        ('7', 'Opinion Articles', 'Press', 'Jan 16-20', '200K readers'),
        ('8', 'Media Tour', 'Event', 'Jan 20', '50+ posts'),
        ('9', 'Radio Tour', 'Radio', 'Jan 22-27', '200K listeners'),
        ('10', 'YouTube Episode', 'Video', 'Jan 28', '500K views'),
    ]
    
    add_table(pdf, 
              ['#', 'Product', 'Type', 'Date', 'Target'],
              products, 60)
    
    # ===== KPIs =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '7', 'Key Performance Indicators')
    
    pdf.set_y(60)
    add_kpi_grid(pdf, [
        ('5M+', 'Total Reach'),
        ('50+', 'Media Coverage'),
        ('100+', 'Investor Inquiries'),
        ('80%', 'Target Awareness')
    ])
    
    # Success Metrics Card
    pdf.set_y(130)
    add_card(pdf, 'Success Metrics', 
             '> Media Coverage: 50+ news stories in first month\n'
             '> Digital Engagement: 500K+ social media interactions\n'
             '> Lead Generation: 100+ serious investor inquiries\n'
             '> Brand Awareness: 80% of target audience\n'
             '> Views: 2M+ video content views')
    
    # ===== Budget =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    add_section_header(pdf, '8', 'Budget Allocation')
    
    budget_items = [
        ('Launch Event', 'Venue + Catering + Organization', '$15,000'),
        ('Video Production', '4K Film + Videos', '$8,000'),
        ('Digital Advertising', 'Google + Meta + LinkedIn', '$3,000'),
        ('Media Tour', 'Transport + Catering + Gifts', '$2,000'),
        ('Public Relations', 'Media coordination + Press releases', '$2,000'),
        ('TOTAL', '', '$30,000'),
    ]
    
    add_budget_table(pdf, budget_items, 60)
    
    # ===== End Page =====
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Logo
    pdf.set_xy(85, 80)
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(85, 80, 40, 40, 'F')
    
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(85, 90)
    pdf.cell(40, 20, 'N', align='C')
    
    # Thank You
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(16, 185, 129)
    pdf.set_xy(20, 140)
    pdf.cell(170, 15, 'Thank You', align='C')
    
    # Contact Box
    pdf.set_y(170)
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(0.5)
    pdf.rect(50, 170, 110, 60, 'D')
    
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(245, 158, 11)
    pdf.set_xy(50, 175)
    pdf.cell(110, 10, 'Contact Us', align='C')
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(226, 232, 240)
    
    contacts = [
        'www.noblesproperties.com',
        'info@noblesproperties.com',
        '+962 6 XXX XXXX'
    ]
    
    y = 190
    for contact in contacts:
        pdf.set_xy(50, y)
        pdf.cell(110, 8, contact, align='C')
        y += 10
    
    # Footer
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(20, 265)
    pdf.cell(170, 10, '2026 Nobles Properties - All Rights Reserved', align='C')
    
    # Save PDF
    output_path = '/Users/taherirshaid/Desktop/Project/24-45-Platform/ALIC_PR_Plan_Professional.pdf'
    pdf.output(output_path)
    
    print(f"✅ PDF Created Successfully!")
    print(f"📄 Path: {output_path}")
    return output_path


def add_section_header(pdf, num, title):
    """Add section header with number"""
    # Header background
    pdf.set_fill_color(20, 60, 50)
    pdf.set_draw_color(16, 185, 129)
    pdf.rect(20, 20, 170, 30, 'D')
    
    # Number circle
    pdf.set_fill_color(16, 185, 129)
    pdf.ellipse(25, 25, 20, 20, 'F')
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(25, 28)
    pdf.cell(20, 14, num, align='C')
    
    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(16, 185, 129)
    pdf.set_xy(50, 28)
    pdf.cell(130, 14, title)


def add_card(pdf, title, content):
    """Add a content card"""
    y = pdf.get_y()
    
    # Card background
    pdf.set_fill_color(30, 41, 59)
    pdf.set_draw_color(100, 116, 139)
    pdf.rect(20, y, 170, 50, 'DF')
    
    # Title
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(245, 158, 11)
    pdf.set_xy(25, y + 5)
    pdf.cell(160, 8, title)
    
    # Content
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(203, 213, 225)
    pdf.set_xy(25, y + 15)
    pdf.multi_cell(160, 5, content)


def add_kpi_grid(pdf, kpis):
    """Add KPI grid"""
    y = pdf.get_y()
    x_start = 25
    
    for i, (value, label) in enumerate(kpis):
        x = x_start + (i * 42)
        
        # KPI box
        pdf.set_fill_color(20, 60, 50)
        pdf.set_draw_color(16, 185, 129)
        pdf.rect(x, y, 38, 45, 'D')
        
        # Value
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(16, 185, 129)
        pdf.set_xy(x, y + 8)
        pdf.cell(38, 12, value, align='C')
        
        # Label
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(148, 163, 184)
        pdf.set_xy(x, y + 25)
        pdf.cell(38, 8, label, align='C')


def add_swot_card(pdf, title, items, color):
    """Add SWOT analysis card"""
    y = pdf.get_y()
    
    # Card background
    pdf.set_fill_color(30, 41, 59)
    pdf.set_draw_color(color[0], color[1], color[2])
    pdf.rect(20, y, 170, 60, 'D')
    
    # Left border
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.rect(20, y, 4, 60, 'F')
    
    # Title
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(color[0], color[1], color[2])
    pdf.set_xy(28, y + 5)
    pdf.cell(160, 8, title)
    
    # Items
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(226, 232, 240)
    
    item_y = y + 15
    for item in items:
        pdf.set_xy(28, item_y)
        pdf.cell(160, 5, f"- {item}")
        item_y += 10


def add_objective_card(pdf, num, title, desc, y):
    """Add objective card"""
    # Card background
    pdf.set_fill_color(20, 45, 40)
    pdf.set_draw_color(16, 185, 129)
    pdf.rect(20, y, 170, 40, 'D')
    
    # Number box
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(25, y + 8, 25, 25, 'F')
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(25, y + 14)
    pdf.cell(25, 12, str(num), align='C')
    
    # Title
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(16, 185, 129)
    pdf.set_xy(55, y + 8)
    pdf.cell(130, 8, title)
    
    # Description
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(55, y + 18)
    pdf.multi_cell(130, 5, desc)


def add_audience_card(pdf, name, desc, y):
    """Add audience card"""
    pdf.set_fill_color(30, 41, 59)
    pdf.set_draw_color(100, 116, 139)
    pdf.rect(20, y, 170, 30, 'DF')
    
    # Icon circle
    pdf.set_fill_color(59, 130, 246)
    pdf.ellipse(25, y + 5, 20, 20, 'F')
    
    # Name
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(226, 232, 240)
    pdf.set_xy(50, y + 8)
    pdf.cell(135, 6, name)
    
    # Description
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(50, y + 16)
    pdf.cell(135, 6, desc)


def add_phase_card(pdf, num, title, date, products, color):
    """Add phase card"""
    y = pdf.get_y()
    height = 20 + len(products) * 8
    
    # Card background
    pdf.set_fill_color(25, 35, 50)
    pdf.set_draw_color(color[0], color[1], color[2])
    pdf.rect(20, y, 170, height, 'D')
    
    # Left border
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.rect(20, y, 4, height, 'F')
    
    # Number circle
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.ellipse(28, y + 5, 20, 20, 'F')
    
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(28, y + 10)
    pdf.cell(20, 10, num, align='C')
    
    # Title
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(color[0], color[1], color[2])
    pdf.set_xy(52, y + 5)
    pdf.cell(130, 8, title)
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(245, 158, 11)
    pdf.set_xy(52, y + 14)
    pdf.cell(130, 6, date)
    
    # Products list
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(226, 232, 240)
    
    item_y = y + 25
    for product in products:
        pdf.set_xy(30, item_y)
        pdf.cell(155, 5, f"  - {product}")
        item_y += 8
    
    pdf.set_y(y + height + 5)


def add_table(pdf, headers, rows, y):
    """Add data table"""
    pdf.set_y(y)
    
    # Header
    pdf.set_fill_color(16, 185, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    
    col_widths = [15, 50, 35, 35, 35]
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
    pdf.ln()
    
    # Rows
    pdf.set_text_color(226, 232, 240)
    pdf.set_font('Helvetica', '', 8)
    
    for row in rows:
        pdf.set_fill_color(30, 41, 59)
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 8, cell, 1, 0, 'C', True)
        pdf.ln()


def add_budget_table(pdf, items, y):
    """Add budget table"""
    pdf.set_y(y)
    
    # Header
    pdf.set_fill_color(16, 185, 129)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    
    pdf.cell(50, 12, 'Item', 1, 0, 'C', True)
    pdf.cell(80, 12, 'Details', 1, 0, 'C', True)
    pdf.cell(40, 12, 'Cost', 1, 1, 'C', True)
    
    # Rows
    pdf.set_font('Helvetica', '', 9)
    
    for item, details, cost in items:
        if item == 'TOTAL':
            pdf.set_fill_color(20, 60, 50)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(16, 185, 129)
        else:
            pdf.set_fill_color(30, 41, 59)
            pdf.set_text_color(226, 232, 240)
        
        pdf.cell(50, 10, item, 1, 0, 'C', True)
        pdf.cell(80, 10, details, 1, 0, 'C', True)
        pdf.cell(40, 10, cost, 1, 1, 'C', True)


if __name__ == "__main__":
    create_pr_plan_pdf()
