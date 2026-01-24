#!/usr/bin/env python3
"""
تحديث أرقام الشرائح بعد إضافة شرائح صوت الجمهور
"""

# قراءة الملف
with open('templates/tenant/mys_qatar/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# البحث عن موقع الشريحة 37 القديمة (المحادثات)
old_slide_37_pattern = 'الشريحة 37: تحليل المحادثات'
if old_slide_37_pattern in content:
    print('Found old slide 37 (conversations)')
    
    # استبدال الأرقام من 64 إلى 37 بإضافة 4 لكل منها
    # نبدأ من الأكبر للأصغر لتجنب الاستبدال المتكرر
    for old_num in range(64, 36, -1):
        new_num = old_num + 4
        
        # استبدال في ID - فقط بعد الموقع المحدد
        old_id = f'id="slide-{old_num}"'
        new_id = f'id="slide-{new_num}"'
        
        # العثور على الشريحة القديمة التي تحتاج تحديث
        pattern_pos = content.find(old_slide_37_pattern)
        if pattern_pos > 0:
            # البحث عن ID بعد هذا الموقع فقط
            search_start = pattern_pos
            found_pos = content.find(old_id, search_start)
            if found_pos > 0:
                content = content[:found_pos] + new_id + content[found_pos + len(old_id):]
                print(f'  Updated slide-{old_num} to slide-{new_num}')
        
        # استبدال في التعليقات
        old_comment = f'الشريحة {old_num}:'
        new_comment = f'الشريحة {new_num}:'
        search_start = content.find(old_slide_37_pattern)
        if search_start > 0:
            found_pos = content.find(old_comment, search_start)
            if found_pos > 0:
                content = content[:found_pos] + new_comment + content[found_pos + len(old_comment):]
        
        # استبدال في الفوتر
        old_footer = f'<span class="content-footer-page">{old_num}</span>'
        new_footer = f'<span class="content-footer-page">{new_num}</span>'
        search_start = content.find(old_slide_37_pattern)
        if search_start > 0:
            found_pos = content.find(old_footer, search_start)
            if found_pos > 0:
                content = content[:found_pos] + new_footer + content[found_pos + len(old_footer):]

# حفظ الملف
with open('templates/tenant/mys_qatar/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! Updated slide numbers.')
