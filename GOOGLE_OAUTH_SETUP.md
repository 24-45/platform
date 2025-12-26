# إعداد تسجيل الدخول بـ Google OAuth

## الخطوة 1: إنشاء مشروع في Google Cloud Console

1. اذهب إلى: https://console.cloud.google.com/
2. أنشئ مشروع جديد باسم `24-45-Platform`
3. اختر المشروع من القائمة العلوية

## الخطوة 2: تفعيل Google+ API

1. من القائمة الجانبية اختر **APIs & Services** > **Library**
2. ابحث عن **Google+ API** أو **Google People API**
3. اضغط **Enable**

## الخطوة 3: إعداد شاشة الموافقة (OAuth Consent Screen)

1. اذهب إلى **APIs & Services** > **OAuth consent screen**
2. اختر **External** (أو Internal إذا كان لديك Google Workspace)
3. املأ البيانات:
   - **App name**: `منصة 24°45°`
   - **User support email**: بريدك الإلكتروني
   - **Developer contact email**: بريدك الإلكتروني
4. في **Scopes** أضف:
   - `email`
   - `profile`
   - `openid`
5. في **Test users** أضف إيميلات المستخدمين للاختبار

## الخطوة 4: إنشاء بيانات الاعتماد (Credentials)

1. اذهب إلى **APIs & Services** > **Credentials**
2. اضغط **Create Credentials** > **OAuth client ID**
3. اختر **Web application**
4. **Name**: `24-45 Platform Web Client`
5. **Authorized JavaScript origins**:
   - `http://localhost:5001`
   - `http://127.0.0.1:5001`
   - `https://24-45.com` (بعد النشر)
6. **Authorized redirect URIs**:
   - `http://localhost:5001/auth/google/callback`
   - `http://127.0.0.1:5001/auth/google/callback`
   - `https://24-45.com/auth/google/callback` (بعد النشر)
7. اضغط **Create**
8. احفظ **Client ID** و **Client Secret**

## الخطوة 5: إعداد المتغيرات البيئية

أنشئ ملف `.env` في مجلد المشروع:

```bash
cp .env.example .env
```

ثم عدل القيم:

```
GOOGLE_CLIENT_ID=123456789-xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxx
SECRET_KEY=your-random-secret-key
```

## الخطوة 6: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

## الخطوة 7: تشغيل التطبيق

```bash
python3 app.py
```

---

## ملاحظات مهمة:

1. **للاختبار المحلي**: استخدم `http://localhost:5001` وليس `http://127.0.0.1:5001` في المتصفح
2. **Test Users**: أثناء وضع الاختبار، فقط المستخدمين المضافين في Test Users يمكنهم تسجيل الدخول
3. **Production**: بعد النشر، يجب التحقق من التطبيق (Verification) للسماح لجميع المستخدمين

---

## إضافة مستخدم جديد

عدل ملف `data/users.json`:

```json
{
    "id": "user3",
    "email": "user@gmail.com",
    "name": "اسم المستخدم",
    "role": "client",
    "tenant_access": ["nobles"],
    "default_tenant": "nobles",
    "active": true
}
```
