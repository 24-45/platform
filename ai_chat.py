import os
import json
import glob
from pathlib import Path

def load_project_knowledge_base():
    """
    Loads ALL relevant analysis and report files to build a comprehensive context.
    Leverages Gemini Flash's large context window.
    """
    knowledge = []
    
    # 1. Define patterns for crucial data files
    # We want to catch all JSON analysis results and Markdown reports
    patterns = [
        "*.json",
        "*.md",
        "*.txt" 
    ]
    
    # Files to exclude (system files, huge raw dumps, unrelated projects)
    exclude_files = [
        "package.json", "package-lock.json", "tsconfig.json", 
        "requirements.txt", "cookies.txt", "google_oauth_setup.md",
        "deep_qualitative_analysis.py",
        "jamal_urls.txt", "musaifri_urls.txt"
    ]
    
    # Exclude files strictly by prefix for other known projects
    exclude_prefixes = [
        "ALIC_", 
        "Motor_City_", 
        "تقرير تحليل السمعة",
        "نسخة من"
    ]

    found_files = []
    
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            filename = os.path.basename(filepath)
            
            # Check explicit file exclusions
            if filename.lower() in [f.lower() for f in exclude_files]:
                continue
            
            # Check prefix exclusions (Project Isolation)
            if any(filename.startswith(prefix) for prefix in exclude_prefixes):
                continue
                
            if filename.startswith('.'): # Skip hidden files
                continue
                
            if filename in found_files: # Avoid duplicates
                continue
                
            try:
                # Limit individual file size to avoid one huge log file eating everything
                # 200KB per file limit seems reasonable for analysis structure
                file_size = os.path.getsize(filepath)
                if file_size > 500 * 1024: 
                    # If too huge, read specific chunk? or skip?
                    # Let's read first 100KB for huge files
                    pass 
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(200000) # Read up to 200k chars per file
                    
                    # Add meta-data about the file to help AI understand what it is looking at
                    file_header = f"\n\n=== FILE START: {filename} ===\n"
                    if filename.endswith('.json'):
                        file_type_hint = "(Data Source: Structured Analysis Results)"
                    elif filename.endswith('.md'):
                        file_type_hint = "(Document: Report Content/Draft)"
                    else:
                        file_type_hint = "(Context: Text Data)"
                        
                    knowledge.append(f"{file_header}{file_type_hint}\n{content}\n=== FILE END ===\n")
                    found_files.append(filename)
                    
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    print(f"AI Knowledge Base Loaded: {len(found_files)} files.")
    return "\n".join(knowledge)

def _normalize_text(text):
    """Simple normalization for Arabic text"""
    if not text: return ""
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    return text

def _run_local_search(query, context_data, error_message=None):
    """
    Fallback mechanism that searches locally in the text when AI is unavailable.
    """
    # Normalize query for better matching
    norm_query = _normalize_text(query)
    words = norm_query.split()
    
    # Filter stopwords-ish
    keywords = [w for w in words if len(w) >= 3] # Adjusted to >= 3 to catch 'اسم', 'رقم' etc.
    
    relevant_paragraphs = []
    
    # Split context into chunks
    chunks = context_data.split('\n') 
    
    seen = set()
    
    for chunk in chunks:
        if not chunk.strip(): continue
        
        norm_chunk = _normalize_text(chunk)
        
        # Scoring system
        score = 0
        
        # 1. Exact phrase match bonus
        if norm_query in norm_chunk:
            score += 10
            
        # 2. Keyword match
        for word in keywords:
            if word in norm_chunk:
                score += 1
        
        # 3. Penalize table headers or generic lists
        if "|" in chunk and "الاسم" in chunk and "التخصص" in chunk: # Table header detection
             score -= 20
        if chunk.strip().startswith("|") and len(chunk) < 50: # Short table rows
             score -= 5

        # 4. Boost likely titles if asking for name
        if ("اسم" in norm_query or "عنوان" in norm_query) and "تقرير" in norm_chunk:
             if len(chunk) < 100: # Short lines with "Report" are likely titles
                  score += 5
        
        if score > 0:
            # Clean up the chunk for display
            display_text = chunk.strip()
            if len(display_text) > 300:
                display_text = display_text[:300] + "..."
                
            if display_text not in seen:
                relevant_paragraphs.append((score, display_text))
                seen.add(display_text)

    # Sort by score descending
    relevant_paragraphs.sort(key=lambda x: x[0], reverse=True)
    
    header = ""
    if error_message:
        header = f"⚠️ {error_message}\n\n"
        header += "🔄 تحولت تلقائياً إلى وضع 'البحث المحلي' في البيانات:\n\n"
    else:
        header = "⚠️ نظام الذكاء الاصطناعي يعمل في وضع 'البحث المحلي' (غير متصل بالإنترنت).\n\n"

    if relevant_paragraphs:
        # Return top 5 matches
        result = header + "وجدت المعلومات التالية ذات الصلة في التقرير:\n\n"
        
        for i, (score, text) in enumerate(relevant_paragraphs[:7]): # Show top 7
            result += f"- {text}\n\n"
            
        return result
    else:
        return header + "عذراً، لم أجد نتائج مطابقة عبر البحث المحلي في ملفات التحليل.\nحاول استخدام كلمات مفتاحية مختلفة."

