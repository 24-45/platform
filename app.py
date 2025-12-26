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
            
            if user and user.get('active', True):
                # مستخدم موجود - تسجيل الدخول
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
                elif user.get('default_tenant'):
                    return redirect(url_for('tenant_home', tenant_slug=user['default_tenant']))
                else:
                    return redirect(url_for('platform_home'))
            else:
                # مستخدم غير مسجل
                flash('هذا البريد الإلكتروني غير مسجل في النظام. تواصل مع المسؤول للحصول على صلاحية الدخول.', 'error')
                return redirect(url_for('login'))
                
    except Exception as e:
        print(f"Google OAuth Error: {e}")
        flash('حدث خطأ أثناء تسجيل الدخول. حاول مرة أخرى.', 'error')
    
    return redirect(url_for('login'))


@app.route('/login/password', methods=['POST'])
def login_password():
    """تسجيل الدخول بكلمة المرور"""
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    
    user = get_user_by_email(email)
    
    if user and user.get('active', True):
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
            elif user.get('default_tenant'):
                return redirect(url_for('tenant_home', tenant_slug=user['default_tenant']))
            else:
                return redirect(url_for('platform_home'))
        else:
            flash('كلمة المرور غير صحيحة', 'error')
    else:
        flash('البريد الإلكتروني غير مسجل في النظام', 'error')
    
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
@login_required
@tenant_access_required
def tenant_project_report(tenant_slug, project_slug):
    """صفحة تقرير مشروع العميل"""
    tenant = get_tenant_by_slug(tenant_slug)
    if not tenant:
        return render_template('404.html'), 404
    
    project = get_tenant_project_by_slug(tenant_slug, project_slug)
    if not project:
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
        'tenants': tenants,
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
    
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            user['name'] = name
            user['email'] = email
            user['default_tenant'] = default_tenant
            user['tenants'] = tenants
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


# ==================== تشغيل التطبيق ====================

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5001,
        host='127.0.0.1',
        threaded=True,
        use_reloader=True
    )

