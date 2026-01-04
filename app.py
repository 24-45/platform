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
        # تجاوز تسجيل الدخول في وضع التطوير
        if app.debug and 'user_id' not in session:
            session['user_id'] = 'dev-admin'
            session['user_email'] = 'admin@24-45.com'
            session['user_name'] = 'مطور'
            session['role'] = 'admin'
            session['tenant_access'] = ['nobles', 'zakah', 'waqf', 'alic']
            session['default_tenant'] = 'nobles'
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def tenant_access_required(f):
    """ديكوريتور للتحقق من صلاحية الوصول للعميل"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Admin يمكنه الوصول لكل العملاء
        if session.get('role') == 'admin':
            return f(*args, **kwargs)
        
        tenant_slug = kwargs.get('tenant_slug')
        user_tenants = session.get('tenant_access', [])
        
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
            return json.load(f)
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
    """تسجيل دخول تلقائي للتطوير - احذف هذا في الإنتاج!"""
    session['user_id'] = 'dev-admin'
    session['user_email'] = 'admin@24-45.com'
    session['user_name'] = 'مطور'
    session['role'] = 'admin'
    session['tenant_access'] = ['nobles', 'zakah', 'waqf']
    session['default_tenant'] = 'nobles'
    return redirect(url_for('admin_campaigns'))


@app.route('/dev-login-alic')
def dev_login_alic():
    """تسجيل دخول تلقائي كعميل ALIC للتطوير"""
    session['user_id'] = 'user4'
    session['user_email'] = 'alic@24-45.com'
    session['user_name'] = 'عميل ALIC'
    session['role'] = 'client'
    session['tenant_access'] = ['alic', 'zakah', 'waqf']
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


# ==================== صفحة ALIC - شركة أليك للتطوير ====================

@app.route('/alic')
def alic_page():
    """صفحة شركة أليك للتطوير - قيد الإنشاء"""
    tenant = get_tenant_by_slug('alic')
    return render_template('platform/coming_soon.html', tenant=tenant, project_name='شركة أليك للتطوير')


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
    # عرض صفحة تسجيل الدخول للجميع
    # إذا المستخدم مسجل دخول، يمكنه تسجيل الخروج أو الاستمرار
    return render_template('platform/login.html')


@app.route('/auth/google')
def google_login():
    """بدء عملية تسجيل الدخول بجوجل"""
    # استخدام الرابط مباشرة لتجنب مشاكل redirect_uri_mismatch
    if request.host.endswith('pythonanywhere.com'):
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
                    
                    # توجيه حسب الصلاحية
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        # توجيه للـ Dashboard لعرض المشاريع المتاحة
                        return redirect(url_for('client_dashboard'))
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
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                # توجيه للـ Dashboard لعرض المشاريع المتاحة
                return redirect(url_for('client_dashboard'))
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
    
    # إذا كان المستخدم admin يرى جميع المشاريع
    user_role = session.get('role', 'client')
    if user_role == 'admin':
        # استبعاد المشاريع المخفية
        accessible_tenants = [t for t in all_tenants if t.get('active', True) and not t.get('hidden', False)]
    else:
        # عرض المشاريع التي يملك المستخدم صلاحية الوصول إليها
        user_tenants = session.get('tenant_access', [])
        accessible_tenants = [t for t in all_tenants if t.get('active', True) and t.get('id') in user_tenants and not t.get('hidden', False)]
    
    return render_template('platform/client_dashboard.html', tenants=accessible_tenants)


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
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    # البحث أولاً في projects.json
    project = get_tenant_project_by_slug(tenant_slug, project_slug)
    
    # إذا لم يوجد، البحث في campaigns.json
    if not project:
        campaign = get_campaign_by_id(project_slug)
        if campaign:
            # توجيه للراوت الجديد للحملات
            return redirect(url_for('campaign_report', campaign_id=project_slug))
        return render_template('404.html'), 404
    
    template = get_tenant_template(tenant_slug, 'project_report.html')
    return render_template(template, 
                         tenant=tenant,
                         project=project)


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
    role = request.form.get('role', 'client')  # الدور الجديد
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['name'] = name
            user['email'] = email
            user['default_tenant'] = default_tenant
            user['tenant_access'] = tenants
            user['role'] = role  # تحديث الدور
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
def admin_campaigns():
    """إدارة الحملات - لوحة التحكم"""
    # مؤقتاً للتطوير - تسجيل دخول تلقائي
    if 'user_id' not in session:
        session['user_id'] = 'dev-admin'
        session['user_email'] = 'admin@24-45.com'
        session['user_name'] = 'مطور'
        session['role'] = 'admin'
        session['tenant_access'] = ['nobles', 'zakah', 'waqf']
        session['default_tenant'] = 'nobles'
    
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
def admin_new_campaign():
    """إنشاء حملة جديدة - الـ Wizard"""
    # مؤقتاً للتطوير - تسجيل دخول تلقائي
    if 'user_id' not in session:
        session['user_id'] = 'dev-admin'
        session['user_email'] = 'admin@24-45.com'
        session['user_name'] = 'مطور'
        session['role'] = 'admin'
        session['tenant_access'] = ['nobles', 'zakah', 'waqf']
        session['default_tenant'] = 'nobles'
    
    # GET - عرض الـ Wizard الجديد
    campaign_types = load_campaign_types()
    tenants = get_all_tenants()
    
    return render_template('tenant/nobles/admin/campaign_wizard.html',
                         campaign_types=campaign_types,
                         tenants=tenants)


@app.route('/api/campaigns/create', methods=['POST'])
def api_create_campaign():
    """API - إنشاء حملة جديدة من الـ Wizard"""
    # مؤقتاً للتطوير - تسجيل دخول تلقائي
    if 'user_id' not in session:
        session['user_id'] = 'dev-admin'
        session['role'] = 'admin'
    
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
def admin_edit_campaign(campaign_id):
    """تحرير حملة"""
    # مؤقتاً للتطوير - تسجيل دخول تلقائي
    if 'user_id' not in session:
        session['user_id'] = 'dev-admin'
        session['user_email'] = 'admin@24-45.com'
        session['user_name'] = 'مطور'
        session['role'] = 'admin'
        session['tenant_access'] = ['nobles', 'zakah', 'waqf']
        session['default_tenant'] = 'nobles'
    
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
def admin_update_campaign(campaign_id):
    """تحديث بيانات حملة"""
    # مؤقتاً للتطوير
    if 'role' not in session:
        session['role'] = 'admin'
    
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
def admin_view_brief(campaign_id):
    """عرض الموجز الإبداعي للفريق"""
    # مؤقتاً للتطوير
    if 'user_id' not in session:
        session['user_id'] = 'dev-admin'
        session['role'] = 'admin'
    
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

