/**
 * نظام إدارة الحملة الاتصالية المتكامل
 * Campaign Management System v1.0
 * 
 * يشمل: المهام، الاعتمادات، المراسلات، التقارير
 * مع مساعد AI ذكي مُدرَّب على بيانات المشروع
 */

// ==========================================
// التهيئة والمتغيرات العامة
// ==========================================

const CampaignManager = {
    currentProjectId: null,
    currentUser: null,
    currentSubTab: 'dashboard',
    tasks: [],
    approvals: [],
    messages: [],
    
    // Firebase References
    db: null,
    
    // ==========================================
    // بيانات مشروع ALIC - لمساعد AI
    // ==========================================
    projectKnowledge: {
        // معلومات المشروع الأساسية
        basicInfo: {
            name: 'مدينة أليك اللوجستية والصناعية - الموقر',
            nameEn: 'ALIC Logistic & Industrial City - Al Muwaqqar',
            type: 'صناعي ولوجستي',
            location: 'الموقر، عمّان، الأردن',
            address: 'منطقة الموقر - على بعد 15 كم من مطار الملكة علياء الدولي',
            totalArea: '525,000 م²',
            leasableArea: '350,000 م²',
            startDate: '2025-01-01',
            expectedCompletion: '2027-12-31',
            totalInvestment: '150 مليون دولار'
        },
        
        // الرؤية والرسالة
        vision: 'أن تكون المدينة اللوجستية الرائدة في المنطقة ومركزاً إقليمياً للتجارة والخدمات اللوجستية',
        mission: 'توفير بنية تحتية عالمية المستوى تدعم نمو الأعمال وتعزز الكفاءة التشغيلية',
        
        // القطاعات المستهدفة
        targetSectors: [
            'شركات الخدمات اللوجستية (3PL)',
            'التجارة الإلكترونية والتوزيع',
            'الصناعات الخفيفة والتجميع',
            'التخزين البارد والمبرد',
            'خدمات الشحن والتفريغ'
        ],
        
        // المميزات التنافسية
        competitiveAdvantages: [
            'موقع استراتيجي قرب مطار الملكة علياء الدولي (15 كم فقط)',
            'بنية تحتية متكاملة وحديثة',
            'مرونة في مساحات التأجير (500 - 50,000 م²)',
            'خدمات جمركية ولوجستية في الموقع',
            'أسعار تنافسية: 5-15 دينار/م² شهرياً',
            'شبكة طرق داخلية تربط المدينة بالمطار الدولي'
        ],
        
        // مراحل المشروع
        phases: [
            { name: 'الأعمال التمهيدية', status: 'قيد التنفيذ', progress: 20, dates: 'يناير - يونيو 2025' },
            { name: 'البنية التحتية', status: 'مخطط', progress: 0, dates: 'يوليو 2025 - يونيو 2026' },
            { name: 'المباني اللوجستية', status: 'مخطط', progress: 0, dates: 'يوليو 2026 - يونيو 2027' },
            { name: 'التشغيل', status: 'مخطط', progress: 0, dates: 'يوليو - ديسمبر 2027' }
        ],
        
        // المرافق والخدمات
        facilities: [
            'مناطق تخزين مبردة وجافة وفق معايير عالمية',
            'مركز تنظيمي للجهات الجمركية واللوجستية',
            'محطة وقود ومركز صيانة للشاحنات',
            'مباني إدارية ومرافق خدمية',
            'نظام أمني متكامل 24/7',
            'شبكة ألياف ضوئية عالية السرعة',
            'مسجد ومصلى وعيادة طبية',
            'مطاعم وكافيتريات للعاملين'
        ],
        
        // الجمهور المستهدف (من الاستبيان)
        targetAudience: {
            primary: [
                'مديرو العمليات في شركات الخدمات اللوجستية',
                'مديرو سلاسل الإمداد',
                'أصحاب شركات التجارة الإلكترونية',
                'مديرو المشتريات في الشركات الكبرى',
                'المستثمرون في القطاع اللوجستي'
            ],
            challenges: [
                'ارتفاع تكاليف التخزين في المواقع الحالية',
                'صعوبة الوصول السريع للأسواق الإقليمية',
                'نقص المساحات المناسبة بمواصفات عالمية',
                'غياب الخدمات المتكاملة في موقع واحد'
            ]
        },
        
        // المنافسون (من المقارنات المعيارية)
        competitors: {
            local: 'مدينة الحسن الصناعية، المناطق الحرة الأردنية',
            regional: 'جبل علي (دبي)، مدينة خليفة الصناعية (أبوظبي)، King Abdullah Economic City (السعودية)',
            global: 'Prologis (عالمي)، Singapore Logistics Hub'
        },
        
        // استراتيجية الاتصال المقترحة
        communicationStrategy: {
            mainMessage: 'بوابتك اللوجستية للأسواق الإقليمية من قلب الأردن',
            keyMessages: [
                'موقع استراتيجي يربط 3 قارات',
                'أقرب مدينة لوجستية لمطار الملكة علياء الدولي',
                'بنية تحتية بمعايير عالمية بتكلفة تنافسية',
                'حلول متكاملة من التخزين للتوزيع'
            ],
            channels: [
                { name: 'LinkedIn', priority: 'أساسي', reason: 'للوصول لصناع القرار B2B' },
                { name: 'المعارض المتخصصة', priority: 'أساسي', reason: 'مثل معرض Logistics Middle East' },
                { name: 'الصحف الاقتصادية', priority: 'داعم', reason: 'للمصداقية والتغطية الإعلامية' },
                { name: 'البريد المباشر', priority: 'أساسي', reason: 'للتواصل مع قوائم الشركات المستهدفة' },
                { name: 'الموقع الإلكتروني', priority: 'أساسي', reason: 'كمرجع رئيسي للمعلومات' }
            ]
        },
        
        // خطة المحتوى المقترحة
        contentPlan: {
            types: [
                { type: 'فيديو تعريفي', description: 'جولة افتراضية في المشروع والموقع', frequency: 'ربع سنوي' },
                { type: 'إنفوجرافيك', description: 'مقارنات الموقع والأسعار والخدمات', frequency: 'شهري' },
                { type: 'دراسات حالة', description: 'قصص نجاح العملاء الأوائل', frequency: 'فور التوقيع' },
                { type: 'مقالات قيادة فكرية', description: 'اتجاهات القطاع اللوجستي', frequency: 'أسبوعي' },
                { type: 'بيانات صحفية', description: 'إعلانات المراحل والشراكات', frequency: 'حسب الأحداث' }
            ]
        },
        
        // معلومات التواصل
        contact: {
            phone: '+962 (06) 5546161',
            email: 'info@noblesproperties.com',
            salesEmail: 'alic@noblesproperties.com',
            company: 'نوبلز العقارية (Nobles Properties)'
        },
        
        // ==========================================
        // خطة الاتصال والعلاقات العامة الكاملة
        // ==========================================
        communicationPlan: {
            // الأهداف الاستراتيجية الاتصالية (من تاب خطة الاتصال والعلاقات العامة)
            strategicObjectives: [
                {
                    number: 1,
                    title: 'بناء الوعي بمفهوم المدن اللوجستية المُدارة',
                    description: 'تثقيف السوق الأردني والإقليمي بمفهوم "المدينة اللوجستية المُدارة" كنموذج جديد يختلف عن المناطق الصناعية التقليدية',
                    kpi: 'نسبة التعرف على العلامة التجارية في القطاع اللوجستي'
                },
                {
                    number: 2,
                    title: 'تعزيز مكانة أليك كشريك استراتيجي',
                    description: 'ترسيخ صورة أليك كـ"شريك نمو" وليس مجرد مؤجر مساحات، مع إبراز القيمة المضافة والخدمات المتكاملة',
                    kpi: 'جودة التغطية الإعلامية ونبرة الرسائل الصحفية'
                },
                {
                    number: 3,
                    title: 'ربط أليك برؤية التحديث الاقتصادي',
                    description: 'تموضع أليك كمُمكّن وطني لأهداف رؤية التحديث الاقتصادي الأردنية وجذب الاستثمارات الأجنبية',
                    kpi: 'عدد الإشارات في خطابات ومنشورات الجهات الرسمية'
                }
            ],
            
            // الأهداف التشغيلية
            operationalObjectives: {
                primary: 'بناء الوعي بمشروع ALIC كمدينة لوجستية متكاملة قبل الإطلاق Q1 2026',
                targets: [
                    'جذب 50+ استفسار جاد من شركات لوجستية خلال 6 أشهر',
                    'تحقيق تغطية إعلامية في 10+ وسائل إعلام اقتصادية',
                    'بناء قاعدة متابعين 5000+ على LinkedIn'
                ],
                kpis: [
                    'عدد الاستفسارات الواردة',
                    'نسبة التغطية الإعلامية',
                    'عدد زيارات الموقع',
                    'عدد العقود الموقعة',
                    'معدل التحويل من استفسار لزيارة'
                ]
            },
            
            // تحليل SWOT الاتصالي
            swot: {
                strengths: [
                    'موقع استراتيجي: 15 دقيقة من المطار، 20 من الحدود',
                    '3 شراكات موقعة: محامص الشعب، قبلان، مصنع تجميل',
                    'بنية جاهزة: كهرباء، مياه، طرق معبدة',
                    'مطور متكامل: بناء + تمويل + إدارة',
                    'نظام تقسيط: ميزة فريدة في السوق'
                ],
                weaknesses: [
                    'ALIC علامة جديدة غير معروفة بعد في السوق',
                    'مرحلة ما قبل الإطلاق: لا يوجد محتوى مرئي للمشروع حالياً',
                    'منافسة مع مدن صناعية راسخة ذات سمعة طويلة',
                    'تحدي إيصال القيمة الفريدة لـ ALIC'
                ],
                opportunities: [
                    'نقص المساحات الجاهزة: فجوة في السوق',
                    'نمو التجارة الإلكترونية: زيادة الطلب على التخزين',
                    'التوسع للسعودية: قبلان نموذج للتصدير',
                    'رؤية التحديث الاقتصادي: دعم حكومي للقطاع',
                    'LinkedIn: جمهور B2B جاهز'
                ],
                threats: [
                    'منافس محلي: مدينة الحسن الصناعية',
                    'منافسة إقليمية: KAEC + Jebel Ali',
                    'حساسية الأسعار: يجب موافقة الإدارة قبل النشر',
                    'محاذير اتصالية: تجنب مقارنة المدن الحكومية مباشرة'
                ]
            },
            
            // أهداف التغطية الجغرافية
            coverageTargets: {
                local: { name: 'الأردن', percentage: 85 },
                regional: { name: 'الخليج والشرق الأوسط', percentage: 10 },
                global: { name: 'أوروبا وآسيا', percentage: 5 }
            },
            
            // التوقيت والجدول الزمني
            timeline: {
                launchDate: 'Q1 2026',
                preLaunchPhase: '6 أشهر قبل الإطلاق',
                phases: [
                    { name: 'مرحلة التأسيس', duration: 'الشهر 1-2', activities: 'بناء الهوية + إعداد المحتوى الأساسي' },
                    { name: 'مرحلة التشويق', duration: 'الشهر 3-4', activities: 'حملات تشويقية + PR + بناء القوائم' },
                    { name: 'مرحلة الإطلاق', duration: 'الشهر 5-6', activities: 'إطلاق رسمي + فعاليات + تغطية إعلامية مكثفة' }
                ]
            },
            
            // الرسائل حسب الشريحة
            messagesBySegment: {
                logistics3PL: {
                    segment: 'شركات الخدمات اللوجستية (3PL)',
                    mainMessage: 'وفّر 30% من وقت التوصيل - أقرب موقع لوجستي للمطار',
                    proofPoints: ['15 دقيقة من المطار', 'مستودعات جاهزة للتشغيل الفوري', 'خدمات جمركية في الموقع']
                },
                ecommerce: {
                    segment: 'شركات التجارة الإلكترونية',
                    mainMessage: 'انطلق للسوق السعودي من أليك - بوابتك للتوسع الإقليمي',
                    proofPoints: ['20 دقيقة من الحدود السعودية', 'قصة نجاح قبلان', 'حلول تخزين مرنة']
                },
                manufacturers: {
                    segment: 'الصناعات الخفيفة',
                    mainMessage: 'ابدأ الإنتاج فوراً - كل شيء جاهز',
                    proofPoints: ['بنية تحتية متكاملة', 'نظام تقسيط مرن', 'خدمات إدارية متكاملة']
                }
            },
            
            // المحاذير الاتصالية (Red Lines)
            redLines: [
                'عدم ذكر أسعار محددة دون موافقة الإدارة',
                'تجنب المقارنة المباشرة مع المدن الصناعية الحكومية',
                'عدم الإعلان عن شراكات قبل التوقيع الرسمي',
                'تجنب المبالغة في الوعود غير المحققة بعد'
            ],
            
            // قصص النجاح المتاحة
            successStories: [
                { client: 'محامص الشعب', story: 'توسع الطاقة الإنتاجية 3x في موقع استراتيجي' },
                { client: 'قبلان', story: 'بوابة التصدير للسعودية - نموذج للنجاح الإقليمي' },
                { client: 'مصنع التجميل', story: 'إنتاج محلي بمعايير عالمية' }
            ],
            
            // تحليل الفجوات (Gap Analysis)
            gapAnalysis: [
                { area: 'الوعي بالعلامة', current: 'ALIC علامة جديدة - مرحلة بناء الوعي قبل الإطلاق Q1 2026', bestPractice: 'KAEC: حملات تشويقية + PR قبل الإطلاق بـ 6 أشهر' },
                { area: 'المحتوى المرئي', current: 'مرحلة ما قبل البناء - لا يوجد محتوى مرئي للمشروع حالياً', bestPractice: 'DIC: Renders + جولات افتراضية + فيديو تشويقي قبل الإطلاق' },
                { area: 'التمايز التنافسي', current: 'منافسة مع مدن صناعية راسخة ذات سمعة طويلة', bestPractice: 'Prologis: قصة فريدة + USP واضح + رسائل متخصصة لكل شريحة' },
                { area: 'إيصال القيمة الفريدة', current: 'تحدي إبراز ما يميز ALIC عن المنافسين الراسخين', bestPractice: 'GLP: التركيز على المرونة + السرعة + خدمة العملاء كميزة' }
            ]
        },
        
        // ==========================================
        // المقارنات المعيارية (Benchmarks)
        // ==========================================
        benchmarks: {
            // نطاق الدراسة
            scope: {
                entities: 14,
                countries: 6,
                models: 4,
                description: 'تحليل مقارن شامل لاستراتيجيات الاتصال والعلاقات العامة للمدن والمناطق الصناعية'
            },
            
            // أهداف الدراسة
            studyObjectives: [
                'تفكيك الرسائل الاتصالية والقيم المقترحة',
                'تحليل القنوات والأدوات الاتصالية',
                'استخلاص أفضل الممارسات القابلة للتطبيق',
                'تحديد الفجوات والفرص التنافسية'
            ],
            
            // الكيانات المدروسة
            entities: {
                global: [
                    { name: 'Prologis', country: 'أمريكا', strategy: 'Beyond the Box - منصات حلول متكاملة (Essentials): العمليات، الطاقة، التنقل، القوى العاملة' },
                    { name: 'GLP', country: 'سنغافورة', strategy: 'المنظومة البيئية الثلاثية: العقارات + التكنولوجيا + التمويل' }
                ],
                gulf: [
                    { name: 'DIC - مدينة دبي الصناعية', country: 'الإمارات', strategy: 'حملة صناعة التألق (Make Brilliance) - مواءمة مع اصنع في الإمارات' },
                    { name: 'KEZAD', country: 'أبوظبي', strategy: 'المركز المتكامل للتجارة - 550 كم² + طريق المعدن الساخن + الترخيص المزدوج' },
                    { name: 'KAEC', country: 'السعودية', strategy: 'مواءمة مع رؤية 2030 + بوابة البحر الأحمر' }
                ],
                regional: [
                    { name: 'أوراسكوم', country: 'مصر', strategy: 'مجتمعات صناعية متكاملة + دعم SMEs' },
                    { name: 'بولاريس باركس', country: 'مصر', strategy: 'حلول متكاملة + بوصلة للمستثمرين' },
                    { name: 'إسباش', country: 'تركيا', strategy: 'التخصص العنقودي + مراكز R&D' },
                    { name: 'طنجة المتوسط', country: 'المغرب', strategy: 'بوابة أفريقيا وأوروبا - Nearshoring' }
                ],
                local: [
                    { name: 'Agility - القسطل', country: 'الأردن', type: 'منافس رئيسي', strategy: 'مركز لوجستي متكامل' },
                    { name: 'منطقة الرجم الشامي', country: 'الأردن', strategy: 'صناعية تقليدية' },
                    { name: 'مدينة سحاب الصناعية', country: 'الأردن', strategy: 'صناعية تقليدية' },
                    { name: 'مدينة الموقر الصناعية', country: 'الأردن', strategy: 'صناعية تقليدية' },
                    { name: 'مدينة التجمعات الصناعية', country: 'الأردن', strategy: 'صناعية تقليدية' }
                ]
            },
            
            // الرؤى من النماذج الأربعة
            modelInsights: {
                global: {
                    title: 'منظومات عالمية متكاملة',
                    insight: 'اللاعبون العالميون مثل Prologis و GLP يقدمون منصات خدمات شاملة تتجاوز الإيجار التقليدي نحو حلول القيمة المضافة',
                    recommendation: 'تطوير "ALIC Essentials" - منصة خدمات متكاملة'
                },
                gulf: {
                    title: 'مواءمة مع الرؤى الوطنية',
                    insight: 'المنصات الخليجية تربط حملاتها الاتصالية ببرامج التحول الاقتصادي (رؤية السعودية 2030، اصنع في الإمارات)',
                    recommendation: 'ربط الرسائل برؤية التحديث الاقتصادي الأردني'
                },
                regional: {
                    title: 'تخصص قطاعي وتمكين الشركات',
                    insight: 'المناطق المتخصصة في مصر وتركيا تركز على بناء مجتمعات صناعية موجهة لقطاعات محددة مع حلول تمويل وتدريب',
                    recommendation: 'برنامج "بوصلة أليك" لتمكين المستثمرين'
                },
                local: {
                    title: 'التميز المحلي والهوية الوطنية',
                    insight: 'المدن الصناعية الأردنية تركز على الموقع الاستراتيجي والأسعار التنافسية لكن فجوة في الخدمات المتكاملة',
                    recommendation: 'أليك تسد الفجوة كأول مدينة لوجستية مُدارة بمعايير عالمية'
                }
            },
            
            // المقارنة الرئيسية
            comparison: {
                valueProposition: {
                    global: 'الكفاءة، التكنولوجيا، تأثير الشبكة',
                    gulf: 'الرؤية الوطنية، تكامل الموانئ، الحجم',
                    regional: 'مجتمعات متكاملة، دعم SMEs، تكلفة منخفضة',
                    local: 'الموقع الاستراتيجي، أسعار تنافسية، فجوة في الخدمات المتكاملة'
                },
                sustainability: {
                    global: 'مركزية - حياد كربوني، طاقة شمسية',
                    gulf: 'استراتيجية - مواءمة الحياد 2050',
                    regional: 'ناشئة - حدائق بيئية',
                    local: 'غائبة - لا توجد مناطق ESG معتمدة'
                },
                technology: {
                    global: 'منتج - Essentials، روبوتات',
                    gulf: 'ممكن - مدن ذكية، منصات رقمية',
                    regional: 'ميزة - عدادات ذكية، ألياف ضوئية',
                    local: 'محدودة - بنية تحتية تقليدية'
                }
            },
            
            // الخلاصة الاستراتيجية
            strategicConclusion: 'أليك في موقع فريد لسد فجوة السوق الأردني بتقديم أول مدينة لوجستية مُدارة بمعايير عالمية. المطلوب: الترويج للقيمة المضافة لا المساحات، وبناء شراكات استراتيجية مع شركات 3PL والتجارة الإلكترونية.'
        },
        
        // ==========================================
        // الجمهور المستهدف التفصيلي
        // ==========================================
        targetAudienceMatrix: {
            primary: [
                {
                    segment: 'الشركات الصناعية المتوسطة والكبرى',
                    icon: 'industry',
                    wants: 'مساحات جاهزة للتشغيل الفوري، تكلفة تشغيلية تنافسية، بنية تحتية متكاملة، تسهيلات دفع مرنة',
                    weWant: 'شراء/استئجار وحدات صناعية، نقل عملياتهم للمدينة، عقود طويلة الأمد',
                    message: 'وسّع إنتاجك بدون عناء البناء - مستودعات جاهزة بتقسيط مريح تصل إلى 10 سنوات',
                    channels: ['زيارات ميدانية', 'غرف صناعة'],
                    tone: 'عملية'
                },
                {
                    segment: 'المستثمرون الإقليميون',
                    icon: 'globe',
                    wants: 'قاعدة انطلاق إقليمية، موقع استراتيجي قرب الحدود، اتفاقيات تجارة حرة، استقرار تشريعي',
                    weWant: 'استثمارات مباشرة، نقل قواعدهم التشغيلية، شراكات استراتيجية طويلة الأمد',
                    message: 'قاعدتك الأردنية للانطلاق - بوابة الأسواق الإقليمية + اتفاقيات تجارة حرة مع 50+ دولة',
                    channels: ['مؤتمرات استثمار', 'علاقات عامة'],
                    tone: 'استراتيجية'
                },
                {
                    segment: 'شركات 3PL واللوجستيات',
                    icon: 'truck',
                    wants: 'قرب من المطار والميناء الجاف، مستودعات حديثة، بنية تقنية متطورة، سهولة الوصول',
                    weWant: 'إنشاء مراكز توزيع، خدمات Fulfillment للتجارة الإلكترونية، عقود تخزين',
                    message: '15 دقيقة من المطار، 20 من الحدود - أقرب موقع لوجستي للتوصيل السريع',
                    channels: ['LinkedIn', 'معارض لوجستية'],
                    tone: 'تقنية'
                }
            ],
            secondary: [
                {
                    segment: 'الجهات الحكومية',
                    icon: 'landmark',
                    wants: 'نجاح المشروع كداعم للاقتصاد، التزام بالقوانين، خلق فرص عمل، دعم رؤية التحديث',
                    weWant: 'تسهيلات تنظيمية، دعم البنية التحتية، ترويج للمدينة كوجهة استثمارية وطنية'
                },
                {
                    segment: 'المؤسسات المالية',
                    icon: 'university',
                    wants: 'فرص استثمارية آمنة، أصول عقارية بعائد مضمون، تدفقات نقدية مستقرة',
                    weWant: 'تمويل مشاريع التوسع، برامج تمويل للمستثمرين، شراكات استثمارية'
                },
                {
                    segment: 'الإعلام المتخصص',
                    icon: 'newspaper',
                    wants: 'قصص نجاح حصرية، أخبار إيجابية، محتوى جذاب',
                    weWant: 'تغطية إيجابية مستمرة، بناء السمعة، نشر الوعي بأهمية المشروع إقليمياً'
                }
            ]
        },
        
        // ==========================================
        // المنتجات الاتصالية للحملة
        // ==========================================
        campaignProducts: [
            // المرحلة 1: التهيئة والتشويق (5-12 يناير 2026)
            {
                id: 'p1',
                phase: 1,
                phaseName: 'التهيئة والتشويق',
                title: 'منشور LinkedIn تشويقي',
                type: 'social_media',
                platform: 'LinkedIn',
                date: '2026-01-01',
                objective: 'بناء الوعي بمفهوم المدن اللوجستية المُدارة',
                audience: 'الشركات الصناعية',
                message: 'وسّع إنتاجك بدون عناء البناء - مستودعات جاهزة',
                deliverables: ['نص المنشور', 'صورة/جرافيك', 'جدول النشر'],
                budget: '$300 B2B',
                reach: '15,000+ صانع قرار'
            },
            {
                id: 'p2',
                phase: 1,
                phaseName: 'التهيئة والتشويق',
                title: 'بيان صحفي الكشف عن ALIC',
                type: 'press_release',
                platform: 'الغد، المملكة، رؤيا، Jordan Times، عمون',
                date: '2025-12-26',
                objective: 'بناء الوعي بمفهوم المدن اللوجستية المُدارة',
                audience: 'الإعلام المتخصص',
                message: 'قصة نجاح أردنية - مدينة لوجستية تعيد رسم الخارطة',
                deliverables: ['البيان الصحفي', 'ملف الوسائط', 'قائمة التوزيع'],
                reach: '500,000+ قارئ'
            },
            {
                id: 'p3',
                phase: 1,
                phaseName: 'التهيئة والتشويق',
                title: 'حملة SMS لغرفة الصناعة',
                type: 'sms_campaign',
                platform: 'SMS + Email',
                date: '2025-12-27',
                objective: 'بناء الوعي بمفهوم المدن اللوجستية المُدارة',
                audience: 'أعضاء غرفة صناعة عمان',
                message: 'وسّع إنتاجك بدون عناء البناء - مستودعات جاهزة بتقسيط مريح',
                deliverables: ['نص الرسالة SMS', 'نص البريد الإلكتروني', 'قائمة المستلمين', 'تقرير الإرسال'],
                reach: '2,500+ عضو'
            },
            {
                id: 'p4',
                phase: 1,
                phaseName: 'التهيئة والتشويق',
                title: 'فيديو تشويقي (Teaser)',
                type: 'video',
                platform: 'YouTube, LinkedIn, Instagram',
                date: '2026-01-05',
                objective: 'بناء الترقب والفضول',
                audience: 'الجمهور العام والمستثمرين',
                message: '15 كم تفصلك عن العالم',
                deliverables: ['الفيديو النهائي (30 ثانية)', 'ملف السيناريو', 'ملفات المصدر'],
                budget: '$2,000'
            },
            {
                id: 'p5',
                phase: 1,
                phaseName: 'التهيئة والتشويق',
                title: 'مقال رأي اقتصادي',
                type: 'article',
                platform: 'الغد، الرأي',
                date: '2026-01-10',
                objective: 'بناء المصداقية والريادة الفكرية',
                audience: 'صناع القرار الاقتصادي',
                message: 'لماذا الأردن مركز لوجستي إقليمي؟',
                deliverables: ['المقال', 'صورة الكاتب', 'السيرة الذاتية']
            },
            // المرحلة 2: الإطلاق الاستراتيجي (13-22 يناير 2026)
            {
                id: 'p6',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'حدث تسليم محامص الشعب',
                type: 'event',
                platform: 'في الموقع',
                date: '2026-01-15',
                objective: 'إثبات النجاح والمصداقية',
                audience: 'الإعلام، المستثمرين، الشركاء',
                message: 'أول قصة نجاح - محامص الشعب تتوسع مع أليك',
                deliverables: ['خطة الحدث', 'قائمة المدعوين', 'البرنامج', 'التغطية الإعلامية']
            },
            {
                id: 'p7',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'فيديو محامص الشعب (قصة النجاح)',
                type: 'video',
                platform: 'YouTube, LinkedIn',
                date: '2026-01-15',
                objective: 'إثبات النجاح والمصداقية',
                audience: 'الشركات الصناعية، المستثمرين',
                message: 'كيف توسعت محامص الشعب 3x مع أليك',
                deliverables: ['الفيديو النهائي (3 دقائق)', 'المقابلات', 'B-Roll']
            },
            {
                id: 'p8',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'بيان صحفي الإطلاق الرسمي',
                type: 'press_release',
                platform: 'جميع الوسائل الإعلامية',
                date: '2026-01-15',
                objective: 'الإعلان الرسمي عن الإطلاق',
                audience: 'الإعلام، الجمهور العام',
                message: 'نوبلز العقارية تُطلق ALIC رسمياً',
                deliverables: ['البيان الصحفي', 'صور الحدث', 'تصريحات المسؤولين']
            },
            {
                id: 'p9',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'مقابلة تلفزيونية (رؤيا/المملكة)',
                type: 'interview',
                platform: 'رؤيا، المملكة',
                date: '2026-01-16',
                objective: 'بناء المصداقية والوصول الجماهيري',
                audience: 'الجمهور الأردني العام',
                message: 'رؤية أليك للاقتصاد الأردني',
                deliverables: ['نقاط الحديث', 'Media Kit', 'تسجيل المقابلة']
            },
            {
                id: 'p10',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'جولة إعلامية في الموقع',
                type: 'media_tour',
                platform: 'في الموقع',
                date: '2026-01-17',
                objective: 'بناء المصداقية وإثبات الجاهزية',
                audience: 'الصحفيين والإعلاميين',
                message: 'شاهد بنفسك - أليك جاهزة',
                deliverables: ['برنامج الجولة', 'قائمة الصحفيين', 'ملف إعلامي', 'نقل وضيافة']
            },
            {
                id: 'p11',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'حملة LinkedIn الرئيسية',
                type: 'social_media',
                platform: 'LinkedIn',
                date: '2026-01-15',
                objective: 'الوصول لصناع القرار B2B',
                audience: 'مديرو العمليات، مديرو سلاسل الإمداد',
                message: 'أليك - شريكك للنمو',
                deliverables: ['5 منشورات', 'جرافيكس', 'جدول النشر'],
                budget: '$1,500'
            },
            {
                id: 'p12',
                phase: 2,
                phaseName: 'الإطلاق الاستراتيجي',
                title: 'Email Newsletter',
                type: 'email',
                platform: 'البريد الإلكتروني',
                date: '2026-01-16',
                objective: 'التواصل المباشر مع العملاء المحتملين',
                audience: 'قائمة العملاء المحتملين',
                message: 'أليك أُطلقت رسمياً - احجز موعدك',
                deliverables: ['تصميم النشرة', 'قائمة المستلمين', 'تقرير الفتح والنقر']
            },
            // المرحلة 3: ترسيخ الريادة (23-31 يناير 2026)
            {
                id: 'p13',
                phase: 3,
                phaseName: 'ترسيخ الريادة',
                title: 'ملف Case Study محامص الشعب',
                type: 'document',
                platform: 'موقع الويب، LinkedIn',
                date: '2026-01-22',
                objective: 'إثبات النجاح بالأرقام',
                audience: 'الشركات الصناعية، المستثمرين',
                message: 'كيف وفّرت محامص الشعب 30% من تكاليف التشغيل',
                deliverables: ['PDF التقرير', 'نسخة ويب', 'ملخص تنفيذي']
            },
            {
                id: 'p14',
                phase: 3,
                phaseName: 'ترسيخ الريادة',
                title: 'Infographic الإنجازات',
                type: 'design',
                platform: 'جميع القنوات',
                date: '2026-01-25',
                objective: 'تلخيص الإنجازات بصرياً',
                audience: 'جميع الشرائح',
                message: 'أليك بالأرقام',
                deliverables: ['الإنفوجرافيك', 'نسخ متعددة الأحجام']
            },
            {
                id: 'p15',
                phase: 3,
                phaseName: 'ترسيخ الريادة',
                title: 'تقرير أثر اقتصادي',
                type: 'report',
                platform: 'موقع الويب، الإعلام',
                date: '2026-01-28',
                objective: 'إثبات القيمة الاقتصادية للمشروع',
                audience: 'الحكومة، المستثمرين، الإعلام',
                message: 'أليك تُساهم في الناتج المحلي',
                deliverables: ['التقرير الكامل', 'ملخص تنفيذي', 'بيانات داعمة']
            },
            {
                id: 'p16',
                phase: 3,
                phaseName: 'ترسيخ الريادة',
                title: 'حملة LinkedIn B2B',
                type: 'advertising',
                platform: 'LinkedIn Ads',
                date: '2026-01-21',
                objective: 'جذب عملاء جدد',
                audience: 'صناع القرار في الشركات المستهدفة',
                message: 'احجز موقعك في أليك',
                deliverables: ['الإعلانات', 'استهداف الجمهور', 'تقرير الأداء'],
                budget: '$3,000'
            },
            {
                id: 'p17',
                phase: 3,
                phaseName: 'ترسيخ الريادة',
                title: 'تقرير ختام الحملة',
                type: 'report',
                platform: 'داخلي',
                date: '2026-01-31',
                objective: 'تقييم أداء الحملة',
                audience: 'الإدارة، الفريق',
                message: 'نتائج حملة الإطلاق',
                deliverables: ['التقرير النهائي', 'تحليل KPIs', 'توصيات مستقبلية']
            }
        ]
    },
    
    // ==========================================
    // التهيئة
    // ==========================================
    init: function(projectId) {
        this.currentProjectId = projectId || 'alic-almuwaqqar';
        
        // التحقق من وجود Firebase
        this.hasFirebase = typeof firebase !== 'undefined' && firebase.firestore;
        if (this.hasFirebase) {
            this.db = firebase.firestore();
            this.setupRealtimeListeners();
            this.loadQuestionnaireData(); // تحميل بيانات الاستبيان
        } else {
            console.log('⚠️ Firebase not available - running in offline mode');
        }
        
        // عرض التبويبات دائماً (حتى بدون Firebase)
        this.renderSubTabs();
        this.loadDashboard();
        
        console.log('✅ Campaign Manager initialized for:', this.currentProjectId);
        console.log('🤖 AI Assistant loaded with project knowledge');
    },
    
    // تحميل بيانات الاستبيان من Firebase
    loadQuestionnaireData: async function() {
        if (!this.hasFirebase || !this.db) return;
        
        try {
            const doc = await this.db.collection('questionnaires').doc(this.currentProjectId).get();
            if (doc.exists) {
                this.projectKnowledge.questionnaireData = doc.data();
                console.log('📋 Questionnaire data loaded for AI');
            }
        } catch (error) {
            console.log('Note: No questionnaire data found, using defaults');
        }
    },
    
    // ==========================================
    // Sub-Tabs Navigation
    // ==========================================
    subTabs: [
        { id: 'dashboard', icon: 'fa-tachometer-alt', label: 'الملخص' },
        { id: 'tasks', icon: 'fa-tasks', label: 'المهام' },
        { id: 'approvals', icon: 'fa-check-double', label: 'الاعتمادات' },
        { id: 'messages', icon: 'fa-comments', label: 'المراسلات' },
        { id: 'reports', icon: 'fa-chart-pie', label: 'التقارير' }
    ],
    
    renderSubTabs: function() {
        const container = document.getElementById('campaign-subtabs');
        if (!container) return;
        
        let html = '<div class="subtabs-nav">';
        this.subTabs.forEach(tab => {
            const isActive = tab.id === this.currentSubTab ? 'active' : '';
            html += `
                <button class="subtab-btn ${isActive}" onclick="CampaignManager.switchSubTab('${tab.id}')">
                    <i class="fas ${tab.icon}"></i>
                    <span>${tab.label}</span>
                    ${tab.id === 'approvals' ? '<span class="badge" id="approvals-badge" style="display:none;">0</span>' : ''}
                    ${tab.id === 'messages' ? '<span class="badge" id="messages-badge" style="display:none;">0</span>' : ''}
                </button>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    },
    
    switchSubTab: function(tabId) {
        this.currentSubTab = tabId;
        
        // Update active state
        document.querySelectorAll('.subtab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.onclick.toString().includes(tabId)) {
                btn.classList.add('active');
            }
        });
        
        // Load content
        const contentContainer = document.getElementById('campaign-content');
        switch(tabId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'tasks':
                this.loadTasksView();
                break;
            case 'approvals':
                this.loadApprovalsView();
                break;
            case 'messages':
                this.loadMessagesView();
                break;
            case 'reports':
                this.loadReportsView();
                break;
        }
    },
    
    // ==========================================
    // Dashboard - الملخص
    // ==========================================
    loadDashboard: function() {
        const container = document.getElementById('campaign-content');
        if (!container) return;
        
        container.innerHTML = `
            <div class="dashboard-grid">
                <!-- إحصائيات سريعة -->
                <div class="stats-row">
                    <div class="stat-card stat-total">
                        <div class="stat-icon"><i class="fas fa-clipboard-list"></i></div>
                        <div class="stat-info">
                            <span class="stat-number" id="total-tasks">0</span>
                            <span class="stat-label">إجمالي المهام</span>
                        </div>
                    </div>
                    <div class="stat-card stat-progress">
                        <div class="stat-icon"><i class="fas fa-spinner"></i></div>
                        <div class="stat-info">
                            <span class="stat-number" id="in-progress-tasks">0</span>
                            <span class="stat-label">قيد التنفيذ</span>
                        </div>
                    </div>
                    <div class="stat-card stat-review">
                        <div class="stat-icon"><i class="fas fa-eye"></i></div>
                        <div class="stat-info">
                            <span class="stat-number" id="review-tasks">0</span>
                            <span class="stat-label">للمراجعة</span>
                        </div>
                    </div>
                    <div class="stat-card stat-done">
                        <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                        <div class="stat-info">
                            <span class="stat-number" id="completed-tasks">0</span>
                            <span class="stat-label">مكتملة</span>
                        </div>
                    </div>
                </div>
                
                <!-- التقدم الإجمالي -->
                <div class="progress-section">
                    <h3><i class="fas fa-chart-line"></i> تقدم الحملة</h3>
                    <div class="progress-bar-container">
                        <div class="progress-bar" id="overall-progress" style="width: 0%"></div>
                    </div>
                    <span class="progress-text" id="progress-text">0%</span>
                </div>
                
                <!-- الإجراءات العاجلة -->
                <div class="urgent-actions">
                    <h3><i class="fas fa-exclamation-triangle"></i> تحتاج اهتمامك</h3>
                    <div id="urgent-items">
                        <p class="empty-state">لا توجد إجراءات عاجلة</p>
                    </div>
                </div>
                
                <!-- آخر النشاطات -->
                <div class="recent-activity">
                    <h3><i class="fas fa-history"></i> آخر النشاطات</h3>
                    <div id="activity-feed">
                        <p class="empty-state">لا توجد نشاطات حديثة</p>
                    </div>
                </div>
            </div>
        `;
        
        this.updateDashboardStats();
    },
    
    updateDashboardStats: function() {
        const total = this.tasks.length;
        const inProgress = this.tasks.filter(t => t.status === 'in_progress').length;
        const review = this.tasks.filter(t => t.status === 'in_review').length;
        const completed = this.tasks.filter(t => t.status === 'completed').length;
        
        document.getElementById('total-tasks').textContent = total;
        document.getElementById('in-progress-tasks').textContent = inProgress;
        document.getElementById('review-tasks').textContent = review;
        document.getElementById('completed-tasks').textContent = completed;
        
        const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
        document.getElementById('overall-progress').style.width = progress + '%';
        document.getElementById('progress-text').textContent = progress + '%';
    },
    
    // ==========================================
    // Tasks - نظام المهام (Kanban)
    // ==========================================
    taskStatuses: [
        { id: 'backlog', label: 'قائمة الانتظار', color: '#64748b' },
        { id: 'in_progress', label: 'قيد التنفيذ', color: '#f59e0b' },
        { id: 'in_review', label: 'للمراجعة', color: '#8b5cf6' },
        { id: 'approved', label: 'معتمد', color: '#10b981' },
        { id: 'completed', label: 'مكتمل', color: '#22c55e' }
    ],
    
    loadTasksView: function() {
        const container = document.getElementById('campaign-content');
        if (!container) return;
        
        let kanbanHTML = `
            <div class="tasks-header">
                <div class="tasks-filters">
                    <select id="phase-filter" onchange="CampaignManager.filterTasks()">
                        <option value="all">كل المراحل</option>
                        <option value="planning">التخطيط</option>
                        <option value="pre_launch">ما قبل الإطلاق</option>
                        <option value="launch">الإطلاق</option>
                        <option value="post_launch">ما بعد الإطلاق</option>
                    </select>
                    <select id="assignee-filter" onchange="CampaignManager.filterTasks()">
                        <option value="all">كل الأعضاء</option>
                    </select>
                </div>
                <div class="tasks-actions">
                    <button class="btn-ai" onclick="CampaignManager.showAIAssistant()">
                        <i class="fas fa-robot"></i> مساعد AI
                    </button>
                    <button class="btn-add" onclick="CampaignManager.showAddTaskModal()">
                        <i class="fas fa-plus"></i> إضافة مهمة
                    </button>
                </div>
            </div>
            
            <div class="kanban-board" id="kanban-board">
        `;
        
        this.taskStatuses.forEach(status => {
            const tasksInStatus = this.tasks.filter(t => t.status === status.id);
            kanbanHTML += `
                <div class="kanban-column" data-status="${status.id}">
                    <div class="column-header" style="border-top-color: ${status.color}">
                        <span class="column-title">${status.label}</span>
                        <span class="column-count">${tasksInStatus.length}</span>
                    </div>
                    <div class="column-tasks" id="column-${status.id}" 
                         ondrop="CampaignManager.dropTask(event, '${status.id}')"
                         ondragover="CampaignManager.allowDrop(event)">
                        ${this.renderTaskCards(tasksInStatus)}
                        ${status.id === 'backlog' ? '<button class="add-task-inline" onclick="CampaignManager.showAddTaskModal()"><i class="fas fa-plus"></i> إضافة مهمة</button>' : ''}
                    </div>
                </div>
            `;
        });
        
        kanbanHTML += '</div>';
        container.innerHTML = kanbanHTML;
    },
    
    renderTaskCards: function(tasks) {
        if (tasks.length === 0) return '';
        
        return tasks.map(task => `
            <div class="task-card" draggable="true" 
                 ondragstart="CampaignManager.dragTask(event, '${task.id}')"
                 onclick="CampaignManager.showTaskDetail('${task.id}')">
                <div class="task-priority priority-${task.priority || 'medium'}"></div>
                <h4 class="task-title">${task.title}</h4>
                <p class="task-desc">${(task.description || '').substring(0, 60)}${task.description && task.description.length > 60 ? '...' : ''}</p>
                <div class="task-meta">
                    <span class="task-phase">${this.getPhaseLabel(task.phase)}</span>
                    ${task.dueDate ? `<span class="task-due"><i class="fas fa-calendar"></i> ${this.formatDate(task.dueDate)}</span>` : ''}
                </div>
                <div class="task-footer">
                    ${task.assignedTo ? `<img class="task-avatar" src="${task.assignedTo.avatar || '/static/images/default-avatar.png'}" title="${task.assignedTo.name}">` : ''}
                    <div class="task-stats">
                        ${task.commentsCount ? `<span><i class="fas fa-comment"></i> ${task.commentsCount}</span>` : ''}
                        ${task.attachmentsCount ? `<span><i class="fas fa-paperclip"></i> ${task.attachmentsCount}</span>` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    },
    
    // Drag & Drop
    dragTask: function(event, taskId) {
        event.dataTransfer.setData('taskId', taskId);
    },
    
    allowDrop: function(event) {
        event.preventDefault();
        event.currentTarget.classList.add('drag-over');
    },
    
    dropTask: function(event, newStatus) {
        event.preventDefault();
        event.currentTarget.classList.remove('drag-over');
        
        const taskId = event.dataTransfer.getData('taskId');
        this.updateTaskStatus(taskId, newStatus);
    },
    
    updateTaskStatus: function(taskId, newStatus) {
        const taskIndex = this.tasks.findIndex(t => t.id === taskId);
        if (taskIndex === -1) return;
        
        const oldStatus = this.tasks[taskIndex].status;
        this.tasks[taskIndex].status = newStatus;
        
        // Update Firebase
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('tasks').doc(taskId)
            .update({ 
                status: newStatus,
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            })
            .then(() => {
                this.loadTasksView();
                this.addActivityLog('task_status_changed', {
                    taskId, oldStatus, newStatus
                });
                
                // إذا انتقل للمراجعة، أنشئ طلب اعتماد
                if (newStatus === 'in_review') {
                    this.createApprovalRequest(taskId);
                }
            })
            .catch(err => console.error('Error updating task:', err));
    },
    
    // ==========================================
    // Add Task Modal
    // ==========================================
    showAddTaskModal: function() {
        const modal = document.getElementById('add-task-modal');
        if (!modal) {
            this.createAddTaskModal();
        }
        document.getElementById('add-task-modal').style.display = 'flex';
    },
    
    createAddTaskModal: function() {
        const modalHTML = `
            <div id="add-task-modal" class="modal-overlay" style="display:none;">
                <div class="modal-content task-modal">
                    <div class="modal-header">
                        <h3><i class="fas fa-plus-circle"></i> إضافة مهمة جديدة</h3>
                        <button onclick="CampaignManager.closeModal('add-task-modal')" class="modal-close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- AI Assistant -->
                        <div class="ai-assistant-box" id="ai-task-assistant">
                            <div class="ai-header">
                                <i class="fas fa-robot"></i>
                                <span>مساعد AI - اكتب وصفاً قصيراً وسأساعدك</span>
                            </div>
                            <div class="ai-input">
                                <input type="text" id="ai-prompt" placeholder="مثال: أريد مهمة لتصميم البيان الصحفي...">
                                <button onclick="CampaignManager.generateTaskWithAI()">
                                    <i class="fas fa-magic"></i>
                                </button>
                            </div>
                            <div id="ai-suggestions" class="ai-suggestions"></div>
                        </div>
                        
                        <form id="add-task-form">
                            <div class="form-group">
                                <label>عنوان المهمة *</label>
                                <input type="text" id="task-title" required placeholder="عنوان واضح ومختصر">
                            </div>
                            <div class="form-group">
                                <label>الوصف</label>
                                <textarea id="task-description" rows="3" placeholder="تفاصيل المهمة..."></textarea>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>المرحلة</label>
                                    <select id="task-phase">
                                        <option value="planning">التخطيط</option>
                                        <option value="pre_launch">ما قبل الإطلاق</option>
                                        <option value="launch">الإطلاق</option>
                                        <option value="post_launch">ما بعد الإطلاق</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>الأولوية</label>
                                    <select id="task-priority">
                                        <option value="low">منخفضة</option>
                                        <option value="medium" selected>متوسطة</option>
                                        <option value="high">عالية</option>
                                        <option value="urgent">عاجلة</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>تاريخ البدء</label>
                                    <input type="date" id="task-start-date">
                                </div>
                                <div class="form-group">
                                    <label>تاريخ الاستحقاق</label>
                                    <input type="date" id="task-due-date">
                                </div>
                            </div>
                            <div class="form-group">
                                <label>المسؤول</label>
                                <select id="task-assignee">
                                    <option value="">غير محدد</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>تتطلب اعتماد؟</label>
                                <label class="switch">
                                    <input type="checkbox" id="task-requires-approval">
                                    <span class="slider"></span>
                                </label>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" onclick="CampaignManager.closeModal('add-task-modal')" class="btn-cancel">إلغاء</button>
                        <button type="button" onclick="CampaignManager.saveTask()" class="btn-save">
                            <i class="fas fa-save"></i> حفظ المهمة
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    },
    
    saveTask: function() {
        const title = document.getElementById('task-title').value.trim();
        if (!title) {
            alert('يرجى إدخال عنوان المهمة');
            return;
        }
        
        const task = {
            title: title,
            description: document.getElementById('task-description').value.trim(),
            phase: document.getElementById('task-phase').value,
            priority: document.getElementById('task-priority').value,
            startDate: document.getElementById('task-start-date').value || null,
            dueDate: document.getElementById('task-due-date').value || null,
            assigneeId: document.getElementById('task-assignee').value || null,
            requiresApproval: document.getElementById('task-requires-approval').checked,
            status: 'backlog',
            createdBy: this.currentUser?.uid || null,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        };
        
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('tasks').add(task)
            .then(docRef => {
                task.id = docRef.id;
                this.tasks.push(task);
                this.closeModal('add-task-modal');
                this.loadTasksView();
                this.addActivityLog('task_created', { taskId: docRef.id, title });
                this.showNotification('تم إضافة المهمة بنجاح', 'success');
            })
            .catch(err => {
                console.error('Error adding task:', err);
                this.showNotification('حدث خطأ في إضافة المهمة', 'error');
            });
    },
    
    // ==========================================
    // AI Assistant
    // ==========================================
    
    showAIAssistant: function() {
        const modal = document.getElementById('ai-assistant-modal');
        if (!modal) {
            this.createAIAssistantModal();
        }
        document.getElementById('ai-assistant-modal').style.display = 'flex';
    },
    
    createAIAssistantModal: function() {
        const modalHTML = `
            <div id="ai-assistant-modal" class="modal-overlay" style="display:none;">
                <div class="modal-content" style="max-width: 750px;">
                    <div class="modal-header" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 16px 16px 0 0; padding: 25px;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-robot" style="font-size: 24px; color: #fff;"></i>
                            </div>
                            <div>
                                <h3 style="margin: 0; color: #fff; font-size: 1.3rem;">مساعد AI - مشروع أليك</h3>
                                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.85rem;">مُدرَّب على خطة الاتصال والعلاقات العامة الكاملة</p>
                            </div>
                        </div>
                        <button onclick="CampaignManager.closeModal('ai-assistant-modal')" class="modal-close" style="color: #fff;">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body" style="padding: 25px;">
                        <!-- Chat Area -->
                        <div id="ai-chat-area" style="height: 320px; overflow-y: auto; background: rgba(0,0,0,0.2); border-radius: 12px; padding: 15px; margin-bottom: 15px;">
                            <div class="ai-message bot" style="display: flex; gap: 10px; margin-bottom: 15px;">
                                <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                    <i class="fas fa-robot" style="color: #fff; font-size: 14px;"></i>
                                </div>
                                <div style="background: rgba(139, 92, 246, 0.2); padding: 12px 15px; border-radius: 12px; border-top-right-radius: 4px; max-width: 80%;">
                                    <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem; line-height: 1.6;">
                                        مرحباً! 👋 أنا مساعد حملة <strong>مدينة أليك اللوجستية والصناعية</strong>
                                        <br><br>
                                        أعرف كل تفاصيل المشروع <strong>وخطة الاتصال والعلاقات العامة</strong>:
                                        <br><br>
                                        🎯 <strong>الأهداف الاتصالية</strong> و SWOT<br>
                                        📋 <strong>خطة العلاقات العامة</strong> والجدول الزمني<br>
                                        💬 <strong>الرسائل حسب الشريحة</strong><br>
                                        ⚠️ <strong>المحاذير الاتصالية</strong> (Red Lines)<br>
                                        🏆 <strong>قصص النجاح</strong> والشراكات
                                        <br><br>
                                        🎯 <strong>الهدف:</strong> بناء الوعي قبل إطلاق Q1 2026
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Quick Actions - Row 1: الأهداف والاستراتيجية -->
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px;">
                            <button onclick="CampaignManager.askAI('ما هي الأهداف الاتصالية؟')" style="background: rgba(220, 31, 39, 0.2); border: 1px solid rgba(220, 31, 39, 0.3); color: #ff6b6b; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                🎯 الأهداف
                            </button>
                            <button onclick="CampaignManager.askAI('تحليل SWOT')" style="background: rgba(220, 31, 39, 0.2); border: 1px solid rgba(220, 31, 39, 0.3); color: #ff6b6b; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📊 SWOT
                            </button>
                            <button onclick="CampaignManager.askAI('خطة الاتصال والعلاقات العامة')" style="background: rgba(220, 31, 39, 0.2); border: 1px solid rgba(220, 31, 39, 0.3); color: #ff6b6b; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📋 خطة PR
                            </button>
                            <button onclick="CampaignManager.askAI('الجدول الزمني للحملة')" style="background: rgba(220, 31, 39, 0.2); border: 1px solid rgba(220, 31, 39, 0.3); color: #ff6b6b; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📅 الجدول
                            </button>
                        </div>
                        
                        <!-- Quick Actions - Row 2: المشروع والمعلومات -->
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px;">
                            <button onclick="CampaignManager.askAI('ما هو مشروع أليك؟')" style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                🏭 المشروع
                            </button>
                            <button onclick="CampaignManager.askAI('من الجمهور المستهدف؟')" style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                👥 الجمهور
                            </button>
                            <button onclick="CampaignManager.askAI('الرسائل حسب الشريحة')" style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                💬 الرسائل
                            </button>
                            <button onclick="CampaignManager.askAI('من المنافسون؟')" style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                🏆 المنافسون
                            </button>
                        </div>
                        
                        <!-- Quick Actions - Row 3: المحتوى والمحاذير -->
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px;">
                            <button onclick="CampaignManager.askAI('اكتب لي بيان صحفي')" style="background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.3); color: #c4b5fd; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📰 بيان صحفي
                            </button>
                            <button onclick="CampaignManager.askAI('أفكار محتوى للحملة')" style="background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.3); color: #c4b5fd; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                💡 محتوى
                            </button>
                            <button onclick="CampaignManager.askAI('ما المحاذير الاتصالية؟')" style="background: rgba(251, 191, 36, 0.2); border: 1px solid rgba(251, 191, 36, 0.3); color: #fcd34d; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                ⚠️ المحاذير
                            </button>
                            <button onclick="CampaignManager.askAI('قصص النجاح والشراكات')" style="background: rgba(251, 191, 36, 0.2); border: 1px solid rgba(251, 191, 36, 0.3); color: #fcd34d; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                🏆 الشراكات
                            </button>
                        </div>
                        
                        <!-- Quick Actions - Row 4: المنتجات والمهام -->
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px;">
                            <button onclick="CampaignManager.askAI('ما هي المنتجات الاتصالية؟')" style="background: rgba(236, 72, 153, 0.2); border: 1px solid rgba(236, 72, 153, 0.3); color: #f9a8d4; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📦 المنتجات الاتصالية
                            </button>
                            <button onclick="CampaignManager.askAI('أنشئ مهام من المنتجات')" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 100%); border: 2px solid rgba(16, 185, 129, 0.5); color: #6ee7b7; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem; font-weight: 700;">
                                ✨ أنشئ المهام تلقائياً
                            </button>
                            <button onclick="CampaignManager.askAI('ما هي المقارنات المعيارية؟')" style="background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.3); color: #93c5fd; padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.75rem;">
                                📊 المقارنات المعيارية
                            </button>
                        </div>
                        
                        <!-- Input Area -->
                        <div style="display: flex; gap: 10px;">
                            <input type="text" id="ai-chat-input" placeholder="اسألني عن الأهداف، خطة PR، SWOT، المحاذير..." 
                                style="flex: 1; padding: 15px; background: rgba(0,0,0,0.3); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; color: #fff; font-size: 0.95rem;"
                                onkeypress="if(event.key==='Enter') CampaignManager.sendAIMessage()">
                            <button onclick="CampaignManager.sendAIMessage()" 
                                style="padding: 15px 25px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border: none; border-radius: 12px; color: #fff; cursor: pointer;">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    },
    
    sendAIMessage: function() {
        const input = document.getElementById('ai-chat-input');
        const message = input.value.trim();
        if (!message) return;
        
        this.askAI(message);
        input.value = '';
    },
    
    askAI: function(question) {
        const chatArea = document.getElementById('ai-chat-area');
        
        // إضافة رسالة المستخدم
        chatArea.innerHTML += `
            <div class="ai-message user" style="display: flex; gap: 10px; margin-bottom: 15px; flex-direction: row-reverse;">
                <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <i class="fas fa-user" style="color: #fff; font-size: 14px;"></i>
                </div>
                <div style="background: rgba(16, 185, 129, 0.2); padding: 12px 15px; border-radius: 12px; border-top-left-radius: 4px; max-width: 80%;">
                    <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem;">${question}</p>
                </div>
            </div>
        `;
        
        // إضافة مؤشر التحميل
        chatArea.innerHTML += `
            <div id="ai-typing" class="ai-message bot" style="display: flex; gap: 10px; margin-bottom: 15px;">
                <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <i class="fas fa-robot" style="color: #fff; font-size: 14px;"></i>
                </div>
                <div style="background: rgba(139, 92, 246, 0.2); padding: 12px 15px; border-radius: 12px;">
                    <i class="fas fa-circle" style="color: #8b5cf6; font-size: 8px; animation: pulse 1s infinite;"></i>
                    <i class="fas fa-circle" style="color: #8b5cf6; font-size: 8px; animation: pulse 1s infinite 0.2s; margin: 0 3px;"></i>
                    <i class="fas fa-circle" style="color: #8b5cf6; font-size: 8px; animation: pulse 1s infinite 0.4s;"></i>
                </div>
            </div>
        `;
        
        chatArea.scrollTop = chatArea.scrollHeight;
        
        // محاكاة رد الـ AI
        setTimeout(() => {
            const response = this.getAIResponse(question);
            document.getElementById('ai-typing').remove();
            
            chatArea.innerHTML += `
                <div class="ai-message bot" style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                        <i class="fas fa-robot" style="color: #fff; font-size: 14px;"></i>
                    </div>
                    <div style="background: rgba(139, 92, 246, 0.2); padding: 12px 15px; border-radius: 12px; border-top-right-radius: 4px; max-width: 80%;">
                        <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem; line-height: 1.6; white-space: pre-line;">${response}</p>
                    </div>
                </div>
            `;
            chatArea.scrollTop = chatArea.scrollHeight;
        }, 1500);
    },
    
    getAIResponse: function(question) {
        const q = question.toLowerCase();
        const pk = this.projectKnowledge;
        const cp = pk.communicationPlan;
        
        // ==========================================
        // الأهداف الاستراتيجية الاتصالية (من تاب خطة الاتصال والعلاقات العامة)
        // ==========================================
        if (q.includes('أهداف') || q.includes('هدف') || q.includes('استراتيج') || (q.includes('اتصال') && !q.includes('قنوات'))) {
            return `🎯 **الأهداف الاستراتيجية الاتصالية لمشروع أليك:**
*(من قسم التوجه الاتصالي - تاب خطة الاتصال والعلاقات العامة)*

${cp.strategicObjectives.map(obj => `
**${obj.number}. ${obj.title}**
${obj.description}
📊 *مؤشر القياس:* ${obj.kpi}
`).join('\n')}

---
**الأهداف التشغيلية:**
• ${cp.operationalObjectives.primary}

**المستهدفات:**
${cp.operationalObjectives.targets.map((t, i) => `${i+1}. ${t}`).join('\n')}

**مؤشرات الأداء (KPIs):**
${cp.operationalObjectives.kpis.map(k => '📈 ' + k).join('\n')}

📅 **تاريخ الإطلاق المستهدف:** ${cp.timeline.launchDate}`;
        }
        
        // ==========================================
        // تحليل SWOT (جديد!)
        // ==========================================
        if (q.includes('swot') || q.includes('سووت') || q.includes('تحليل الموقف') || (q.includes('نقاط') && (q.includes('قوة') || q.includes('ضعف')))) {
            return `📊 **تحليل SWOT الاتصالي لمشروع أليك:**

💪 **نقاط القوة (Strengths):**
${cp.swot.strengths.map(s => '✅ ' + s).join('\n')}

⚠️ **نقاط الضعف (Weaknesses):**
${cp.swot.weaknesses.map(w => '⚡ ' + w).join('\n')}

🌟 **الفرص (Opportunities):**
${cp.swot.opportunities.map(o => '💡 ' + o).join('\n')}

🛡️ **التهديدات (Threats):**
${cp.swot.threats.map(t => '⚠️ ' + t).join('\n')}`;
        }
        
        // ==========================================
        // خطة الاتصال والعلاقات العامة (جديد!)
        // ==========================================
        if (q.includes('خطة') || q.includes('علاقات عامة') || q.includes('pr') || q.includes('خطة اتصال')) {
            return `📋 **خطة الاتصال والعلاقات العامة لأليك:**

**الأهداف الاستراتيجية:**
${cp.strategicObjectives.map(obj => `${obj.number}. ${obj.title}`).join('\n')}

**المراحل الزمنية:**
${cp.timeline.phases.map(p => `📌 **${p.name}** (${p.duration})
   ${p.activities}`).join('\n\n')}

**تاريخ الإطلاق:** ${cp.timeline.launchDate}
**فترة ما قبل الإطلاق:** ${cp.timeline.preLaunchPhase}

**القنوات الرئيسية:**
${pk.communicationStrategy.channels.filter(c => c.priority === 'أساسي').map(c => '• ' + c.name + ' - ' + c.reason).join('\n')}

📊 راجع تاب "خطة الاتصال والعلاقات العامة" للتفاصيل الكاملة.`;
        }
        
        // ==========================================
        // الرسائل حسب الشريحة (جديد!)
        // ==========================================
        if (q.includes('شريحة') || q.includes('شرائح') || q.includes('segment') || (q.includes('رسائل') && q.includes('مختلف'))) {
            const segments = cp.messagesBySegment;
            return `🎯 **الرسائل المخصصة لكل شريحة:**

**1. ${segments.logistics3PL.segment}:**
💬 "${segments.logistics3PL.mainMessage}"
📌 نقاط الإثبات:
${segments.logistics3PL.proofPoints.map(p => '   • ' + p).join('\n')}

**2. ${segments.ecommerce.segment}:**
💬 "${segments.ecommerce.mainMessage}"
📌 نقاط الإثبات:
${segments.ecommerce.proofPoints.map(p => '   • ' + p).join('\n')}

**3. ${segments.manufacturers.segment}:**
💬 "${segments.manufacturers.mainMessage}"
📌 نقاط الإثبات:
${segments.manufacturers.proofPoints.map(p => '   • ' + p).join('\n')}

💡 كل شريحة تحتاج رسالة مختلفة!`;
        }
        
        // ==========================================
        // المحاذير الاتصالية (Red Lines) - جديد!
        // ==========================================
        if (q.includes('محاذير') || q.includes('ممنوع') || q.includes('تجنب') || q.includes('red line') || q.includes('حذر')) {
            return `🚫 **المحاذير الاتصالية (Red Lines):**

${cp.redLines.map((r, i) => `${i+1}. ⚠️ ${r}`).join('\n')}

💡 **نصيحة مهمة:**
• أي معلومات عن الأسعار → موافقة الإدارة أولاً
• أي إعلان عن شراكة → بعد التوقيع الرسمي فقط
• المقارنات → ركز على مميزات أليك، لا على عيوب الآخرين`;
        }
        
        // ==========================================
        // قصص النجاح (جديد!)
        // ==========================================
        if (q.includes('قصص نجاح') || q.includes('شراكات') || q.includes('عملاء') || q.includes('case study')) {
            return `🏆 **قصص النجاح والشراكات الموقعة:**

${cp.successStories.map((s, i) => `**${i+1}. ${s.client}:**
   📖 ${s.story}`).join('\n\n')}

💡 **كيف تستخدم هذه القصص:**
• في البيانات الصحفية: اقتباسات من الشركاء
• في السوشيال ميديا: فيديوهات شهادات
• في العروض التقديمية: دليل على النجاح
• في المحتوى: دراسات حالة تفصيلية

⚠️ **ملاحظة:** تأكد من موافقة الشريك قبل نشر أي محتوى عنه.`;
        }
        
        // ==========================================
        // الجدول الزمني (جديد!)
        // ==========================================
        if (q.includes('جدول') || q.includes('timeline') || q.includes('توقيت') || q.includes('متى نبدأ')) {
            return `📅 **الجدول الزمني لخطة الاتصال:**

**تاريخ الإطلاق المستهدف:** ${cp.timeline.launchDate}
**فترة التحضير:** ${cp.timeline.preLaunchPhase}

**المراحل التفصيلية:**

${cp.timeline.phases.map((p, i) => `**المرحلة ${i+1}: ${p.name}**
⏰ المدة: ${p.duration}
📋 الأنشطة: ${p.activities}`).join('\n\n')}

**مراحل تطوير المشروع:**
${pk.phases.map((p, i) => `${i+1}. ${p.name} (${p.status}) - ${p.dates}`).join('\n')}`;
        }
        
        // ==========================================
        // معلومات المشروع الأساسية
        // ==========================================
        if (q.includes('المشروع') && (q.includes('ما هو') || q.includes('عن') || q.includes('معلومات') || q.includes('وصف'))) {
            return `🏭 **مشروع أليك اللوجستية والصناعية**

**الموقع:** ${pk.basicInfo.location}
📍 ${pk.basicInfo.address}

**المساحة الإجمالية:** ${pk.basicInfo.totalArea}
**المساحة القابلة للتأجير:** ${pk.basicInfo.leasableArea}
**إجمالي الاستثمار:** ${pk.basicInfo.totalInvestment}

**الرؤية:** ${pk.vision}

**الرسالة:** ${pk.mission}

🎯 يستهدف المشروع قطاعات:
${pk.targetSectors.map(s => '• ' + s).join('\n')}`;
        }
        
        // ==========================================
        // المميزات التنافسية
        // ==========================================
        if (q.includes('مميز') || q.includes('تنافس') || q.includes('لماذا') || q.includes('أفضل')) {
            return `⭐ **المميزات التنافسية لمشروع أليك:**

${pk.competitiveAdvantages.map((a, i) => `${i+1}. ${a}`).join('\n')}

💡 **نقطة البيع الفريدة (USP):**
أقرب مدينة لوجستية لمطار الملكة علياء الدولي - 15 كم فقط!

🎯 **الرسالة الرئيسية:**
"${pk.communicationStrategy.mainMessage}"`;
        }
        
        // ==========================================
        // المنافسون
        // ==========================================
        // المقارنات المعيارية (Benchmarks)
        // ==========================================
        if (q.includes('مقارنات معيارية') || q.includes('benchmark') || q.includes('نماذج عالمية') || q.includes('دراسة مرجعية')) {
            const bm = pk.benchmarks;
            return `📊 **دراسة المقارنات المعيارية لمشروع أليك:**

**نطاق الدراسة:**
• عدد الكيانات: ${bm.scope.totalEntities} كيان
• عدد الدول: ${bm.scope.totalCountries} دول
• النماذج المدروسة: ${bm.scope.modelTypes} نماذج (عالمي، خليجي، إقليمي، محلي)

**أهداف الدراسة:**
${bm.studyObjectives.map((obj, i) => `${i+1}. ${obj}`).join('\n')}

**الكيانات العالمية:**
${bm.entities.global.map(e => `• **${e.name}** (${e.country}): ${e.strategy}`).join('\n')}

**النماذج الخليجية:**
${bm.entities.gulf.map(e => `• **${e.name}** (${e.country}): ${e.strategy}`).join('\n')}

💡 **الخلاصة الاستراتيجية:**
${bm.strategicConclusion}

🔍 اسألني عن أي نموذج بالتحديد (Prologis, GLP, DIC, KEZAD, إلخ)`;
        }
        
        // ==========================================
        // نموذج Prologis
        // ==========================================
        if (q.includes('prologis') || q.includes('برولوجيس')) {
            const prologis = pk.benchmarks.entities.global.find(e => e.name === 'Prologis');
            const insight = pk.benchmarks.modelInsights.global;
            return `🏢 **نموذج Prologis - الرائد العالمي:**

**المعلومات الأساسية:**
• الدولة: ${prologis.country}
• الاستراتيجية: ${prologis.strategy}

**الرؤى المستفادة:**
${insight.insights.map(i => '• ' + i).join('\n')}

**التوصيات لمشروع أليك:**
${insight.recommendations.map(r => '• ' + r).join('\n')}

💡 Prologis يركز على التكامل التقني وخدمات القيمة المضافة - وهذا ما يجب أن نطبقه في أليك!`;
        }
        
        // ==========================================
        // نموذج GLP
        // ==========================================
        if (q.includes('glp') || q.includes('جي ال بي')) {
            const glp = pk.benchmarks.entities.global.find(e => e.name === 'GLP');
            return `🏢 **نموذج GLP - العملاق الآسيوي:**

**المعلومات الأساسية:**
• الدولة: ${glp.country}
• الاستراتيجية: ${glp.strategy}

**ما يميز GLP:**
• نموذج Fund Management (إدارة الصناديق)
• تطوير مستدام مع تركيز على ESG
• مرونة عالية في التصميم والتنفيذ
• شراكات استراتيجية طويلة الأمد

**الدروس لأليك:**
1. تبني نموذج الشراكة بدلاً من البيع المباشر فقط
2. التركيز على الاستدامة كميزة تنافسية
3. بناء علاقات طويلة الأمد مع المستثمرين`;
        }
        
        // ==========================================
        // النموذج الخليجي (DIC, KEZAD, KAEC)
        // ==========================================
        if (q.includes('dic') || q.includes('دبي للاستثمار') || q.includes('kezad') || q.includes('كيزاد') || q.includes('kaec') || q.includes('مدينة الملك عبدالله') || q.includes('نموذج خليجي')) {
            const gulf = pk.benchmarks.entities.gulf;
            const gulfInsight = pk.benchmarks.modelInsights.gulf;
            return `🌴 **النماذج الخليجية:**

${gulf.map(e => `**${e.name}** (${e.country}):
   📋 ${e.strategy}`).join('\n\n')}

**رؤى النموذج الخليجي:**
${gulfInsight.insights.map(i => '• ' + i).join('\n')}

**التوصيات لأليك من النموذج الخليجي:**
${gulfInsight.recommendations.map(r => '• ' + r).join('\n')}

💡 النماذج الخليجية تعتمد على الدعم الحكومي والحوافز - يجب أن نركز على الكفاءة التشغيلية كبديل!`;
        }
        
        // ==========================================
        // تحليل الفجوات (Gap Analysis)
        // ==========================================
        if (q.includes('فجوات') || q.includes('gap') || q.includes('تحليل الفجوة')) {
            const gaps = cp.gapAnalysis;
            return `🔍 **تحليل الفجوات الاتصالية لمشروع أليك:**

${gaps.map((gap, i) => `**${i+1}. ${gap.gap}**
   📍 الوضع الحالي: ${gap.currentState}
   ⭐ أفضل الممارسات: ${gap.bestPractice}`).join('\n\n')}

**الأولويات المقترحة:**
1. 🚨 عاجل: بناء الوعي بالعلامة التجارية
2. ⚠️ مهم: إنتاج محتوى بصري احترافي
3. 📋 متوسط: تطوير رسائل تمايز واضحة

💡 سد هذه الفجوات سيضع أليك في موقع تنافسي قوي!`;
        }
        
        // ==========================================
        // مصفوفة الجمهور المستهدف (Target Audience Matrix)
        // ==========================================
        if (q.includes('مصفوفة') || q.includes('شرائح') || q.includes('matrix') || q.includes('جمهور رئيسي') || q.includes('جمهور ثانوي')) {
            const primary = pk.targetAudienceMatrix.primary;
            const secondary = pk.targetAudienceMatrix.secondary;
            return `👥 **مصفوفة الجمهور المستهدف لمشروع أليك:**

**📌 الجمهور الرئيسي:**
${primary.map((p, i) => `
**${i+1}. ${p.segment}:**
   🎯 ما يريدون: ${p.wants}
   💼 ما نريده منهم: ${p.weWant}
   💬 الرسالة: ${p.message}
   📱 القنوات: ${p.channels}
   🎨 النبرة: ${p.tone}`).join('\n')}

**📎 الجمهور الثانوي:**
${secondary.map(s => `• ${s.segment}: ${s.role}`).join('\n')}

💡 ركز جهودك على الجمهور الرئيسي أولاً!`;
        }
        
        // ==========================================
        // رؤى النماذج المختلفة
        // ==========================================
        if (q.includes('رؤى') || q.includes('insights') || q.includes('دروس مستفادة')) {
            const models = pk.benchmarks.modelInsights;
            return `💡 **الرؤى والدروس المستفادة من النماذج الأربعة:**

**🌍 النموذج العالمي (Prologis, GLP):**
${models.global.recommendations.map(r => '• ' + r).join('\n')}

**🌴 النموذج الخليجي (DIC, KEZAD, KAEC):**
${models.gulf.recommendations.map(r => '• ' + r).join('\n')}

**🌐 النموذج الإقليمي (Tanger Med, Orascom):**
${models.regional.recommendations.map(r => '• ' + r).join('\n')}

**🏠 النموذج المحلي (Agility, وادي سحاب):**
${models.local.recommendations.map(r => '• ' + r).join('\n')}

**الخلاصة لأليك:**
${pk.benchmarks.strategicConclusion}`;
        }
        
        // ==========================================
        // المنافسون والمقارنات
        // ==========================================
        if (q.includes('منافس') || q.includes('سوق') || q.includes('مقارن')) {
            return `🏆 **تحليل المنافسين لمشروع أليك:**

**المنافسون المحليون:**
${pk.competitors.local}

**المنافسون الإقليميون:**
${pk.competitors.regional}

**المنافسون العالميون:**
${pk.competitors.global}

💡 **نقاط التفوق على المنافسين:**
1. موقع استراتيجي قرب المطار الدولي
2. أسعار تأجير تنافسية (5-15 دينار/م² شهرياً)
3. خدمات متكاملة في موقع واحد
4. بنية تحتية حديثة بمعايير عالمية

📊 راجع تاب "المقارنات المعيارية" للتحليل التفصيلي.`;
        }
        
        // ==========================================
        // الجمهور المستهدف
        // ==========================================
        if (q.includes('جمهور') || q.includes('عميل') || q.includes('مستهدف') || q.includes('من نستهدف')) {
            const primary = pk.targetAudienceMatrix.primary;
            const secondary = pk.targetAudienceMatrix.secondary;
            return `👥 **الجمهور المستهدف لمشروع أليك:**

**📌 الشرائح الرئيسية (3 شرائح):**
${primary.map((p, i) => `**${i+1}. ${p.segment}:**
   🎯 ما يريدون: ${p.wants}
   💬 الرسالة المناسبة: ${p.message}
   📱 القنوات: ${p.channels}`).join('\n\n')}

**📎 الجمهور الثانوي:**
${secondary.map(s => `• ${s.segment}: ${s.role}`).join('\n')}

**التحديات التي يواجهها جمهورنا:**
${pk.targetAudience.challenges.map(c => '• ' + c).join('\n')}

💡 **نصيحة:** خصص رسالتك لكل شريحة - فالمستثمر يهتم بالعائد، والشركة الصناعية تهتم بالتكلفة والموقع!

🔍 اسألني "مصفوفة الجمهور" للتفاصيل الكاملة.`;
        }
        
        // ==========================================
        // مراحل المشروع
        // ==========================================
        if (q.includes('مرحل') || q.includes('جدول') || q.includes('تاريخ') || q.includes('متى') || q.includes('timeline')) {
            return `📅 **مراحل تطوير مشروع أليك:**

${pk.phases.map((p, i) => `**المرحلة ${i+1}: ${p.name}**
   📊 الحالة: ${p.status}
   ⏳ التقدم: ${p.progress}%
   📆 الفترة: ${p.dates}`).join('\n\n')}

**تاريخ الإطلاق:** ${pk.basicInfo.startDate}
**الانتهاء المتوقع:** ${pk.basicInfo.expectedCompletion}`;
        }
        
        // ==========================================
        // قنوات التواصل - مُخصصة لأليك
        // ==========================================
        if (q.includes('قنوات') || q.includes('تواصل') || q.includes('منصات') || q.includes('سوشيال')) {
            return `📱 **قنوات التواصل المُوصى بها لمشروع أليك:**

${pk.communicationStrategy.channels.map(c => `**${c.name}** (${c.priority})
   📝 السبب: ${c.reason}`).join('\n\n')}

💡 **استراتيجية القنوات:**
• التركيز على LinkedIn للوصول لصناع القرار B2B
• المعارض المتخصصة للتواصل المباشر
• البريد الإلكتروني لقوائم الشركات المستهدفة

🎯 جمهورنا رجال أعمال، ركز على المنصات المهنية!`;
        }
        
        // ==========================================
        // البيان الصحفي - مُخصص لأليك
        // ==========================================
        if (q.includes('بيان') || q.includes('صحفي')) {
            return `📰 **نموذج بيان صحفي لمشروع أليك:**

**للنشر الفوري**
التاريخ: [أدخل التاريخ]

**نوبلز العقارية تطلق "أليك" - المدينة اللوجستية الأقرب لمطار الملكة علياء الدولي**

**عمّان، الأردن** - أعلنت شركة نوبلز العقارية، الرائدة في التطوير العقاري منذ 2008، عن إطلاق مشروعها الاستراتيجي "مدينة أليك اللوجستية والصناعية" في منطقة الموقر.

يقع المشروع على بُعد 15 كم فقط من مطار الملكة علياء الدولي، ويمتد على مساحة ${pk.basicInfo.totalArea}، ليشكل بوابة لوجستية إقليمية بمعايير عالمية.

**أبرز المميزات:**
• أقرب مدينة لوجستية للمطار الدولي
• مساحات مرنة من 500 إلى 50,000 م²
• خدمات جمركية ولوجستية متكاملة
• بنية تحتية بمواصفات عالمية

**تصريح:**
صرح [اسم المتحدث]، [المنصب] في نوبلز العقارية:
"${pk.communicationStrategy.mainMessage} - نهدف لتمكين الشركات من النمو والتوسع إقليمياً."

**للتواصل:**
📧 ${pk.contact.salesEmail}
📞 ${pk.contact.phone}

---
هل تريد تعديل أي جزء؟`;
        }
        
        // ==========================================
        // أفكار المحتوى - مخصصة لأليك
        // ==========================================
        if (q.includes('أفكار') || q.includes('محتوى') || q.includes('content')) {
            return `💡 **أفكار محتوى مُخصصة لمشروع أليك:**

${pk.contentPlan.types.map(t => `**${t.type}:**
   📝 ${t.description}
   📅 التكرار: ${t.frequency}`).join('\n\n')}

**أفكار إضافية للسوشيال ميديا:**

📹 **فيديو:**
• "15 كم تفصلك عن العالم" - فيديو الموقع الاستراتيجي
• جولة درون للموقع مع إظهار القرب من المطار
• مقابلة مع مدير المشروع

📊 **إنفوجرافيك:**
• مقارنة أسعار التخزين: أليك vs المنافسين
• خريطة الوصول للأسواق الإقليمية
• إحصائيات القطاع اللوجستي في الأردن

📝 **مقالات:**
• "لماذا الأردن مركز لوجستي إقليمي؟"
• "كيف تختار موقع مستودعك؟"
• "اتجاهات التجارة الإلكترونية في المنطقة"`;
        }
        
        // ==========================================
        // المهام والتخطيط - مخصصة لأليك
        // ==========================================
        if (q.includes('مهام') || q.includes('تحضير') || q.includes('تخطيط') || q.includes('خطة')) {
            return `📋 **المهام التحضيرية لحملة أليك:**

**المرحلة 1 - الإعداد (الشهر الأول):**
1. ✅ تحديد الرسائل الرئيسية للحملة
2. □ إعداد ملف المشروع التفصيلي (Fact Sheet)
3. □ تصميم الهوية البصرية للحملة
4. □ إنشاء قائمة الشركات المستهدفة

**المرحلة 2 - المحتوى (الشهر الثاني):**
5. □ كتابة البيان الصحفي للإطلاق
6. □ إنتاج الفيديو التعريفي
7. □ تصميم البروشور الرقمي
8. □ إعداد عرض تقديمي للمستثمرين

**المرحلة 3 - الإطلاق (الشهر الثالث):**
9. □ إطلاق صفحة المشروع على الموقع
10. □ حملة LinkedIn المستهدفة
11. □ التواصل مع الصحفيين الاقتصاديين
12. □ جدولة زيارات الموقع

**الجمهور المستهدف:**
${pk.targetAudience.primary.slice(0, 3).map(p => '• ' + p).join('\n')}

هل تريد إضافة أي من هذه المهام للكانبان؟`;
        }
        
        // ==========================================
        // الرسائل الرئيسية
        // ==========================================
        if (q.includes('رسال') || q.includes('message') || q.includes('ماذا نقول') || q.includes('slogan')) {
            return `💬 **الرسائل الرئيسية لمشروع أليك:**

🎯 **الرسالة الأساسية:**
"${pk.communicationStrategy.mainMessage}"

**الرسائل الداعمة:**
${pk.communicationStrategy.keyMessages.map((m, i) => `${i+1}. ${m}`).join('\n')}

**نبرة التواصل (Tone of Voice):**
• مهنية وموثوقة
• واضحة ومباشرة
• طموحة دون مبالغة

**كلمات مفتاحية للاستخدام:**
بوابة إقليمية، موقع استراتيجي، معايير عالمية، خدمات متكاملة، تنافسية، كفاءة تشغيلية

**كلمات يُفضل تجنبها:**
أرخص (بدلاً منها: الأكثر تنافسية)، الأفضل (بدلاً منها: الرائد)`;
        }
        
        // ==========================================
        // المرافق والخدمات
        // ==========================================
        if (q.includes('مرافق') || q.includes('خدمات') || q.includes('بنية') || q.includes('تجهيز')) {
            return `🏗️ **المرافق والخدمات في مشروع أليك:**

**البنية التحتية:**
${pk.facilities.map(f => '• ' + f).join('\n')}

**أنواع المساحات المتوفرة:**
• مستودعات: 500 - 10,000 م²
• مكاتب إدارية: 50 - 500 م²
• أراضي صناعية: 1,000 - 50,000 م²

**الأسعار التقريبية:**
• التأجير: 5-15 دينار/م² شهرياً

💡 هذه المعلومات مهمة لأي محتوى تسويقي تكتبه!`;
        }
        
        // ==========================================
        // معلومات التواصل
        // ==========================================
        if (q.includes('تواصل') && (q.includes('رقم') || q.includes('هاتف') || q.includes('إيميل') || q.includes('بريد'))) {
            return `📞 **معلومات التواصل:**

**شركة نوبلز العقارية**
${pk.contact.company}

📧 البريد العام: ${pk.contact.email}
📧 مبيعات أليك: ${pk.contact.salesEmail}
📞 الهاتف: ${pk.contact.phone}

🌐 الموقع: noblesproperties.com`;
        }
        
        // ==========================================
        // استراتيجية عامة
        // ==========================================
        if (q.includes('خطة تسويق')) {
            return `📊 **استراتيجية الاتصال لمشروع أليك:**

**الأهداف الاستراتيجية الاتصالية:**
${cp.strategicObjectives.map(obj => `${obj.number}. ${obj.title}`).join('\n')}

**الجمهور المستهدف:**
${pk.targetAudience.primary.slice(0, 3).map(p => '• ' + p).join('\n')}

**الرسالة الأساسية:**
"${pk.communicationStrategy.mainMessage}"

**القنوات الرئيسية:**
${pk.communicationStrategy.channels.filter(c => c.priority === 'أساسي').map(c => '• ' + c.name).join('\n')}

**مؤشرات القياس:**
${cp.strategicObjectives.map(obj => '• ' + obj.kpi).join('\n')}

📋 راجع تاب "خطة الاتصال والعلاقات العامة" للتفاصيل الكاملة.`;
        }
        
        // ==========================================
        // إنشاء المهام من المنتجات الاتصالية
        // ==========================================
        if (q.includes('أنشئ مهام') || q.includes('انشاء مهام') || q.includes('انشئ مهام') || q.includes('إنشاء مهام') || q.includes('create tasks') || q.includes('أضف المهام من المنتجات') || q.includes('مهام من المنتجات')) {
            // تشغيل إنشاء المهام
            this.createTasksFromProducts();
            
            const products = pk.campaignProducts;
            const phase1 = products.filter(p => p.phase === 1);
            const phase2 = products.filter(p => p.phase === 2);
            const phase3 = products.filter(p => p.phase === 3);
            
            return `✅ **جاري إنشاء المهام من المنتجات الاتصالية...**

📦 **المنتجات الاتصالية المتاحة:**

**المرحلة 1 - التهيئة والتشويق (${phase1.length} منتج):**
${phase1.map(p => `• ${p.title} (${p.date})`).join('\n')}

**المرحلة 2 - الإطلاق الاستراتيجي (${phase2.length} منتج):**
${phase2.map(p => `• ${p.title} (${p.date})`).join('\n')}

**المرحلة 3 - ترسيخ الريادة (${phase3.length} منتج):**
${phase3.map(p => `• ${p.title} (${p.date})`).join('\n')}

⏳ **الإجمالي:** ${products.length} مهمة سيتم إضافتها

🔄 يتم الآن حفظ المهام في Firebase...
انتقل إلى لوحة المهام لرؤية المهام الجديدة!`;
        }
        
        // ==========================================
        // عرض المنتجات الاتصالية
        // ==========================================
        if (q.includes('منتجات اتصالية') || q.includes('المنتجات الاتصالية') || q.includes('campaign products') || q.includes('ما هي المنتجات')) {
            const products = pk.campaignProducts;
            const phase1 = products.filter(p => p.phase === 1);
            const phase2 = products.filter(p => p.phase === 2);
            const phase3 = products.filter(p => p.phase === 3);
            
            return `📦 **المنتجات الاتصالية لحملة أليك:**

**📌 المرحلة 1: التهيئة والتشويق (5-12 يناير)**
${phase1.map(p => `• **${p.title}** - ${p.platform}
   📅 ${p.date} | 🎯 ${p.objective}`).join('\n')}

**🚀 المرحلة 2: الإطلاق الاستراتيجي (13-22 يناير)**
${phase2.map(p => `• **${p.title}** - ${p.platform}
   📅 ${p.date} | 🎯 ${p.objective}`).join('\n')}

**🏆 المرحلة 3: ترسيخ الريادة (23-31 يناير)**
${phase3.map(p => `• **${p.title}** - ${p.platform}
   📅 ${p.date} | 🎯 ${p.objective}`).join('\n')}

**📊 الإجمالي:** ${products.length} منتج اتصالي

💡 قل "أنشئ مهام من المنتجات" لتحويلها لمهام في لوحة الكانبان!`;
        }
        
        // ==========================================
        // الرد الافتراضي الذكي (محدّث!)
        // ==========================================
        return `👋 مرحباً! أنا مساعد حملة **مشروع أليك اللوجستية والصناعية**.

أعرف كل تفاصيل المشروع وخطة الاتصال والعلاقات العامة!

📍 **معلومات المشروع:**
• "ما هو مشروع أليك؟"
• "ما مميزات المشروع؟"
• "من الجمهور المستهدف؟"
• "من المنافسون؟"

🎯 **الأهداف والاستراتيجية:**
• "ما هي الأهداف الاتصالية؟"
• "خطة الاتصال والعلاقات العامة"
• "تحليل SWOT"
• "الجدول الزمني للحملة"

📝 **المحتوى والرسائل:**
• "اكتب لي بيان صحفي"
• "ما الرسائل الرئيسية؟"
• "الرسائل حسب الشريحة"
• "أفكار محتوى"

⚠️ **معلومات مهمة:**
• "ما المحاذير الاتصالية؟"
• "قصص النجاح والشراكات"

💡 **الهدف الاستراتيجي الأول:**
${cp.strategicObjectives[0].title}

جرب أحد الأسئلة أعلاه أو اسألني أي شيء عن أليك! 😊`;
    },
    
    generateTaskWithAI: function() {
        const prompt = document.getElementById('ai-prompt').value.trim();
        if (!prompt) return;
        
        const suggestionsDiv = document.getElementById('ai-suggestions');
        suggestionsDiv.innerHTML = '<div class="ai-loading"><i class="fas fa-spinner fa-spin"></i> جاري التفكير...</div>';
        
        // AI Suggestions based on prompt (محاكاة - يمكن ربطها بـ OpenAI API)
        const suggestions = this.getAISuggestions(prompt);
        
        setTimeout(() => {
            suggestionsDiv.innerHTML = suggestions.map(s => `
                <div class="ai-suggestion" onclick="CampaignManager.applyAISuggestion('${s.title}', '${s.description}')">
                    <strong>${s.title}</strong>
                    <p>${s.description}</p>
                </div>
            `).join('');
        }, 1000);
    },
    
    getAISuggestions: function(prompt) {
        // اقتراحات ذكية بناءً على الكلمات المفتاحية
        const suggestions = [];
        
        if (prompt.includes('بيان') || prompt.includes('صحفي')) {
            suggestions.push(
                { title: 'إعداد البيان الصحفي للإطلاق', description: 'كتابة بيان صحفي شامل يتضمن معلومات المشروع والرؤية' },
                { title: 'مراجعة البيان الصحفي', description: 'مراجعة لغوية وتحريرية للبيان قبل النشر' }
            );
        }
        if (prompt.includes('تصميم') || prompt.includes('هوية')) {
            suggestions.push(
                { title: 'تصميم الهوية البصرية', description: 'إنشاء الشعار والألوان والخطوط الخاصة بالحملة' },
                { title: 'تصميم قوالب السوشيال ميديا', description: 'تصميم قوالب جاهزة للنشر على منصات التواصل' }
            );
        }
        if (prompt.includes('إعلام') || prompt.includes('صحافة')) {
            suggestions.push(
                { title: 'إعداد قائمة وسائل الإعلام', description: 'تجميع قائمة بالصحفيين والمنصات الإعلامية المستهدفة' },
                { title: 'جدولة المقابلات الصحفية', description: 'تنسيق مواعيد المقابلات مع الصحفيين' }
            );
        }
        
        // إذا لم تجد اقتراحات محددة
        if (suggestions.length === 0) {
            suggestions.push(
                { title: prompt, description: 'مهمة جديدة بناءً على طلبك' }
            );
        }
        
        return suggestions;
    },
    
    applyAISuggestion: function(title, description) {
        document.getElementById('task-title').value = title;
        document.getElementById('task-description').value = description;
        document.getElementById('ai-suggestions').innerHTML = '';
        document.getElementById('ai-prompt').value = '';
    },
    
    // ==========================================
    // إنشاء المهام من المنتجات الاتصالية
    // ==========================================
    createTasksFromProducts: async function() {
        const products = this.projectKnowledge.campaignProducts;
        
        if (!products || products.length === 0) {
            this.showNotification('لا توجد منتجات اتصالية متاحة', 'error');
            return;
        }
        
        try {
            const batch = this.db.batch();
            const tasksRef = this.db.collection('projects').doc(this.currentProjectId).collection('tasks');
            let addedCount = 0;
            
            // تحويل المنتجات لمهام
            for (const product of products) {
                // تحقق من وجود المهمة مسبقاً
                const existingTask = this.tasks.find(t => t.productId === product.id);
                if (existingTask) {
                    console.log(`Task for product ${product.id} already exists, skipping...`);
                    continue;
                }
                
                const task = {
                    title: product.title,
                    description: `**المنتج الاتصالي:** ${product.title}\n\n**الهدف:** ${product.objective}\n\n**الجمهور:** ${product.audience}\n\n**الرسالة:** ${product.message}\n\n**المنصة:** ${product.platform}`,
                    phase: this.getPhaseFromNumber(product.phase),
                    priority: product.type === 'event' || product.type === 'press_release' ? 'critical' : 'high',
                    dueDate: product.date,
                    type: product.type,
                    platform: product.platform,
                    status: 'backlog',
                    productId: product.id,
                    phaseName: product.phaseName,
                    deliverables: product.deliverables || [],
                    budget: product.budget || null,
                    expectedReach: product.reach || null,
                    requiresApproval: product.type === 'press_release' || product.type === 'video' || product.type === 'event',
                    createdBy: this.currentUser?.uid || 'ai-assistant',
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
                    source: 'campaign_products'
                };
                
                const taskRef = tasksRef.doc();
                batch.set(taskRef, task);
                addedCount++;
            }
            
            if (addedCount > 0) {
                await batch.commit();
                
                // إضافة سجل النشاط
                this.addActivityLog('tasks_created_from_products', {
                    count: addedCount,
                    products: products.map(p => p.title)
                });
                
                // تحديث واجهة المستخدم
                await this.loadTasks();
                this.loadTasksView();
                
                this.showNotification(`✅ تم إنشاء ${addedCount} مهمة من المنتجات الاتصالية`, 'success');
            } else {
                this.showNotification('جميع المهام موجودة مسبقاً', 'info');
            }
            
        } catch (error) {
            console.error('Error creating tasks from products:', error);
            this.showNotification('حدث خطأ في إنشاء المهام', 'error');
        }
    },
    
    getPhaseFromNumber: function(phaseNum) {
        const phases = {
            1: 'pre_launch',
            2: 'launch',
            3: 'post_launch'
        };
        return phases[phaseNum] || 'planning';
    },
    
    // إنشاء مهمة واحدة من منتج محدد
    createTaskFromProduct: async function(productId) {
        const product = this.projectKnowledge.campaignProducts.find(p => p.id === productId);
        
        if (!product) {
            this.showNotification('المنتج غير موجود', 'error');
            return;
        }
        
        // تحقق من وجود المهمة مسبقاً
        const existingTask = this.tasks.find(t => t.productId === productId);
        if (existingTask) {
            this.showNotification('هذه المهمة موجودة مسبقاً', 'warning');
            return;
        }
        
        const task = {
            title: product.title,
            description: `**المنتج الاتصالي:** ${product.title}\n\n**الهدف:** ${product.objective}\n\n**الجمهور:** ${product.audience}\n\n**الرسالة:** ${product.message}\n\n**المنصة:** ${product.platform}`,
            phase: this.getPhaseFromNumber(product.phase),
            priority: product.type === 'event' || product.type === 'press_release' ? 'critical' : 'high',
            dueDate: product.date,
            type: product.type,
            platform: product.platform,
            status: 'backlog',
            productId: product.id,
            phaseName: product.phaseName,
            deliverables: product.deliverables || [],
            budget: product.budget || null,
            expectedReach: product.reach || null,
            requiresApproval: product.type === 'press_release' || product.type === 'video' || product.type === 'event',
            createdBy: this.currentUser?.uid || 'ai-assistant',
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
            source: 'campaign_products'
        };
        
        try {
            const docRef = await this.db.collection('projects').doc(this.currentProjectId)
                .collection('tasks').add(task);
            
            task.id = docRef.id;
            this.tasks.push(task);
            
            this.addActivityLog('task_created_from_product', {
                taskId: docRef.id,
                productId: product.id,
                title: product.title
            });
            
            this.loadTasksView();
            this.showNotification(`✅ تم إنشاء مهمة: ${product.title}`, 'success');
            
        } catch (error) {
            console.error('Error creating task:', error);
            this.showNotification('حدث خطأ في إنشاء المهمة', 'error');
        }
    },
    
    // ==========================================
    // Approvals - الاعتمادات
    // ==========================================
    loadApprovalsView: function() {
        const container = document.getElementById('campaign-content');
        if (!container) return;
        
        const pendingApprovals = this.approvals.filter(a => a.status === 'pending');
        const completedApprovals = this.approvals.filter(a => a.status !== 'pending');
        
        container.innerHTML = `
            <div class="approvals-view">
                <div class="approvals-section">
                    <h3><i class="fas fa-clock"></i> في انتظار الاعتماد (${pendingApprovals.length})</h3>
                    <div class="approvals-list" id="pending-approvals">
                        ${pendingApprovals.length ? this.renderApprovalCards(pendingApprovals) : '<p class="empty-state">لا توجد اعتمادات معلقة</p>'}
                    </div>
                </div>
                <div class="approvals-section completed">
                    <h3><i class="fas fa-history"></i> سجل الاعتمادات</h3>
                    <div class="approvals-list" id="completed-approvals">
                        ${completedApprovals.length ? this.renderApprovalCards(completedApprovals) : '<p class="empty-state">لا يوجد سجل</p>'}
                    </div>
                </div>
            </div>
        `;
    },
    
    renderApprovalCards: function(approvals) {
        return approvals.map(approval => `
            <div class="approval-card status-${approval.status}">
                <div class="approval-header">
                    <span class="approval-title">${approval.title}</span>
                    <span class="approval-status">${this.getApprovalStatusLabel(approval.status)}</span>
                </div>
                <p class="approval-desc">${approval.description || ''}</p>
                <div class="approval-meta">
                    <span><i class="fas fa-calendar"></i> ${this.formatDate(approval.createdAt)}</span>
                    ${approval.deadline ? `<span class="deadline"><i class="fas fa-hourglass-half"></i> موعد نهائي: ${this.formatDate(approval.deadline)}</span>` : ''}
                </div>
                ${approval.status === 'pending' && this.canApprove() ? `
                    <div class="approval-actions">
                        <button onclick="CampaignManager.approveItem('${approval.id}')" class="btn-approve">
                            <i class="fas fa-check"></i> اعتماد
                        </button>
                        <button onclick="CampaignManager.requestRevision('${approval.id}')" class="btn-revision">
                            <i class="fas fa-edit"></i> طلب تعديل
                        </button>
                        <button onclick="CampaignManager.rejectItem('${approval.id}')" class="btn-reject">
                            <i class="fas fa-times"></i> رفض
                        </button>
                    </div>
                ` : ''}
            </div>
        `).join('');
    },
    
    approveItem: function(approvalId) {
        this.updateApprovalStatus(approvalId, 'approved');
    },
    
    requestRevision: function(approvalId) {
        const feedback = prompt('أدخل ملاحظات التعديل المطلوبة:');
        if (feedback) {
            this.updateApprovalStatus(approvalId, 'revision_requested', feedback);
        }
    },
    
    rejectItem: function(approvalId) {
        const reason = prompt('أدخل سبب الرفض:');
        if (reason) {
            this.updateApprovalStatus(approvalId, 'rejected', reason);
        }
    },
    
    updateApprovalStatus: function(approvalId, status, feedback = '') {
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('approvals').doc(approvalId)
            .update({
                status: status,
                feedback: feedback,
                reviewedBy: this.currentUser?.uid,
                reviewedAt: firebase.firestore.FieldValue.serverTimestamp()
            })
            .then(() => {
                const index = this.approvals.findIndex(a => a.id === approvalId);
                if (index !== -1) {
                    this.approvals[index].status = status;
                }
                this.loadApprovalsView();
                this.showNotification('تم تحديث حالة الاعتماد', 'success');
            });
    },
    
    // ==========================================
    // Messages - المراسلات
    // ==========================================
    loadMessagesView: function() {
        const container = document.getElementById('campaign-content');
        if (!container) return;
        
        container.innerHTML = `
            <div class="messages-view">
                <div class="messages-sidebar">
                    <button class="btn-new-message" onclick="CampaignManager.showNewMessageModal()">
                        <i class="fas fa-plus"></i> رسالة جديدة
                    </button>
                    <div class="messages-list" id="messages-list">
                        ${this.messages.length ? this.renderMessagesList() : '<p class="empty-state">لا توجد رسائل</p>'}
                    </div>
                </div>
                <div class="message-detail" id="message-detail">
                    <div class="empty-state">
                        <i class="fas fa-envelope-open"></i>
                        <p>اختر رسالة لعرضها</p>
                    </div>
                </div>
            </div>
        `;
    },
    
    renderMessagesList: function() {
        return this.messages.map(msg => `
            <div class="message-item ${msg.isRead ? '' : 'unread'}" onclick="CampaignManager.showMessage('${msg.id}')">
                <div class="message-avatar">
                    <img src="${msg.from?.avatar || '/static/images/default-avatar.png'}">
                </div>
                <div class="message-preview">
                    <div class="message-header">
                        <span class="message-sender">${msg.from?.name || 'مجهول'}</span>
                        <span class="message-time">${this.formatTimeAgo(msg.createdAt)}</span>
                    </div>
                    <div class="message-subject">${msg.subject}</div>
                    <div class="message-snippet">${(msg.body || '').substring(0, 50)}...</div>
                </div>
            </div>
        `).join('');
    },
    
    // ==========================================
    // Reports - التقارير
    // ==========================================
    loadReportsView: function() {
        const container = document.getElementById('campaign-content');
        if (!container) return;
        
        const stats = this.calculateStats();
        
        container.innerHTML = `
            <div class="reports-view">
                <div class="reports-header">
                    <h3><i class="fas fa-chart-pie"></i> تقرير حالة الحملة</h3>
                    <div class="reports-actions">
                        <button onclick="CampaignManager.generateReport('pdf')" class="btn-export">
                            <i class="fas fa-file-pdf"></i> تصدير PDF
                        </button>
                        <button onclick="CampaignManager.generateReport('email')" class="btn-export">
                            <i class="fas fa-envelope"></i> إرسال بالبريد
                        </button>
                    </div>
                </div>
                
                <div class="report-content">
                    <!-- ملخص تنفيذي -->
                    <div class="report-section">
                        <h4>الملخص التنفيذي</h4>
                        <div class="executive-summary">
                            <div class="summary-item">
                                <span class="label">إجمالي المهام:</span>
                                <span class="value">${stats.total}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">المكتملة:</span>
                                <span class="value success">${stats.completed} (${stats.completionRate}%)</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">قيد التنفيذ:</span>
                                <span class="value warning">${stats.inProgress}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">متأخرة:</span>
                                <span class="value danger">${stats.overdue}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- التقدم حسب المرحلة -->
                    <div class="report-section">
                        <h4>التقدم حسب المرحلة</h4>
                        <div class="phase-progress">
                            ${this.renderPhaseProgress()}
                        </div>
                    </div>
                    
                    <!-- الاعتمادات المعلقة -->
                    <div class="report-section">
                        <h4>الاعتمادات المعلقة</h4>
                        <p>${this.approvals.filter(a => a.status === 'pending').length} اعتماد في الانتظار</p>
                    </div>
                </div>
            </div>
        `;
    },
    
    calculateStats: function() {
        const total = this.tasks.length;
        const completed = this.tasks.filter(t => t.status === 'completed').length;
        const inProgress = this.tasks.filter(t => t.status === 'in_progress').length;
        const overdue = this.tasks.filter(t => {
            if (!t.dueDate) return false;
            return new Date(t.dueDate) < new Date() && t.status !== 'completed';
        }).length;
        
        return {
            total,
            completed,
            inProgress,
            overdue,
            completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
        };
    },
    
    // ==========================================
    // Firebase Realtime Listeners
    // ==========================================
    setupRealtimeListeners: function() {
        // التحقق من وجود Firebase
        if (!this.hasFirebase || !this.db) {
            console.log('⚠️ Realtime listeners skipped - Firebase not available');
            return;
        }
        
        // Tasks listener
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('tasks')
            .orderBy('createdAt', 'desc')
            .onSnapshot(snapshot => {
                this.tasks = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
                if (this.currentSubTab === 'tasks') this.loadTasksView();
                if (this.currentSubTab === 'dashboard') this.updateDashboardStats();
            });
        
        // Approvals listener
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('approvals')
            .orderBy('createdAt', 'desc')
            .onSnapshot(snapshot => {
                this.approvals = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
                const pending = this.approvals.filter(a => a.status === 'pending').length;
                this.updateBadge('approvals-badge', pending);
                if (this.currentSubTab === 'approvals') this.loadApprovalsView();
            });
        
        // Messages listener
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('messages')
            .orderBy('createdAt', 'desc')
            .onSnapshot(snapshot => {
                this.messages = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
                const unread = this.messages.filter(m => !m.isRead).length;
                this.updateBadge('messages-badge', unread);
                if (this.currentSubTab === 'messages') this.loadMessagesView();
            });
    },
    
    // ==========================================
    // Utility Functions
    // ==========================================
    closeModal: function(modalId) {
        document.getElementById(modalId).style.display = 'none';
    },
    
    showNotification: function(message, type = 'info') {
        // Simple notification
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `<i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle"></i> ${message}`;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },
    
    updateBadge: function(badgeId, count) {
        const badge = document.getElementById(badgeId);
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    },
    
    formatDate: function(date) {
        if (!date) return '';
        const d = date.toDate ? date.toDate() : new Date(date);
        return d.toLocaleDateString('ar-SA');
    },
    
    formatTimeAgo: function(date) {
        if (!date) return '';
        const d = date.toDate ? date.toDate() : new Date(date);
        const diff = Date.now() - d.getTime();
        const minutes = Math.floor(diff / 60000);
        if (minutes < 60) return `منذ ${minutes} دقيقة`;
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `منذ ${hours} ساعة`;
        return this.formatDate(date);
    },
    
    getPhaseLabel: function(phase) {
        const labels = {
            'planning': 'التخطيط',
            'pre_launch': 'ما قبل الإطلاق',
            'launch': 'الإطلاق',
            'post_launch': 'ما بعد الإطلاق'
        };
        return labels[phase] || phase;
    },
    
    getApprovalStatusLabel: function(status) {
        const labels = {
            'pending': 'في الانتظار',
            'approved': 'معتمد',
            'rejected': 'مرفوض',
            'revision_requested': 'طلب تعديل'
        };
        return labels[status] || status;
    },
    
    canApprove: function() {
        // التحقق من صلاحيات الاعتماد
        return this.currentUser?.role === 'admin' || this.currentUser?.role === 'client';
    },
    
    addActivityLog: function(action, data) {
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('activity')
            .add({
                action,
                data,
                userId: this.currentUser?.uid,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            });
    },
    
    createApprovalRequest: function(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task || !task.requiresApproval) return;
        
        this.db.collection('projects').doc(this.currentProjectId)
            .collection('approvals')
            .add({
                taskId,
                title: `اعتماد: ${task.title}`,
                description: task.description,
                status: 'pending',
                createdBy: this.currentUser?.uid,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            });
    },
    
    renderPhaseProgress: function() {
        const phases = ['planning', 'pre_launch', 'launch', 'post_launch'];
        return phases.map(phase => {
            const phaseTasks = this.tasks.filter(t => t.phase === phase);
            const completed = phaseTasks.filter(t => t.status === 'completed').length;
            const total = phaseTasks.length;
            const percent = total > 0 ? Math.round((completed / total) * 100) : 0;
            
            return `
                <div class="phase-item">
                    <div class="phase-header">
                        <span>${this.getPhaseLabel(phase)}</span>
                        <span>${completed}/${total}</span>
                    </div>
                    <div class="phase-bar">
                        <div class="phase-fill" style="width: ${percent}%"></div>
                    </div>
                </div>
            `;
        }).join('');
    }
};

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // ستتم التهيئة عند فتح تاب المراقبة
});
