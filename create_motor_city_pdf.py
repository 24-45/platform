#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحويل موتور سيتي إلى كتاب PDF احترافي
Motor City Professional PDF Book Generator
Using WeasyPrint for proper Arabic support
"""

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

# ═══════════════════════════════════════════════════════════════
# المحتوى الكامل للكتاب
# ═══════════════════════════════════════════════════════════════

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>موتور سيتي - الخطة الاستراتيجية</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tajawal', Arial, sans-serif;
            direction: rtl;
            line-height: 1.8;
            color: #1e293b;
        }
        
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
                color: #64748b;
            }
        }
        
        @page cover {
            margin: 0;
            @bottom-center { content: none; }
        }
        
        @page title-page {
            margin: 0;
            @bottom-center { content: none; }
        }
        
        /* ═══════════════════════════════════════ */
        /* الغلاف الأمامي */
        /* ═══════════════════════════════════════ */
        .front-cover {
            page: cover;
            page-break-after: always;
            width: 100%;
            height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 3cm;
            position: relative;
        }
        
        .cover-top-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 8mm;
            background: #dc1f27;
        }
        
        .cover-top-accent {
            position: absolute;
            top: 8mm;
            left: 0;
            right: 0;
            height: 2mm;
            background: #fbbf24;
        }
        
        .cover-bottom-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 8mm;
            background: #dc1f27;
        }
        
        .cover-logo {
            color: #fff;
            font-size: 14pt;
            font-weight: 700;
            letter-spacing: 3px;
            margin-bottom: 5mm;
        }
        
        .cover-logo-ar {
            color: #fbbf24;
            font-size: 12pt;
            margin-bottom: 30mm;
        }
        
        .cover-title-en {
            color: #fff;
            font-size: 42pt;
            font-weight: 800;
            margin-bottom: 5mm;
        }
        
        .cover-title-ar {
            color: #fbbf24;
            font-size: 36pt;
            font-weight: 800;
            margin-bottom: 15mm;
        }
        
        .cover-line {
            width: 80mm;
            height: 2px;
            background: #fbbf24;
            margin: 0 auto 15mm;
        }
        
        .cover-subtitle {
            color: #94a3b8;
            font-size: 14pt;
            margin-bottom: 5mm;
        }
        
        .cover-subtitle-en {
            color: #94a3b8;
            font-size: 12pt;
            margin-bottom: 20mm;
        }
        
        .cover-info {
            color: #fbbf24;
            font-size: 11pt;
            margin-bottom: 3mm;
        }
        
        .cover-date {
            position: absolute;
            bottom: 20mm;
            color: #64748b;
            font-size: 10pt;
        }
        
        /* ═══════════════════════════════════════ */
        /* صفحة العنوان */
        /* ═══════════════════════════════════════ */
        .title-page {
            page: title-page;
            page-break-after: always;
            padding: 2cm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            min-height: 100vh;
        }
        
        .title-page-border {
            border: 2px solid #dc1f27;
            padding: 3cm;
            width: 100%;
        }
        
        .title-page-inner {
            border: 1px solid #fbbf24;
            padding: 2cm;
        }
        
        .title-main-en {
            color: #1e293b;
            font-size: 28pt;
            font-weight: 800;
            margin-bottom: 8mm;
        }
        
        .title-main-ar {
            color: #dc1f27;
            font-size: 24pt;
            font-weight: 800;
            margin-bottom: 15mm;
        }
        
        .title-line {
            width: 60mm;
            height: 2px;
            background: #dc1f27;
            margin: 0 auto 15mm;
        }
        
        .title-sub {
            color: #475569;
            font-size: 14pt;
            margin-bottom: 5mm;
        }
        
        .title-info {
            color: #475569;
            font-size: 11pt;
            margin-bottom: 3mm;
        }
        
        .title-copyright {
            color: #94a3b8;
            font-size: 9pt;
            margin-top: 20mm;
        }
        
        /* ═══════════════════════════════════════ */
        /* فهرس المحتويات */
        /* ═══════════════════════════════════════ */
        .toc-page {
            page-break-after: always;
        }
        
        .toc-title {
            color: #1e293b;
            font-size: 24pt;
            font-weight: 800;
            text-align: center;
            margin-bottom: 5mm;
        }
        
        .toc-subtitle {
            color: #dc1f27;
            font-size: 14pt;
            text-align: center;
            margin-bottom: 15mm;
        }
        
        .toc-line {
            width: 60mm;
            height: 2px;
            background: #dc1f27;
            margin: 0 auto 20mm;
        }
        
        .toc-item {
            display: flex;
            align-items: center;
            margin-bottom: 15mm;
            padding-bottom: 5mm;
            border-bottom: 1px dashed #e2e8f0;
        }
        
        .toc-number {
            width: 30px;
            height: 30px;
            background: #dc1f27;
            color: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 12pt;
            margin-left: 15px;
        }
        
        .toc-text {
            flex: 1;
        }
        
        .toc-text-ar {
            color: #1e293b;
            font-size: 13pt;
            font-weight: 700;
        }
        
        .toc-text-en {
            color: #64748b;
            font-size: 10pt;
        }
        
        .toc-page-num {
            color: #dc1f27;
            font-size: 12pt;
            font-weight: 700;
        }
        
        /* ═══════════════════════════════════════ */
        /* فواصل الأقسام */
        /* ═══════════════════════════════════════ */
        .section-divider {
            page-break-before: always;
            page-break-after: always;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 3cm;
            margin: -2cm;
        }
        
        .section-circle {
            width: 150px;
            height: 150px;
            border: 3px solid;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 20mm;
        }
        
        .section-circle.green { border-color: #10b981; }
        .section-circle.cyan { border-color: #06b6d4; }
        .section-circle.purple { border-color: #8b5cf6; }
        .section-circle.red { border-color: #dc1f27; }
        
        .section-num {
            font-size: 48pt;
            font-weight: 800;
            color: #fff;
        }
        
        .section-num.green { color: #10b981; }
        .section-num.cyan { color: #06b6d4; }
        .section-num.purple { color: #8b5cf6; }
        .section-num.red { color: #dc1f27; }
        
        .section-title-ar {
            color: #fff;
            font-size: 28pt;
            font-weight: 800;
            margin-bottom: 5mm;
        }
        
        .section-title-en {
            color: #fbbf24;
            font-size: 16pt;
        }
        
        /* ═══════════════════════════════════════ */
        /* صفحات المحتوى */
        /* ═══════════════════════════════════════ */
        .content-page {
            page-break-after: always;
        }
        
        .content-header {
            background: #0f172a;
            color: #fff;
            padding: 10px 20px;
            margin: -2cm -2cm 20mm -2cm;
            text-align: center;
            font-size: 12pt;
        }
        
        .content-title {
            color: #1e293b;
            font-size: 18pt;
            font-weight: 800;
            margin-bottom: 5mm;
            padding-bottom: 3mm;
            border-bottom: 3px solid #dc1f27;
        }
        
        .content-subtitle {
            color: #64748b;
            font-size: 11pt;
            margin-bottom: 15mm;
        }
        
        .content-text {
            color: #475569;
            font-size: 11pt;
            line-height: 2;
            margin-bottom: 10mm;
            text-align: justify;
        }
        
        .content-list {
            margin-bottom: 10mm;
            padding-right: 20px;
        }
        
        .content-list li {
            color: #475569;
            font-size: 11pt;
            line-height: 2;
            margin-bottom: 3mm;
        }
        
        /* بطاقات المعلومات */
        .info-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-right: 4px solid #dc1f27;
            padding: 15px 20px;
            margin-bottom: 10mm;
            border-radius: 8px;
        }
        
        .info-card-title {
            color: #dc1f27;
            font-size: 12pt;
            font-weight: 700;
            margin-bottom: 5mm;
        }
        
        .info-card-value {
            color: #1e293b;
            font-size: 11pt;
        }
        
        /* جدول البيانات */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15mm;
        }
        
        .data-table th {
            background: #0f172a;
            color: #fff;
            padding: 12px 15px;
            text-align: right;
            font-size: 10pt;
            font-weight: 700;
        }
        
        .data-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
            font-size: 10pt;
            color: #475569;
        }
        
        .data-table tr:nth-child(even) {
            background: #f8fafc;
        }
        
        /* إحصائيات */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 15mm;
        }
        
        .stat-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
        }
        
        .stat-value {
            color: #dc1f27;
            font-size: 24pt;
            font-weight: 800;
            display: block;
        }
        
        .stat-label {
            color: #64748b;
            font-size: 10pt;
        }
        
        /* ═══════════════════════════════════════ */
        /* الغلاف الخلفي */
        /* ═══════════════════════════════════════ */
        .back-cover {
            page: cover;
            page-break-before: always;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 3cm;
            margin: -2cm;
            position: relative;
        }
        
        .back-cover .cover-top-bar,
        .back-cover .cover-bottom-bar {
            position: absolute;
            left: 0;
            right: 0;
            height: 8mm;
            background: #dc1f27;
        }
        
        .back-cover .cover-top-bar { top: 0; }
        .back-cover .cover-bottom-bar { bottom: 0; }
        
        .back-logo-en {
            color: #fff;
            font-size: 28pt;
            font-weight: 800;
            margin-bottom: 3mm;
        }
        
        .back-logo-sub {
            color: #fff;
            font-size: 18pt;
            margin-bottom: 10mm;
        }
        
        .back-logo-ar {
            color: #fbbf24;
            font-size: 16pt;
            margin-bottom: 15mm;
        }
        
        .back-line {
            width: 60mm;
            height: 2px;
            background: #fbbf24;
            margin: 0 auto 15mm;
        }
        
        .back-contact {
            color: #94a3b8;
            font-size: 11pt;
            margin-bottom: 5mm;
        }
        
        .back-copyright {
            color: #64748b;
            font-size: 9pt;
            margin-top: 20mm;
        }
        
        /* طباعة */
        @media print {
            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        }
    </style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- الغلاف الأمامي -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="front-cover">
    <div class="cover-top-bar"></div>
    <div class="cover-top-accent"></div>
    
    <div class="cover-logo">NOBLES REAL ESTATE</div>
    <div class="cover-logo-ar">نوبلز العقارية</div>
    
    <div class="cover-title-en">MOTOR CITY</div>
    <div class="cover-title-ar">موتور سيتي</div>
    
    <div class="cover-line"></div>
    
    <div class="cover-subtitle">الخطة الاستراتيجية للاتصال والعلاقات العامة</div>
    <div class="cover-subtitle-en">Strategic Communication & PR Plan</div>
    
    <div class="cover-info">الموقع: منطقة أحد، شرق عمان، الأردن</div>
    <div class="cover-info">المساحة: 210,000 متر مربع</div>
    <div class="cover-info">الوحدات: 757 معرض سيارات</div>
    
    <div class="cover-date">يناير 2026</div>
    <div class="cover-bottom-bar"></div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- صفحة العنوان -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="title-page">
    <div class="title-page-border">
        <div class="title-page-inner">
            <div class="title-main-en">MOTOR CITY</div>
            <div class="title-main-ar">موتور سيتي</div>
            
            <div class="title-line"></div>
            
            <div class="title-sub">الخطة الاستراتيجية المتكاملة</div>
            <div class="title-sub">للاتصال والعلاقات العامة</div>
            
            <br><br>
            
            <div class="title-info">إعداد: منصة 24°45°</div>
            <div class="title-info">لصالح: نوبلز العقارية</div>
            <div class="title-info">الإصدار: 1.0</div>
            <div class="title-info">التاريخ: يناير 2026</div>
            
            <div class="title-copyright">جميع الحقوق محفوظة © نوبلز العقارية 2026</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- فهرس المحتويات -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="toc-page">
    <div class="toc-title">فهرس المحتويات</div>
    <div class="toc-subtitle">Table of Contents</div>
    <div class="toc-line"></div>
    
    <div class="toc-item">
        <div class="toc-number">1</div>
        <div class="toc-text">
            <div class="toc-text-ar">التمهيد والمقدمة</div>
            <div class="toc-text-en">Introduction</div>
        </div>
        <div class="toc-page-num">5</div>
    </div>
    
    <div class="toc-item">
        <div class="toc-number">2</div>
        <div class="toc-text">
            <div class="toc-text-ar">نظرة عامة على المشروع</div>
            <div class="toc-text-en">Project Overview</div>
        </div>
        <div class="toc-page-num">7</div>
    </div>
    
    <div class="toc-item">
        <div class="toc-number">3</div>
        <div class="toc-text">
            <div class="toc-text-ar">الوضع الراهن - دراسة السوق</div>
            <div class="toc-text-en">Current Status</div>
        </div>
        <div class="toc-page-num">15</div>
    </div>
    
    <div class="toc-item">
        <div class="toc-number">4</div>
        <div class="toc-text">
            <div class="toc-text-ar">المقارنات المعيارية العالمية</div>
            <div class="toc-text-en">Global Benchmarks</div>
        </div>
        <div class="toc-page-num">25</div>
    </div>
    
    <div class="toc-item">
        <div class="toc-number">5</div>
        <div class="toc-text">
            <div class="toc-text-ar">الخطة الاستراتيجية</div>
            <div class="toc-text-en">Strategic Plan</div>
        </div>
        <div class="toc-page-num">45</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- التمهيد والمقدمة -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="content-page">
    <div class="content-header">التمهيد والمقدمة</div>
    
    <div class="content-title">مقدمة</div>
    <div class="content-subtitle">Introduction</div>
    
    <p class="content-text">
        يمثل مشروع موتور سيتي نقلة نوعية في قطاع معارض السيارات في الأردن، حيث يهدف إلى إنشاء أول مدينة متكاملة ومتخصصة لمعارض السيارات في المملكة الأردنية الهاشمية.
    </p>
    
    <p class="content-text">
        يقع المشروع في منطقة أحد شرق عمان على مساحة إجمالية تبلغ 210,000 متر مربع، ويضم 757 معرضاً للسيارات مع كافة الخدمات المساندة من مراكز صيانة ومحلات قطع غيار ومرافق خدمية متكاملة.
    </p>
    
    <div class="content-title" style="margin-top: 20mm;">أهداف الخطة الاستراتيجية</div>
    
    <ul class="content-list">
        <li>بناء الوعي بالمشروع وترسيخ مكانته كوجهة رئيسية لقطاع السيارات</li>
        <li>جذب المستأجرين والمستثمرين المحتملين من أصحاب معارض السيارات</li>
        <li>تعزيز السمعة المؤسسية لشركة نوبلز العقارية</li>
        <li>إدارة التوقعات والتواصل الفعال مع جميع أصحاب المصلحة</li>
        <li>بناء علاقات إيجابية مع الجهات الحكومية والإعلامية</li>
    </ul>
    
    <div class="info-card">
        <div class="info-card-title">منهجية الدراسة</div>
        <div class="info-card-value">
            تستند هذه الخطة إلى دراسة معيارية شاملة لأفضل الممارسات العالمية في مدن السيارات، بالإضافة إلى دراسة ميدانية للسوق المحلي شملت أكثر من 350 معرضاً في عمان.
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- فاصل القسم الأول: نظرة عامة -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="section-divider">
    <div class="section-circle green">
        <div class="section-num green">1</div>
    </div>
    <div class="section-title-ar">نظرة عامة</div>
    <div class="section-title-en">Overview</div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- محتوى نظرة عامة -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="content-page">
    <div class="content-header">القسم الأول: نظرة عامة</div>
    
    <div class="content-title">معلومات المشروع الأساسية</div>
    <div class="content-subtitle">Basic Project Information</div>
    
    <table class="data-table">
        <tr>
            <th style="width: 35%;">البيان</th>
            <th>التفاصيل</th>
        </tr>
        <tr>
            <td><strong>اسم المشروع</strong></td>
            <td>موتور سيتي - Motor City</td>
        </tr>
        <tr>
            <td><strong>الموقع</strong></td>
            <td>منطقة أحد، شرق عمان، الأردن</td>
        </tr>
        <tr>
            <td><strong>المساحة الإجمالية</strong></td>
            <td>210,000 متر مربع</td>
        </tr>
        <tr>
            <td><strong>عدد الوحدات</strong></td>
            <td>757 معرض سيارات</td>
        </tr>
        <tr>
            <td><strong>نوع المشروع</strong></td>
            <td>مدينة سيارات متكاملة</td>
        </tr>
        <tr>
            <td><strong>المطور</strong></td>
            <td>نوبلز العقارية</td>
        </tr>
        <tr>
            <td><strong>تاريخ التسليم المتوقع</strong></td>
            <td>2027</td>
        </tr>
    </table>
    
    <div class="content-title" style="margin-top: 15mm;">الرؤية والرسالة</div>
    
    <div class="info-card">
        <div class="info-card-title">الرؤية</div>
        <div class="info-card-value">
            أن يصبح موتور سيتي الوجهة الأولى والمرجعية لقطاع السيارات في الأردن والمنطقة، مقدماً تجربة متكاملة تجمع بين البيع والخدمة والترفيه.
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-card-title">الرسالة</div>
        <div class="info-card-value">
            نسعى لتحويل تجربة شراء وصيانة السيارات في الأردن من خلال توفير بيئة احترافية متكاملة تجمع جميع الخدمات تحت سقف واحد، مع الالتزام بأعلى معايير الجودة والخدمة.
        </div>
    </div>
</div>

<div class="content-page">
    <div class="content-header">القسم الأول: نظرة عامة</div>
    
    <div class="content-title">المزايا التنافسية</div>
    <div class="content-subtitle">Competitive Advantages</div>
    
    <div class="stats-grid">
        <div class="stat-box">
            <span class="stat-value">757</span>
            <span class="stat-label">معرض سيارات</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">210K</span>
            <span class="stat-label">متر مربع</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">24/7</span>
            <span class="stat-label">أمن وحراسة</span>
        </div>
    </div>
    
    <ul class="content-list">
        <li><strong>الموقع الاستراتيجي:</strong> على الطريق الدولي شرق عمان مع سهولة الوصول من جميع الاتجاهات</li>
        <li><strong>البنية التحتية المتكاملة:</strong> كهرباء، مياه، اتصالات، طرق داخلية معبدة</li>
        <li><strong>الخدمات المساندة:</strong> مراكز صيانة، محلات قطع غيار، بنوك، مطاعم</li>
        <li><strong>التصميم العصري:</strong> تصاميم معمارية حديثة مستوحاة من أفضل مدن السيارات العالمية</li>
        <li><strong>أول مدينة سيارات:</strong> المشروع الأول من نوعه في الأردن</li>
        <li><strong>إدارة احترافية:</strong> فريق إدارة متخصص من نوبلز العقارية</li>
    </ul>
    
    <div class="content-title" style="margin-top: 15mm;">القطاعات المستهدفة</div>
    
    <ul class="content-list">
        <li>معارض السيارات الجديدة والمستعملة</li>
        <li>وكلاء العلامات التجارية العالمية</li>
        <li>مراكز الصيانة المعتمدة</li>
        <li>محلات قطع الغيار والإكسسوارات</li>
        <li>شركات تأجير السيارات</li>
        <li>شركات التمويل والتأمين</li>
    </ul>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- فاصل القسم الثاني: الوضع الراهن -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="section-divider">
    <div class="section-circle cyan">
        <div class="section-num cyan">2</div>
    </div>
    <div class="section-title-ar">الوضع الراهن</div>
    <div class="section-title-en">Current Status</div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- محتوى الوضع الراهن -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="content-page">
    <div class="content-header">القسم الثاني: الوضع الراهن</div>
    
    <div class="content-title">تحليل سوق معارض السيارات في عمان</div>
    <div class="content-subtitle">Car Showrooms Market Analysis in Amman</div>
    
    <p class="content-text">
        تم إجراء دراسة ميدانية شاملة لسوق معارض السيارات في عمان خلال الفترة من 12 إلى 18 مارس 2025، بواسطة 8 باحثين ميدانيين تحت إشراف مشرفين اثنين ومشرف رئيسي.
    </p>
    
    <div class="stats-grid">
        <div class="stat-box">
            <span class="stat-value">352</span>
            <span class="stat-label">معرض مستطلع</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">97%</span>
            <span class="stat-label">معدل الاستجابة</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">7</span>
            <span class="stat-label">أيام بحث</span>
        </div>
    </div>
    
    <div class="content-title" style="margin-top: 15mm;">أبرز التحديات في السوق</div>
    
    <table class="data-table">
        <tr>
            <th>التحدي</th>
            <th style="width: 20%; text-align: center;">النسبة</th>
        </tr>
        <tr>
            <td>البائعون غير المنظمين (الدلالين)</td>
            <td style="text-align: center;"><strong>31.9%</strong></td>
        </tr>
        <tr>
            <td>التحديات الاقتصادية (أسعار الوقود، ضعف القدرة الشرائية)</td>
            <td style="text-align: center;">24.1%</td>
        </tr>
        <tr>
            <td>ارتفاع الرسوم الجمركية والضرائب</td>
            <td style="text-align: center;">11.2%</td>
        </tr>
        <tr>
            <td>المنافسة الشديدة</td>
            <td style="text-align: center;">10.5%</td>
        </tr>
        <tr>
            <td>صعوبة التمويل</td>
            <td style="text-align: center;">8.3%</td>
        </tr>
    </table>
</div>

<div class="content-page">
    <div class="content-header">القسم الثاني: الوضع الراهن</div>
    
    <div class="content-title">مؤشرات التشغيل الرئيسية</div>
    <div class="content-subtitle">Key Operating Indicators</div>
    
    <table class="data-table">
        <tr>
            <th>المؤشر</th>
            <th>الوصف</th>
            <th style="width: 15%; text-align: center;">النسبة</th>
        </tr>
        <tr>
            <td>المساحة الداخلية</td>
            <td>أقل من 50 متر مربع</td>
            <td style="text-align: center;">53.7%</td>
        </tr>
        <tr>
            <td>المساحة الخارجية</td>
            <td>10-100 متر مربع</td>
            <td style="text-align: center;">48.9%</td>
        </tr>
        <tr>
            <td>السيارات المعروضة</td>
            <td>10 سيارات أو أقل</td>
            <td style="text-align: center;">56.8%</td>
        </tr>
        <tr>
            <td>المبيعات الشهرية</td>
            <td>أقل من 5 سيارات</td>
            <td style="text-align: center;">80.1%</td>
        </tr>
        <tr>
            <td>الإيجار الشهري</td>
            <td>500 دينار أو أقل</td>
            <td style="text-align: center;">51.4%</td>
        </tr>
    </table>
    
    <div class="content-title" style="margin-top: 15mm;">التطلعات نحو مدينة المعارض الموحدة</div>
    
    <div class="stats-grid">
        <div class="stat-box">
            <span class="stat-value">87.5%</span>
            <span class="stat-label">راضون عن الموقع الحالي</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">32.4%</span>
            <span class="stat-label">يفضلون الانتقال للمدينة</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">45.5%</span>
            <span class="stat-label">يرون فرص تسويقية أفضل</span>
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-card-title">أسباب التردد في الانتقال</div>
        <div class="info-card-value">
            • 58.7% يرون أن الموقع المقترح بعيد عن العملاء<br>
            • 22.3% قلقون من زيادة المنافسة<br>
            • 11.7% يعتبرون موقعهم الحالي ميزة تنافسية
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- فاصل القسم الثالث: المقارنات المعيارية -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="section-divider">
    <div class="section-circle purple">
        <div class="section-num purple">3</div>
    </div>
    <div class="section-title-ar">المقارنات المعيارية</div>
    <div class="section-title-en">Benchmarks</div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- محتوى المقارنات المعيارية -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="content-page">
    <div class="content-header">القسم الثالث: المقارنات المعيارية</div>
    
    <div class="content-title">التجارب العالمية في مدن السيارات</div>
    <div class="content-subtitle">Global Experiences in Car Cities</div>
    
    <p class="content-text">
        تغطي هذه الدراسة ست تجارب متميزة في تطوير مدن ومناطق السيارات المتكاملة، تشمل نماذج دولية (ألمانيا وتركيا) وإقليمية (الإمارات والسعودية) ومحلية (الأردن)، لاستخلاص أفضل الممارسات والدروس المستفادة لمشروع موتور سيتي.
    </p>
    
    <div class="stats-grid">
        <div class="stat-box">
            <span class="stat-value">6</span>
            <span class="stat-label">تجارب مدروسة</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">5</span>
            <span class="stat-label">دول ومناطق</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">3</span>
            <span class="stat-label">مستويات تحليلية</span>
        </div>
    </div>
    
    <div class="content-title" style="margin-top: 15mm;">الكيانات المدروسة</div>
    
    <table class="data-table">
        <tr>
            <th>الكيان</th>
            <th>الدولة</th>
            <th>النموذج</th>
        </tr>
        <tr>
            <td><strong>Autostadt</strong></td>
            <td>ألمانيا 🇩🇪</td>
            <td>مدينة سيارات ترفيهية - فولكس واجن</td>
        </tr>
        <tr>
            <td><strong>Autopia Istanbul</strong></td>
            <td>تركيا 🇹🇷</td>
            <td>مركز تسوق سيارات متكامل</td>
        </tr>
        <tr>
            <td><strong>Motor World Abu Dhabi</strong></td>
            <td>الإمارات 🇦🇪</td>
            <td>أكبر صالة عرض في العالم</td>
        </tr>
        <tr>
            <td><strong>Dubai Auto Zone</strong></td>
            <td>الإمارات 🇦🇪</td>
            <td>منطقة حرة متخصصة</td>
        </tr>
        <tr>
            <td><strong>معارض القادسية</strong></td>
            <td>السعودية 🇸🇦</td>
            <td>تجمع تقليدي للمعارض</td>
        </tr>
        <tr>
            <td><strong>المنطقة الحرة</strong></td>
            <td>الأردن 🇯🇴</td>
            <td>منطقة حرة متعددة الأغراض</td>
        </tr>
    </table>
</div>

<div class="content-page">
    <div class="content-header">القسم الثالث: المقارنات المعيارية</div>
    
    <div class="content-title">الدروس المستفادة الرئيسية</div>
    <div class="content-subtitle">Key Lessons Learned</div>
    
    <div class="info-card">
        <div class="info-card-title">1. استراتيجيات الاتصال</div>
        <div class="info-card-value">
            أهمية التواصل الاستباقي والشفاف مع أصحاب المصلحة قبل وأثناء وبعد الإعلان عن المشاريع الكبرى. التجارب الناجحة اعتمدت على بناء جسور الثقة مبكراً.
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-card-title">2. إدارة التوقعات</div>
        <div class="info-card-value">
            ضرورة وضع توقعات واقعية وتقديم وعود قابلة للتحقيق. المشاريع التي فشلت في إدارة التوقعات واجهت مقاومة شديدة من المتضررين.
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-card-title">3. التعامل مع المتضررين</div>
        <div class="info-card-value">
            تقديم حلول بديلة وحوافز للمتضررين من القرارات. التجارب الناجحة حولت المعارضين إلى شركاء من خلال برامج الدعم والتمكين.
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-card-title">4. نماذج النجاح</div>
        <div class="info-card-value">
            المشاريع الأكثر نجاحاً جمعت بين الرؤية الطموحة والتنفيذ المرن. Autostadt وMotor World نماذج للتكامل بين الخدمات والتجربة المتميزة.
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- فاصل القسم الرابع: الخطة الاستراتيجية -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="section-divider">
    <div class="section-circle red">
        <div class="section-num red">4</div>
    </div>
    <div class="section-title-ar">الخطة الاستراتيجية</div>
    <div class="section-title-en">Strategic Plan</div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- محتوى الخطة الاستراتيجية -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="content-page">
    <div class="content-header">القسم الرابع: الخطة الاستراتيجية</div>
    
    <div class="content-title">محاور الخطة الاتصالية</div>
    <div class="content-subtitle">Communication Plan Pillars</div>
    
    <div class="info-card">
        <div class="info-card-title">الهدف الرئيسي</div>
        <div class="info-card-value">
            تموضع موتور سيتي كوجهة رئيسية ومرجعية لقطاع السيارات في الأردن والمنطقة
        </div>
    </div>
    
    <div class="content-title" style="margin-top: 15mm;">الجمهور المستهدف</div>
    
    <ul class="content-list">
        <li><strong>الجمهور الأساسي:</strong> أصحاب معارض السيارات الحاليين في عمان</li>
        <li><strong>الجمهور الثانوي:</strong> المستثمرون في قطاع السيارات</li>
        <li><strong>صناع القرار:</strong> الجهات الحكومية والتنظيمية</li>
        <li><strong>المؤثرون:</strong> الإعلاميون والمحللون الاقتصاديون</li>
    </ul>
    
    <div class="content-title" style="margin-top: 15mm;">الرسائل المركزية</div>
    
    <div class="info-card" style="border-right-color: #10b981;">
        <div class="info-card-title" style="color: #10b981;">الرسالة الرئيسية</div>
        <div class="info-card-value">
            "من التشتت إلى التكامل - موتور سيتي، مدينة السيارات الأولى في الأردن"
        </div>
    </div>
    
    <ul class="content-list">
        <li>موتور سيتي ليس مجرد موقع جديد، بل منظومة متكاملة للنجاح</li>
        <li>استثمارك في موتور سيتي هو استثمار في مستقبل أعمالك</li>
        <li>نحن لا نبني معارض، نحن نبني مستقبل قطاع السيارات في الأردن</li>
    </ul>
</div>

<div class="content-page">
    <div class="content-header">القسم الرابع: الخطة الاستراتيجية</div>
    
    <div class="content-title">القنوات الاتصالية</div>
    <div class="content-subtitle">Communication Channels</div>
    
    <table class="data-table">
        <tr>
            <th>القناة</th>
            <th>الاستخدام</th>
        </tr>
        <tr>
            <td><strong>العلاقات العامة</strong></td>
            <td>بناء السمعة والمصداقية مع الإعلام والجهات الرسمية</td>
        </tr>
        <tr>
            <td><strong>الإعلام التقليدي</strong></td>
            <td>الصحف الاقتصادية، التلفزيون، الإذاعات</td>
        </tr>
        <tr>
            <td><strong>وسائل التواصل الاجتماعي</strong></td>
            <td>LinkedIn للمحترفين، Instagram للصور، YouTube للفيديو</td>
        </tr>
        <tr>
            <td><strong>التواصل المباشر</strong></td>
            <td>زيارات ميدانية، اجتماعات فردية، مؤتمرات</td>
        </tr>
        <tr>
            <td><strong>الفعاليات</strong></td>
            <td>معارض السيارات، مؤتمرات القطاع، جولات الموقع</td>
        </tr>
    </table>
    
    <div class="content-title" style="margin-top: 15mm;">الجدول الزمني</div>
    
    <table class="data-table">
        <tr>
            <th>المرحلة</th>
            <th>الفترة</th>
            <th>الأنشطة الرئيسية</th>
        </tr>
        <tr>
            <td><strong>التأسيس</strong></td>
            <td>Q1 2026</td>
            <td>بناء الهوية، إطلاق الموقع، بناء قاعدة البيانات</td>
        </tr>
        <tr>
            <td><strong>التوعية</strong></td>
            <td>Q2 2026</td>
            <td>حملات إعلامية، لقاءات أصحاب المعارض</td>
        </tr>
        <tr>
            <td><strong>الجذب</strong></td>
            <td>Q3-Q4 2026</td>
            <td>عروض الحجز المبكر، جولات الموقع</td>
        </tr>
        <tr>
            <td><strong>الإطلاق</strong></td>
            <td>2027</td>
            <td>حفل الافتتاح، تغطية إعلامية واسعة</td>
        </tr>
    </table>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- الغلاف الخلفي -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div class="back-cover">
    <div class="cover-top-bar"></div>
    
    <div class="back-logo-en">NOBLES</div>
    <div class="back-logo-sub">REAL ESTATE</div>
    <div class="back-logo-ar">نوبلز العقارية</div>
    
    <div class="back-line"></div>
    
    <div class="back-contact">www.nobles.jo</div>
    <div class="back-contact">info@nobles.jo</div>
    <div class="back-contact">+962 6 XXX XXXX</div>
    
    <div class="back-copyright">© 2026 Nobles Real Estate. All Rights Reserved.</div>
    
    <div class="cover-bottom-bar"></div>
</div>

</body>
</html>
"""

def create_pdf():
    """إنشاء ملف PDF"""
    print("🚀 بدء إنشاء كتاب موتور سيتي PDF...")
    
    # إعدادات الخطوط
    font_config = FontConfiguration()
    
    # إنشاء HTML
    html = HTML(string=HTML_CONTENT)
    
    # CSS إضافي للطباعة
    css = CSS(string='''
        @page { margin: 2cm; }
        @page cover { margin: 0; }
    ''', font_config=font_config)
    
    # إنشاء PDF
    output_file = "motor_city_book_arabic.pdf"
    html.write_pdf(output_file, stylesheets=[css], font_config=font_config)
    
    print(f"✅ تم إنشاء الكتاب بنجاح: {output_file}")
    print(f"📂 المسار الكامل: {os.path.abspath(output_file)}")
    
    return output_file

if __name__ == "__main__":
    create_pdf()
