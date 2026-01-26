"""
24°45° Platform - منصة الإحداثيات الإعلامية
Data Scraping, Content Analysis & Media Automation
تجريف البيانات وتحليل المضمون وأتمتة العمليات الاتصالية
"""

from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for, session, flash
from pathlib import Path
from functools import wraps
from authlib.integrations.flask_client import OAuth
import json
import os
import logging
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# إعداد logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'platform-24-45-secret-key-2025')
app.jinja_env.auto_reload = True

# إعداد HTTPS للإنتاج (PythonAnywhere)
app.config['PREFERRED_URL_SCHEME'] = 'https'

# إعداد Google OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID', ''),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', ''),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# مسار ملفات البيانات
DATA_PATH = Path(app.root_path) / 'data'
TENANTS_PATH = DATA_PATH / 'tenants'


# ==================== نظام المصادقة ====================

def load_users():
    """تحميل بيانات المستخدمين"""
    users_file = DATA_PATH / 'users.json'
    if users_file.exists():
        with open(users_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('users', [])
    return []


def get_user_by_email(email):
    """البحث عن مستخدم بالإيميل"""
    users = load_users()
    for user in users:
        if user.get('email', '').lower() == email.lower():
            return user
    return None


def get_current_user_permissions():
    """قراءة صلاحيات المستخدم الحالي من الملف مباشرة (لتحديث فوري)"""
    user_email = session.get('user_email')
    if not user_email:
        return {}
    user = get_user_by_email(user_email)
    if not user:
        return {}
    
    tenant_access = user.get('tenant_access', [])
    role = user.get('role', 'client')
    
    # ✅ تبسيط الصلاحيات:
    # - Admin لديه كل الصلاحيات
    # - أي مستخدم لديه tenant_access يمكنه الوصول للمشاريع
    # - صلاحية ALIC تُعطى لمن لديه nobles أو can_access_alic_report
    
    return {
        'tenant_access': tenant_access,
        'role': role,
        'can_access_alic_report': user.get('can_access_alic_report', False) or 'nobles' in tenant_access,
    }


def authenticate_user(email, password):
    """التحقق من بيانات المستخدم"""
    user = get_user_by_email(email)
    if user and user.get('password') == password and user.get('active', True):
        return user
    return None


def login_required(f):
    """ديكوريتور للتحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # ✅ تجاوز تلقائي في وضع التطوير
        if app.debug and 'user_id' not in session:
            session['user_id'] = 'dev-admin'
            session['user_email'] = 'admin@24-45.com'
            session['user_name'] = 'مطور'
            session['role'] = 'admin'
            session['tenant_access'] = ['nobles', 'zakah', 'waqf', 'qatar_sports']
            session['default_tenant'] = 'nobles'
        
        if 'user_id' not in session:
            # ✅ حفظ الرابط الأصلي كـ query parameter
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def tenant_access_required(f):
    """ديكوريتور للتحقق من صلاحية الوصول للعميل"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # ✅ حفظ الرابط الأصلي كـ query parameter
            return redirect(url_for('login', next=request.url))
        
        # Admin يمكنه الوصول لكل العملاء
        if session.get('role') == 'admin':
            return f(*args, **kwargs)
        
        tenant_slug = kwargs.get('tenant_slug')
        project_slug = kwargs.get('project_slug', '')
        
        # قراءة الصلاحيات من الملف مباشرة (لتحديث فوري بدون إعادة تسجيل الدخول)
        permissions = get_current_user_permissions()
        user_tenants = permissions.get('tenant_access', [])
        
        # السماح بالوصول لتقرير ALIC #01 إذا كان لديه الصلاحية
        if tenant_slug == 'nobles' and project_slug == 'alic-almuwaqqar':
            if permissions.get('can_access_alic_report', False):
                return f(*args, **kwargs)
        
        if tenant_slug and tenant_slug not in user_tenants:
            flash('ليس لديك صلاحية للوصول لهذا العميل', 'error')
            # توجيه للعميل الافتراضي أو صفحة الخطأ
            default_tenant = session.get('default_tenant')
            if default_tenant:
                return redirect(url_for('tenant_home', tenant_slug=default_tenant))
            return redirect(url_for('access_denied'))
        
        return f(*args, **kwargs)
    return decorated_function


def is_admin():
    """التحقق إذا المستخدم أدمن"""
    return session.get('role') == 'admin'


# ==================== Context Processor للقوالب ====================

@app.context_processor
def inject_tenant_urls():
    """توفير دوال url_for البديلة للقوالب"""
    def get_current_tenant():
        """الحصول على tenant_slug من المسار الحالي"""
        if request.view_args and 'tenant_slug' in request.view_args:
            return request.view_args['tenant_slug']
        # محاولة استخراج من المسار
        path_parts = request.path.strip('/').split('/')
        if path_parts and path_parts[0] in ['nobles', 'zakah', 'waqf']:
            return path_parts[0]
        return None
    
    current_tenant = get_current_tenant()
    
    # دوال مساعدة للقوالب
    def tenant_url_for(endpoint, **kwargs):
        """url_for مخصص للمستأجرين"""
        tenant = current_tenant
        if not tenant:
            return url_for(endpoint, **kwargs)
        
        # تحويل الـ endpoints القديمة للجديدة
        endpoint_map = {
            'index': 'tenant_home',
            'projects': 'tenant_projects', 
            'reports': 'tenant_reports',
            'about': 'tenant_about',
            'project_report': 'tenant_project_report',
            'project_detail': 'tenant_project_detail',
        }
        
        new_endpoint = endpoint_map.get(endpoint, endpoint)
        if new_endpoint.startswith('tenant_'):
            kwargs['tenant_slug'] = tenant
        
        return url_for(new_endpoint, **kwargs)
    
    return {
        'current_tenant': current_tenant,
        'tenant_url_for': tenant_url_for,
    }


# ==================== وظائف تحميل البيانات ====================

def load_platform_config():
    """تحميل إعدادات المنصة"""
    config_file = DATA_PATH / 'platform.json'
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"platform": {}, "tenants": []}


