window.renderMediaServices = function (containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Split content into parts to avoid size limits
    const part1 = `
        <div class="hero-banner">
            <h1 class="hero-title">الخدمات المقدمة</h1>
            <p class="hero-subtitle">باقة شاملة من الخدمات الإعلامية والاتصالية المتكاملة</p>
        </div>

        <!-- مقدمة احترافية -->
        <section class="section">
            <div class="achievement-section" style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border: 3px solid #00b4a6; box-shadow: 0 8px 30px rgba(0,180,166,0.15); padding: 40px;">
                <div style="text-align: center; margin-bottom: 35px;">
                    <div style="display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #00b4a6 0%, #4dd0e1 100%); color: white; width: 90px; height: 90px; border-radius: 50%; font-size: 2.5rem; margin-bottom: 25px; box-shadow: 0 6px 25px rgba(0,180,166,0.4);">🎯</div>
                    <h2 style="color: #00695c; font-size: 2rem; font-weight: 900; margin-bottom: 20px; line-height: 1.4;">
                        نقدم حلولاً إعلامية متكاملة لتعزيز حضور هيئة الزكاة والضريبة والجمارك
                    </h2>
                </div>
                
                <div style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); padding: 30px; border-radius: 15px; border-right: 5px solid #26a69a; margin-bottom: 30px;">
                    <p style="color: #00695c; font-size: 1.15rem; line-height: 2; margin: 0; text-align: justify;">
                        في عالم يتسارع فيه إيقاع التحول الرقمي والإعلامي، تبرز الحاجة إلى <strong style="color: #00695c;">استراتيجيات اتصال متطورة</strong> تواكب تطلعات المؤسسات الحكومية الرائدة. نوفر لهيئة الزكاة والضريبة والجمارك <strong style="color: #00695c;">مجموعة شاملة من الخدمات الإعلامية والاتصالية</strong> المصممة خصيصاً لتعزيز حضورها المحلي والإقليمي والدولي، وبناء جسور التواصل الفعّال مع جميع الفئات المستهدفة.
                    </p>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-bottom: 30px;">
                    <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffecb3 100%); padding: 25px; border-radius: 12px; border-top: 4px solid #ffa726; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">📢</div>
                        <h4 style="color: #f57c00; font-weight: 800; margin-bottom: 12px; font-size: 1.1rem;">تغطية إعلامية شاملة</h4>
                        <p style="color: #f57c00; margin: 0; font-size: 0.95rem; line-height: 1.6;">من الصحافة التقليدية إلى المنصات الرقمية والشبكات الاجتماعية</p>
                    </div>
                    
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 25px; border-radius: 12px; border-top: 4px solid #2196f3; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🌍</div>
                        <h4 style="color: #1565c0; font-weight: 800; margin-bottom: 12px; font-size: 1.1rem;">انتشار عالمي</h4>
                        <p style="color: #1565c0; margin: 0; font-size: 0.95rem; line-height: 1.6;">وصول استراتيجي للمنصات الدولية والإقليمية المؤثرة</p>
                    </div>
                    
                    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 25px; border-radius: 12px; border-top: 4px solid #ab47bc; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🤝</div>
                        <h4 style="color: #7b1fa2; font-weight: 800; margin-bottom: 12px; font-size: 1.1rem;">شراكات استراتيجية</h4>
                        <p style="color: #7b1fa2; margin: 0; font-size: 0.95rem; line-height: 1.6;">علاقات قوية مع كبار الإعلاميين والمؤثرين والخبراء</p>
                    </div>
                    
                    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 25px; border-radius: 12px; border-top: 4px solid #66bb6a; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">📊</div>
                        <h4 style="color: #388e3c; font-weight: 800; margin-bottom: 12px; font-size: 1.1rem;">قياس دقيق للأثر</h4>
                        <p style="color: #388e3c; margin: 0; font-size: 0.95rem; line-height: 1.6;">تقييم مستمر للفعالية وتحليل شامل للنتائج</p>
                    </div>
                </div>

                <div style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); padding: 30px; border-radius: 15px; border-right: 5px solid #29b6f6;">
                    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
                        <div style="background: #29b6f6; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; flex-shrink: 0; box-shadow: 0 4px 15px rgba(41,182,246,0.3);">💡</div>
                        <h3 style="color: #0277bd; font-size: 1.3rem; font-weight: 800; margin: 0;">رؤيتنا</h3>
                    </div>
                    <p style="color: #0277bd; font-size: 1.05rem; line-height: 1.9; margin: 0; text-align: justify;">
                        نسعى لأن نكون <strong>الشريك الإعلامي الاستراتيجي الأول</strong> للهيئة، من خلال تقديم خدمات متميزة تعكس ريادتها في التحول الرقمي والشفافية المؤسسية، وتعزز ثقة جميع المتعاملين معها من أفراد وشركات ومستثمرين محليين ودوليين. نؤمن بأن <strong>الاتصال الفعّال</strong> هو حجر الزاوية في بناء السمعة المؤسسية المتميزة.
                    </p>
                </div>
            </div>
        </section>

        <!-- الخدمات الإعلامية -->
        <div style="display: grid; gap: 30px;">
                    
            <!-- خدمات الإعلام التقليدي والرقمي -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #26a69a; box-shadow: 0 4px 15px rgba(38,166,154,0.1);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #26a69a 0%, #00695c 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(38,166,154,0.3);">📰</div>
                    <h3 style="color: #00695c; font-size: 1.5rem; font-weight: 800; margin: 0;">خدمات الإعلام التقليدي والرقمي</h3>
                </div>
                
                <div class="achievement-grid">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">📡 خدمة توزيع البيانات والأخبار</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">نيوز واير (محلياً ودولياً)</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">📝 نشر مواد صحفية متنوعة</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">تقارير، سؤال وجواب، تحقيق استقصائي</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">✍️ التنسيق مع كتاب الرأي</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">كتاب درجة أولى وخبراء متخصصون</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">📻 تنسيق المداخلات الإذاعية</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">إدارة اللقاءات الإذاعية والتلفزيونية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">🎙️ برامج البودكاست والحوارات</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">اللقاءات التلفزيونية الحوارية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%); border-right: 4px solid #26a69a;">
                        <strong style="color: #00695c; font-size: 1.05rem; display: block; margin-bottom: 10px;">🌐 النشر في المواقع الإخبارية</strong>
                        <span style="color: #00695c; font-size: 0.9rem;">المواقع العامة والمتخصصة</span>
                    </div>
                </div>
            </div>

            <!-- خدمات وسائل التواصل الاجتماعي -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #29b6f6; box-shadow: 0 4px 15px rgba(41,182,246,0.1);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #29b6f6 0%, #0277bd 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(41,182,246,0.3);">📱</div>
                    <h3 style="color: #0277bd; font-size: 1.5rem; font-weight: 800; margin: 0;">خدمات وسائل التواصل الاجتماعي</h3>
                </div>
                
                <div class="achievement-grid">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 10px;">
                            <img src="/static/images/tenants/zakah/X.png" alt="X" style="width: 20px; height: 20px; object-fit: contain;">
                            النشر في منصة إكس
                        </strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">الحسابات المشهورة والمؤثرة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: block; margin-bottom: 10px;">🎬 الفيديوهات والتقارير المصورة</strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">تيك توك، ترويج، توثيق، تغطية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: block; margin-bottom: 10px;">🔊 المساحات الصوتية</strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">تخطيط وإدارة المساحات على منصة إكس</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: block; margin-bottom: 10px;">📊 إدارة الحملات الممولة</strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">إعلانات المؤثرين والسوشيال ميديا</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: block; margin-bottom: 10px;">🔍 إعلانات الأونلاين</strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">جوجل والتطبيقات المختلفة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e1f5fe 0%, #b3e5fc 100%); border-right: 4px solid #29b6f6;">
                        <strong style="color: #0277bd; font-size: 1.05rem; display: block; margin-bottom: 10px;">#️⃣ رفع الهاشتاجات لترند</strong>
                        <span style="color: #0277bd; font-size: 0.9rem;">على منصة إكس والمنصات الأخرى</span>
                    </div>
                </div>
            </div>

            <!-- خدمات المحتوى والتصميم -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #66bb6a; box-shadow: 0 4px 15px rgba(102,187,106,0.1);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #66bb6a 0%, #388e3c 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(102,187,106,0.3);">🎨</div>
                    <h3 style="color: #388e3c; font-size: 1.5rem; font-weight: 800; margin: 0;">خدمات المحتوى والتصميم</h3>
                </div>
                
                <div class="achievement-grid">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border-right: 4px solid #66bb6a;">
                        <strong style="color: #388e3c; font-size: 1.05rem; display: block; margin-bottom: 10px;">🎨 التصاميم والمكملات الترويجية</strong>
                        <span style="color: #388e3c; font-size: 0.9rem;">بأنواعها المختلفة والمتنوعة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border-right: 4px solid #66bb6a;">
                        <strong style="color: #388e3c; font-size: 1.05rem; display: block; margin-bottom: 10px;">📚 الكتيبات والنشرات</strong>
                        <span style="color: #388e3c; font-size: 0.9rem;">الأدلة التعريفية التوعوية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border-right: 4px solid #66bb6a;">
                        <strong style="color: #388e3c; font-size: 1.05rem; display: block; margin-bottom: 10px;">📧 خدمات الرسائل النصية</strong>
                        <span style="color: #388e3c; font-size: 0.9rem;">بما ينسجم مع الاستراتيجية الإعلامية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border-right: 4px solid #66bb6a;">
                        <strong style="color: #388e3c; font-size: 1.05rem; display: block; margin-bottom: 10px;">💬 إدارة القنوات في التيلجرام والواتس أب</strong>
                        <span style="color: #388e3c; font-size: 0.9rem;">إدارة شاملة للقنوات والمجموعات على منصات التواصل المختلفة</span>
                    </div>
                </div>
            </div>

            <!-- خدمات العلاقات والشراكات -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #ffa726; box-shadow: 0 4px 15px rgba(255,167,38,0.1);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #ffa726 0%, #f57c00 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(255,167,38,0.3);">🤝</div>
                    <h3 style="color: #f57c00; font-size: 1.5rem; font-weight: 800; margin: 0;">خدمات العلاقات والشراكات</h3>
                </div>
                
                <div class="achievement-grid">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-right: 4px solid #ffa726;">
                        <strong style="color: #f57c00; font-size: 1.05rem; display: block; margin-bottom: 10px;">📝 اللقاءات مع الكتاب والإعلاميين</strong>
                        <span style="color: #f57c00; font-size: 0.9rem;">تنسيق وإدارة اللقاءات الدورية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-right: 4px solid #ffa726;">
                        <strong style="color: #f57c00; font-size: 1.05rem; display: block; margin-bottom: 10px;">👑 اللقاءات مع قادة الرأي</strong>
                        <span style="color: #f57c00; font-size: 0.9rem;">وصناع السياسات والمؤثرين</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-right: 4px solid #ffa726;">
                        <strong style="color: #f57c00; font-size: 1.05rem; display: block; margin-bottom: 10px;">🔄 مناقشات الطاولة المستديرة</strong>
                        <span style="color: #f57c00; font-size: 0.9rem;">تنسيق وإدارة الجلسات التفاعلية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-right: 4px solid #ffa726;">
                        <strong style="color: #f57c00; font-size: 1.05rem; display: block; margin-bottom: 10px;">🌱 مبادرات المسؤولية المجتمعية</strong>
                        <span style="color: #f57c00; font-size: 0.9rem;">تصميم وتنفيذ البرامج المجتمعية</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-right: 4px solid #ffa726;">
                        <strong style="color: #f57c00; font-size: 1.05rem; display: block; margin-bottom: 10px;">👥 برامج سفراء السمعة</strong>
                        <span style="color: #f57c00; font-size: 0.9rem;">تخطيط وتنفيذ مبادرات السفراء</span>
                    </div>
                </div>
            </div>

            <!-- خدمات العلاقات الدولية -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #ab47bc; box-shadow: 0 4px 15px rgba(171,71,188,0.1);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #ab47bc 0%, #7b1fa2 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(171,71,188,0.3);">🌍</div>
                    <h3 style="color: #7b1fa2; font-size: 1.5rem; font-weight: 800; margin: 0;">خدمات العلاقات الدولية المتخصصة</h3>
                </div>
                
                <div class="achievement-grid">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">📖 إدارة العلاقة مع المجلات الدولية</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">المجلات ذات الصلة والمؤثرة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">🏛️ العلاقة مع مراكز الدراسات</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">مراكز الدراسات الدولية ذات الصلة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">📊 العلاقة مع المؤشرات الدولية</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">المؤشرات والتصنيفات ذات الصلة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">🎪 العلاقة مع الفعاليات الدولية</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">المؤتمرات والمعارض ذات الصلة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">🏆 العلاقة مع الجوائز الدولية</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">الجوائز والتقديرات ذات الصلة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">👨‍🔬 العلاقة مع الخبراء الدوليين</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">الخبراء والأكاديميين ذوي الصلة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-right: 4px solid #ab47bc;">
                        <strong style="color: #7b1fa2; font-size: 1.05rem; display: block; margin-bottom: 10px;">🏢 العلاقة مع المنظمات الدولية</strong>
                        <span style="color: #7b1fa2; font-size: 0.9rem;">المنظمات والهيئات ذات الصلة</span>
                    </div>
                </div>
            </div>

            <!-- قسم Media Contact Matrix -->
            <div style="background: white; padding: 25px; border-radius: 15px; border: 2px solid #e91e63; margin-top: 30px;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 15px;">📊</div>
                    <h4 style="color: #ad1457; font-size: 1.4rem; font-weight: 700; margin-bottom: 15px;">Media Contact Matrix</h4>
                    <h5 style="color: #ad1457; font-size: 1.2rem; font-weight: 600; margin-bottom: 20px;">قائمة وسائل الإعلام ذات الأولوية لهيئة الزكاة والضريبة والجمارك</h5>
                </div>
                
                <div style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #e91e63; margin-bottom: 25px;">
                    <p style="color: #ad1457; font-size: 1rem; line-height: 1.7; margin: 0; text-align: center;">
                        تضم هذه القائمة أبرز وسائل الإعلام العالمية في الولايات المتحدة وبريطانيا، إضافة إلى منصات ومنظمات مؤثرة تهتم بالقضايا الاقتصادية والضريبية والتنموية، وهي الجهات التي <strong>يُوصى بالتواصل معها</strong> في إطار الاستراتيجية الإعلامية الدولية لهيئة الزكاة والضريبة والجمارك.
                    </p>
                </div>

                <!-- جدول Media Outlets -->
                <div style="background: white; border-radius: 12px; overflow: hidden; border: 2px solid #e91e63; box-shadow: 0 4px 15px rgba(233,30,99,0.1); margin-bottom: 25px;">
                    <!-- رأس الجدول -->
                    <div style="background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%); color: white; padding: 15px; display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; font-weight: 700; font-size: 0.9rem; text-align: center;">
                        <div>Media Outlet</div>
                        <div>التعريف بالعربية</div>
                        <div>الفئة</div>
                        <div>نوع الوسيلة</div>
                        <div>مستوى التأثير</div>
                        <div>الزاوية المقترحة للهيئة</div>
                    </div>

                    <!-- The Wall Street Journal -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">The Wall Street Journal</div>
                        <div style="color: #555;">صحيفة أمريكية مرموقة تُعد مرجعًا في الأخبار الاقتصادية والمالية</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الولايات المتحدة</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #e91e63; font-weight: 600;">الإصلاحات الضريبية والتحول الاقتصادي</div>
                    </div>

                    <!-- Bloomberg -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Bloomberg</div>
                        <div style="color: #555;">شبكة مالية عالمية متعددة المنصات تغطي الأسواق والضرائب والتجارة</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الولايات المتحدة</div>
                        <div style="color: #666; text-align: center;">وكالة / تلفزيون / منصة رقمية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #e91e63; font-weight: 600;">التكامل الجمركي والتحول الرقمي</div>
                    </div>

                    <!-- Reuters -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Reuters</div>
                        <div style="color: #555;">وكالة أنباء عالمية تتميز بالدقة والانتشار وتغطي الاقتصاد والحوكمة</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الولايات المتحدة / بريطانيا</div>
                        <div style="color: #666; text-align: center;">وكالة أنباء</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #e91e63; font-weight: 600;">الشفافية والسياسات الضريبية</div>
                    </div>

                    <!-- Financial Times -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Financial Times</div>
                        <div style="color: #555;">صحيفة بريطانية عالمية تهتم بالأسواق الناشئة والسياسات المالية</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">بريطانيا</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #e91e63; font-weight: 600;">ثقة المستثمرين والبيئة الضريبية</div>
                    </div>

                    <!-- The Economist -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">The Economist</div>
                        <div style="color: #555;">مجلة تحليلية عالمية تتناول الاقتصاد الكلي والتنمية والحوكمة</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">بريطانيا</div>
                        <div style="color: #666; text-align: center;">مجلة أسبوعية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #e91e63; font-weight: 600;">الإصلاح المالي والحوكمة الاقتصادية</div>
                    </div>

                    <!-- Politico -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Politico</div>
                        <div style="color: #555;">منصة تركز على السياسات العامة والضرائب والتجارة في واشنطن</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الولايات المتحدة</div>
                        <div style="color: #666; text-align: center;">منصة سياسية</div>
                        <div style="background: #ff9800; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">متخصصة</div>
                        <div style="color: #e91e63; font-weight: 600;">الضرائب الدولية والسياسات العامة</div>
                    </div>

                    <!-- International Tax Review -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">International Tax Review</div>
                        <div style="color: #555;">مجلة متخصصة في القوانين الضريبية والممارسات العالمية</div>
                        <div style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">عالمي</div>
                        <div style="color: #666; text-align: center;">مجلة متخصصة</div>
                        <div style="background: #ff9800; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">متخصصة</div>
                        <div style="color: #e91e63; font-weight: 600;">الأنظمة الضريبية المقارنة</div>
                    </div>

                    <!-- Tax Notes International -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Tax Notes International</div>
                        <div style="color: #555;">نشرة مهنية تتابع التطورات في السياسات الضريبية الدولية</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الولايات المتحدة</div>
                        <div style="color: #666; text-align: center;">منصة تحليلية</div>
                        <div style="background: #ff9800; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">متخصصة</div>
                        <div style="color: #e91e63; font-weight: 600;">الإصلاحات التنظيمية الضريبية</div>
                    </div>

                    <!-- Devex -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Devex</div>
                        <div style="color: #555;">منصة تغطي قضايا التنمية والحوكمة والتمويل الدولي</div>
                        <div style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">عالمي</div>
                        <div style="color: #666; text-align: center;">منصة تنموية</div>
                        <div style="background: #ff9800; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">متخصصة</div>
                        <div style="color: #e91e63; font-weight: 600;">التكامل المؤسسي والتقنيات الحكومية</div>
                    </div>

                    <!-- Arab News -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Arab News</div>
                        <div style="color: #555;">صحيفة سعودية ناطقة بالإنجليزية ذات انتشار دولي</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">إقليمي / السعودية</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="background: #2196f3; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 2</div>
                        <div style="color: #e91e63; font-weight: 600;">تحسين صورة المملكة الاستثمارية</div>
                    </div>

                    <!-- Asharq Business -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Asharq Business with Bloomberg</div>
                        <div style="color: #555;">منصة اقتصادية عربية بالشراكة مع بلومبرغ، تغطي أخبار الاقتصاد الخليجي</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">إقليمي / السعودية</div>
                        <div style="color: #666; text-align: center;">منصة تلفزيونية ورقمية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1 إقليمي</div>
                        <div style="color: #e91e63; font-weight: 600;">التنويع الاقتصادي والشفافية</div>
                    </div>

                    <!-- Zawya -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Zawya (by Refinitiv)</div>
                        <div style="color: #555;">منصة بيانات وأخبار مالية تغطي الأسواق العربية والخليجية</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">إقليمي</div>
                        <div style="color: #666; text-align: center;">منصة رقمية</div>
                        <div style="background: #2196f3; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 2</div>
                        <div style="color: #e91e63; font-weight: 600;">إبراز كفاءة الأنظمة الضريبية والجمركية</div>
                    </div>

                    <!-- MEED -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">MEED</div>
                        <div style="color: #555;">مجلة اقتصادية بريطانية تتابع مشاريع البنية التحتية والاستثمار في الشرق الأوسط</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">بريطانيا / الشرق الأوسط</div>
                        <div style="color: #666; text-align: center;">مجلة اقتصادية</div>
                        <div style="background: #2196f3; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 2</div>
                        <div style="color: #e91e63; font-weight: 600;">تحسين مناخ الأعمال والتجارة</div>
                    </div>
                </div>

                <!-- إحصائيات سريعة -->
                <div style="margin-top: 25px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #2196f3;">
                        <div style="color: #1565c0; font-size: 1.5rem; font-weight: 700;">6</div>
                        <div style="color: #1565c0; font-size: 0.9rem; font-weight: 600;">منصات Tier 1 عالمية</div>
                    </div>
                    <div style="background: #fff3e0; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #ff9800;">
                        <div style="color: #f57c00; font-size: 1.5rem; font-weight: 700;">5</div>
                        <div style="color: #f57c00; font-size: 0.9rem; font-weight: 600;">منصات متخصصة</div>
                    </div>
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #4caf50;">
                        <div style="color: #2e7d32; font-size: 1.5rem; font-weight: 700;">3</div>
                        <div style="color: #2e7d32; font-size: 0.9rem; font-weight: 600;">منصات إقليمية مؤثرة</div>
                    </div>
                    <div style="background: #fce4ec; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #e91e63;">
                        <div style="color: #ad1457; font-size: 1.5rem; font-weight: 700;">14</div>
                        <div style="color: #ad1457; font-size: 0.9rem; font-weight: 600;">إجمالي المنصات المستهدفة</div>
                    </div>
                </div>
            </div>

            <!-- قسم Media Contact Matrix - Arab & Gulf Region -->
            <div style="background: white; padding: 25px; border-radius: 15px; border: 2px solid #4caf50; margin-top: 30px;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 15px;">🌍</div>
                    <h4 style="color: #2e7d32; font-size: 1.4rem; font-weight: 700; margin-bottom: 15px;">Media Contact Matrix – Arab & Gulf Region</h4>
                    <h5 style="color: #2e7d32; font-size: 1.2rem; font-weight: 600; margin-bottom: 20px;">قائمة وسائل الإعلام ذات الأولوية في المنطقة العربية والخليج</h5>
                </div>
                
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #4caf50; margin-bottom: 25px;">
                    <p style="color: #2e7d32; font-size: 1rem; line-height: 1.7; margin: 0; text-align: center;">
                        تضم هذه القائمة أبرز وسائل الإعلام في المملكة العربية السعودية والخليج والشرق الأوسط، إضافة إلى منصات ومنظمات مؤثرة تهتم بالقضايا الاقتصادية والضريبية والتنموية، وهي الجهات التي <strong>يُوصى بالتواصل معها</strong> في إطار الاستراتيجية الإعلامية الإقليمية.
                    </p>
                </div>

                <!-- جدول Media Outlets العربية والخليجية -->
                <div style="background: white; border-radius: 12px; overflow: hidden; border: 2px solid #4caf50; box-shadow: 0 4px 15px rgba(76,175,80,0.1); margin-bottom: 25px;">
                    <!-- رأس الجدول -->
                    <div style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); color: white; padding: 15px; display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; font-weight: 700; font-size: 0.9rem; text-align: center;">
                        <div>Media Outlet</div>
                        <div>التعريف بالعربية</div>
                        <div>الفئة</div>
                        <div>نوع الوسيلة</div>
                        <div>مستوى التأثير</div>
                        <div>الزاوية المقترحة للهيئة</div>
                    </div>

                    <!-- Aleqtisadiah -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Aleqtisadiah</div>
                        <div style="color: #555;">الصحيفة السعودية المتخصصة في الاقتصاد والأسواق المالية</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">السعودية</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">الأنظمة الضريبية والتحول الاقتصادي</div>
                    </div>

                    <!-- Okaz -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Okaz</div>
                        <div style="color: #555;">صحيفة سعودية واسعة الانتشار تتابع القضايا الحكومية والتنظيمية</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">السعودية</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">التوعية الضريبية والتنظيم المؤسسي</div>
                    </div>

                    <!-- Asharq Al-Awsat -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Asharq Al-Awsat</div>
                        <div style="color: #555;">صحيفة عربية دولية تصدر من لندن وتغطي الشأن السعودي والخليجي</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">السعودية / الشرق الأوسط</div>
                        <div style="color: #666; text-align: center;">صحيفة دولية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">الصورة الذهنية للمملكة</div>
                    </div>

                    <!-- Al Arabiya Business -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Al Arabiya Business</div>
                        <div style="color: #555;">منصة اقتصادية تابعة لقناة العربية تركز على التحول الاقتصادي السعودي</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">السعودية / الخليج</div>
                        <div style="color: #666; text-align: center;">منصة رقمية / تلفزيونية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">التحول الرقمي المالي</div>
                    </div>

                    <!-- Gulf News -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Gulf News</div>
                        <div style="color: #555;">صحيفة إماراتية ناطقة بالإنجليزية تُقرأ من قِبل المستثمرين والوافدين</div>
                        <div style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الإمارات / الخليج</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية (إنجليزية)</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">صورة المملكة الاستثمارية</div>
                    </div>

                    <!-- Sky News Arabia -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Sky News Arabia</div>
                        <div style="color: #555;">منصة إخبارية إقليمية تقدم محتوى اقتصادي وتحليلي</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الشرق الأوسط</div>
                        <div style="color: #666; text-align: center;">قناة تلفزيونية / رقمية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">توضيح المبادرات والسياسات العامة</div>
                    </div>

                    <!-- Forbes Middle East -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr 2fr; gap: 10px; padding: 15px; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #2e7d32; text-align: center;">Forbes Middle East</div>
                        <div style="color: #555;">النسخة الإقليمية لمجلة فوربس، جمهورها من التنفيذيين والمستثمرين</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">الخليج / الشرق الأوسط</div>
                        <div style="color: #666; text-align: center;">مجلة شهرية</div>
                        <div style="background: #4caf50; color: white; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600; font-size: 0.8rem;">Tier 1</div>
                        <div style="color: #4caf50; font-weight: 600;">ابتكارات التحول الضريبي</div>
                    </div>
                </div>

                <!-- إحصائيات سريعة للمنطقة العربية والخليج -->
                <div style="margin-top: 25px; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #4caf50;">
                        <div style="color: #2e7d32; font-size: 1.4rem; font-weight: 700;">4</div>
                        <div style="color: #2e7d32; font-size: 0.85rem; font-weight: 600;">منصات سعودية</div>
                    </div>
                    <div style="background: #f3e5f5; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #9c27b0;">
                        <div style="color: #7b1fa2; font-size: 1.4rem; font-weight: 700;">2</div>
                        <div style="color: #7b1fa2; font-size: 0.85rem; font-weight: 600;">منصات إماراتية</div>
                    </div>
                    <div style="background: #fff3e0; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #ff9800;">
                        <div style="color: #f57c00; font-size: 1.4rem; font-weight: 700;">2</div>
                        <div style="color: #f57c00; font-size: 0.85rem; font-weight: 600;">منصات إقليمية</div>
                    </div>
                    <div style="background: #f1f8e9; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #689f38;">
                        <div style="color: #2e7d32; font-size: 1.4rem; font-weight: 700;">8</div>
                        <div style="color: #2e7d32; font-size: 0.85rem; font-weight: 600;">إجمالي المنصات الإقليمية</div>
                    </div>
                </div>
            </div>

            <!-- قائمة وسائل الإعلام المعتمدة لدى البنك الدولي -->
            <div style="background: white; padding: 25px; border-radius: 15px; border: 2px solid #3f51b5; margin-top: 30px;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 15px;">🏦</div>
                    <h4 style="color: #1a237e; font-size: 1.4rem; font-weight: 700; margin-bottom: 15px;">World Bank Approved Media List</h4>
                    <h5 style="color: #1a237e; font-size: 1.2rem; font-weight: 600; margin-bottom: 20px;">قائمة وسائل الإعلام المعتمدة لدى البنك الدولي</h5>
                </div>
                
                <div style="background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #3f51b5; margin-bottom: 25px;">
                    <p style="color: #1a237e; font-size: 1rem; line-height: 1.7; margin: 0; text-align: center;">
                        تُعد هذه القائمة مرجعاً أساسياً للمنظمات الدولية، حيث يعتمد البنك الدولي على هذه الوسائل في تقييم الشفافية والأداء الاقتصادي للدول. التواجد الإيجابي في هذه المنصات <strong>يعزز تصنيف المملكة</strong> في مؤشرات سهولة ممارسة الأعمال والشفافية المالية.
                    </p>
                </div>

                <!-- جدول World Bank List -->
                <div style="background: white; border-radius: 12px; overflow: hidden; border: 2px solid #3f51b5; box-shadow: 0 4px 15px rgba(63,81,181,0.1); margin-bottom: 25px;">
                    <!-- رأس الجدول -->
                    <div style="background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%); color: white; padding: 15px; display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; font-weight: 700; font-size: 0.9rem; text-align: center;">
                        <div>Media Outlet</div>
                        <div>التعريف</div>
                        <div>المقر الرئيسي</div>
                        <div>النوع</div>
                        <div>الأهمية للهيئة</div>
                    </div>

                    <!-- The New York Times -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">The New York Times</div>
                        <div style="color: #555;">صحيفة أمريكية ذات تأثير عالمي واسع</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">USA</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="color: #3f51b5; font-weight: 600;">بناء السمعة الدولية العامة</div>
                    </div>

                    <!-- The Washington Post -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">The Washington Post</div>
                        <div style="color: #555;">صحيفة أمريكية تركز على السياسة والاقتصاد</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">USA</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="color: #3f51b5; font-weight: 600;">التأثير على صناع القرار</div>
                    </div>

                    <!-- BBC World News -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">BBC World News</div>
                        <div style="color: #555;">شبكة إخبارية عالمية ذات مصداقية عالية</div>
                        <div style="background: #fff3e0; color: #f57c00; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">UK</div>
                        <div style="color: #666; text-align: center;">تلفزيون / رقمي</div>
                        <div style="color: #3f51b5; font-weight: 600;">الوصول لجمهور عالمي متنوع</div>
                    </div>

                    <!-- CNN International -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">CNN International</div>
                        <div style="color: #555;">شبكة إخبارية أمريكية رائدة عالمياً</div>
                        <div style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">USA</div>
                        <div style="color: #666; text-align: center;">تلفزيون / رقمي</div>
                        <div style="color: #3f51b5; font-weight: 600;">تغطية الفعاليات والمؤتمرات الكبرى</div>
                    </div>

                    <!-- Le Monde -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Le Monde</div>
                        <div style="color: #555;">الصحيفة الفرنسية الأولى، مؤثرة في أوروبا</div>
                        <div style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">France</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="color: #3f51b5; font-weight: 600;">استهداف المستثمرين الأوروبيين</div>
                    </div>

                    <!-- Der Spiegel -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Der Spiegel</div>
                        <div style="color: #555;">مجلة ألمانية أسبوعية واسعة الانتشار</div>
                        <div style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">Germany</div>
                        <div style="color: #666; text-align: center;">مجلة أسبوعية</div>
                        <div style="color: #3f51b5; font-weight: 600;">تعزيز العلاقات الاقتصادية مع ألمانيا</div>
                    </div>

                    <!-- Asahi Shimbun -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; border-bottom: 1px solid #f5f5f5; align-items: center; font-size: 0.85rem;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Asahi Shimbun</div>
                        <div style="color: #555;">من كبرى الصحف اليابانية والآسيوية</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">Japan</div>
                        <div style="color: #666; text-align: center;">صحيفة يومية</div>
                        <div style="color: #3f51b5; font-weight: 600;">استهداف السوق الآسيوي والياباني</div>
                    </div>

                    <!-- Caixin -->
                    <div style="display: grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 2fr; gap: 10px; padding: 15px; align-items: center; font-size: 0.85rem; background: #fafafa;">
                        <div style="font-weight: 700; color: #1565c0; text-align: center;">Caixin</div>
                        <div style="color: #555;">مجموعة إعلامية صينية رائدة في الاقتصاد والمال</div>
                        <div style="background: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 6px; text-align: center; font-weight: 600;">China</div>
                        <div style="color: #666; text-align: center;">منصة مالية</div>
                        <div style="color: #3f51b5; font-weight: 600;">جذب الاستثمارات الصينية</div>
                    </div>
                </div>
            </div>

            <!-- التقييم وقياس الفعالية -->
            <div class="achievement-section" style="background: white; padding: 30px; border-radius: 15px; border: 2px solid #607d8b; box-shadow: 0 4px 15px rgba(96,125,139,0.1); margin-top: 30px;">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                    <div style="background: linear-gradient(135deg, #607d8b 0%, #455a64 100%); color: white; width: 70px; height: 70px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(96,125,139,0.3);">📈</div>
                    <h3 style="color: #455a64; font-size: 1.5rem; font-weight: 800; margin: 0;">التقييم وقياس فعالية خطة الاتصال والإعلام</h3>
                </div>
                
                <div style="background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%); padding: 20px; border-radius: 12px; border-right: 5px solid #607d8b; margin-bottom: 25px;">
                    <p style="color: #455a64; font-size: 1rem; line-height: 1.7; margin: 0; text-align: justify;">
                        لضمان تحقيق الأهداف الاستراتيجية، نعتمد منهجية صارمة في القياس والتقييم تستند إلى مؤشرات أداء (KPIs) كمية ونوعية دقيقة. يتم مراجعة هذه المؤشرات بشكل دوري لضمان التحسين المستمر للأداء الإعلامي.
                    </p>
                </div>

                <div class="achievement-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
                    <div class="achievement-card" style="background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%); border-right: 4px solid #607d8b;">
                        <strong style="color: #455a64; font-size: 1.05rem; display: block; margin-bottom: 10px;">📊 تقارير الأداء الدورية</strong>
                        <span style="color: #455a64; font-size: 0.9rem;">إصدار تقارير شهرية وربع سنوية وسنوية شاملة</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%); border-right: 4px solid #607d8b;">
                        <strong style="color: #455a64; font-size: 1.05rem; display: block; margin-bottom: 10px;">🔍 تحليل المحتوى الإعلامي</strong>
                        <span style="color: #455a64; font-size: 0.9rem;">قياس جودة الرسائل، النبرة (Sentiment)، ومدى الانتشار</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%); border-right: 4px solid #607d8b;">
                        <strong style="color: #455a64; font-size: 1.05rem; display: block; margin-bottom: 10px;">🌐 قياس التفاعل الرقمي</strong>
                        <span style="color: #455a64; font-size: 0.9rem;">تحليل التفاعل على منصات التواصل (Engagement Rate)</span>
                    </div>
                    <div class="achievement-card" style="background: linear-gradient(135deg, #eceff1 0%, #cfd8dc 100%); border-right: 4px solid #607d8b;">
                        <strong style="color: #455a64; font-size: 1.05rem; display: block; margin-bottom: 10px;">💡 استطلاعات الرأي وقياس الأثر</strong>
                        <span style="color: #455a64; font-size: 0.9rem;">قياس التغير في الوعي والصورة الذهنية لدى الجمهور المستهدف</span>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <footer class="tab-footer">
                <div class="tab-footer__content">
                    <span>جميع الحقوق محفوظة لشركة MARCH © 2025</span>
                    <span>|</span>
                    <a href="mailto:info@march.com.sa">info@march.com.sa</a>
                    <span>|</span>
                    <div class="tab-footer__social">
                        <a href="https://x.com/marchpr_sa" target="_blank"><img src="/static/images/tenants/zakah/X.png" alt="X"></a>
                        <a href="https://www.linkedin.com/company/marchprsa/" target="_blank"><img src="/static/images/tenants/zakah/LinkedIn_icon.svg.png" alt="LinkedIn"></a>
                    </div>
                </div>
            </footer>
        </div>
    `;

    // Part 2 content will be appended here

    container.innerHTML = part1;
};
