#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تصدير العرض التقديمي لهيئة تنمية المجتمع - دبي
Export CDA Dubai Presentation to PDF (16:9)
"""

import json
import os
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# مسار ملف JSON
JSON_PATH = "data/presentations/cda_dubai_pitch.json"
OUTPUT_PDF = "exports/CDA_Dubai_Pitch_2026.pdf"
OUTPUT_HTML = "exports/CDA_Dubai_Pitch_2026.html"

# ألوان هيئة تنمية المجتمع وحكومة دبي
COLORS = {
    "primary": "#00A79D",      # تركواز
    "primary_dark": "#004D47", # تركواز داكن
    "secondary": "#008C84",    # تركواز متوسط
    "gold": "#B8860B",         # ذهبي دبي
    "red": "#E31B23",          # أحمر
    "white": "#FFFFFF",
    "black": "#1A1A1A",
    "gray": "#666666"
}

def load_presentation():
    """تحميل بيانات العرض من JSON"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_css():
    """إنشاء CSS للعرض"""
    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    @page {{
        size: 338.7mm 190.5mm; /* 16:9 ratio */
        margin: 0;
    }}
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        background: #0a0a0a;
    }}
    
    .slide {{
        width: 338.7mm;
        height: 190.5mm;
        position: relative;
        overflow: hidden;
        page-break-after: always;
        page-break-inside: avoid;
        display: flex;
        flex-direction: column;
        padding: 15mm 20mm;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       شريحة الغلاف
       ═══════════════════════════════════════════════════════════════ */
    .slide-cover {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, #003D38 100%);
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    
    .slide-cover::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,255,255,0.02) 35px, rgba(255,255,255,0.02) 70px),
            repeating-linear-gradient(-45deg, transparent, transparent 35px, rgba(255,255,255,0.02) 35px, rgba(255,255,255,0.02) 70px);
    }}
    
    .cover-border {{
        position: absolute;
        top: 10mm;
        left: 10mm;
        right: 10mm;
        bottom: 10mm;
        border: 2px solid rgba({int(COLORS['gold'][1:3], 16)}, {int(COLORS['gold'][3:5], 16)}, {int(COLORS['gold'][5:7], 16)}, 0.4);
        border-radius: 8px;
    }}
    
    .cover-watermark {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 200px;
        font-weight: 900;
        color: {COLORS['gold']};
        opacity: 0.05;
        letter-spacing: 20px;
    }}
    
    .cover-logos {{
        position: absolute;
        top: 20mm;
        left: 25mm;
        right: 25mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .cover-logo {{
        height: 50px;
    }}
    
    .cover-content {{
        position: relative;
        z-index: 10;
    }}
    
    .cover-subtitle {{
        color: {COLORS['gold']};
        font-size: 18px;
        font-weight: 500;
        letter-spacing: 4px;
        margin-bottom: 20px;
    }}
    
    .cover-title {{
        color: {COLORS['white']};
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;
        line-height: 1.3;
    }}
    
    .cover-title-gold {{
        color: {COLORS['gold']};
    }}
    
    .cover-tagline {{
        color: rgba(255,255,255,0.8);
        font-size: 20px;
        margin-top: 30px;
    }}
    
    .cover-date {{
        position: absolute;
        bottom: 25mm;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.3);
        padding: 10px 40px;
        border-radius: 30px;
        border: 1px solid rgba({int(COLORS['gold'][1:3], 16)}, {int(COLORS['gold'][3:5], 16)}, {int(COLORS['gold'][5:7], 16)}, 0.3);
        color: {COLORS['gold']};
        font-size: 14px;
    }}
    
    .cover-confidential {{
        position: absolute;
        bottom: 15mm;
        right: 25mm;
        color: rgba(255,255,255,0.5);
        font-size: 12px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الشرائح القياسية
       ═══════════════════════════════════════════════════════════════ */
    .slide-standard {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, #003D38 100%);
    }}
    
    .slide-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15mm;
    }}
    
    .slide-header-content {{
        flex: 1;
    }}
    
    .slide-number {{
        width: 50px;
        height: 50px;
        background: {COLORS['gold']};
        color: {COLORS['primary_dark']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
    }}
    
    .slide-title {{
        color: {COLORS['white']};
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
    }}
    
    .slide-subtitle {{
        color: {COLORS['gold']};
        font-size: 18px;
        font-weight: 500;
    }}
    
    .slide-body {{
        flex: 1;
        color: {COLORS['white']};
    }}
    
    .slide-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.1);
        font-size: 11px;
        color: rgba(255,255,255,0.5);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       جدول المحتويات
       ═══════════════════════════════════════════════════════════════ */
    .toc-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 20px;
    }}
    
    .toc-card {{
        background: rgba(0,167,157,0.15);
        border: 1px solid rgba(184,134,11,0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }}
    
    .toc-card-num {{
        font-size: 32px;
        font-weight: 900;
        color: {COLORS['gold']};
        margin-bottom: 10px;
    }}
    
    .toc-card-title {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 5px;
    }}
    
    .toc-card-desc {{
        font-size: 13px;
        color: rgba(255,255,255,0.7);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       البطاقات والشبكات
       ═══════════════════════════════════════════════════════════════ */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 20px 0;
    }}
    
    .stat-card {{
        background: rgba(0,167,157,0.2);
        border: 1px solid rgba(184,134,11,0.3);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 42px;
        font-weight: 900;
        color: {COLORS['gold']};
        margin-bottom: 5px;
    }}
    
    .stat-label {{
        font-size: 14px;
        color: rgba(255,255,255,0.8);
    }}
    
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }}
    
    .card {{
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(184,134,11,0.2);
        border-radius: 12px;
        padding: 20px;
    }}
    
    .card-icon {{
        font-size: 36px;
        margin-bottom: 10px;
    }}
    
    .card-title {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 8px;
    }}
    
    .card-text {{
        font-size: 13px;
        color: rgba(255,255,255,0.7);
        line-height: 1.6;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الجداول
       ═══════════════════════════════════════════════════════════════ */
    .table-container {{
        background: rgba(0,0,0,0.2);
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    
    th {{
        background: {COLORS['primary']};
        color: {COLORS['white']};
        padding: 12px 15px;
        text-align: right;
        font-weight: 700;
        font-size: 14px;
    }}
    
    td {{
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: {COLORS['white']};
        font-size: 13px;
    }}
    
    tr:last-child td {{
        border-bottom: none;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       SWOT
       ═══════════════════════════════════════════════════════════════ */
    .swot-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-top: 15px;
    }}
    
    .swot-box {{
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 15px;
    }}
    
    .swot-box.strengths {{ border-right: 4px solid #28a745; }}
    .swot-box.weaknesses {{ border-right: 4px solid #dc3545; }}
    .swot-box.opportunities {{ border-right: 4px solid #ffc107; }}
    .swot-box.threats {{ border-right: 4px solid #6c757d; }}
    
    .swot-title {{
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .swot-list {{
        list-style: none;
        font-size: 12px;
        line-height: 1.8;
    }}
    
    .swot-list li::before {{
        content: '•';
        color: {COLORS['gold']};
        margin-left: 8px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       القوائم
       ═══════════════════════════════════════════════════════════════ */
    .list {{
        list-style: none;
    }}
    
    .list li {{
        padding: 8px 0;
        padding-right: 25px;
        position: relative;
        font-size: 14px;
        line-height: 1.6;
    }}
    
    .list li::before {{
        content: '✓';
        position: absolute;
        right: 0;
        color: {COLORS['gold']};
        font-weight: bold;
    }}
    
    .list-numbered li::before {{
        content: counter(item) '.';
        counter-increment: item;
        color: {COLORS['gold']};
        font-weight: 700;
    }}
    
    .list-numbered {{
        counter-reset: item;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الأولويات والتقييمات
       ═══════════════════════════════════════════════════════════════ */
    .priority-high {{ 
        background: rgba(220,53,69,0.2); 
        color: #ff6b6b;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 12px;
    }}
    
    .priority-medium {{ 
        background: rgba(255,193,7,0.2); 
        color: #ffc107;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 12px;
    }}
    
    .priority-low {{ 
        background: rgba(40,167,69,0.2); 
        color: #28a745;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 12px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       خارطة الطريق
       ═══════════════════════════════════════════════════════════════ */
    .timeline {{
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }}
    
    .timeline-item {{
        flex: 1;
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 15px;
        border-top: 4px solid {COLORS['gold']};
    }}
    
    .timeline-quarter {{
        font-size: 14px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 5px;
    }}
    
    .timeline-focus {{
        font-size: 12px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 10px;
    }}
    
    .timeline-list {{
        list-style: none;
        font-size: 11px;
        line-height: 1.8;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       شريحة الشكر
       ═══════════════════════════════════════════════════════════════ */
    .slide-thanks {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 100%);
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    
    .thanks-title {{
        font-size: 56px;
        font-weight: 900;
        color: {COLORS['white']};
        margin-bottom: 20px;
    }}
    
    .thanks-subtitle {{
        font-size: 24px;
        color: {COLORS['gold']};
        margin-bottom: 40px;
    }}
    
    .thanks-quote {{
        font-size: 18px;
        color: rgba(255,255,255,0.8);
        font-style: italic;
        max-width: 700px;
        margin: 0 auto 40px;
        padding: 20px;
        border-right: 4px solid {COLORS['gold']};
    }}
    
    .contact-grid {{
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 30px;
    }}
    
    .contact-item {{
        text-align: center;
    }}
    
    .contact-icon {{
        font-size: 24px;
        color: {COLORS['gold']};
        margin-bottom: 5px;
    }}
    
    .contact-text {{
        font-size: 14px;
        color: {COLORS['white']};
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       Two Columns Layout
       ═══════════════════════════════════════════════════════════════ */
    .two-columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
    }}
    
    .column {{
        
    }}
    
    .column-title {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(184,134,11,0.3);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       Problem Cards
       ═══════════════════════════════════════════════════════════════ */
    .problem-header {{
        background: rgba(220,53,69,0.15);
        border: 1px solid rgba(220,53,69,0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .problem-statement {{
        font-size: 18px;
        font-weight: 500;
        color: {COLORS['white']};
        line-height: 1.6;
    }}
    
    .evidence-box {{
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
    }}
    
    .evidence-title {{
        font-size: 14px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 10px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       Package Cards
       ═══════════════════════════════════════════════════════════════ */
    .package-header {{
        background: rgba(0,167,157,0.2);
        border: 1px solid {COLORS['gold']};
        border-radius: 12px;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .package-meta {{
        display: flex;
        gap: 20px;
    }}
    
    .package-meta-item {{
        font-size: 13px;
        color: rgba(255,255,255,0.8);
    }}
    
    .package-meta-item strong {{
        color: {COLORS['gold']};
    }}
    
    .deliverables-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }}
    
    .deliverable-card {{
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 15px;
    }}
    
    .deliverable-title {{
        font-size: 15px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 5px;
    }}
    
    .deliverable-desc {{
        font-size: 12px;
        color: rgba(255,255,255,0.7);
        margin-bottom: 8px;
    }}
    
    .deliverable-output {{
        font-size: 11px;
        color: {COLORS['gold']};
        background: rgba(184,134,11,0.15);
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
    }}
    
    /* Investment */
    .investment-box {{
        background: {COLORS['gold']};
        color: {COLORS['primary_dark']};
        padding: 15px 25px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }}
    
    .investment-label {{
        font-size: 12px;
        font-weight: 500;
    }}
    
    .investment-value {{
        font-size: 24px;
        font-weight: 900;
    }}
    """

def render_slide_cover(slide, data):
    """شريحة الغلاف"""
    return f"""
    <div class="slide slide-cover">
        <div class="cover-border"></div>
        <div class="cover-watermark">CDA</div>
        
        <div class="cover-content">
            <div class="cover-subtitle">تقرير الرصد وتحليل المضمون</div>
            <h1 class="cover-title">{slide['title']}</h1>
            <h2 class="cover-title cover-title-gold">{slide['subtitle']}</h2>
            <p class="cover-tagline">{slide['content']['tagline']}</p>
        </div>
        
        <div class="cover-date">📅 {slide['content']['date']}</div>
        <div class="cover-confidential">🔒 {slide['content']['classification']}</div>
    </div>
    """

def render_slide_toc(slide, data):
    """شريحة جدول المحتويات"""
    sections_html = ""
    for section in slide['content']['sections']:
        sections_html += f"""
        <div class="toc-card">
            <div class="toc-card-num">{section['num']}</div>
            <div class="toc-card-title">{section['title']}</div>
            <div class="toc-card-desc">{section['desc']}</div>
        </div>
        """
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="toc-grid">
                {sections_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_about(slide, data):
    """شريحة من نحن"""
    stats_html = ""
    for stat in slide['content']['stats']:
        stats_html += f"""
        <div class="stat-card">
            <div class="stat-value">{stat['value']}</div>
            <div class="stat-label">{stat['label']}</div>
        </div>
        """
    
    specs_html = "".join([f"<li>{s}</li>" for s in slide['content']['specializations']])
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <p style="font-size: 18px; margin-bottom: 25px; color: rgba(255,255,255,0.9);">{slide['content']['intro']}</p>
            <div class="stats-grid">
                {stats_html}
            </div>
            <div class="two-columns" style="margin-top: 20px;">
                <div class="column">
                    <div class="column-title">تخصصاتنا</div>
                    <ul class="list">{specs_html}</ul>
                </div>
                <div class="column">
                    <div class="column-title">عملاؤنا</div>
                    <ul class="list">
                        {"".join([f"<li>{c}</li>" for c in slide['content']['clients_served']])}
                    </ul>
                </div>
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_methodology(slide, data):
    """شريحة المنهجية"""
    phases_html = ""
    for phase in slide['content']['phases']:
        items = "".join([f"<li>{i}</li>" for i in phase['items']])
        phases_html += f"""
        <div class="card">
            <div class="card-title" style="color: {COLORS['gold']};">{phase['num']}. {phase['title']}</div>
            <ul class="list" style="font-size: 12px;">{items}</ul>
        </div>
        """
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="cards-grid">
                {phases_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_overview(slide, data):
    """شريحة نظرة عامة على الهيئة"""
    values_html = "".join([f"<span style='background: rgba(184,134,11,0.2); padding: 8px 15px; border-radius: 20px; margin-left: 10px; font-size: 14px;'>{v}</span>" for v in slide['content']['values']])
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="two-columns">
                <div class="column">
                    <div class="card" style="margin-bottom: 15px;">
                        <div class="card-title" style="color: {COLORS['gold']};">الرؤية</div>
                        <div class="card-text" style="font-size: 18px; font-weight: 500;">"{slide['content']['vision']}"</div>
                    </div>
                    <div class="card">
                        <div class="card-title" style="color: {COLORS['gold']};">الرسالة</div>
                        <div class="card-text" style="font-size: 14px;">"{slide['content']['mission']}"</div>
                    </div>
                </div>
                <div class="column">
                    <div class="stats-grid" style="grid-template-columns: repeat(2, 1fr);">
                        <div class="stat-card">
                            <div class="stat-value">{slide['content']['established']}</div>
                            <div class="stat-label">سنة التأسيس</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{slide['content']['employees']}</div>
                            <div class="stat-label">الموظفون</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{slide['content']['branches']}</div>
                            <div class="stat-label">مراكز الخدمة</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{slide['content']['annual_beneficiaries']}</div>
                            <div class="stat-label">المستفيدون سنوياً</div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <div class="column-title">القيم المؤسسية</div>
                {values_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_audience(slide, data):
    """شريحة الفئات المستهدفة"""
    segments_html = ""
    for seg in slide['content']['segments']:
        services = "، ".join(seg['services'])
        segments_html += f"""
        <div class="card">
            <div class="card-icon">{seg['icon']}</div>
            <div class="card-title">{seg['name']}</div>
            <div class="card-text">
                <strong style="color: {COLORS['gold']};">{seg['size']}</strong> مستفيد<br>
                <span style="font-size: 11px;">{services}</span>
            </div>
        </div>
        """
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="cards-grid" style="grid-template-columns: repeat(3, 1fr);">
                {segments_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_swot(slide, data):
    """شريحة SWOT"""
    c = slide['content']
    
    def make_list(items):
        return "".join([f"<li>{i}</li>" for i in items])
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="swot-grid">
                <div class="swot-box strengths">
                    <div class="swot-title" style="color: #28a745;">💪 نقاط القوة</div>
                    <ul class="swot-list">{make_list(c['strengths'])}</ul>
                </div>
                <div class="swot-box weaknesses">
                    <div class="swot-title" style="color: #dc3545;">⚠️ نقاط الضعف</div>
                    <ul class="swot-list">{make_list(c['weaknesses'])}</ul>
                </div>
                <div class="swot-box opportunities">
                    <div class="swot-title" style="color: #ffc107;">🎯 الفرص</div>
                    <ul class="swot-list">{make_list(c['opportunities'])}</ul>
                </div>
                <div class="swot-box threats">
                    <div class="swot-title" style="color: #6c757d;">⚡ التهديدات</div>
                    <ul class="swot-list">{make_list(c['threats'])}</ul>
                </div>
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_problem_detail(slide, data):
    """شريحة تفاصيل المشكلة"""
    evidence = slide['content'].get('evidence', [])
    evidence_html = "".join([f"<li>{e}</li>" for e in evidence])
    
    causes = slide['content'].get('root_causes', [])
    causes_html = "".join([f"<li>{c}</li>" for c in causes]) if causes else ""
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="problem-header">
                <div class="problem-statement">{slide['content']['problem_statement']}</div>
            </div>
            <div class="two-columns">
                <div class="column">
                    <div class="evidence-box">
                        <div class="evidence-title">📊 الأدلة والشواهد</div>
                        <ul class="list" style="font-size: 13px;">{evidence_html}</ul>
                    </div>
                </div>
                <div class="column">
                    <div class="evidence-box">
                        <div class="evidence-title">🔍 الأسباب الجذرية</div>
                        <ul class="list" style="font-size: 13px;">{causes_html if causes_html else '<li>تحليل معمق مطلوب</li>'}</ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_package_detail(slide, data):
    """شريحة تفاصيل الحزمة"""
    deliverables_html = ""
    for d in slide['content']['deliverables']:
        deliverables_html += f"""
        <div class="deliverable-card">
            <div class="deliverable-title">{d['item']}</div>
            <div class="deliverable-desc">{d['description']}</div>
            <div class="deliverable-output">📦 {d['output']}</div>
        </div>
        """
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="package-header">
                <div style="font-size: 16px; color: white;">{slide['content']['objective']}</div>
                <div class="package-meta">
                    <div class="package-meta-item"><strong>المدة:</strong> {slide['content']['duration']}</div>
                </div>
            </div>
            <div class="deliverables-grid">
                {deliverables_html}
            </div>
            <div class="investment-box">
                <div class="investment-label">الاستثمار المقدر</div>
                <div class="investment-value">{slide['content']['investment']}</div>
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_roadmap(slide, data):
    """شريحة خارطة الطريق"""
    quarters_html = ""
    for q_key in ['q1', 'q2', 'q3', 'q4']:
        q = slide['content'][q_key]
        activities = "".join([f"<li>{a}</li>" for a in q['activities']])
        quarters_html += f"""
        <div class="timeline-item">
            <div class="timeline-quarter">{q['title']}</div>
            <div class="timeline-focus">{q['focus']}</div>
            <ul class="timeline-list">{activities}</ul>
            <div style="margin-top: 10px; font-size: 11px; color: {COLORS['gold']};">🎯 {q['milestone']}</div>
        </div>
        """
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="timeline">
                {quarters_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_kpis(slide, data):
    """شريحة مؤشرات الأداء"""
    def render_kpi_table(category, metrics):
        rows = ""
        for m in metrics:
            rows += f"""
            <tr>
                <td>{m['metric']}</td>
                <td style="color: #dc3545;">{m['current']}</td>
                <td style="color: #ffc107;">{m['year1']}</td>
                <td style="color: #28a745;">{m['year3']}</td>
            </tr>
            """
        return f"""
        <div class="table-container" style="margin-bottom: 15px;">
            <div style="font-size: 14px; font-weight: 700; color: {COLORS['gold']}; margin-bottom: 10px;">{category}</div>
            <table>
                <tr>
                    <th>المؤشر</th>
                    <th>الحالي</th>
                    <th>السنة 1</th>
                    <th>السنة 3</th>
                </tr>
                {rows}
            </table>
        </div>
        """
    
    c = slide['content']
    tables_html = ""
    tables_html += render_kpi_table(c['awareness_kpis']['category'], c['awareness_kpis']['metrics'])
    tables_html += render_kpi_table(c['engagement_kpis']['category'], c['engagement_kpis']['metrics'])
    tables_html += render_kpi_table(c['reputation_kpis']['category'], c['reputation_kpis']['metrics'])
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            {tables_html}
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_thank_you(slide, data):
    """شريحة الشكر"""
    return f"""
    <div class="slide slide-thanks">
        <div class="cover-border"></div>
        <div class="cover-watermark">CDA</div>
        
        <div class="thanks-title">{slide['title']}</div>
        <div class="thanks-subtitle">{slide['subtitle']}</div>
        
        <div class="thanks-quote">
            "{slide['content']['closing_message']}"
        </div>
        
        <div class="contact-grid">
            <div class="contact-item">
                <div class="contact-icon">📧</div>
                <div class="contact-text">{slide['content']['contact']['email']}</div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">📞</div>
                <div class="contact-text">{slide['content']['contact']['phone']}</div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">🌐</div>
                <div class="contact-text">{slide['content']['contact']['website']}</div>
            </div>
        </div>
    </div>
    """

def render_slide_generic(slide, data):
    """شريحة عامة"""
    content_html = ""
    
    # Try to render content based on what's available
    if 'content' in slide:
        c = slide['content']
        
        # If there are packages overview
        if 'packages' in c:
            content_html = '<div class="cards-grid" style="grid-template-columns: repeat(3, 1fr);">'
            for pkg in c['packages']:
                content_html += f"""
                <div class="card">
                    <div class="card-icon">{pkg['icon']}</div>
                    <div class="card-title">{pkg['name']}</div>
                    <div class="card-text">
                        <span class="priority-{'high' if pkg['priority'] == 'حرج' or pkg['priority'] == 'أساسي' else 'medium'}">{pkg['priority']}</span>
                        <br><small>{pkg['timeline']}</small>
                    </div>
                </div>
                """
            content_html += '</div>'
        
        # If there are steps
        elif 'immediate_steps' in c:
            content_html = '<div class="timeline">'
            for step in c['immediate_steps']:
                content_html += f"""
                <div class="timeline-item" style="flex: 1;">
                    <div class="timeline-quarter">الخطوة {step['step']}</div>
                    <div style="font-size: 16px; font-weight: 700; color: white; margin: 10px 0;">{step['action']}</div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.7);">{step['description']}</div>
                    <div style="margin-top: 10px; font-size: 11px; color: {COLORS['gold']};">⏱️ {step['timeline']}</div>
                </div>
                """
            content_html += '</div>'
        
        # If there are differentiators
        elif 'differentiators' in c:
            content_html = '<div class="cards-grid" style="grid-template-columns: repeat(3, 1fr);">'
            for d in c['differentiators']:
                content_html += f"""
                <div class="card">
                    <div class="card-icon">{d['icon']}</div>
                    <div class="card-title">{d['point']}</div>
                    <div class="card-text">{d['detail']}</div>
                </div>
                """
            content_html += '</div>'
        
        # If there are scenarios (investment)
        elif 'scenarios' in c:
            content_html = '<div class="two-columns">'
            for scenario in c['scenarios']:
                includes = "".join([f"<li>{i}</li>" for i in scenario['includes']])
                content_html += f"""
                <div class="card" style="padding: 20px;">
                    <div class="card-title" style="font-size: 20px; margin-bottom: 15px;">{scenario['name']}</div>
                    <div class="card-text" style="margin-bottom: 15px;">{scenario['description']}</div>
                    <ul class="list" style="font-size: 12px; margin-bottom: 15px;">{includes}</ul>
                    <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr); gap: 10px;">
                        <div class="stat-card" style="padding: 10px;">
                            <div class="stat-value" style="font-size: 18px;">{scenario['year1']}</div>
                            <div class="stat-label" style="font-size: 10px;">السنة 1</div>
                        </div>
                        <div class="stat-card" style="padding: 10px;">
                            <div class="stat-value" style="font-size: 18px;">{scenario['year2']}</div>
                            <div class="stat-label" style="font-size: 10px;">السنة 2</div>
                        </div>
                        <div class="stat-card" style="padding: 10px;">
                            <div class="stat-value" style="font-size: 18px;">{scenario['year3']}</div>
                            <div class="stat-label" style="font-size: 10px;">السنة 3</div>
                        </div>
                    </div>
                    <div class="investment-box" style="margin-top: 15px;">
                        <div class="investment-label">إجمالي 3 سنوات</div>
                        <div class="investment-value">{scenario['total_3y']}</div>
                    </div>
                </div>
                """
            content_html += '</div>'
        
        # Default: try to show any available info
        else:
            content_html = f'<div class="card"><div class="card-text">{str(c)[:500]}...</div></div>'
    
    return f"""
    <div class="slide slide-standard">
        <div class="slide-header">
            <div class="slide-header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide.get('subtitle', '')}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            {content_html}
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide(slide, data):
    """اختيار القالب المناسب للشريحة"""
    slide_type = slide.get('type', 'generic')
    
    renderers = {
        'cover': render_slide_cover,
        'toc': render_slide_toc,
        'about': render_slide_about,
        'methodology': render_slide_methodology,
        'overview': render_slide_overview,
        'audience': render_slide_audience,
        'swot': render_slide_swot,
        'problem_detail': render_slide_problem_detail,
        'package_detail': render_slide_package_detail,
        'roadmap': render_slide_roadmap,
        'kpis': render_slide_kpis,
        'thank_you': render_slide_thank_you,
    }
    
    renderer = renderers.get(slide_type, render_slide_generic)
    return renderer(slide, data)

def generate_html(data):
    """إنشاء HTML كامل للعرض"""
    slides_html = ""
    for slide in data['slides']:
        slides_html += render_slide(slide, data)
    
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data['presentation']['title']} - {data['presentation']['client']}</title>
        <style>
            {generate_css()}
        </style>
    </head>
    <body>
        {slides_html}
    </body>
    </html>
    """

def export_pdf(html_content, output_path):
    """تصدير HTML إلى PDF"""
    font_config = FontConfiguration()
    
    # Create exports directory if not exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html = HTML(string=html_content)
    css = CSS(string=generate_css(), font_config=font_config)
    
    html.write_pdf(output_path, stylesheets=[css], font_config=font_config)
    print(f"✅ تم تصدير PDF إلى: {output_path}")

def main():
    print("🚀 بدء تصدير العرض التقديمي...")
    print("=" * 50)
    
    # Load presentation data
    data = load_presentation()
    print(f"📊 تم تحميل العرض: {data['presentation']['title']}")
    print(f"📑 عدد الشرائح: {len(data['slides'])}")
    
    # Generate HTML
    html_content = generate_html(data)
    
    # Save HTML
    os.makedirs("exports", exist_ok=True)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"📄 تم حفظ HTML إلى: {OUTPUT_HTML}")
    
    # Export PDF
    try:
        export_pdf(html_content, OUTPUT_PDF)
    except Exception as e:
        print(f"⚠️ خطأ في تصدير PDF: {e}")
        print("💡 جرب: pip install weasyprint")
    
    print("=" * 50)
    print("✨ اكتمل التصدير بنجاح!")

if __name__ == "__main__":
    main()