def get_all_tenants():
    """جلب جميع العملاء المسجلين"""
    tenants_file = DATA_PATH / 'tenants.json'
    if tenants_file.exists():
        with open(tenants_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tenants', [])
    return []


def get_tenant_by_slug(slug):
    """جلب عميل بواسطة الـ slug"""
    tenants = get_all_tenants()
    for tenant in tenants:
        if tenant.get('slug') == slug:
            return tenant
    return None


def load_tenant_projects(tenant_slug):
    """تحميل مشاريع عميل محدد"""
    tenant_file = TENANTS_PATH / tenant_slug / 'projects.json'
    if tenant_file.exists():
        with open(tenant_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # ترتيب المشاريع حسب حقل order إن وجد
            if 'projects' in data:
                data['projects'] = sorted(data['projects'], key=lambda x: x.get('order', x.get('id', 999)))
            return data
    return {"projects": []}


def get_tenant_project_by_slug(tenant_slug, project_slug):
    """جلب مشروع محدد من عميل محدد"""
    data = load_tenant_projects(tenant_slug)
    for project in data.get('projects', []):
        if project.get('slug') == project_slug:
            return project
    return None


def load_tenant_config(tenant_slug):
    """تحميل إعدادات عميل محدد"""
    config_file = TENANTS_PATH / tenant_slug / 'config.json'
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# ==================== ملفات ثابتة ====================

@app.route('/favicon.ico')
def favicon():
    """تقديم الأيقونة الافتراضية"""
    static_path = Path(app.root_path) / 'static'
    return send_from_directory(static_path, 'images/favicon.svg', mimetype='image/svg+xml')


# ==================== تسجيل دخول تلقائي للتطوير ====================

@app.route('/dev-login')
def dev_login():
    """تسجيل دخول تلقائي للتطوير - يعمل فقط في البيئة المحلية"""
    # ⚠️ حماية: يعمل فقط في وضع التطوير المحلي
    if not app.debug or request.remote_addr not in ['127.0.0.1', 'localhost', '::1']:
        return render_template('404.html'), 404
    
    session['user_id'] = 'dev-admin'
    session['user_email'] = 'admin@24-45.com'
    session['user_name'] = 'مطور'
    session['role'] = 'admin'
    session['tenant_access'] = ['nobles', 'zakah', 'waqf', 'qatar_sports']
    session['default_tenant'] = 'nobles'
    return redirect(url_for('admin_campaigns'))


@app.route('/dev-login-alic')
def dev_login_alic():
    """تسجيل دخول تلقائي كعميل ALIC للتطوير - يعمل فقط في البيئة المحلية"""
    # ⚠️ حماية: يعمل فقط في وضع التطوير المحلي
    if not app.debug or request.remote_addr not in ['127.0.0.1', 'localhost', '::1']:
        return render_template('404.html'), 404
    
    session['user_id'] = 'user4'
    session['user_email'] = 'alic@24-45.com'
    session['user_name'] = 'عميل ALIC'
    session['role'] = 'client'
    session['tenant_access'] = ['nobles']  # ALIC هو مشروع تحت nobles
    return redirect(url_for('client_projects'))



# ==================== صفحة ZATCA - الهيئة العامة للزكاة والضريبة والجمارك ====================

@app.route('/zatca')
def zatca_page():
    """صفحة الهيئة العامة للزكاة والضريبة والجمارك - بدون تسجيل دخول"""
    tenant = get_tenant_by_slug('zakah')
    return render_template('tenant/zakah/index.html', tenant=tenant)


# ==================== صفحة WAQF - الهيئة العامة للأوقاف ====================

@app.route('/waqf')
def waqf_page():
    """صفحة الهيئة العامة للأوقاف - بدون تسجيل دخول"""
    tenant = get_tenant_by_slug('waqf')
    return render_template('tenant/waqf/index.html', tenant=tenant)


# ==================== صفحة وزارة الرياضة والشباب - قطر ====================

@app.route('/qatar-sports')
@app.route('/qatar-sports/')
def qatar_sports_page():
    """صفحة وزارة الرياضة والشباب - قطر"""
    tenant = get_tenant_by_slug('qatar_sports')
    return render_template('tenant/qatar_sports/index.html', tenant=tenant)


@app.route('/qatar_sports/')
@app.route('/tenant/qatar_sports/')
@app.route('/tenant/qatar_sports')
def qatar_sports_main():
    """صفحة وزارة الرياضة والشباب - قطر (المسار الرئيسي)"""
    tenant = get_tenant_by_slug('qatar_sports')
    return render_template('tenant/qatar_sports/index.html', tenant=tenant)


# ==================== صفحة وزارة الشباب والرياضة - قطر ====================

@app.route('/mys-qatar')
@app.route('/mys-qatar/')
def mys_qatar_page():
    """صفحة وزارة الشباب والرياضة - قطر"""
    tenant = get_tenant_by_slug('mys_qatar')
    return render_template('tenant/mys_qatar/index.html', tenant=tenant)


@app.route('/mys_qatar/')
@app.route('/tenant/mys_qatar/')
@app.route('/tenant/mys_qatar')
def mys_qatar_main():
    """صفحة وزارة الشباب والرياضة - قطر (المسار الرئيسي)"""
    tenant = get_tenant_by_slug('mys_qatar')
    return render_template('tenant/mys_qatar/index.html', tenant=tenant)


@app.route('/qatar_sports/export-pdf')
def qatar_sports_export_pdf():
    """
    تصدير العرض التقديمي إلى PDF بمقاس 33.87cm × 19.05cm
    تم التحديث: استخدام دقة HD مع معامل تكبير 2 للحفاظ على التنسيق والجودة
    """
    import asyncio
    from playwright.async_api import async_playwright
    from flask import Response
    from datetime import datetime
    from io import BytesIO
    
    # 1. إعدادات المتصفح: 1280x720 (الأبعاد الطبيعية عند تحويل cm إلى px في المتصفح)
    # 33.87cm * 96dpi / 2.54 = ~1280px
    VIEWPORT_W = 1280
    VIEWPORT_H = 720
    
    # 2. معامل التكبير للحصول على دقة عالية للطباعة (300 DPI تقريباً)
    # 1280 * 3.125 = 4000px
    SCALE_FACTOR = 3.125
    
    async def generate_pdf():
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--force-color-profile=srgb',
                    '--font-render-hinting=none'
                ]
            )
            # محاكاة شاشة عالية الدقة (Retina)
            context = await browser.new_context(
                viewport={'width': VIEWPORT_W, 'height': VIEWPORT_H},
                device_scale_factor=SCALE_FACTOR
            )
            page = await context.new_page()
            
            base_url = request.host_url.rstrip('/')
            url = f"{base_url}/qatar_sports/"
            
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_selector('.slide', timeout=20000)
            # انتظار إضافي لتحميل الصور والرسوم
            await page.wait_for_timeout(3000)
            
            slide_ids = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.slide'))
                    .map(slide => slide.id)
                    .filter(Boolean);
            }''')
            
            if not slide_ids:
                raise ValueError('لم يتم العثور على أي شرائح للتصدير')
            
            # حقن CSS لإخفاء القوائم فقط، دون التلاعب بالأبعاد
            await page.add_style_tag(content='''
                /* إخفاء عناصر التحكم والواجهة */
                .toc-container, .slides-nav, .fab-container, .grid-view-overlay,
                .slide-nav-minimal, .slide-nav-dropdown, .interactive-toolbar,
                .progress-bar-container, .search-modal, .notes-panel,
                .bookmarks-panel, .share-modal, .platform-bar,
                #interactiveToolbar, .slide__number, .slide__platform-logo {
                    display: none !important;
                }
                
                /* ضبط الصفحة لتملأ الشاشة */
                html, body {
                    overflow: hidden !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    background: #ffffff !important;
                    width: 100vw !important;
                    height: 100vh !important;
                }
                
                /* إخفاء جميع الشرائح بقوة */
                .slide {
                    display: none !important;
                    opacity: 0 !important;
                    visibility: hidden !important;
                    z-index: -100 !important;
                }
                
                /* الشريحة النشطة تملأ الشاشة */
                .slide.export-active {
                    display: flex !important;
                    opacity: 1 !important;
                    visibility: visible !important;
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    width: 100vw !important;
                    height: 100vh !important;
                    z-index: 9999 !important;
                    background: white !important; /* أو الخلفية الافتراضية */
                    margin: 0 !important;
                }
            ''')
            
            screenshots = []
            for slide_id in slide_ids:
                # تفعيل الشريحة الحالية فقط
                await page.evaluate('''(targetId) => {
                    document.querySelectorAll('.slide').forEach(slide => {
                        if (slide.id === targetId) {
                            slide.classList.add('export-active');
                            // تأكيد النمط عبر JS أيضاً ليغلب أي نمط مضمن
                            slide.style.setProperty('display', 'flex', 'important');
                        } else {
                            slide.classList.remove('export-active');
                            slide.style.setProperty('display', 'none', 'important');
                        }
                    });
                }''', slide_id)
                
                await page.wait_for_timeout(500)
                
                # التقاط الصورة (ستكون بدقة 3840x2160 بسبب scale factor)
                screenshot = await page.screenshot(
                    type='png',
                    full_page=False
                )
                screenshots.append(screenshot)
            
            await context.close()
            await browser.close()
            
            # قسم تجميع PDF
            try:
                from reportlab.lib.units import cm
                from reportlab.pdfgen import canvas
                from PIL import Image
                from reportlab.lib.utils import ImageReader
                
                # أبعاد الصفحة النهائية المطلوبة
                PAGE_PDF_W = 33.87 * cm
                PAGE_PDF_H = 19.05 * cm
                
                pdf_buffer = BytesIO()
                c = canvas.Canvas(pdf_buffer, pagesize=(PAGE_PDF_W, PAGE_PDF_H))
                
                for screenshot in screenshots:
                    img = Image.open(BytesIO(screenshot))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    img_buffer = BytesIO()
                    img.save(img_buffer, format='JPEG', quality=95)
                    img_buffer.seek(0)
                
                    # رسم الصورة لتملأ الصفحة بالكامل (تمدد لملء الفراغ)
                    c.drawImage(
                        ImageReader(img_buffer),
                        0,
                        0,
                        width=PAGE_PDF_W,
                        height=PAGE_PDF_H,
                        preserveAspectRatio=False 
                    )
                    c.showPage()
                
                c.save()
                pdf_buffer.seek(0)
                return pdf_buffer.getvalue()
                
            except ImportError:
                # إذا لم تكن المكتبات متوفرة، استخدم الطريقة القديمة
                logger.warning("reportlab/PIL not available, using fallback method")
                return None
    
    try:
        # تشغيل الدالة غير المتزامنة
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pdf_bytes = loop.run_until_complete(generate_pdf())
        loop.close()
        
        if pdf_bytes is None:
            return jsonify({'error': 'Missing required libraries (reportlab, Pillow)'}), 500
        
        # إرسال الملف للتحميل
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qatar_sports_presentation_{timestamp}.pdf"
        
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"خطأ في تصدير PDF: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== AI Chat API ====================
@app.route('/api/ai-chat', methods=['POST'])
def ai_chat_endpoint():
    """
    Endpoint to handle AI queries about the report data.
    """
    try:
        data = request.get_json()
        user_query = data.get('query')
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
            
        # Lazy import to ensure module is picked up
        import ai_chat
        import importlib
        importlib.reload(ai_chat) # Relax for dev
        
        # Get optional API key from request header if client wants to provide it
        client_api_key = request.headers.get('X-OpenAI-Key')
        
        response_text = ai_chat.query_intelligence_engine(user_query, api_key=client_api_key)
        
        return jsonify({'response': response_text})
    except Exception as e:
        logger.error(f"AI Chat Error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/mys-qatar/export-pdf')
def mys_qatar_export_pdf():
    """
    تصدير PDF لوزارة الرياضة - إصلاح التنسيق الجذري
    """
    import asyncio
    from playwright.async_api import async_playwright
    from flask import Response
    from datetime import datetime
    from io import BytesIO
    
    # 1. إعدادات المتصفح: 1280x720 (مطابق لأبعاد CSS بالسنتيمتر)
    VIEWPORT_W = 1280
    VIEWPORT_H = 720
    # 2. دقة عالية جداً (x3.125 => ~4000px width)
    SCALE_FACTOR = 3.125
    
    async def generate_pdf():
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            base_url = request.host_url.rstrip('/')
            url = f"{base_url}/mys-qatar/"
            
            # سياق أولي لجلب عدد الشرائح
            context = await browser.new_context(viewport={'width': VIEWPORT_W, 'height': VIEWPORT_H})
            page = await context.new_page()
            
            logger.info(f"Loading: {url}")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_selector('.slide', timeout=30000)
            
            slide_ids = await page.evaluate('() => Array.from(document.querySelectorAll(".slide")).map(s => s.id)')
            await context.close()
            
            screenshots = []
            
            # معالجة كل شريحة
            for i, slide_id in enumerate(slide_ids):
                # إنشاء سياق جديد "نظيف" لكل شريحة لضمان عدم تداخل الذاكرة
                ctx = await browser.new_context(
                    viewport={'width': VIEWPORT_W, 'height': VIEWPORT_H},
                    device_scale_factor=SCALE_FACTOR
                )
                pg = await ctx.new_page()
                
                await pg.goto(url, wait_until='networkidle', timeout=60000)
                await pg.wait_for_timeout(2000) # انتظار استقرار الأنيميشن
                
                # إخفاء العناصر وتجهيز الشريحة
                await pg.evaluate(f'''
                    () => {{
                        // 1. إزالة القوائم
                        const selectors = [
                            '.toc-container', '.slides-nav', '.fab-container', '.grid-overlay',
                            '.slide-nav-minimal', '.slide-nav-dropdown', '.interactive-toolbar',
                            '.platform-bar', '.notes-panel', '.bookmarks-panel',
                            '.share-modal', '.progress-bar-container', '#interactiveToolbar'
                        ];
                        selectors.forEach(s => document.querySelectorAll(s).forEach(e => e.style.setProperty('display', 'none', 'important')));
                        
                        // 2. إخفاء كل الشرائح (Brutal Force)
                        document.querySelectorAll('.slide').forEach(el => {{
                           el.style.setProperty('display', 'none', 'important');
                           el.style.setProperty('opacity', '0', 'important');
                           el.style.setProperty('visibility', 'hidden', 'important');
                           el.style.position = 'absolute'; // أبعده عن التدفق
                           el.style.zIndex = '-1';
                           el.classList.remove('active', 'current', 'export-active');
                        }});

                        // 3. منع الهوامش
                        document.body.style.margin = '0';
                        document.body.style.padding = '0';
                        document.body.style.overflow = 'hidden';
                        document.documentElement.style.margin = '0';
                        document.documentElement.style.padding = '0';
                        document.documentElement.style.overflow = 'hidden';

                        // 4. إظهار الشريحة الهدف فقط وتثبيتها
                        const target = document.getElementById('{slide_id}');
                        if (target) {{
                            target.style.setProperty('display', 'flex', 'important');
                            target.style.setProperty('opacity', '1', 'important');
                            target.style.setProperty('visibility', 'visible', 'important');
                            
                            target.classList.add('export-active');
                            target.style.position = 'fixed';
                            target.style.top = '0';
                            target.style.left = '0';
                            target.style.width = '100vw';
                            target.style.height = '100vh';
                            target.style.margin = '0';
                            target.style.zIndex = '9999';
                        }}
                    }}
                ''')
                
                await pg.wait_for_timeout(500)
                
                screenshot = await pg.screenshot(type='png')
                screenshots.append(screenshot)
                
                await ctx.close()
            
            await browser.close()
            
            # تجميع PDF
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from PIL import Image
            from reportlab.lib.utils import ImageReader
            
            PAGE_W = 33.87 * cm
            PAGE_H = 19.05 * cm
            
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=(PAGE_W, PAGE_H))
            
            for screenshot in screenshots:
                img = Image.open(BytesIO(screenshot))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img_buffer = BytesIO()
                img.save(img_buffer, format='JPEG', quality=95)
                img_buffer.seek(0)
                
                c.drawImage(
                    ImageReader(img_buffer),
                    0, 0,
                    width=PAGE_W,
                    height=PAGE_H,
                    preserveAspectRatio=False
                )
                c.showPage()
                
            c.save()
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pdf_bytes = loop.run_until_complete(generate_pdf())
        loop.close()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mys_qatar_report_{timestamp}.pdf"
        
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/mys-qatar/export-pdf-test')
def mys_qatar_export_pdf_test():
    """
    اختبار تصدير الشريحة الأولى فقط - بدون resize
    """
    import asyncio
    from playwright.async_api import async_playwright
    from flask import Response
    from datetime import datetime
    from io import BytesIO
    
    SLIDE_WIDTH = 4000
    SLIDE_HEIGHT = 2250
    
    async def generate_pdf():
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=4000,2250'
                ]
            )
            page = await browser.new_page()
            
            await page.set_viewport_size({'width': SLIDE_WIDTH, 'height': SLIDE_HEIGHT})
            
            url = f'http://127.0.0.1:5001/mys-qatar/'
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(5)
            
            logger.info("اختبار: تصوير الشريحة الأولى")
            
            await page.evaluate('''() => {
                const slide1 = document.getElementById('slide-1');
                if (slide1) {
                    document.querySelectorAll('.slide').forEach(s => {
                        s.style.display = 'none';
                    });
                    slide1.style.display = 'block';
                    slide1.classList.add('export-active');
                }
            }''')
            
            await asyncio.sleep(2)
            
            screenshot = await page.screenshot(
                type='png',
                full_page=False
            )
            
            await browser.close()
            
            from PIL import Image
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            
            PAGE_WIDTH = 33.87 * cm
            PAGE_HEIGHT = 19.05 * cm
            
            img = Image.open(BytesIO(screenshot))
            img_buffer = BytesIO()
            img.save(img_buffer, format='JPEG', quality=95, optimize=True)
            img_buffer.seek(0)
            
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
            
            c.drawImage(
                ImageReader(img_buffer),
                0, 0,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                preserveAspectRatio=False
            )
            
            c.save()
            pdf_data = pdf_buffer.getvalue()
            
            logger.info("تم إنشاء PDF للاختبار بنجاح - الشريحة الأولى فقط")
            return pdf_data
    
    try:
        pdf_data = asyncio.run(generate_pdf())
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'mys_qatar_test_slide1_{timestamp}.pdf'
        
        return Response(
            pdf_data,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"خطأ في اختبار تصدير PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ==================== تقرير السمعة الإعلامية - وزارة الرياضة والشباب ====================

@app.route('/slides/qatar-sports-report')
@app.route('/slides/qatar-sports-report/')
def qatar_sports_report_slides():
    """عرض تقديمي احترافي: تقرير السمعة الإعلامية - وزارة الرياضة والشباب قطر"""
    import json
    import os
    
    # تحميل بيانات التقرير
    report_path = os.path.join('static', 'data', 'qatar_sports_analysis', 'report_phases', 'PROFESSIONAL_REPORT_FINAL.json')
    report_data = {}
    
    try:
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
    except Exception as e:
        logger.error(f"خطأ في تحميل بيانات التقرير: {e}")
    
    # استخدام الملف الصحيح الذي يحتوي على الشرائح المحدثة
    tenant = get_tenant_by_slug('mys_qatar')
    return render_template('tenant/mys_qatar/index.html', tenant=tenant, report=report_data)


# ==================== صفحة نوبلز للمعاينة (بدون تسجيل دخول - للتطوير فقط) ====================

@app.route('/nobles-preview')
def nobles_preview():
    """صفحة نوبلز للمعاينة - بدون تسجيل دخول (للتطوير المحلي فقط)"""
    if not app.debug:
        return redirect(url_for('login'))
    
    tenant = get_tenant_by_slug('nobles')
    data = load_tenant_projects('nobles')
    config = load_tenant_config('nobles')
    if not config and 'company' in data:
        config = data
    
    return render_template('tenant/nobles/index.html', 
                         tenant=tenant,
                         config=config,
                         projects=data.get('projects', []))


# ==================== صفحة الأوقاف للمعاينة (بدون تسجيل دخول - للتطوير فقط) ====================

@app.route('/waqf-preview')
def waqf_preview():
    """صفحة الأوقاف للمعاينة - بدون تسجيل دخول (للتطوير المحلي فقط)"""
    if not app.debug:
        return redirect(url_for('login'))
    
    tenant = get_tenant_by_slug('waqf')
    data = load_tenant_projects('waqf')
    config = load_tenant_config('waqf')
    if not config and 'company' in data:
        config = data
    
    return render_template('tenant/waqf/index.html', 
                         tenant=tenant,
                         config=config,
                         projects=data.get('projects', []))


# ==================== روابط مباشرة للمشاريع ====================

@app.route('/alic')
def alic_page():
    """توجيه لتقرير مشروع ALIC تحت نوبلز"""
    return redirect(url_for('tenant_project_report', tenant_slug='nobles', project_slug='alic-almuwaqqar'))


@app.route('/motor-city')
def motor_city_page():
    """توجيه لتقرير مشروع Motor City تحت نوبلز"""
    return redirect(url_for('tenant_project_report', tenant_slug='nobles', project_slug='automotive-city'))


# ==================== صفحة ALIC للمعاينة (بدون تسجيل دخول - للتطوير فقط) ====================

@app.route('/alic-preview')
def alic_preview():
    """صفحة تقرير ALIC للمعاينة - بدون تسجيل دخول (للتطوير المحلي فقط)"""
    if not app.debug:
        return redirect(url_for('login'))
    
    tenant = get_tenant_by_slug('nobles')
    if not tenant:
        return render_template('404.html'), 404
    
    project = get_tenant_project_by_slug('nobles', 'alic-almuwaqqar')
    if not project:
        return render_template('404.html'), 404
    
    template = get_tenant_template('nobles', 'project_report_alic.html')
    return render_template(template, tenant=tenant, project=project)


@app.route('/motor-city-preview')
def motor_city_preview():
    """صفحة تقرير Motor City للمعاينة - بدون تسجيل دخول (للتطوير المحلي فقط)"""
    if not app.debug:
        return redirect(url_for('login'))
    
    tenant = get_tenant_by_slug('nobles')
    if not tenant:
        return render_template('404.html'), 404
    
    project = get_tenant_project_by_slug('nobles', 'automotive-city')
    if not project:
        return render_template('404.html'), 404
    
    template = get_tenant_template('nobles', 'project_report_motor_city.html')
    return render_template(template, tenant=tenant, project=project)


# ==================== الصفحة الرئيسية للمنصة ====================

@app.route('/')
def platform_home():
    """الصفحة الرئيسية للمنصة"""
    # عرض الصفحة الرئيسية للجميع (مسجل أو غير مسجل)
    
    config = load_platform_config()
    return render_template('platform/index.html', platform=config.get('platform', {}))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    # ✅ حفظ الرابط الأصلي في session قبل OAuth
    next_url = request.args.get('next')
    if next_url:
        session['next_url'] = next_url
    # عرض صفحة تسجيل الدخول للجميع
    # إذا المستخدم مسجل دخول، يمكنه تسجيل الخروج أو الاستمرار
    return render_template('platform/login.html')


@app.route('/auth/google')
def google_login():
    """بدء عملية تسجيل الدخول بجوجل"""
    # استخدام الرابط مباشرة لتجنب مشاكل redirect_uri_mismatch
    host = request.host
    if '24-45.com' in host:
        redirect_uri = 'https://www.24-45.com/auth/google/callback'
    elif 'pythonanywhere.com' in host:
        redirect_uri = 'https://24-45.pythonanywhere.com/auth/google/callback'
    else:
        redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/google/callback')
def google_callback():
    """استقبال رد جوجل بعد تسجيل الدخول"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if user_info:
            email = user_info.get('email', '')
            name = user_info.get('name', '')
            picture = user_info.get('picture', '')
            
            # البحث عن المستخدم في قاعدة البيانات
            user = get_user_by_email(email)
            
            if user:
                # التحقق من حالة الحساب
                status = user.get('status', 'approved')  # للتوافق مع الحسابات القديمة
                
                if status == 'pending':
                    # حساب منتظر الموافقة
                    session['pending_user'] = {
                        'name': user.get('name', name),
                        'email': email,
                        'picture': picture
                    }
                    flash('حسابك بانتظار موافقة المسؤول. سيتم إشعارك عند الموافقة.', 'warning')
                    return redirect(url_for('pending_approval'))
                    
                elif status == 'rejected':
                    flash('تم رفض طلب تسجيلك. تواصل مع المسؤول لمزيد من المعلومات.', 'error')
                    return redirect(url_for('login'))
                    
                elif not user.get('active', True):
                    flash('حسابك معطل. تواصل مع المسؤول.', 'error')
                    return redirect(url_for('login'))
                    
                else:
                    # حساب موافق عليه - تسجيل الدخول
                    session['user_id'] = user['id']
                    session['user_email'] = user['email']
                    session['user_name'] = user.get('name', name)
                    session['user_picture'] = picture
                    session['role'] = user['role']
                    session['tenant_access'] = user.get('tenant_access', [])
                    session['default_tenant'] = user.get('default_tenant')
                    session['can_access_projects'] = user.get('can_access_projects', False)
                    session['can_access_alic_report'] = user.get('can_access_alic_report', False)
                    
                    # ✅ التوجيه للرابط الأصلي إذا كان موجوداً
                    next_url = session.pop('next_url', None)
                    if next_url:
                        return redirect(next_url)
                    
                    # توجيه حسب الصلاحية
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        # توجيه للـ Dashboard لعرض المشاريع المتاحة
                        return redirect(url_for('client_projects'))
            else:
                # مستخدم جديد - إنشاء حساب بانتظار الموافقة
                import uuid
                new_user = {
                    'id': str(uuid.uuid4())[:8],
                    'email': email,
                    'name': name,
                    'picture': picture,
                    'role': 'client',
                    'tenant_access': [],
                    'default_tenant': '',
                    'active': True,
                    'status': 'pending',  # بانتظار الموافقة
                    'registered_at': __import__('datetime').datetime.now().isoformat()
                }
                
                users = load_users()
                users.append(new_user)
                save_users(users)
                
                # رسالة ترحيب للمستخدم الجديد
                flash(f'مرحباً {name}! تم إنشاء حسابك بنجاح وهو الآن بانتظار موافقة المسؤول.', 'success')
                
                # توجيه لصفحة الانتظار
                session['pending_user'] = {
                    'name': name,
                    'email': email,
                    'picture': picture
                }
                return redirect(url_for('pending_approval'))
                
    except Exception as e:
        print(f"Google OAuth Error: {e}")
        flash('حدث خطأ أثناء تسجيل الدخول. حاول مرة أخرى.', 'error')
    
    return redirect(url_for('login'))


@app.route('/pending-approval')
def pending_approval():
    """صفحة انتظار موافقة الأدمن"""
    pending_user = session.get('pending_user')
    if not pending_user:
        return redirect(url_for('login'))
    return render_template('platform/pending_approval.html', user=pending_user)


@app.route('/login/password', methods=['POST'])
def login_password():
    """تسجيل الدخول بكلمة المرور"""
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    
    user = get_user_by_email(email)
    
    if user:
        # التحقق من حالة الحساب
        status = user.get('status', 'approved')
        
        if status == 'pending':
            flash('حسابك بانتظار موافقة المسؤول. سيتم إشعارك عند الموافقة.', 'warning')
            return redirect(url_for('login'))
        elif status == 'rejected':
            flash('تم رفض طلب تسجيلك. تواصل مع المسؤول للمزيد من المعلومات.', 'error')
            return redirect(url_for('login'))
        elif not user.get('active', True):
            flash('حسابك معطل حالياً. تواصل مع المسؤول.', 'error')
            return redirect(url_for('login'))
        
        # التحقق من كلمة المرور
        if user.get('password') == password:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user.get('name', email)
            session['role'] = user['role']
            session['tenant_access'] = user.get('tenant_access', [])
            session['default_tenant'] = user.get('default_tenant')
            session['can_access_projects'] = user.get('can_access_projects', False)
            session['can_access_alic_report'] = user.get('can_access_alic_report', False)
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                # توجيه للـ Dashboard لعرض المشاريع المتاحة
                return redirect(url_for('client_projects'))
        else:
            flash('كلمة المرور غير صحيحة', 'error')
    else:
        # مستخدم غير موجود - توجيهه لتسجيل الدخول بـ Google
        flash('هذا البريد غير مسجل. سجّل دخولك بحساب Google للتسجيل التلقائي.', 'info')
    
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect(url_for('platform_home'))


@app.route('/access-denied')
def access_denied():
    """صفحة عدم الصلاحية"""
    return render_template('platform/access_denied.html'), 403


@app.route('/admin')
@login_required
def admin_dashboard():
    """لوحة تحكم الأدمن"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    tenants = get_all_tenants()
    users = load_users()
    return render_template('platform/admin.html', tenants=tenants, users=users)


@app.route('/Project')
@login_required
def client_projects():
    """صفحة المشاريع للعميل - عرض جميع المشاريع"""
    all_tenants = get_all_tenants()
    
    # قراءة الصلاحيات من الملف مباشرة (لتحديث فوري)
    permissions = get_current_user_permissions()
    user_role = permissions.get('role', session.get('role', 'client'))
    user_tenants = permissions.get('tenant_access', [])
    
    # إذا كان المستخدم admin يرى جميع المشاريع
    if user_role == 'admin':
        accessible_tenants = [t for t in all_tenants if t.get('active', True) and not t.get('hidden', False)]
    else:
        # ✅ تبسيط: إذا كان لديه أي tenant_access يمكنه الوصول
        if not user_tenants:
            flash('ليس لديك صلاحية الوصول لهذه الصفحة', 'error')
            return redirect(url_for('access_denied'))
        
        # عرض المشاريع التي يملك المستخدم صلاحية الوصول إليها
        accessible_tenants = [t for t in all_tenants if t.get('active', True) and t.get('id') in user_tenants and not t.get('hidden', False)]
    
    # ✅ إذا كان المستخدم لديه مشروع واحد فقط، حوّله مباشرة
    if len(accessible_tenants) == 1 and user_role != 'admin':
        single_tenant = accessible_tenants[0]
        return redirect(url_for('tenant_home', tenant_slug=single_tenant.get('id')))
    
    # إضافة تقرير ALIC #01 إذا كان المستخدم يملك الصلاحية
    can_access_alic_report = permissions.get('can_access_alic_report', False) or user_role == 'admin' or 'nobles' in user_tenants
    
    return render_template('platform/client_dashboard.html', 
                         tenants=accessible_tenants,
                         can_access_alic_report=can_access_alic_report)


@app.route('/about')
def platform_about():
    """صفحة من نحن - المنصة"""
    config = load_platform_config()
    return render_template('platform/about.html', platform=config.get('platform', {}))


@app.route('/services')
def platform_services():
    """صفحة الخدمات"""
    config = load_platform_config()
    return render_template('platform/services.html', platform=config.get('platform', {}))


@app.route('/contact')
def platform_contact():
    """صفحة التواصل"""
    config = load_platform_config()
    return render_template('platform/contact.html', platform=config.get('platform', {}))


@app.route('/clients')
@login_required
def platform_clients():
    """صفحة العملاء - للأدمن فقط"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    tenants = [t for t in get_all_tenants() if t.get('active', True)]
    return render_template('platform/clients.html', tenants=tenants)


# ==================== مسارات العميل (Tenant Routes) ====================

def get_tenant_template(tenant_slug, template_name):
    """
    جلب القالب المناسب للعميل
    إذا وجد قالب مخصص للعميل، يستخدمه
    وإلا يستخدم القالب الافتراضي
    """
    custom_template = f'tenant/{tenant_slug}/{template_name}'
    default_template = f'tenant/{template_name}'
    
    # التحقق من وجود القالب المخصص
    template_path = Path(app.root_path) / 'templates' / 'tenant' / tenant_slug / template_name
    if template_path.exists():
        return custom_template
    return default_template


@app.route('/<tenant_slug>/')
@login_required
@tenant_access_required
def tenant_home(tenant_slug):
    """الصفحة الرئيسية للعميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    data = load_tenant_projects(tenant_slug)
    config = load_tenant_config(tenant_slug)
    
    # إذا كان config فارغ، نستخدم بيانات الشركة من ملف المشاريع
    if not config and 'company' in data:
        config = data
    
    template = get_tenant_template(tenant_slug, 'index.html')
    return render_template(template, 
                         tenant=tenant,
                         config=config,
                         projects=data.get('projects', []))


@app.route('/<tenant_slug>/projects')
@login_required
@tenant_access_required
def tenant_projects(tenant_slug):
    """صفحة مشاريع العميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    data = load_tenant_projects(tenant_slug)
    template = get_tenant_template(tenant_slug, 'projects.html')
    return render_template(template, 
                         tenant=tenant,
                         projects=data.get('projects', []))


@app.route('/<tenant_slug>/project/<project_slug>')
@login_required
@tenant_access_required
def tenant_project_detail(tenant_slug, project_slug):
    """صفحة تفاصيل مشروع العميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    project = get_tenant_project_by_slug(tenant_slug, project_slug)
    if not project:
        return render_template('404.html'), 404
    
    template = get_tenant_template(tenant_slug, 'project_detail.html')
    return render_template(template, 
                         tenant=tenant,
                         project=project)


@app.route('/<tenant_slug>/reports')
@login_required
@tenant_access_required
def tenant_reports(tenant_slug):
    """صفحة تقارير العميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    data = load_tenant_projects(tenant_slug)
    template = get_tenant_template(tenant_slug, 'reports.html')
    return render_template(template, 
                         tenant=tenant,
                         projects=data.get('projects', []))


@app.route('/<tenant_slug>/report/<project_slug>')
@app.route('/<tenant_slug>/project-report/<project_slug>')
@login_required
@tenant_access_required
def tenant_project_report(tenant_slug, project_slug):
    """صفحة تقرير مشروع العميل"""
    try:
        logger.info(f"Loading project report: tenant={tenant_slug}, project={project_slug}")
        
        tenant = get_tenant_by_slug(tenant_slug)
        if not tenant:
            logger.error(f"Tenant not found: {tenant_slug}")
            return render_template('404.html'), 404
        
        # البحث أولاً في projects.json
        project = get_tenant_project_by_slug(tenant_slug, project_slug)
        logger.info(f"Project found: {project is not None}")
        
        # إذا لم يوجد، البحث في campaigns.json
        if not project:
            campaign = get_campaign_by_id(project_slug)
            if campaign:
                logger.info(f"Redirecting to campaign report: {project_slug}")
                return redirect(url_for('campaign_report', campaign_id=project_slug))
            logger.error(f"Project not found: {project_slug}")
            return render_template('404.html'), 404
        
        # اختيار القالب المناسب حسب المشروع - فصل كامل بين المشاريع
        if project_slug == 'automotive-city':
            template_name = 'project_report_motor_city.html'
        elif project_slug == 'alic-almuwaqqar':
            template_name = 'project_report_alic.html'
        else:
            template_name = 'project_report.html'
        
        template = get_tenant_template(tenant_slug, template_name)
        logger.info(f"Using template: {template}")
        
        return render_template(template, 
                             tenant=tenant,
                             project=project)
    except Exception as e:
        logger.error(f"Error in tenant_project_report: {str(e)}")
        logger.error(traceback.format_exc())
        raise


@app.route('/<tenant_slug>/about')
@login_required
@tenant_access_required
def tenant_about(tenant_slug):
    """صفحة من نحن للعميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    config = load_tenant_config(tenant_slug)
    template = get_tenant_template(tenant_slug, 'about.html')
    return render_template(template, tenant=tenant, config=config)


@app.route('/<tenant_slug>/login')
def tenant_login(tenant_slug):
    """صفحة تسجيل الدخول للعميل - توجيه لصفحة الدخول الرئيسية"""
    return redirect(url_for('login'))


# ==================== API للمنصة ====================

@app.route('/api/platform')
def api_platform():
    """API: معلومات المنصة"""
    config = load_platform_config()
    return jsonify(config)


@app.route('/api/tenants')
def api_tenants():
    """API: جلب جميع العملاء"""
    tenants = get_all_tenants()
    active_tenants = [t for t in tenants if t.get('active', True)]
    return jsonify({"tenants": active_tenants})


@app.route('/api/<tenant_slug>/projects')
def api_tenant_projects(tenant_slug):
    """API: جلب مشاريع عميل محدد"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return jsonify({"error": "العميل غير موجود"}), 404
    
    data = load_tenant_projects(tenant_slug)
    return jsonify(data)


@app.route('/api/<tenant_slug>/project/<project_slug>')
def api_tenant_project(tenant_slug, project_slug):
    """API: جلب مشروع محدد"""
    project = get_tenant_project_by_slug(tenant_slug, project_slug)
    if not project:
        return jsonify({"error": "المشروع غير موجود"}), 404
    return jsonify(project)


# ==================== API للأدوات الإعلامية ====================

def load_media_tools():
    """تحميل قاعدة بيانات الأدوات الإعلامية"""
    media_file = DATA_PATH / 'media_database' / 'media_tools.json'
    if media_file.exists():
        with open(media_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"influencers": [], "newspapers": [], "news_accounts": [], "statistics": {}}


@app.route('/api/media-tools')
@login_required
def api_media_tools():
    """API: جلب جميع الأدوات الإعلامية"""
    data = load_media_tools()
    return jsonify({"success": True, "data": data})


@app.route('/api/media-tools/influencers')
@login_required
def api_media_influencers():
    """API: جلب المؤثرين"""
    data = load_media_tools()
    
    # فلترة حسب المعايير
    tier = request.args.get('tier')
    city = request.args.get('city')
    specialization = request.args.get('specialization')
    search = request.args.get('search', '').lower()
    
    influencers = data.get('influencers', [])
    
    if tier:
        influencers = [i for i in influencers if i.get('category_tier') == tier]
    if city:
        influencers = [i for i in influencers if i.get('city') == city]
    if specialization:
        influencers = [i for i in influencers if specialization in i.get('specializations', [])]
    if search:
        influencers = [i for i in influencers if search in i.get('name', '').lower() or search in i.get('description', '').lower()]
    
    # ترتيب حسب المتابعين
    influencers = sorted(influencers, key=lambda x: x.get('total_followers', 0), reverse=True)
    
    return jsonify({"success": True, "data": influencers, "total": len(influencers)})


@app.route('/api/media-tools/newspapers')
@login_required
def api_media_newspapers():
    """API: جلب الصحف"""
    data = load_media_tools()
    
    city = request.args.get('city')
    search = request.args.get('search', '').lower()
    
    newspapers = data.get('newspapers', [])
    
    if city:
        newspapers = [n for n in newspapers if n.get('city') == city]
    if search:
        newspapers = [n for n in newspapers if search in n.get('name', '').lower()]
    
    return jsonify({"success": True, "data": newspapers, "total": len(newspapers)})


@app.route('/api/media-tools/news-accounts')
@login_required
def api_media_news_accounts():
    """API: جلب الحسابات الإخبارية"""
    data = load_media_tools()
    return jsonify({"success": True, "data": data.get('news_accounts', [])})


@app.route('/api/media-tools/statistics')
@login_required
def api_media_statistics():
    """API: إحصائيات الأدوات الإعلامية"""
    data = load_media_tools()
    return jsonify({"success": True, "data": data.get('statistics', {})})


@app.route('/api/media-tools/search')
@login_required
def api_media_search():
    """API: بحث في الأدوات الإعلامية"""
    data = load_media_tools()
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({"success": True, "results": [], "total": 0})
    
    results = []
    
    # البحث في المؤثرين
    for item in data.get('influencers', []):
        if query in item.get('name', '').lower() or query in item.get('description', '').lower():
            item['type'] = 'influencer'
            results.append(item)
    
    # البحث في الصحف
    for item in data.get('newspapers', []):
        if query in item.get('name', '').lower() or query in item.get('description', '').lower():
            item['type'] = 'newspaper'
            results.append(item)
    
    # البحث في الحسابات الإخبارية
    for item in data.get('news_accounts', []):
        if query in item.get('name', '').lower() or query in item.get('description', '').lower():
            item['type'] = 'news_account'
            results.append(item)
    
    # ترتيب النتائج حسب المتابعين
    results = sorted(results, key=lambda x: x.get('total_followers', 0), reverse=True)
    
    return jsonify({"success": True, "results": results, "total": len(results)})


# ==================== معالجة الأخطاء ====================

@app.errorhandler(404)
def page_not_found(e):
    """صفحة 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """صفحة 500"""
    return render_template('500.html'), 500


# ==================== إدارة المستخدمين (الأدمن) ====================

def save_users(users):
    """حفظ المستخدمين في الملف"""
    users_file = DATA_PATH / 'users.json'
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump({'users': users}, f, ensure_ascii=False, indent=2)


@app.route('/admin/users/add', methods=['POST'])
@login_required
def admin_add_user():
    """إضافة مستخدم جديد"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    role = request.form.get('role', 'user')
    default_tenant = request.form.get('default_tenant', '')
    tenants = request.form.getlist('tenants')
    
    if not name or not email:
        flash('الاسم والإيميل مطلوبان', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # تحقق من عدم وجود المستخدم
    users = load_users()
    for user in users:
        if user['email'] == email:
            flash('هذا الإيميل مسجل مسبقاً', 'error')
            return redirect(url_for('admin_dashboard'))
    
    # إنشاء مستخدم جديد
    import uuid
    new_user = {
        'id': str(uuid.uuid4())[:8],
        'email': email,
        'name': name,
        'role': role,
        'tenant_access': tenants,
        'default_tenant': default_tenant,
        'active': True
    }
    
    users.append(new_user)
    save_users(users)
    
    flash(f'تم إضافة المستخدم {name} بنجاح', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/users/edit', methods=['POST'])
@login_required
def admin_edit_user():
    """تعديل مستخدم"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    user_id = request.form.get('user_id')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    default_tenant = request.form.get('default_tenant', '')
    tenants = request.form.getlist('tenants')
    role = request.form.get('role', 'client')
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['name'] = name
            user['email'] = email
            user['default_tenant'] = default_tenant
            user['tenant_access'] = tenants
            user['role'] = role
            break
    
    save_users(users)
    flash(f'تم تعديل المستخدم {name} بنجاح', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/users/toggle/<user_id>', methods=['POST'])
@login_required
def admin_toggle_user(user_id):
    """تفعيل/تعطيل مستخدم"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['active'] = not user.get('active', True)
            status = 'تفعيل' if user['active'] else 'تعطيل'
            flash(f'تم {status} المستخدم {user["name"]}', 'success')
            break
    
    save_users(users)
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/users/delete/<user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """حذف مستخدم"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    users = load_users()
    users = [u for u in users if u['id'] != user_id]
    save_users(users)
    
    flash('تم حذف المستخدم بنجاح', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/users/approve/<user_id>', methods=['POST'])
@login_required
def admin_approve_user(user_id):
    """الموافقة على مستخدم منتظر"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    default_tenant = request.form.get('default_tenant', '')
    tenants = request.form.getlist('tenants')
    role = request.form.get('role', 'client')
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['status'] = 'approved'
            user['role'] = role
            user['tenant_access'] = tenants if tenants else []
            user['default_tenant'] = default_tenant
            user['approved_at'] = __import__('datetime').datetime.now().isoformat()
            flash(f'تمت الموافقة على {user["name"]}', 'success')
            break
    
    save_users(users)
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/users/reject/<user_id>', methods=['POST'])
@login_required
def admin_reject_user(user_id):
    """رفض طلب مستخدم"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['status'] = 'rejected'
            flash(f'تم رفض طلب {user["name"]}', 'info')
            break
    
    save_users(users)
    return redirect(url_for('admin_dashboard'))


# ==================== نظام الحملات الإعلامية ====================

CAMPAIGNS_PATH = DATA_PATH / 'campaigns'
TEMPLATES_DATA_PATH = DATA_PATH / 'templates'


def load_campaigns():
    """تحميل جميع الحملات"""
    campaigns_file = CAMPAIGNS_PATH / 'campaigns.json'
    if campaigns_file.exists():
        with open(campaigns_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"campaigns": []}


def save_campaigns(data):
    """حفظ الحملات"""
    campaigns_file = CAMPAIGNS_PATH / 'campaigns.json'
    with open(campaigns_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_campaign_by_id(campaign_id):
    """جلب حملة بواسطة الـ ID"""
    data = load_campaigns()
    for campaign in data.get('campaigns', []):
        if campaign.get('id') == campaign_id:
            return campaign
    return None


def load_campaign_template():
    """تحميل قالب الحملة"""
    template_file = TEMPLATES_DATA_PATH / 'campaign_template.json'
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@app.route('/campaign/<campaign_id>')
@login_required
def campaign_report(campaign_id):
    """عرض تقرير الحملة"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return render_template('404.html'), 404
    
    tenant_slug = campaign.get('tenant_id', 'nobles')
    tenant = get_tenant_by_slug(tenant_slug)
    
    # استخدام قالب الحملات الجديد
    return render_template('tenant/nobles/campaign_report.html', 
                         tenant=tenant,
                         campaign=campaign)


@app.route('/admin/campaigns')
@login_required
def admin_campaigns():
    """إدارة الحملات - لوحة التحكم"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    data = load_campaigns()
    tenants = get_all_tenants()
    template = load_campaign_template()
    
    return render_template('tenant/nobles/admin/campaigns.html',
                         campaigns=data.get('campaigns', []),
                         campaigns_count=len(data.get('campaigns', [])),
                         tenants=tenants,
                         template=template)


def load_campaign_types():
    """تحميل أنواع الحملات"""
    types_file = DATA_PATH / 'templates' / 'campaign_types.json'
    if types_file.exists():
        with open(types_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('campaign_types', [])
    return []


@app.route('/admin/campaigns/new', methods=['GET', 'POST'])
@login_required
def admin_new_campaign():
    """إنشاء حملة جديدة - الـ Wizard"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    # GET - عرض الـ Wizard الجديد
    campaign_types = load_campaign_types()
    tenants = get_all_tenants()
    
    return render_template('tenant/nobles/admin/campaign_wizard.html',
                         campaign_types=campaign_types,
                         tenants=tenants)


@app.route('/api/campaigns/create', methods=['POST'])
@login_required
def api_create_campaign():
    """API - إنشاء حملة جديدة من الـ Wizard"""
    if not is_admin():
        return jsonify({'error': 'غير مصرح'}), 403
    
    from datetime import datetime
    
    data = request.get_json()
    
    # إنشاء slug من الاسم
    campaign_name = data.get('basic_info', {}).get('name', 'حملة جديدة')
    campaign_slug = campaign_name.lower().replace(' ', '-').replace('/', '-')
    campaign_slug = ''.join(c for c in campaign_slug if c.isalnum() or c == '-')
    
    # التأكد من عدم تكرار الـ ID
    existing = get_campaign_by_id(campaign_slug)
    if existing:
        campaign_slug = f"{campaign_slug}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # حساب المدة الإجمالية من المراحل
    phases = data.get('phases', [])
    total_duration = sum(p.get('duration_days', 0) for p in phases)
    
    # إنشاء الحملة الجديدة
    new_campaign = {
        "id": campaign_slug,
        "campaign_type": data.get('campaign_type', 'awareness'),
        "tenant_id": "nobles",
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "created_by": session.get('user_id'),
        
        "basic_info": {
            "name": data.get('basic_info', {}).get('name', ''),
            "name_en": data.get('basic_info', {}).get('name_en', ''),
            "description": data.get('basic_info', {}).get('description', ''),
            "tagline": "",
            "duration_days": total_duration,
            "total_products": 0,
            "budget": data.get('basic_info', {}).get('budget', 0),
            "currency": data.get('basic_info', {}).get('currency', 'SAR'),
            "start_date": data.get('basic_info', {}).get('start_date', ''),
            "end_date": data.get('basic_info', {}).get('end_date', '')
        },
        
        "client_info": {
            "company_name": data.get('client_info', {}).get('company_name', ''),
            "company_name_en": data.get('client_info', {}).get('company_name_en', ''),
            "company_description": data.get('client_info', {}).get('company_description', ''),
            "industry": data.get('client_info', {}).get('industry', ''),
            "location": data.get('client_info', {}).get('location', '')
        },
        
        "project_info": {
            "project_name": data.get('project_info', {}).get('project_name', ''),
            "project_tagline": data.get('project_info', {}).get('project_tagline', ''),
            "project_description": data.get('project_info', {}).get('project_description', '')
        },
        
        "phases": phases,
        
        "client_brief": {
            "status": "pending",
            "submitted_at": None,
            "responses": {}
        },
        
        "analysis": {
            "swot": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
            "pestel": {},
            "communication_gaps": []
        },
        
        "products": [],
        "timeline": {"phases": phases, "milestones": []},
        
        "progress": {
            "overall_percentage": 0,
            "completed_products": 0,
            "in_progress_products": 0,
            "pending_products": 0,
            "days_remaining": total_duration
        },
        
        "activity_log": [{
            "action": "created",
            "timestamp": datetime.now().isoformat(),
            "user_id": session.get('user_id'),
            "details": "تم إنشاء الحملة"
        }]
    }
    
    # حفظ الحملة
    campaigns_data = load_campaigns()
    campaigns_data['campaigns'].append(new_campaign)
    save_campaigns(campaigns_data)
    
    return jsonify({
        'success': True,
        'campaign_id': campaign_slug,
        'message': 'تم إنشاء الحملة بنجاح'
    })


@app.route('/admin/campaigns/<campaign_id>')
@login_required
def admin_edit_campaign(campaign_id):
    """تحرير حملة"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        flash('الحملة غير موجودة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    campaign_types = load_campaign_types()
    tenants = get_all_tenants()
    
    return render_template('tenant/nobles/admin/campaign_editor.html',
                         campaign=campaign,
                         campaign_types=campaign_types,
                         tenants=tenants)


@app.route('/admin/campaigns/<campaign_id>/update', methods=['POST'])
@login_required
def admin_update_campaign(campaign_id):
    """تحديث بيانات حملة"""
    if not is_admin():
        return jsonify({'error': 'غير مصرح'}), 403
    
    data = load_campaigns()
    campaign_index = None
    
    for i, c in enumerate(data.get('campaigns', [])):
        if c.get('id') == campaign_id:
            campaign_index = i
            break
    
    if campaign_index is None:
        return jsonify({'error': 'الحملة غير موجودة'}), 404
    
    # تحديث البيانات
    update_data = request.get_json()
    section = update_data.get('section')
    section_data = update_data.get('data', {})
    
    if section:
        # معالجة خاصة لقسم analysis (تحديث جزئي)
        if section == 'analysis' and 'swot' in section_data:
            if 'analysis' not in data['campaigns'][campaign_index]:
                data['campaigns'][campaign_index]['analysis'] = {}
            data['campaigns'][campaign_index]['analysis']['swot'] = section_data['swot']
        else:
            data['campaigns'][campaign_index][section] = section_data
        
        data['campaigns'][campaign_index]['updated_at'] = __import__('datetime').datetime.now().isoformat()
        save_campaigns(data)
        return jsonify({'success': True, 'message': 'تم الحفظ بنجاح'})
    
    return jsonify({'error': 'لم يتم تحديد القسم'}), 400


@app.route('/admin/campaigns/<campaign_id>/delete', methods=['POST'])
def admin_delete_campaign(campaign_id):
    """حذف حملة"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    data = load_campaigns()
    data['campaigns'] = [c for c in data.get('campaigns', []) if c.get('id') != campaign_id]
    save_campaigns(data)
    
    flash('تم حذف الحملة بنجاح', 'success')
    return redirect(url_for('admin_campaigns'))


# ==================== API للحملات ====================

@app.route('/api/campaigns/<campaign_id>')
@login_required
def api_get_campaign(campaign_id):
    """API - جلب بيانات حملة"""
    campaign = get_campaign_by_id(campaign_id)
    if campaign:
        return jsonify(campaign)
    return jsonify({'error': 'الحملة غير موجودة'}), 404


@app.route('/api/campaigns/<campaign_id>/section/<section>', methods=['GET', 'POST'])
@login_required
def api_campaign_section(campaign_id, section):
    """API - جلب أو تحديث قسم من الحملة"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'error': 'الحملة غير موجودة'}), 404
    
    if request.method == 'GET':
        return jsonify(campaign.get(section, {}))
    
    # POST - تحديث القسم
    if not is_admin():
        return jsonify({'error': 'غير مصرح'}), 403
    
    data = load_campaigns()
    for c in data.get('campaigns', []):
        if c.get('id') == campaign_id:
            c[section] = request.get_json()
            c['updated_at'] = __import__('datetime').datetime.now().isoformat()
            break
    
    save_campaigns(data)
    return jsonify({'success': True})


# ==================== نظام الاستبانة (Creative Brief) ====================

def load_questionnaire_template():
    """تحميل قالب الاستبانة"""
    template_file = DATA_PATH / 'templates' / 'questionnaire_templates.json'
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # استخراج القالب الأول (creative_brief)
            templates = data.get('questionnaire_templates', [])
            if templates:
                return templates[0]  # يحتوي على sections
    return {"sections": []}


@app.route('/brief/<campaign_id>')
def client_brief(campaign_id):
    """صفحة الاستبانة للعميل - رابط عام بدون تسجيل دخول"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return render_template('tenant/nobles/404.html'), 404
    
    # التحقق إذا كانت الاستبانة مرسلة مسبقاً
    client_brief_data = campaign.get('client_brief', {})
    if client_brief_data.get('status') == 'submitted':
        return render_template('tenant/nobles/brief_submitted.html', campaign=campaign)
    
    # استخدام الأسئلة المخصصة إن وجدت، وإلا القالب الافتراضي
    custom_questions = campaign.get('custom_questions')
    if custom_questions:
        # تحويل الأسئلة المخصصة إلى تنسيق sections
        questionnaire = {
            'sections': [{
                'id': 'custom',
                'title': 'الموجز الإبداعي',
                'questions': custom_questions
            }]
        }
    else:
        questionnaire = load_questionnaire_template()
    
    return render_template('tenant/nobles/client_brief.html',
                         campaign=campaign,
                         questionnaire=questionnaire)


@app.route('/api/brief/<campaign_id>/submit', methods=['POST'])
def api_submit_brief(campaign_id):
    """API - استلام إجابات الاستبانة من العميل"""
    from datetime import datetime
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'success': False, 'error': 'الحملة غير موجودة'}), 404
    
    data = request.get_json()
    responses = data.get('responses', {})
    
    # تحديث بيانات الحملة
    campaigns_data = load_campaigns()
    for c in campaigns_data.get('campaigns', []):
        if c.get('id') == campaign_id:
            c['client_brief'] = {
                'status': 'submitted',
                'submitted_at': datetime.now().isoformat(),
                'responses': responses
            }
            c['updated_at'] = datetime.now().isoformat()
            
            # إضافة للسجل
            if 'activity_log' not in c:
                c['activity_log'] = []
            c['activity_log'].append({
                'action': 'brief_submitted',
                'timestamp': datetime.now().isoformat(),
                'user_id': 'client',
                'details': 'تم إرسال الموجز الإبداعي من العميل'
            })
            break
    
    save_campaigns(campaigns_data)
    
    return jsonify({
        'success': True,
        'message': 'تم إرسال الموجز الإبداعي بنجاح'
    })


@app.route('/admin/campaigns/<campaign_id>/brief')
@login_required
def admin_view_brief(campaign_id):
    """عرض الموجز الإبداعي للفريق"""
    if not is_admin():
        return redirect(url_for('access_denied'))
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        flash('الحملة غير موجودة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    questionnaire = load_questionnaire_template()
    
    return render_template('tenant/nobles/admin/brief_view.html',
                         campaign=campaign,
                         questionnaire=questionnaire)


@app.route('/admin/campaigns/<campaign_id>/copy-brief-link')
def get_brief_link(campaign_id):
    """الحصول على رابط الاستبانة"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'error': 'الحملة غير موجودة'}), 404
    
    brief_link = url_for('client_brief', campaign_id=campaign_id, _external=True)
    return jsonify({
        'success': True,
        'link': brief_link,
        'campaign_name': campaign.get('basic_info', {}).get('name', '')
    })


# ==================== API لحفظ واسترجاع إجابات الاستبانة ====================

QUESTIONNAIRE_RESPONSES_PATH = DATA_PATH / 'questionnaire_responses'

def ensure_questionnaire_dir():
    """التأكد من وجود مجلد إجابات الاستبانة"""
    if not QUESTIONNAIRE_RESPONSES_PATH.exists():
        QUESTIONNAIRE_RESPONSES_PATH.mkdir(parents=True)

@app.route('/api/questionnaire/<project_id>/save', methods=['POST'])
def api_save_questionnaire(project_id):
    """حفظ إجابات الاستبانة للمشروع"""
    ensure_questionnaire_dir()
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'لا توجد بيانات'}), 400
    
    # إضافة معلومات الحفظ
    data['savedAt'] = json.dumps({"$date": {"$numberLong": str(int(__import__('time').time() * 1000))}})
    data['updatedAt'] = __import__('datetime').datetime.now().isoformat()
    
    # حفظ في ملف JSON
    response_file = QUESTIONNAIRE_RESPONSES_PATH / f'{project_id}.json'
    try:
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'تم الحفظ بنجاح',
            'savedAt': data['updatedAt']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/questionnaire/<project_id>/load', methods=['GET'])
def api_load_questionnaire(project_id):
    """تحميل إجابات الاستبانة المحفوظة للمشروع"""
    ensure_questionnaire_dir()
    
    response_file = QUESTIONNAIRE_RESPONSES_PATH / f'{project_id}.json'
    
    if response_file.exists():
        try:
            with open(response_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({
                'success': True,
                'data': data
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        return jsonify({
            'success': True,
            'data': None,
            'message': 'لا توجد إجابات محفوظة'
        })


# ==================== API لإدارة أسئلة الاستبانة ====================

@app.route('/api/questionnaire/template')
def api_questionnaire_template():
    """جلب قالب الاستبانة الافتراضي"""
    template = load_questionnaire_template()
    return jsonify(template)


@app.route('/api/campaigns/<campaign_id>/questions', methods=['GET', 'POST'])
def api_campaign_questions(campaign_id):
    """جلب أو حفظ أسئلة مخصصة للحملة"""
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'error': 'الحملة غير موجودة'}), 404
    
    if request.method == 'GET':
        # جلب الأسئلة المخصصة للحملة أو الافتراضية
        custom_questions = campaign.get('custom_questions', None)
        if custom_questions:
            return jsonify({'questions': custom_questions})
        else:
            # إرجاع الأسئلة من القالب الافتراضي
            template = load_questionnaire_template()
            questions = []
            for section in template.get('sections', []):
                for q in section.get('questions', []):
                    questions.append({
                        **q,
                        'section_id': section.get('id'),
                        'section_title': section.get('title')
                    })
            return jsonify({'questions': questions})
    
    # POST - حفظ الأسئلة المخصصة
    data = request.get_json()
    questions = data.get('questions', [])
    
    campaigns_data = load_campaigns()
    for c in campaigns_data.get('campaigns', []):
        if c.get('id') == campaign_id:
            c['custom_questions'] = questions
            c['updated_at'] = __import__('datetime').datetime.now().isoformat()
            break
    
    save_campaigns(campaigns_data)
    
    return jsonify({
        'success': True,
        'message': 'تم حفظ الأسئلة بنجاح'
    })


# ==================== نظام العروض المالية ====================

@app.route('/admin/quotations')
@login_required
def admin_quotations():
    """صفحة جميع العروض المالية - للأدمن فقط"""
    if not is_admin():
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    # جلب جميع الحملات
    data = load_campaigns()
    campaigns = data.get('campaigns', [])
    
    # تصفية الحملات التي لديها عروض مالية أو منتجات
    quotations_list = []
    for campaign in campaigns:
        quotation_data = {
            'campaign_id': campaign.get('id'),
            'campaign_name': campaign.get('basic_info', {}).get('name', 'حملة بدون اسم'),
            'client_name': campaign.get('basic_info', {}).get('client', 'عميل غير محدد'),
            'status': campaign.get('status', 'draft'),
            'has_quotation': bool(campaign.get('quotation')),
            'total': 0,
            'currency': 'USD',
            'updated_at': None
        }
        
        # إذا كان هناك عرض مالي محفوظ
        if campaign.get('quotation'):
            q = campaign['quotation']
            quotation_data['total'] = q.get('grand_total', 0)
            quotation_data['currency'] = q.get('currency', 'USD')
            quotation_data['updated_at'] = q.get('updated_at')
        
        quotations_list.append(quotation_data)
    
    return render_template('tenant/nobles/admin/quotations.html',
                         quotations=quotations_list,
                         campaigns_count=len(campaigns))


@app.route('/admin/campaigns/<campaign_id>/quotation')
@login_required
def admin_campaign_quotation(campaign_id):
    """صفحة العرض المالي للحملة - للأدمن فقط"""
    if not is_admin():
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        flash('الحملة غير موجودة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    tenant_slug = campaign.get('tenant_id', 'nobles')
    tenant = get_tenant_by_slug(tenant_slug)
    
    return render_template('tenant/nobles/admin/quotation.html',
                         campaign=campaign,
                         tenant=tenant)


@app.route('/admin/campaigns/<campaign_id>/quotation-v2')
@login_required
def admin_campaign_quotation_v2(campaign_id):
    """صفحة العرض المالي النسخة الثانية - هيكل جديد"""
    if not is_admin():
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        flash('الحملة غير موجودة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    tenant_slug = campaign.get('tenant_id', 'nobles')
    tenant = get_tenant_by_slug(tenant_slug)
    
    return render_template('tenant/nobles/admin/quotation_v2.html',
                         campaign=campaign,
                         tenant=tenant)


@app.route('/admin/campaigns/<campaign_id>/quotation/save', methods=['POST'])
@login_required
def admin_save_quotation(campaign_id):
    """حفظ بيانات العرض المالي"""
    if not is_admin():
        return jsonify({'error': 'غير مصرح'}), 403
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({'error': 'الحملة غير موجودة'}), 404
    
    data = request.get_json()
    quotation_data = data.get('quotation', {})
    
    # تحديث بيانات العرض المالي في الحملة
    campaigns_data = load_campaigns()
    for c in campaigns_data.get('campaigns', []):
        if c.get('id') == campaign_id:
            c['quotation'] = quotation_data
            c['updated_at'] = __import__('datetime').datetime.now().isoformat()
            break
    
    save_campaigns(campaigns_data)
    
    return jsonify({
        'success': True,
        'message': 'تم حفظ العرض المالي بنجاح'
    })


@app.route('/admin/campaigns/<campaign_id>/quotation/pdf')
@login_required  
def admin_quotation_pdf(campaign_id):
    """توليد PDF للعرض المالي"""
    if not is_admin():
        flash('ليس لديك صلاحية للوصول لهذه الصفحة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        flash('الحملة غير موجودة', 'error')
        return redirect(url_for('admin_campaigns'))
    
    tenant_slug = campaign.get('tenant_id', 'nobles')
    tenant = get_tenant_by_slug(tenant_slug)
    
    return render_template('tenant/nobles/admin/quotation_pdf.html',
                         campaign=campaign,
                         tenant=tenant)


# ==================== تشغيل التطبيق ====================

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5001,
        host='127.0.0.1',
        threaded=True,
        use_reloader=True
    )