def _run_gpt_engine(query, api_key, system_prompt):
    """Execution logic for OpenAI GPT"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        # Pass exception up to be handled by caller
        raise e

def _run_gemini_engine(query, api_key, system_prompt):
    """Execution logic for Google Gemini"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Use a modern supported model
        # 'gemini-flash-latest' alias usually points to the best available free-tier Flash model.
        model_name = 'gemini-flash-latest'
        
        model = genai.GenerativeModel(model_name)
        
        # Combine system prompt with query
        full_prompt = f"System Instructions:\n{system_prompt}\n\nUser Question: {query}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
         # Try fallback to 'gemini-1.5-flash' if the first one failed?
         # Or just raise
         raise e

def query_intelligence_engine(query, api_key=None):
    """
    Sends the user query + context to an AI engine (Gemini Preferred, then OpenAI).
    """
    # Reload env vars to ensure we catch new keys added to .env without restart
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    context_data = load_project_knowledge_base()
    
    if not context_data:
        return "عذراً، لم أتمكن من تحميل بيانات التقرير. يرجى التأكد من وجود ملفات التحليل."

    system_prompt = f"""
    أنت محلل بيانات استراتيجي ومساعد ذكي لمنصة "الإحداثيات الإعلامية" (24°45° Platform).
    
    المهمة الحالية:
    أنت الآن تعمل كمساعد ذكي للعرض الفني الخاص بـ "مشروع تطوير التسويق المؤسسي وإدارة السمعة" لهيئة تنمية المجتمع - دبي.
    
    نبذة عن المشروع:
    - العميل: هيئة تنمية المجتمع - دبي
    - المشروع: تطوير منظومة التسويق المؤسسي وإدارة السمعة
    - الهدف: بناء سمعة مؤسسية متميزة وتحقيق ريادة في التواصل الاستراتيجي
    
    المنهجية المقترحة: إطار المسارين المتكاملين
    1. المسار الاستراتيجي التأسيسي: بناء الهوية السردية، خريطة أصحاب المصلحة، إطار قياس السمعة
    2. المسار التشغيلي التنفيذي: استراتيجية المحتوى، إدارة القنوات، منظومة الأزمات
    
    القواعد:
    1. أجب على الأسئلة المتعلقة بالعرض الفني ومحتواه
    2. استخدم المعلومات من ملف cda_dubai_proposal.json كمصدر رئيسي
    3. كن مختصراً وواضحاً في إجاباتك
    4. استخدم التنسيق المناسب (نقاط، عناوين) لتسهيل القراءة
    5. إذا سُئلت عن تفاصيل غير موجودة في البيانات، وضح ذلك بلطف
    
    --- بداية سياق البيانات الكامل ---
    {context_data} 
    --- نهاية سياق البيانات ---
    """
    
    # 1. Try Configured Keys
    # We prefer Google API Key if provided as it is often free/cheaper
    google_key = os.environ.get('GOOGLE_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    
    # Allow overriding via arg (though currently not passed from frontend)
    if api_key and api_key.startswith("sk-"):
        openai_key = api_key
    elif api_key:
        google_key = api_key

    # Attempt 1: Gemini
    if google_key:
        try:
            return _run_gemini_engine(query, google_key, system_prompt)
        except Exception as e:
            print(f"Gemini Error: {e}")
            # Fall through to OpenAI or Local

    # Attempt 2: OpenAI
    if openai_key:
        try:
            return _run_gpt_engine(query, openai_key, system_prompt)
        except Exception as e:
            error_str = str(e)
            if "insufficient_quota" in error_str or "429" in error_str:
                current_source = "OpenAI Quota Exceeded"
            else:
                print(f"OpenAI Error: {e}")
    
    # Attempt 3: Local Fallback
    error_msg = "لم يتم العثور على مفتاح API (Google/OpenAI) أو حدث خطأ في الاتصال."
    if google_key or openai_key:
        error_msg = "حدث خطأ في مزودي الذكاء الاصطناعي (Gemini/OpenAI)."
        
    return _run_local_search(query, context_data, error_message=error_msg)
