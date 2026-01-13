# -*- coding: utf-8 -*-
"""
خطة الاتصال والعلاقات العامة - ALIC
PDF Generator with Nobles Branding
"""

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def create_pr_plan_pdf():
    """Create professional PR Plan PDF with Nobles branding"""
    
    html_content = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>خطة الاتصال والعلاقات العامة - ALIC</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: #0F172A;
            color: #e2e8f0;
            direction: rtl;
            line-height: 1.8;
        }
        
        /* Cover Page */
        .cover-page {
            min-height: 100vh;
            background: linear-gradient(135deg, #0F172A 0%, #1e293b 50%, #0F172A 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px;
            page-break-after: always;
            position: relative;
            overflow: hidden;
        }
        
        .cover-page::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 20%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(245, 158, 11, 0.1) 0%, transparent 50%);
        }
        
        .cover-content {
            position: relative;
            z-index: 1;
        }
        
        .cover-logo {
            width: 180px;
            height: 180px;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 40px;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3);
        }
        
        .cover-logo-text {
            color: white;
            font-size: 48px;
            font-weight: 900;
            letter-spacing: 2px;
        }
        
        .cover-title {
            font-size: 42px;
            font-weight: 900;
            color: #10B981;
            margin-bottom: 20px;
            text-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
        }
        
        .cover-subtitle {
            font-size: 28px;
            font-weight: 700;
            color: #F59E0B;
            margin-bottom: 30px;
        }
        
        .cover-project {
            font-size: 22px;
            color: #94a3b8;
            margin-bottom: 50px;
        }
        
        .cover-divider {
            width: 200px;
            height: 4px;
            background: linear-gradient(90deg, #10B981, #F59E0B);
            margin: 30px auto;
            border-radius: 2px;
        }
        
        .cover-stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
        }
        
        .cover-stat {
            text-align: center;
            padding: 20px 30px;
            background: rgba(16, 185, 129, 0.1);
            border-radius: 16px;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        
        .cover-stat-number {
            font-size: 36px;
            font-weight: 900;
            color: #10B981;
        }
        
        .cover-stat-label {
            font-size: 14px;
            color: #94a3b8;
            margin-top: 5px;
        }
        
        .cover-date {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            color: #64748b;
            font-size: 16px;
        }
        
        /* Section Styles */
        .section {
            padding: 50px;
            page-break-inside: avoid;
        }
        
        .section-header {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border-right: 5px solid #10B981;
        }
        
        .section-number {
            display: inline-block;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #10B981, #059669);
            border-radius: 50%;
            color: white;
            font-size: 24px;
            font-weight: 900;
            line-height: 50px;
            text-align: center;
            margin-left: 15px;
        }
        
        .section-title {
            font-size: 28px;
            font-weight: 800;
            color: #10B981;
            display: inline;
        }
        
        .section-subtitle {
            color: #94a3b8;
            font-size: 16px;
            margin-top: 10px;
        }
        
        /* Cards */
        .card {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 700;
            color: #F59E0B;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-content {
            color: #cbd5e1;
            line-height: 2;
        }
        
        /* SWOT Grid */
        .swot-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .swot-card {
            padding: 25px;
            border-radius: 16px;
            border-right: 4px solid;
        }
        
        .swot-strengths {
            background: rgba(16, 185, 129, 0.1);
            border-color: #10B981;
        }
        
        .swot-weaknesses {
            background: rgba(239, 68, 68, 0.1);
            border-color: #EF4444;
        }
        
        .swot-opportunities {
            background: rgba(59, 130, 246, 0.1);
            border-color: #3B82F6;
        }
        
        .swot-threats {
            background: rgba(245, 158, 11, 0.1);
            border-color: #F59E0B;
        }
        
        .swot-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .swot-strengths .swot-title { color: #10B981; }
        .swot-weaknesses .swot-title { color: #EF4444; }
        .swot-opportunities .swot-title { color: #3B82F6; }
        .swot-threats .swot-title { color: #F59E0B; }
        
        .swot-list {
            list-style: none;
            padding: 0;
        }
        
        .swot-list li {
            padding: 8px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            color: #e2e8f0;
        }
        
        .swot-list li:last-child {
            border-bottom: none;
        }
        
        /* Objectives */
        .objective-card {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.03) 100%);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            display: flex;
            align-items: flex-start;
            gap: 20px;
        }
        
        .objective-number {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #10B981, #059669);
            border-radius: 12px;
            color: white;
            font-size: 20px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .objective-content h4 {
            color: #10B981;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .objective-content p {
            color: #94a3b8;
            line-height: 1.8;
        }
        
        /* Audience Cards */
        .audience-section {
            margin-bottom: 30px;
        }
        
        .audience-title {
            font-size: 20px;
            font-weight: 700;
            color: #F59E0B;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(245, 158, 11, 0.3);
        }
        
        .audience-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }
        
        .audience-card {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .audience-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #3B82F6, #2563EB);
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
        }
        
        .audience-name {
            font-size: 16px;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 8px;
        }
        
        .audience-desc {
            font-size: 13px;
            color: #94a3b8;
        }
        
        /* Phase Cards */
        .phase-card {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, transparent 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-right: 5px solid #10B981;
            page-break-inside: avoid;
        }
        
        .phase-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .phase-number {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #10B981, #059669);
            border-radius: 50%;
            color: white;
            font-size: 28px;
            font-weight: 900;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
        }
        
        .phase-info h3 {
            color: #10B981;
            font-size: 22px;
            font-weight: 800;
        }
        
        .phase-info .date {
            color: #F59E0B;
            font-size: 14px;
            font-weight: 600;
        }
        
        .phase-products {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            padding: 20px;
        }
        
        .product-item {
            padding: 12px 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .product-item:last-child {
            border-bottom: none;
        }
        
        .product-icon {
            width: 35px;
            height: 35px;
            background: rgba(16, 185, 129, 0.2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #10B981;
            font-size: 14px;
        }
        
        .product-name {
            color: #e2e8f0;
            font-weight: 600;
        }
        
        /* Table Styles */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .data-table th {
            background: linear-gradient(135deg, #10B981, #059669);
            color: white;
            padding: 15px;
            text-align: right;
            font-weight: 700;
        }
        
        .data-table td {
            padding: 15px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            color: #e2e8f0;
        }
        
        .data-table tr:last-child td {
            border-bottom: none;
        }
        
        /* KPI Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 30px 0;
        }
        
        .kpi-card {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: 900;
            color: #10B981;
            margin-bottom: 8px;
        }
        
        .kpi-label {
            font-size: 14px;
            color: #94a3b8;
        }
        
        /* End Page */
        .end-page {
            min-height: 100vh;
            background: linear-gradient(135deg, #0F172A 0%, #1e293b 50%, #0F172A 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px;
            page-break-before: always;
            position: relative;
        }
        
        .end-page::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
        }
        
        .end-content {
            position: relative;
            z-index: 1;
        }
        
        .end-logo {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
        }
        
        .end-logo-text {
            color: white;
            font-size: 32px;
            font-weight: 900;
        }
        
        .end-title {
            font-size: 36px;
            font-weight: 900;
            color: #10B981;
            margin-bottom: 15px;
        }
        
        .end-subtitle {
            font-size: 20px;
            color: #94a3b8;
            margin-bottom: 40px;
        }
        
        .end-contact {
            background: rgba(16, 185, 129, 0.1);
            border-radius: 16px;
            padding: 30px 50px;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        
        .end-contact-title {
            color: #F59E0B;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 20px;
        }
        
        .end-contact-item {
            color: #e2e8f0;
            margin: 10px 0;
            font-size: 16px;
        }
        
        .end-footer {
            position: absolute;
            bottom: 30px;
            color: #64748b;
            font-size: 14px;
        }
        
        /* Page Break */
        .page-break {
            page-break-after: always;
        }
        
        /* Print Styles */
        @media print {
            body {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
        }
    </style>
</head>
<body>

    <!-- صفحة الغلاف -->
    <div class="cover-page">
        <div class="cover-content">
            <div class="cover-logo">
                <span class="cover-logo-text">ALIC</span>
            </div>
            <h1 class="cover-title">خطة الاتصال والعلاقات العامة</h1>
            <h2 class="cover-subtitle">Communication & PR Strategy</h2>
            <p class="cover-project">مشروع المدينة اللوجستية الصناعية في عمان</p>
            <p class="cover-project">Amman Logistics & Industrial City</p>
            <div class="cover-divider"></div>
            <div class="cover-stats">
                <div class="cover-stat">
                    <div class="cover-stat-number">20</div>
                    <div class="cover-stat-label">منتج إعلامي</div>
                </div>
                <div class="cover-stat">
                    <div class="cover-stat-number">3</div>
                    <div class="cover-stat-label">مراحل تنفيذية</div>
                </div>
                <div class="cover-stat">
                    <div class="cover-stat-number">85%</div>
                    <div class="cover-stat-label">تغطية محلية</div>
                </div>
            </div>
        </div>
        <div class="cover-date">يناير 2026 | Nobles Properties</div>
    </div>

    <!-- القسم الأول: الملخص التنفيذي -->
    <div class="section">
        <div class="section-header">
            <span class="section-number">1</span>
            <h2 class="section-title">الملخص التنفيذي</h2>
            <p class="section-subtitle">Executive Summary</p>
        </div>
        
        <div class="card">
            <div class="card-title">🎯 الرؤية الاتصالية</div>
            <div class="card-content">
                <p>تقديم ALIC كـ <strong style="color: #10B981;">"محرك النمو الذكي"</strong> للاقتصاد الأردني، وتحويلها من مشروع ناشئ إلى علامة تجارية رائدة في قطاع اللوجستيات والصناعة بالمنطقة.</p>
            </div>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-value">85%</div>
                <div class="kpi-label">تغطية محلية</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">10%</div>
                <div class="kpi-label">تغطية إقليمية</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">5%</div>
                <div class="kpi-label">تغطية دولية</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">20</div>
                <div class="kpi-label">منتج إعلامي</div>
            </div>
        </div>
    </div>

    <!-- القسم الثاني: التحليل الاستراتيجي -->
    <div class="section page-break">
        <div class="section-header">
            <span class="section-number">2</span>
            <h2 class="section-title">التحليل الاستراتيجي SWOT</h2>
            <p class="section-subtitle">Strategic Analysis</p>
        </div>
        
        <div class="swot-grid">
            <div class="swot-card swot-strengths">
                <h3 class="swot-title">💪 نقاط القوة</h3>
                <ul class="swot-list">
                    <li>موقع استراتيجي على مفترق 3 أسواق إقليمية</li>
                    <li>3 شراكات استراتيجية مؤكدة (محامص الشعب، مخابز قبلان، مستثمر خليجي)</li>
                    <li>بنية تحتية جاهزة ومستودعات حديثة</li>
                    <li>سمعة نوبلز القوية في السوق العقاري</li>
                </ul>
            </div>
            
            <div class="swot-card swot-weaknesses">
                <h3 class="swot-title">⚠️ نقاط الضعف</h3>
                <ul class="swot-list">
                    <li>محدودية الوعي بالعلامة التجارية ALIC</li>
                    <li>مرحلة ما قبل الإطلاق الرسمي</li>
                    <li>غياب تغطية إعلامية سابقة</li>
                    <li>الحاجة لبناء هوية بصرية قوية</li>
                </ul>
            </div>
            
            <div class="swot-card swot-opportunities">
                <h3 class="swot-title">🚀 الفرص</h3>
                <ul class="swot-list">
                    <li>فجوة في السوق لمدن لوجستية متكاملة</li>
                    <li>نمو التجارة الإلكترونية 25% سنوياً</li>
                    <li>دعم حكومي لرؤية التحديث الاقتصادي</li>
                    <li>طلب متزايد على المستودعات الذكية</li>
                </ul>
            </div>
            
            <div class="swot-card swot-threats">
                <h3 class="swot-title">🔥 التهديدات</h3>
                <ul class="swot-list">
                    <li>منافسة من مناطق صناعية قائمة</li>
                    <li>تقلبات السوق الإقليمي</li>
                    <li>منافسة إقليمية من دول الخليج</li>
                    <li>تحديات اقتصادية عالمية</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- القسم الثالث: الأهداف الاستراتيجية -->
    <div class="section">
        <div class="section-header">
            <span class="section-number">3</span>
            <h2 class="section-title">الأهداف الاستراتيجية</h2>
            <p class="section-subtitle">Strategic Objectives</p>
        </div>
        
        <div class="objective-card">
            <div class="objective-number">1</div>
            <div class="objective-content">
                <h4>بناء الوعي بالعلامة التجارية</h4>
                <p>تحقيق وعي بـ ALIC لدى 80% من الجمهور المستهدف خلال 3 أشهر من الإطلاق، وتأسيس ALIC كاسم مرادف للتميز اللوجستي في الأردن.</p>
            </div>
        </div>
        
        <div class="objective-card">
            <div class="objective-number">2</div>
            <div class="objective-content">
                <h4>تعزيز المكانة التنافسية</h4>
                <p>تموضع ALIC كأكبر وأحدث مدينة لوجستية صناعية في الأردن، مع التركيز على الميزات التنافسية الفريدة والموقع الاستراتيجي.</p>
            </div>
        </div>
        
        <div class="objective-card">
            <div class="objective-number">3</div>
            <div class="objective-content">
                <h4>الربط بالرؤية الوطنية</h4>
                <p>تأكيد دور ALIC كشريك استراتيجي في تحقيق رؤية التحديث الاقتصادي 2033، ودعم أهداف التنمية الصناعية الوطنية.</p>
            </div>
        </div>
    </div>

    <!-- القسم الرابع: الجماهير المستهدفة -->
    <div class="section page-break">
        <div class="section-header">
            <span class="section-number">4</span>
            <h2 class="section-title">الجماهير المستهدفة</h2>
            <p class="section-subtitle">Target Audiences</p>
        </div>
        
        <div class="audience-section">
            <h3 class="audience-title">🎯 الجمهور الأساسي (Primary)</h3>
            <div class="audience-grid">
                <div class="audience-card">
                    <div class="audience-icon">🏭</div>
                    <div class="audience-name">الشركات الصناعية</div>
                    <div class="audience-desc">مصنعون محليون وإقليميون يبحثون عن مواقع استراتيجية</div>
                </div>
                <div class="audience-card">
                    <div class="audience-icon">💰</div>
                    <div class="audience-name">المستثمرون الإقليميون</div>
                    <div class="audience-desc">رجال أعمال خليجيون ومستثمرون يبحثون عن فرص</div>
                </div>
                <div class="audience-card">
                    <div class="audience-icon">🚚</div>
                    <div class="audience-name">شركات الخدمات اللوجستية</div>
                    <div class="audience-desc">شركات 3PL والتوزيع والتخزين</div>
                </div>
            </div>
        </div>
        
        <div class="audience-section">
            <h3 class="audience-title">🎯 الجمهور الثانوي (Secondary)</h3>
            <div class="audience-grid">
                <div class="audience-card">
                    <div class="audience-icon">🏛️</div>
                    <div class="audience-name">الجهات الحكومية</div>
                    <div class="audience-desc">وزارات ومؤسسات داعمة للاستثمار</div>
                </div>
                <div class="audience-card">
                    <div class="audience-icon">🏦</div>
                    <div class="audience-name">المؤسسات المالية</div>
                    <div class="audience-desc">بنوك وصناديق استثمارية</div>
                </div>
                <div class="audience-card">
                    <div class="audience-icon">📰</div>
                    <div class="audience-name">وسائل الإعلام</div>
                    <div class="audience-desc">صحفيون ومؤثرون اقتصاديون</div>
                </div>
            </div>
        </div>
    </div>

    <!-- القسم الخامس: مراحل التنفيذ -->
    <div class="section">
        <div class="section-header">
            <span class="section-number">5</span>
            <h2 class="section-title">مراحل التنفيذ</h2>
            <p class="section-subtitle">Implementation Phases</p>
        </div>
        
        <!-- المرحلة الأولى -->
        <div class="phase-card">
            <div class="phase-header">
                <div class="phase-number">1</div>
                <div class="phase-info">
                    <h3>مرحلة التأسيس والتشويق</h3>
                    <span class="date">1 - 14 يناير 2026</span>
                </div>
            </div>
            <div class="phase-products">
                <div class="product-item">
                    <div class="product-icon">🎨</div>
                    <span class="product-name">تطوير الهوية البصرية الكاملة لـ ALIC</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">🌐</div>
                    <span class="product-name">إطلاق الموقع الإلكتروني الرسمي</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">📱</div>
                    <span class="product-name">حملة تشويقية على وسائل التواصل</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">📊</div>
                    <span class="product-name">إعداد المواد التسويقية والعروض</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">🎬</div>
                    <span class="product-name">فيديو تشويقي "قريباً... شيء كبير"</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">✉️</div>
                    <span class="product-name">دعوات VIP لحفل الإطلاق</span>
                </div>
                <div class="product-item">
                    <div class="product-icon">📰</div>
                    <span class="product-name">تسريبات إعلامية استراتيجية</span>
                </div>
            </div>
        </div>
        
        <!-- المرحلة الثانية -->
        <div class="phase-card" style="border-color: #F59E0B;">
            <div class="phase-header">
                <div class="phase-number" style="background: linear-gradient(135deg, #F59E0B, #D97706);">2</div>
                <div class="phase-info">
                    <h3 style="color: #F59E0B;">مرحلة الإطلاق الكبير</h3>
                    <span class="date">15 - 22 يناير 2026</span>
                </div>
            </div>
            <div class="phase-products">
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">🎉</div>
                    <span class="product-name">حفل الإطلاق الرسمي VIP - 150 ضيف</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">🎬</div>
                    <span class="product-name">فيلم سينمائي 4K عن ALIC</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">📺</div>
                    <span class="product-name">تغطية تلفزيونية - 5 قنوات رئيسية</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">💼</div>
                    <span class="product-name">حملة LinkedIn - 10 منشورات استراتيجية</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">📢</div>
                    <span class="product-name">حملة إعلانية رقمية - $3,000</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">🎙️</div>
                    <span class="product-name">بودكاست "بذرة" مع عمر عايش</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">✍️</div>
                    <span class="product-name">5 مقالات رأي في الصحف الكبرى</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">🚌</div>
                    <span class="product-name">جولة إعلامية VIP - 25 صحفي ومؤثر</span>
                </div>
            </div>
        </div>
        
        <!-- المرحلة الثالثة -->
        <div class="phase-card" style="border-color: #8B5CF6;">
            <div class="phase-header">
                <div class="phase-number" style="background: linear-gradient(135deg, #8B5CF6, #7C3AED);">3</div>
                <div class="phase-info">
                    <h3 style="color: #8B5CF6;">مرحلة ترسيخ الريادة</h3>
                    <span class="date">23 - 31 يناير 2026</span>
                </div>
            </div>
            <div class="phase-products">
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(139, 92, 246, 0.2); color: #8B5CF6;">📻</div>
                    <span class="product-name">ظهور إذاعي - إذاعة حسنى FM</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(139, 92, 246, 0.2); color: #8B5CF6;">🎙️</div>
                    <span class="product-name">جولة إذاعية - 5 إذاعات أردنية</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(139, 92, 246, 0.2); color: #8B5CF6;">📹</div>
                    <span class="product-name">حلقة المخبر الاقتصادي على YouTube</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(139, 92, 246, 0.2); color: #8B5CF6;">📺</div>
                    <span class="product-name">تقرير برنامج "مال وأعمال"</span>
                </div>
                <div class="product-item">
                    <div class="product-icon" style="background: rgba(139, 92, 246, 0.2); color: #8B5CF6;">💬</div>
                    <span class="product-name">حملة شهادات الشركاء والخبراء</span>
                </div>
            </div>
        </div>
    </div>

    <!-- القسم السادس: المنتجات الإعلامية -->
    <div class="section page-break">
        <div class="section-header">
            <span class="section-number">6</span>
            <h2 class="section-title">المنتجات الإعلامية الرئيسية</h2>
            <p class="section-subtitle">Key Media Products</p>
        </div>
        
        <table class="data-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>المنتج الإعلامي</th>
                    <th>النوع</th>
                    <th>التوقيت</th>
                    <th>الهدف</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>حفل الإطلاق الرسمي</td>
                    <td>حدث VIP</td>
                    <td>15 يناير</td>
                    <td>150 ضيف</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>فيلم سينمائي 4K</td>
                    <td>فيديو</td>
                    <td>15 يناير</td>
                    <td>500K مشاهدة</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>تغطية تلفزيونية</td>
                    <td>TV</td>
                    <td>15-17 يناير</td>
                    <td>2M+ مشاهد</td>
                </tr>
                <tr>
                    <td>4</td>
                    <td>حملة LinkedIn</td>
                    <td>سوشيال</td>
                    <td>13-22 يناير</td>
                    <td>100K impression</td>
                </tr>
                <tr>
                    <td>5</td>
                    <td>إعلانات رقمية</td>
                    <td>Paid Ads</td>
                    <td>13-22 يناير</td>
                    <td>50+ lead</td>
                </tr>
                <tr>
                    <td>6</td>
                    <td>بودكاست "بذرة"</td>
                    <td>صوتي</td>
                    <td>18-20 يناير</td>
                    <td>50K استماع</td>
                </tr>
                <tr>
                    <td>7</td>
                    <td>مقالات رأي</td>
                    <td>صحافة</td>
                    <td>16-20 يناير</td>
                    <td>200K قارئ</td>
                </tr>
                <tr>
                    <td>8</td>
                    <td>جولة إعلامية</td>
                    <td>حدث</td>
                    <td>20 يناير</td>
                    <td>50+ منشور</td>
                </tr>
                <tr>
                    <td>9</td>
                    <td>جولة إذاعية</td>
                    <td>راديو</td>
                    <td>22-27 يناير</td>
                    <td>200K مستمع</td>
                </tr>
                <tr>
                    <td>10</td>
                    <td>المخبر الاقتصادي</td>
                    <td>YouTube</td>
                    <td>28 يناير</td>
                    <td>500K مشاهدة</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- القسم السابع: مؤشرات الأداء -->
    <div class="section">
        <div class="section-header">
            <span class="section-number">7</span>
            <h2 class="section-title">مؤشرات الأداء الرئيسية</h2>
            <p class="section-subtitle">Key Performance Indicators</p>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-value">5M+</div>
                <div class="kpi-label">إجمالي الوصول</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">50+</div>
                <div class="kpi-label">تغطية إعلامية</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">100+</div>
                <div class="kpi-label">استفسار استثماري</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">80%</div>
                <div class="kpi-label">وعي الجمهور المستهدف</div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-title">📊 مقاييس النجاح التفصيلية</div>
            <div class="card-content">
                <p><strong style="color: #10B981;">• التغطية الإعلامية:</strong> 50+ قصة إخبارية في الشهر الأول</p>
                <p><strong style="color: #10B981;">• التفاعل الرقمي:</strong> 500K+ تفاعل على وسائل التواصل</p>
                <p><strong style="color: #10B981;">• توليد العملاء:</strong> 100+ استفسار استثماري جاد</p>
                <p><strong style="color: #10B981;">• الوعي بالعلامة:</strong> 80% من الجمهور المستهدف</p>
                <p><strong style="color: #10B981;">• المشاهدات:</strong> 2M+ مشاهدة للمحتوى المرئي</p>
            </div>
        </div>
    </div>

    <!-- القسم الثامن: الميزانية -->
    <div class="section page-break">
        <div class="section-header">
            <span class="section-number">8</span>
            <h2 class="section-title">الميزانية التقديرية</h2>
            <p class="section-subtitle">Budget Allocation</p>
        </div>
        
        <table class="data-table">
            <thead>
                <tr>
                    <th>البند</th>
                    <th>التفاصيل</th>
                    <th>التكلفة</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>حفل الإطلاق</td>
                    <td>مكان + ضيافة + تنظيم</td>
                    <td>$15,000</td>
                </tr>
                <tr>
                    <td>الإنتاج المرئي</td>
                    <td>فيلم سينمائي 4K + فيديوهات</td>
                    <td>$8,000</td>
                </tr>
                <tr>
                    <td>الإعلانات الرقمية</td>
                    <td>Google + Meta + LinkedIn</td>
                    <td>$3,000</td>
                </tr>
                <tr>
                    <td>الجولة الإعلامية</td>
                    <td>نقل + ضيافة + هدايا</td>
                    <td>$2,000</td>
                </tr>
                <tr>
                    <td>العلاقات العامة</td>
                    <td>تنسيق إعلامي + بيانات صحفية</td>
                    <td>$2,000</td>
                </tr>
                <tr style="background: rgba(16, 185, 129, 0.1);">
                    <td><strong>الإجمالي</strong></td>
                    <td></td>
                    <td><strong style="color: #10B981;">$30,000</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- صفحة النهاية -->
    <div class="end-page">
        <div class="end-content">
            <div class="end-logo">
                <span class="end-logo-text">N</span>
            </div>
            <h1 class="end-title">شكراً لكم</h1>
            <p class="end-subtitle">Thank You</p>
            
            <div class="end-contact">
                <p class="end-contact-title">للتواصل والاستفسار</p>
                <p class="end-contact-item">🌐 www.noblesproperties.com</p>
                <p class="end-contact-item">📧 info@noblesproperties.com</p>
                <p class="end-contact-item">📱 +962 6 XXX XXXX</p>
            </div>
        </div>
        <div class="end-footer">© 2026 Nobles Properties - All Rights Reserved</div>
    </div>

</body>
</html>
'''
    
    # Create PDF
    font_config = FontConfiguration()
    
    html = HTML(string=html_content)
    
    output_path = '/Users/taherirshaid/Desktop/Project/24-45-Platform/ALIC_PR_Plan_Professional.pdf'
    
    html.write_pdf(
        output_path,
        font_config=font_config
    )
    
    print(f"✅ تم إنشاء ملف PDF بنجاح!")
    print(f"📄 المسار: {output_path}")
    return output_path

if __name__ == "__main__":
    create_pr_plan_pdf()
