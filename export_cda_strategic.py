#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تصدير العرض التقديمي الاستراتيجي لهيئة تنمية المجتمع - دبي
Export CDA Dubai Strategic Presentation to PDF (16:9)
الإصدار المحسّن بالهوية الرسمية
"""

import json
import os
import asyncio
from playwright.async_api import async_playwright

# مسار ملف JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data/presentations/cda_dubai_pitch_v2.json")
OUTPUT_PDF = os.path.join(BASE_DIR, "exports/CDA_Dubai_Strategic_2026.pdf")
OUTPUT_HTML = os.path.join(BASE_DIR, "exports/CDA_Dubai_Strategic_2026.html")

# ═══════════════════════════════════════════════════════════════════════════════
# الهوية البصرية الرسمية لهيئة تنمية المجتمع وحكومة دبي
# ═══════════════════════════════════════════════════════════════════════════════
COLORS = {
    "primary": "#C41E3A",        # أحمر عنابي - اللون الرئيسي للهيئة
    "primary_dark": "#8B0A1A",   # عنابي داكن
    "primary_light": "#E85A70",  # عنابي فاتح
    "gold": "#D4AF37",           # ذهبي حكومة دبي
    "gold_dark": "#B8860B",      # ذهبي داكن
    "accent": "#1A1A2E",         # كحلي داكن
    "white": "#FFFFFF",
    "off_white": "#F8F5F2",
    "black": "#1A1A1A",
    "gray": "#6B7280",
    "gray_light": "#9CA3AF"
}

def load_presentation():
    """تحميل بيانات العرض من JSON"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_css():
    """إنشاء CSS احترافي للعرض"""
    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    @page {{
        size: 1920px 1080px;
        margin: 0;
    }}
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Tajawal', -apple-system, BlinkMacSystemFont, sans-serif;
        direction: rtl;
        background: {COLORS['black']};
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الشريحة الأساسية
       ═══════════════════════════════════════════════════════════════ */
    .slide {{
        width: 1920px;
        height: 1080px;
        position: relative;
        overflow: hidden;
        page-break-after: always;
        page-break-inside: avoid;
        display: flex;
        flex-direction: column;
        padding: 70px 90px;
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['accent']} 100%);
    }}
    
    .slide::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(196, 30, 58, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(212, 175, 55, 0.1) 0%, transparent 40%);
        pointer-events: none;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       شريحة الغلاف
       ═══════════════════════════════════════════════════════════════ */
    .slide-cover {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['accent']} 100%);
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 0;
    }}
    
    .cover-pattern {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(196, 30, 58, 0.03) 40px, rgba(196, 30, 58, 0.03) 80px),
            repeating-linear-gradient(-45deg, transparent, transparent 40px, rgba(212, 175, 55, 0.02) 40px, rgba(212, 175, 55, 0.02) 80px);
    }}
    
    .cover-frame {{
        position: absolute;
        top: 50px;
        left: 50px;
        right: 50px;
        bottom: 50px;
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
    }}
    
    .cover-frame::before {{
        content: '';
        position: absolute;
        top: -2px;
        left: 100px;
        right: 100px;
        height: 4px;
        background: linear-gradient(90deg, transparent, {COLORS['gold']}, transparent);
    }}
    
    .cover-frame::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        left: 100px;
        right: 100px;
        height: 4px;
        background: linear-gradient(90deg, transparent, {COLORS['gold']}, transparent);
    }}
    
    .cover-logo-bar {{
        position: absolute;
        top: 80px;
        left: 100px;
        right: 100px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .cover-logo {{
        height: 70px;
        opacity: 0.9;
    }}
    
    .cover-content {{
        position: relative;
        z-index: 10;
        max-width: 1400px;
    }}
    
    .cover-preheader {{
        color: {COLORS['gold']};
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }}
    
    .cover-title {{
        color: {COLORS['white']};
        font-size: 76px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 20px;
        text-shadow: 0 4px 30px rgba(0,0,0,0.3);
    }}
    
    .cover-subtitle {{
        color: {COLORS['gold']};
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 50px;
    }}
    
    .cover-tagline {{
        color: rgba(255,255,255,0.8);
        font-size: 28px;
        font-weight: 400;
        max-width: 900px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    .cover-footer {{
        position: absolute;
        bottom: 80px;
        left: 100px;
        right: 100px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .cover-date {{
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.4);
        padding: 15px 40px;
        border-radius: 50px;
        color: {COLORS['gold']};
        font-size: 18px;
        font-weight: 500;
    }}
    
    .cover-classification {{
        color: rgba(255,255,255,0.5);
        font-size: 14px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       رأس الشريحة القياسية
       ═══════════════════════════════════════════════════════════════ */
    .slide-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 50px;
        position: relative;
        z-index: 10;
    }}
    
    .header-content {{
        flex: 1;
    }}
    
    .slide-number {{
        width: 90px;
        height: 90px;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: {COLORS['white']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        font-weight: 800;
        box-shadow: 0 8px 30px rgba(196, 30, 58, 0.4);
        border: 3px solid rgba(212, 175, 55, 0.3);
    }}
    
    .slide-title {{
        color: {COLORS['white']};
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 12px;
        line-height: 1.2;
    }}
    
    .slide-subtitle {{
        color: {COLORS['gold']};
        font-size: 26px;
        font-weight: 500;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       محتوى الشريحة
       ═══════════════════════════════════════════════════════════════ */
    .slide-body {{
        flex: 1;
        color: {COLORS['white']};
        position: relative;
        z-index: 10;
    }}
    
    .slide-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 25px;
        border-top: 1px solid rgba(255,255,255,0.1);
        font-size: 14px;
        color: rgba(255,255,255,0.4);
        position: relative;
        z-index: 10;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الملخص التنفيذي
       ═══════════════════════════════════════════════════════════════ */
    .exec-summary {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 50px;
        height: 100%;
    }}
    
    .exec-context {{
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
        padding: 40px;
        border-right: 5px solid {COLORS['primary']};
    }}
    
    .exec-context-title {{
        color: {COLORS['gold']};
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 20px;
    }}
    
    .exec-context-text {{
        font-size: 22px;
        line-height: 1.8;
        color: rgba(255,255,255,0.9);
    }}
    
    .exec-pillars {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }}
    
    .exec-pillar {{
        background: linear-gradient(135deg, rgba(196, 30, 58, 0.15) 0%, rgba(0,0,0,0.3) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 30px;
        transition: transform 0.3s;
    }}
    
    .exec-pillar-title {{
        color: {COLORS['gold']};
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }}
    
    .exec-pillar-desc {{
        color: rgba(255,255,255,0.8);
        font-size: 16px;
        line-height: 1.6;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       البطاقات والشبكات
       ═══════════════════════════════════════════════════════════════ */
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
    }}
    
    .cards-grid-4 {{
        grid-template-columns: repeat(4, 1fr);
    }}
    
    .cards-grid-2 {{
        grid-template-columns: repeat(2, 1fr);
    }}
    
    .card {{
        background: linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 20px;
        padding: 35px;
        transition: all 0.3s ease;
    }}
    
    .card-highlight {{
        border-color: rgba(212, 175, 55, 0.4);
        background: linear-gradient(135deg, rgba(196, 30, 58, 0.1) 0%, rgba(0,0,0,0.3) 100%);
    }}
    
    .card-icon {{
        font-size: 48px;
        margin-bottom: 20px;
    }}
    
    .card-title {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 15px;
    }}
    
    .card-text {{
        font-size: 17px;
        color: rgba(255,255,255,0.75);
        line-height: 1.7;
    }}
    
    .card-metric {{
        font-size: 36px;
        font-weight: 900;
        color: {COLORS['gold']};
        margin-bottom: 5px;
    }}
    
    .card-label {{
        font-size: 15px;
        color: rgba(255,255,255,0.6);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الإحصائيات
       ═══════════════════════════════════════════════════════════════ */
    .stats-row {{
        display: flex;
        gap: 30px;
        margin: 30px 0;
    }}
    
    .stat-box {{
        flex: 1;
        background: linear-gradient(135deg, rgba(196, 30, 58, 0.2) 0%, rgba(0,0,0,0.3) 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 56px;
        font-weight: 900;
        color: {COLORS['gold']};
        margin-bottom: 8px;
    }}
    
    .stat-label {{
        font-size: 18px;
        color: rgba(255,255,255,0.7);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       عمودين
       ═══════════════════════════════════════════════════════════════ */
    .two-columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 50px;
    }}
    
    .column-title {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 3px solid rgba(212, 175, 55, 0.3);
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       القوائم
       ═══════════════════════════════════════════════════════════════ */
    .list {{
        list-style: none;
    }}
    
    .list li {{
        padding: 15px 0;
        padding-right: 35px;
        position: relative;
        font-size: 19px;
        line-height: 1.6;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }}
    
    .list li:last-child {{
        border-bottom: none;
    }}
    
    .list li::before {{
        content: '';
        position: absolute;
        right: 0;
        top: 22px;
        width: 12px;
        height: 12px;
        background: {COLORS['gold']};
        border-radius: 50%;
    }}
    
    .list-check li::before {{
        content: '✓';
        background: transparent;
        color: {COLORS['gold']};
        font-weight: bold;
        font-size: 18px;
        top: 15px;
        width: auto;
        height: auto;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       التشخيص والتحديات
       ═══════════════════════════════════════════════════════════════ */
    .diagnosis-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
    }}
    
    .diagnosis-item {{
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border-top: 4px solid {COLORS['gold']};
    }}
    
    .diagnosis-score {{
        font-size: 14px;
        font-weight: 600;
        color: {COLORS['primary']};
        background: rgba(196, 30, 58, 0.15);
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 15px;
    }}
    
    .diagnosis-score.good {{
        color: #22c55e;
        background: rgba(34, 197, 94, 0.15);
    }}
    
    .diagnosis-score.medium {{
        color: {COLORS['gold']};
        background: rgba(212, 175, 55, 0.15);
    }}
    
    .diagnosis-dimension {{
        font-size: 16px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 10px;
    }}
    
    .diagnosis-detail {{
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        line-height: 1.5;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       التحديات
       ═══════════════════════════════════════════════════════════════ */
    .challenges-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
    }}
    
    .challenge-card {{
        background: linear-gradient(180deg, rgba(196, 30, 58, 0.15) 0%, rgba(0,0,0,0.4) 100%);
        border: 1px solid rgba(196, 30, 58, 0.3);
        border-radius: 20px;
        padding: 35px;
        text-align: center;
    }}
    
    .challenge-icon {{
        font-size: 56px;
        margin-bottom: 20px;
    }}
    
    .challenge-title {{
        font-size: 22px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 15px;
    }}
    
    .challenge-summary {{
        font-size: 16px;
        color: rgba(255,255,255,0.7);
        margin-bottom: 20px;
        line-height: 1.5;
    }}
    
    .challenge-impact {{
        font-size: 14px;
        color: {COLORS['primary_light']};
        background: rgba(196, 30, 58, 0.1);
        padding: 10px 15px;
        border-radius: 10px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       المشكلة التفصيلية
       ═══════════════════════════════════════════════════════════════ */
    .problem-box {{
        background: linear-gradient(135deg, rgba(196, 30, 58, 0.1) 0%, rgba(0,0,0,0.3) 100%);
        border: 2px solid rgba(196, 30, 58, 0.3);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
    }}
    
    .problem-statement {{
        font-size: 24px;
        font-weight: 500;
        color: {COLORS['white']};
        line-height: 1.7;
    }}
    
    .evidence-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
    }}
    
    .evidence-box {{
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 30px;
    }}
    
    .evidence-title {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الإطار الاستراتيجي
       ═══════════════════════════════════════════════════════════════ */
    .framework-vision {{
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(0,0,0,0.3) 100%);
        border: 2px solid rgba(212, 175, 55, 0.4);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 40px;
    }}
    
    .framework-vision-text {{
        font-size: 28px;
        font-weight: 600;
        color: {COLORS['white']};
        line-height: 1.6;
    }}
    
    .framework-pillars {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
    }}
    
    .framework-pillar {{
        background: linear-gradient(180deg, rgba(196, 30, 58, 0.2) 0%, rgba(0,0,0,0.4) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 35px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .framework-pillar::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['gold']});
    }}
    
    .pillar-icon {{
        font-size: 48px;
        margin-bottom: 20px;
    }}
    
    .pillar-title {{
        font-size: 22px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 15px;
    }}
    
    .pillar-objective {{
        font-size: 16px;
        color: {COLORS['gold']};
        font-style: italic;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       تفاصيل الركيزة
       ═══════════════════════════════════════════════════════════════ */
    .pillar-detail-header {{
        background: linear-gradient(135deg, rgba(196, 30, 58, 0.2) 0%, rgba(0,0,0,0.3) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
    }}
    
    .pillar-objective-text {{
        font-size: 22px;
        color: {COLORS['white']};
        line-height: 1.6;
    }}
    
    .initiatives-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
    }}
    
    .initiative-card {{
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 30px;
        border-right: 4px solid {COLORS['gold']};
    }}
    
    .initiative-title {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 15px;
    }}
    
    .initiative-desc {{
        font-size: 15px;
        color: rgba(255,255,255,0.8);
        margin-bottom: 15px;
        line-height: 1.6;
    }}
    
    .initiative-deliverables {{
        font-size: 13px;
        color: rgba(255,255,255,0.6);
    }}
    
    .initiative-impact {{
        margin-top: 15px;
        font-size: 14px;
        color: {COLORS['primary_light']};
        font-weight: 500;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       خارطة الطريق
       ═══════════════════════════════════════════════════════════════ */
    .roadmap-phases {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
        position: relative;
    }}
    
    .roadmap-phases::before {{
        content: '';
        position: absolute;
        top: 60px;
        left: 5%;
        right: 5%;
        height: 4px;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['gold']}, {COLORS['primary']}, {COLORS['gold']});
        border-radius: 2px;
    }}
    
    .roadmap-phase {{
        background: rgba(0,0,0,0.4);
        border-radius: 20px;
        padding: 30px;
        position: relative;
        z-index: 1;
    }}
    
    .phase-marker {{
        width: 50px;
        height: 50px;
        background: {COLORS['gold']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 800;
        color: {COLORS['primary_dark']};
        margin: 0 auto 20px;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.4);
    }}
    
    .phase-title {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['white']};
        text-align: center;
        margin-bottom: 10px;
    }}
    
    .phase-period {{
        font-size: 14px;
        color: {COLORS['gold']};
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .phase-focus {{
        font-size: 15px;
        color: rgba(255,255,255,0.7);
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    
    .phase-milestones {{
        list-style: none;
        font-size: 13px;
    }}
    
    .phase-milestones li {{
        padding: 8px 0;
        padding-right: 20px;
        position: relative;
        color: rgba(255,255,255,0.8);
    }}
    
    .phase-milestones li::before {{
        content: '→';
        position: absolute;
        right: 0;
        color: {COLORS['gold']};
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الأرباع السنوية
       ═══════════════════════════════════════════════════════════════ */
    .quarters-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
    }}
    
    .quarter-card {{
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 30px;
        border-top: 5px solid {COLORS['gold']};
    }}
    
    .quarter-title {{
        font-size: 22px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 10px;
    }}
    
    .quarter-focus {{
        font-size: 14px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    
    .quarter-activities {{
        list-style: none;
        font-size: 14px;
        margin-bottom: 20px;
    }}
    
    .quarter-activities li {{
        padding: 8px 0;
        padding-right: 20px;
        position: relative;
        color: rgba(255,255,255,0.8);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }}
    
    .quarter-activities li::before {{
        content: '•';
        position: absolute;
        right: 0;
        color: {COLORS['primary']};
        font-size: 18px;
    }}
    
    .quarter-deliverable {{
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }}
    
    .quarter-deliverable-label {{
        font-size: 12px;
        color: rgba(255,255,255,0.5);
        margin-bottom: 5px;
    }}
    
    .quarter-deliverable-text {{
        font-size: 14px;
        font-weight: 600;
        color: {COLORS['gold']};
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       مؤشرات الأداء
       ═══════════════════════════════════════════════════════════════ */
    .kpi-section {{
        background: rgba(0,0,0,0.2);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }}
    
    .kpi-section-title {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['gold']};
        margin-bottom: 20px;
    }}
    
    .kpi-table {{
        width: 100%;
        border-collapse: collapse;
    }}
    
    .kpi-table th {{
        background: {COLORS['primary']};
        color: {COLORS['white']};
        padding: 15px 20px;
        text-align: right;
        font-weight: 600;
        font-size: 15px;
    }}
    
    .kpi-table th:first-child {{
        border-radius: 0 10px 10px 0;
    }}
    
    .kpi-table th:last-child {{
        border-radius: 10px 0 0 10px;
    }}
    
    .kpi-table td {{
        padding: 15px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 15px;
        color: {COLORS['white']};
    }}
    
    .kpi-current {{
        color: rgba(255,255,255,0.5) !important;
    }}
    
    .kpi-y1 {{
        color: {COLORS['gold']} !important;
        font-weight: 600;
    }}
    
    .kpi-y3 {{
        color: #22c55e !important;
        font-weight: 700;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       لماذا نحن
       ═══════════════════════════════════════════════════════════════ */
    .why-us-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 25px;
    }}
    
    .why-us-card {{
        background: linear-gradient(180deg, rgba(196, 30, 58, 0.15) 0%, rgba(0,0,0,0.4) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 35px 25px;
        text-align: center;
    }}
    
    .why-us-icon {{
        font-size: 48px;
        margin-bottom: 20px;
    }}
    
    .why-us-point {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 15px;
    }}
    
    .why-us-detail {{
        font-size: 14px;
        color: rgba(255,255,255,0.7);
        line-height: 1.6;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       الخطوات التالية
       ═══════════════════════════════════════════════════════════════ */
    .next-steps {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
    }}
    
    .next-step {{
        background: rgba(0,0,0,0.3);
        border-radius: 16px;
        padding: 35px;
        position: relative;
        border-top: 5px solid {COLORS['gold']};
    }}
    
    .step-number {{
        position: absolute;
        top: -20px;
        right: 30px;
        width: 40px;
        height: 40px;
        background: {COLORS['gold']};
        color: {COLORS['primary_dark']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 800;
    }}
    
    .step-action {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 15px;
        margin-top: 10px;
    }}
    
    .step-desc {{
        font-size: 15px;
        color: rgba(255,255,255,0.7);
        margin-bottom: 20px;
        line-height: 1.6;
    }}
    
    .step-timeline {{
        font-size: 14px;
        color: {COLORS['gold']};
        font-weight: 500;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       شريحة الشكر
       ═══════════════════════════════════════════════════════════════ */
    .slide-thanks {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['accent']} 100%);
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    
    .thanks-content {{
        position: relative;
        z-index: 10;
        max-width: 1200px;
    }}
    
    .thanks-title {{
        font-size: 96px;
        font-weight: 900;
        color: {COLORS['white']};
        margin-bottom: 25px;
        text-shadow: 0 4px 30px rgba(0,0,0,0.3);
    }}
    
    .thanks-subtitle {{
        font-size: 36px;
        color: {COLORS['gold']};
        margin-bottom: 50px;
    }}
    
    .thanks-quote {{
        font-size: 26px;
        color: rgba(255,255,255,0.85);
        line-height: 1.8;
        max-width: 1000px;
        margin: 0 auto 50px;
        padding: 30px 50px;
        border-right: 5px solid {COLORS['gold']};
        background: rgba(0,0,0,0.2);
        border-radius: 0 20px 20px 0;
    }}
    
    .contact-row {{
        display: flex;
        justify-content: center;
        gap: 60px;
        margin-top: 40px;
    }}
    
    .contact-item {{
        text-align: center;
    }}
    
    .contact-icon {{
        font-size: 32px;
        color: {COLORS['gold']};
        margin-bottom: 10px;
    }}
    
    .contact-text {{
        font-size: 20px;
        color: {COLORS['white']};
    }}
    
    .thanks-tagline {{
        margin-top: 50px;
        font-size: 22px;
        color: {COLORS['gold']};
        font-weight: 500;
        letter-spacing: 3px;
    }}
    """

# ═══════════════════════════════════════════════════════════════════════════════
# دوال عرض الشرائح
# ═══════════════════════════════════════════════════════════════════════════════

def render_slide_cover(slide, data):
    """شريحة الغلاف"""
    return f"""
    <div class="slide slide-cover">
        <div class="cover-pattern"></div>
        <div class="cover-frame"></div>
        
        <div class="cover-content">
            <div class="cover-preheader">وثيقة عمل استراتيجية</div>
            <h1 class="cover-title">{slide['title']}</h1>
            <h2 class="cover-subtitle">{slide['subtitle']}</h2>
            <p class="cover-tagline">{slide['content']['vision_statement']}</p>
        </div>
        
        <div class="cover-footer">
            <div class="cover-date">📅 {slide['content']['date']}</div>
            <div class="cover-classification">🔒 {slide['content']['classification']}</div>
        </div>
    </div>
    """

def render_slide_executive_summary(slide, data):
    """شريحة الملخص التنفيذي"""
    pillars_html = ""
    for p in slide['content']['pillars']:
        pillars_html += f"""
        <div class="exec-pillar">
            <div class="exec-pillar-title">{p['title']}</div>
            <div class="exec-pillar-desc">{p['desc']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="exec-summary">
                <div>
                    <div class="exec-context">
                        <div class="exec-context-title">السياق</div>
                        <div class="exec-context-text">{slide['content']['context']}</div>
                    </div>
                    <div class="exec-context" style="margin-top: 25px; border-right-color: {COLORS['gold']};">
                        <div class="exec-context-title">الفرصة</div>
                        <div class="exec-context-text">{slide['content']['opportunity']}</div>
                    </div>
                </div>
                <div class="exec-pillars">
                    {pillars_html}
                </div>
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_about_firm(slide, data):
    """شريحة من نحن"""
    expertise_html = ""
    for e in slide['content']['expertise_areas']:
        expertise_html += f"""
        <div class="card">
            <div class="card-title" style="color: {COLORS['gold']};">{e['area']}</div>
            <div class="card-text">{e['detail']}</div>
        </div>
        """
    
    clients_html = "".join([f"<li>{c}</li>" for c in slide['content']['relevant_experience']])
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="two-columns">
                <div>
                    <p style="font-size: 20px; margin-bottom: 20px; color: rgba(255,255,255,0.9); line-height: 1.7;">{slide['content']['positioning']}</p>
                    <div class="exec-context" style="margin-top: 20px;">
                        <div class="exec-context-title">فلسفتنا</div>
                        <div style="font-size: 18px; line-height: 1.8; color: rgba(255,255,255,0.85);">"{slide['content']['philosophy']}"</div>
                    </div>
                </div>
                <div>
                    <div class="column-title">مجالات التخصص</div>
                    <div class="cards-grid cards-grid-2" style="gap: 15px;">
                        {expertise_html}
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

def render_slide_methodology(slide, data):
    """شريحة المنهجية"""
    phases_html = ""
    for p in slide['content']['phases']:
        phases_html += f"""
        <div class="card">
            <div class="card-title" style="color: {COLORS['gold']};">{p['phase']}</div>
            <div style="font-size: 14px; color: {COLORS['primary_light']}; margin-bottom: 10px;">{p['period']}</div>
            <div class="card-text">{p['scope']}</div>
            <div style="margin-top: 15px; font-size: 13px; color: rgba(255,255,255,0.5);">🔧 {p['tools']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <p style="font-size: 22px; margin-bottom: 30px; color: rgba(255,255,255,0.9);">{slide['content']['intro']}</p>
            <div class="cards-grid cards-grid-4">
                {phases_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_org_overview(slide, data):
    """شريحة نظرة عامة على الهيئة"""
    pillars_html = ""
    for p in slide['content']['strategic_pillars']:
        pillars_html += f"""
        <div class="card" style="padding: 25px;">
            <div class="card-title" style="font-size: 20px;">{p['pillar']}</div>
            <div class="card-text" style="font-size: 15px;">{p['scope']}</div>
        </div>
        """
    
    indicators = slide['content']['scale_indicators']
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="exec-context" style="margin-bottom: 30px;">
                <div style="font-size: 22px; line-height: 1.7; color: rgba(255,255,255,0.9);">{slide['content']['mandate']}</div>
            </div>
            <div class="two-columns">
                <div>
                    <div class="column-title">الركائز الاستراتيجية</div>
                    <div class="cards-grid cards-grid-2" style="gap: 15px;">
                        {pillars_html}
                    </div>
                </div>
                <div>
                    <div class="column-title">مؤشرات الحجم</div>
                    <div class="stats-row" style="flex-wrap: wrap;">
                        <div class="stat-box" style="min-width: 45%;">
                            <div class="stat-value">{indicators['beneficiaries']}</div>
                            <div class="stat-label">مستفيد</div>
                        </div>
                        <div class="stat-box" style="min-width: 45%;">
                            <div class="stat-value">{indicators['services']}</div>
                            <div class="stat-label">خدمة</div>
                        </div>
                        <div class="stat-box" style="min-width: 45%;">
                            <div class="stat-value">{indicators['centers']}</div>
                            <div class="stat-label">مركز خدمة</div>
                        </div>
                        <div class="stat-box" style="min-width: 45%;">
                            <div class="stat-value">{indicators['partners']}</div>
                            <div class="stat-label">شريك</div>
                        </div>
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

def render_slide_stakeholder_map(slide, data):
    """شريحة خارطة أصحاب المصلحة"""
    stakeholders_html = ""
    for s in slide['content']['primary_stakeholders']:
        stakeholders_html += f"""
        <div class="card" style="padding: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div class="card-title" style="margin-bottom: 0; font-size: 20px;">{s['segment']}</div>
                <div class="card-metric" style="font-size: 24px;">{s['size']}</div>
            </div>
            <div class="card-text" style="font-size: 14px; margin-bottom: 10px;"><strong style="color: {COLORS['gold']};">الاحتياج:</strong> {s['needs']}</div>
            <div class="card-text" style="font-size: 14px; margin-bottom: 10px;"><strong style="color: {COLORS['gold']};">القنوات:</strong> {s['channels']}</div>
            <div style="font-size: 13px; color: {COLORS['primary_light']}; background: rgba(196, 30, 58, 0.1); padding: 8px 12px; border-radius: 8px;">⚠️ {s['gap']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <p style="font-size: 20px; margin-bottom: 25px; color: rgba(255,255,255,0.85);">{slide['content']['intro']}</p>
            <div class="cards-grid cards-grid-2" style="gap: 20px;">
                {stakeholders_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_diagnosis_overview(slide, data):
    """شريحة التشخيص العام"""
    findings_html = ""
    for f in slide['content']['key_findings']:
        score_class = 'good' if 'إيجابي' in f['score'] else ('medium' if 'متوسط' in f['score'] else '')
        findings_html += f"""
        <div class="diagnosis-item">
            <div class="diagnosis-score {score_class}">{f['score']}</div>
            <div class="diagnosis-dimension">{f['dimension']}</div>
            <div class="diagnosis-detail">{f['detail']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="exec-context" style="margin-bottom: 35px;">
                <div style="font-size: 22px; line-height: 1.7; color: rgba(255,255,255,0.9);">{slide['content']['overall_assessment']}</div>
            </div>
            <div class="diagnosis-grid">
                {findings_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_challenge_overview(slide, data):
    """شريحة نظرة عامة على التحديات"""
    challenges_html = ""
    for c in slide['content']['challenges']:
        challenges_html += f"""
        <div class="challenge-card">
            <div class="challenge-icon">{c['icon']}</div>
            <div class="challenge-title">{c['title']}</div>
            <div class="challenge-summary">{c['summary']}</div>
            <div class="challenge-impact">{c['impact']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="challenges-grid">
                {challenges_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_challenge_detail(slide, data):
    """شريحة تفاصيل التحدي"""
    content = slide['content']
    
    # Handle standard format with problem_statement
    if 'problem_statement' in content:
        evidence_html = "".join([f"<li>{e}</li>" for e in content.get('evidence', [])])
        causes_html = "".join([f"<li>{c}</li>" for c in content.get('root_causes', [])])
        
        return f"""
        <div class="slide">
            <div class="slide-header">
                <div class="header-content">
                    <h1 class="slide-title">{slide['title']}</h1>
                    <p class="slide-subtitle">{slide['subtitle']}</p>
                </div>
                <div class="slide-number">{slide['id']:02d}</div>
            </div>
            <div class="slide-body">
                <div class="problem-box">
                    <div class="problem-statement">{content['problem_statement']}</div>
                </div>
                <div class="evidence-grid">
                    <div class="evidence-box">
                        <div class="evidence-title">📊 الأدلة والشواهد</div>
                        <ul class="list list-check">{evidence_html}</ul>
                    </div>
                    <div class="evidence-box">
                        <div class="evidence-title">🔍 الأسباب الجذرية</div>
                        <ul class="list list-check">{causes_html}</ul>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>هيئة تنمية المجتمع - دبي</span>
                <span>24°45° للاستشارات الاتصالية</span>
            </div>
        </div>
        """
    
    # Handle dual-gap format (narrative_gap + measurement_gap)
    if 'narrative_gap' in content and 'measurement_gap' in content:
        ng = content['narrative_gap']
        mg = content['measurement_gap']
        ng_evidence = "".join([f"<li>{e}</li>" for e in ng.get('evidence', [])])
        mg_evidence = "".join([f"<li>{e}</li>" for e in mg.get('evidence', [])])
        connection = content.get('connection', '')
        
        return f"""
        <div class="slide">
            <div class="slide-header">
                <div class="header-content">
                    <h1 class="slide-title">{slide['title']}</h1>
                    <p class="slide-subtitle">{slide['subtitle']}</p>
                </div>
                <div class="slide-number">{slide['id']:02d}</div>
            </div>
            <div class="slide-body">
                <div class="evidence-grid">
                    <div class="evidence-box" style="border-right: 4px solid {COLORS['primary']};">
                        <div class="evidence-title">📖 فجوة السرد</div>
                        <p style="font-size: 18px; margin-bottom: 15px; color: rgba(255,255,255,0.9);">{ng.get('problem', '')}</p>
                        <ul class="list list-check">{ng_evidence}</ul>
                        <div style="margin-top: 15px; font-size: 15px; color: {COLORS['primary_light']};">⚠️ {ng.get('impact', '')}</div>
                    </div>
                    <div class="evidence-box" style="border-right: 4px solid {COLORS['gold']};">
                        <div class="evidence-title">📊 فجوة القياس</div>
                        <p style="font-size: 18px; margin-bottom: 15px; color: rgba(255,255,255,0.9);">{mg.get('problem', '')}</p>
                        <ul class="list list-check">{mg_evidence}</ul>
                        <div style="margin-top: 15px; font-size: 15px; color: {COLORS['gold']};">⚠️ {mg.get('impact', '')}</div>
                    </div>
                </div>
                <div class="exec-context" style="margin-top: 25px; border-right-color: {COLORS['gold']}; text-align: center;">
                    <div style="font-size: 22px; color: {COLORS['white']};">💡 {connection}</div>
                </div>
            </div>
            <div class="slide-footer">
                <span>هيئة تنمية المجتمع - دبي</span>
                <span>24°45° للاستشارات الاتصالية</span>
            </div>
        </div>
        """
    
    # Fallback generic
    return render_slide_generic(slide, data)

def render_slide_framework_intro(slide, data):
    """شريحة مقدمة الإطار الاستراتيجي"""
    pillars_html = ""
    for p in slide['content']['framework_pillars']:
        pillars_html += f"""
        <div class="framework-pillar">
            <div class="pillar-icon">{p['icon']}</div>
            <div class="pillar-title">{p['pillar']}</div>
            <div class="pillar-objective">{p['objective']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="framework-vision">
                <div class="framework-vision-text">🎯 {slide['content']['vision']}</div>
            </div>
            <div class="framework-pillars">
                {pillars_html}
            </div>
            <div style="text-align: center; margin-top: 30px; font-size: 18px; color: rgba(255,255,255,0.7);">
                {slide['content']['integration_note']}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_pillar_detail(slide, data):
    """شريحة تفاصيل الركيزة"""
    content = slide['content']
    
    # Get objective
    objective = content.get('objective', '')
    
    body_html = ""
    
    # Type 1: strategic_initiatives (standard)
    if 'strategic_initiatives' in content:
        initiatives_html = ""
        for i in content['strategic_initiatives']:
            deliverables = "، ".join(i.get('deliverables', []))
            initiatives_html += f"""
            <div class="initiative-card">
                <div class="initiative-title">{i.get('initiative', '')}</div>
                <div class="initiative-desc">{i.get('description', '')}</div>
                <div class="initiative-deliverables">📦 {deliverables}</div>
                <div class="initiative-impact">✨ {i.get('impact', '')}</div>
            </div>
            """
        body_html = f"""
        <div class="pillar-detail-header">
            <div class="pillar-objective-text">🎯 {objective}</div>
        </div>
        <div class="initiatives-grid">
            {initiatives_html}
        </div>
        """
    
    # Type 2: narrative_architecture + story_bank_project
    elif 'narrative_architecture' in content:
        na = content['narrative_architecture']
        proof_points = "".join([f"<li>{p}</li>" for p in na.get('proof_points', [])])
        
        sb = content.get('story_bank_project', {})
        components_html = ""
        for comp in sb.get('components', []):
            components_html += f"""
            <div class="card" style="padding: 20px;">
                <div class="card-title" style="font-size: 18px; color: {COLORS['gold']};">{comp.get('component', '')}</div>
                <div class="card-text" style="font-size: 14px;">{comp.get('detail', '')}</div>
            </div>
            """
        
        body_html = f"""
        <div class="pillar-detail-header">
            <div class="pillar-objective-text">🎯 {objective}</div>
        </div>
        <div class="two-columns">
            <div>
                <div class="column-title">السرد الرئيسي</div>
                <div class="exec-context" style="margin-bottom: 20px;">
                    <div style="font-size: 22px; color: {COLORS['white']}; font-style: italic;">"{na.get('master_narrative', '')}"</div>
                </div>
                <div class="column-title" style="margin-top: 25px;">نقاط الإثبات</div>
                <ul class="list list-check">{proof_points}</ul>
            </div>
            <div>
                <div class="column-title">مشروع بنك القصص</div>
                <p style="font-size: 17px; margin-bottom: 20px; color: rgba(255,255,255,0.85);">{sb.get('description', '')}</p>
                <div class="cards-grid cards-grid-2" style="gap: 15px;">
                    {components_html}
                </div>
            </div>
        </div>
        """
    
    # Type 3: segmentation_approach
    elif 'segmentation_approach' in content:
        segments_html = ""
        for seg in content['segmentation_approach']:
            channels = "، ".join(seg.get('channels', []))
            segments_html += f"""
            <div class="card" style="padding: 25px;">
                <div class="card-title" style="font-size: 20px;">{seg.get('segment', '')}</div>
                <div style="font-size: 14px; color: {COLORS['gold']}; margin-bottom: 10px;">💡 {seg.get('key_insight', '')}</div>
                <div class="card-text" style="font-size: 14px; margin-bottom: 8px;"><strong>القنوات:</strong> {channels}</div>
                <div class="card-text" style="font-size: 14px; margin-bottom: 8px;"><strong>النبرة:</strong> {seg.get('message_tone', '')}</div>
                <div style="background: rgba(212, 175, 55, 0.15); padding: 10px 15px; border-radius: 8px; font-size: 14px; color: {COLORS['gold']};">
                    🚀 {seg.get('campaign_idea', '')}
                </div>
            </div>
            """
        body_html = f"""
        <div class="pillar-detail-header">
            <div class="pillar-objective-text">🎯 {objective}</div>
        </div>
        <div class="cards-grid">
            {segments_html}
        </div>
        """
    
    # Type 4: measurement_framework
    elif 'measurement_framework' in content:
        mf = content['measurement_framework']
        layers_html = ""
        for layer in mf.get('layers', []):
            metrics = "، ".join(layer.get('metrics', []))
            layers_html += f"""
            <div class="card" style="padding: 25px;">
                <div class="card-title" style="font-size: 20px;">{layer.get('layer', '')}</div>
                <div style="font-size: 14px; color: {COLORS['gold']}; margin-bottom: 10px;">{layer.get('question', '')}</div>
                <div class="card-text" style="font-size: 14px;">{metrics}</div>
            </div>
            """
        
        tools_html = "".join([f"<li>{t}</li>" for t in mf.get('tools', [])])
        
        body_html = f"""
        <div class="pillar-detail-header">
            <div class="pillar-objective-text">🎯 {objective}</div>
        </div>
        <div class="two-columns">
            <div>
                <div class="column-title">طبقات القياس</div>
                <div class="cards-grid cards-grid-2" style="gap: 15px;">
                    {layers_html}
                </div>
            </div>
            <div>
                <div class="column-title">الأدوات والأنظمة</div>
                <ul class="list list-check">{tools_html}</ul>
            </div>
        </div>
        """
    
    # Fallback
    else:
        body_html = f"""
        <div class="pillar-detail-header">
            <div class="pillar-objective-text">🎯 {objective}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            {body_html}
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_roadmap_overview(slide, data):
    """شريحة خارطة الطريق"""
    phases_html = ""
    for i, p in enumerate(slide['content']['phases'], 1):
        milestones = "".join([f"<li>{m}</li>" for m in p['milestones']])
        phases_html += f"""
        <div class="roadmap-phase">
            <div class="phase-marker">{i}</div>
            <div class="phase-title">{p['phase']}</div>
            <div class="phase-period">{p['period']}</div>
            <div class="phase-focus">{p['focus']}</div>
            <ul class="phase-milestones">{milestones}</ul>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="roadmap-phases">
                {phases_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_year1_detail(slide, data):
    """شريحة تفاصيل السنة الأولى"""
    quarters_html = ""
    for q_key in ['q1', 'q2', 'q3', 'q4']:
        q = slide['content'][q_key]
        activities = "".join([f"<li>{a}</li>" for a in q['activities']])
        quarters_html += f"""
        <div class="quarter-card">
            <div class="quarter-title">{q['title']}</div>
            <div class="quarter-focus">{q['focus']}</div>
            <ul class="quarter-activities">{activities}</ul>
            <div class="quarter-deliverable">
                <div class="quarter-deliverable-label">المخرج الرئيسي</div>
                <div class="quarter-deliverable-text">{q['deliverable']}</div>
            </div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="quarters-grid">
                {quarters_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_success_metrics(slide, data):
    """شريحة مؤشرات النجاح"""
    kpi_sections_html = ""
    for cat in slide['content']['kpi_categories']:
        rows = ""
        for m in cat['metrics']:
            rows += f"""
            <tr>
                <td>{m['metric']}</td>
                <td class="kpi-current">{m['current']}</td>
                <td class="kpi-y1">{m['target_y1']}</td>
                <td class="kpi-y3">{m['target_y3']}</td>
            </tr>
            """
        kpi_sections_html += f"""
        <div class="kpi-section">
            <div class="kpi-section-title">{cat['category']}</div>
            <table class="kpi-table">
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
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            {kpi_sections_html}
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_why_us(slide, data):
    """شريحة لماذا نحن"""
    cards_html = ""
    for d in slide['content']['differentiators']:
        cards_html += f"""
        <div class="why-us-card">
            <div class="why-us-icon">{d['icon']}</div>
            <div class="why-us-point">{d['point']}</div>
            <div class="why-us-detail">{d['detail']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="why-us-grid">
                {cards_html}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_next_steps(slide, data):
    """شريحة الخطوات التالية"""
    steps_html = ""
    for s in slide['content']['immediate_steps']:
        steps_html += f"""
        <div class="next-step">
            <div class="step-number">{s['step']}</div>
            <div class="step-action">{s['action']}</div>
            <div class="step-desc">{s['description']}</div>
            <div class="step-timeline">⏱️ {s['timeline']}</div>
        </div>
        """
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide['subtitle']}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            <div class="next-steps">
                {steps_html}
            </div>
            <div style="text-align: center; margin-top: 40px; font-size: 22px; color: rgba(255,255,255,0.85);">
                {slide['content']['commitment']}
            </div>
        </div>
        <div class="slide-footer">
            <span>هيئة تنمية المجتمع - دبي</span>
            <span>24°45° للاستشارات الاتصالية</span>
        </div>
    </div>
    """

def render_slide_thank_you(slide, data):
    """شريحة الشكر"""
    contact = slide['content']['contact']
    
    return f"""
    <div class="slide slide-thanks">
        <div class="cover-pattern"></div>
        <div class="cover-frame"></div>
        
        <div class="thanks-content">
            <h1 class="thanks-title">{slide['title']}</h1>
            <h2 class="thanks-subtitle">{slide['subtitle']}</h2>
            
            <div class="thanks-quote">
                {slide['content']['closing_message']}
            </div>
            
            <div class="contact-row">
                <div class="contact-item">
                    <div class="contact-icon">📧</div>
                    <div class="contact-text">{contact['email']}</div>
                </div>
                <div class="contact-item">
                    <div class="contact-icon">📞</div>
                    <div class="contact-text">{contact['phone']}</div>
                </div>
                <div class="contact-item">
                    <div class="contact-icon">🌐</div>
                    <div class="contact-text">{contact['website']}</div>
                </div>
            </div>
            
            <div class="thanks-tagline">{slide['content']['tagline']}</div>
        </div>
    </div>
    """

def render_slide_generic(slide, data):
    """شريحة عامة"""
    content_html = ""
    c = slide.get('content', {})
    
    # Handle various content types
    if isinstance(c, dict):
        for key, value in c.items():
            if isinstance(value, list):
                items = "".join([f"<li>{str(item)}</li>" for item in value if isinstance(item, str)])
                if items:
                    content_html += f'<ul class="list list-check">{items}</ul>'
            elif isinstance(value, str) and len(value) > 50:
                content_html += f'<p style="font-size: 20px; margin-bottom: 20px; color: rgba(255,255,255,0.85); line-height: 1.7;">{value}</p>'
    
    return f"""
    <div class="slide">
        <div class="slide-header">
            <div class="header-content">
                <h1 class="slide-title">{slide['title']}</h1>
                <p class="slide-subtitle">{slide.get('subtitle', '')}</p>
            </div>
            <div class="slide-number">{slide['id']:02d}</div>
        </div>
        <div class="slide-body">
            {content_html if content_html else '<p style="font-size: 24px; color: rgba(255,255,255,0.8);">محتوى الشريحة</p>'}
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
        'executive_summary': render_slide_executive_summary,
        'about_firm': render_slide_about_firm,
        'methodology': render_slide_methodology,
        'org_overview': render_slide_org_overview,
        'stakeholder_map': render_slide_stakeholder_map,
        'diagnosis_overview': render_slide_diagnosis_overview,
        'challenge_overview': render_slide_challenge_overview,
        'challenge_detail': render_slide_challenge_detail,
        'framework_intro': render_slide_framework_intro,
        'pillar_detail': render_slide_pillar_detail,
        'roadmap_overview': render_slide_roadmap_overview,
        'year1_detail': render_slide_year1_detail,
        'success_metrics': render_slide_success_metrics,
        'why_us': render_slide_why_us,
        'next_steps': render_slide_next_steps,
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

async def export_pdf(html_path, output_path):
    """تصدير HTML إلى PDF باستخدام Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load HTML file
        await page.goto(f'file://{html_path}')
        
        # Wait for fonts to load
        await page.wait_for_timeout(3000)
        
        # Export PDF
        await page.pdf(
            path=output_path,
            width='1920px',
            height='1080px',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        
        await browser.close()
        print(f"✅ تم تصدير PDF إلى: {output_path}")

def main():
    print("🚀 بدء تصدير العرض التقديمي الاستراتيجي...")
    print("═" * 60)
    
    # Load presentation data
    data = load_presentation()
    print(f"📊 تم تحميل العرض: {data['presentation']['title']}")
    print(f"📑 عدد الشرائح: {len(data['slides'])}")
    print(f"🎨 الهوية البصرية: أحمر عنابي + ذهبي حكومة دبي")
    
    # Create exports directory
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    
    # Generate HTML
    html_content = generate_html(data)
    
    # Save HTML
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"📄 تم حفظ HTML إلى: {OUTPUT_HTML}")
    
    # Export PDF using Playwright
    try:
        asyncio.run(export_pdf(OUTPUT_HTML, OUTPUT_PDF))
    except Exception as e:
        print(f"⚠️ خطأ في تصدير PDF: {e}")
        print("💡 جرب: pip install playwright && playwright install chromium")
    
    print("═" * 60)
    print("✨ اكتمل التصدير بنجاح!")

if __name__ == "__main__":
    main()
