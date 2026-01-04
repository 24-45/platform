import { db, collection, onSnapshot, addDoc, updateDoc, deleteDoc, doc, writeBatch } from '/static/js/tenants/zakah/firebase-config.js';

export function initNewsManager(container) {
    window.newsManagerLogic = function () {
        return {
            newsItems: [],
            viewMode: 'calendar',
            isModalOpen: false,
            isAIModalOpen: false,
            isStagingOpen: false,

            // PIN Modal State
            pinModal: {
                isOpen: false,
                title: '',
                description: '',
                input: '',
                expectedPin: '',
                onConfirm: null
            },

            // AI State
            aiApiKey: localStorage.getItem('geminiKey') || 'AIzaSyDUNz5TLSTygSoVRY6FmKsOuD2kibUB6cs',
            aiPrompt: '',
            aiStagingData: [],
            isProcessingAI: false,

            saveApiKey() {
                if (this.aiApiKey) {
                    localStorage.setItem('geminiKey', this.aiApiKey);
                    alert('تم حفظ مفتاح API بنجاح');
                }
            },

            // Current Item State
            currentItem: {
                id: null,
                title: '',
                platform: '',
                platformName: '',
                scope: 'السعودية/محلي',
                impactTier: 'Tier 1',
                country: 'السعودية',
                time: '09:00',
                newsLink: '',
                date: '',
                status: 'scheduled',
                clientApproved: false,
                details: ''
            },

            // Filter State Initialization
            selectedScope: 'السعودية/محلي',
            selectedTier: 'Tier 1',
            isManualPlatform: false,

            // Media Master List
            mediaMasterList: [
                { name: "The Wall Street Journal", scope: "دولي/عالمي", tier: "Tier 1", country: "الولايات المتحدة" },
                { name: "Bloomberg", scope: "دولي/عالمي", tier: "Tier 1", country: "الولايات المتحدة" },
                { name: "Reuters", scope: "دولي/عالمي", tier: "Tier 1", country: "بريطانيا" },
                { name: "Financial Times", scope: "دولي/عالمي", tier: "Tier 1", country: "بريطانيا" },
                { name: "The Economist", scope: "دولي/عالمي", tier: "Tier 1", country: "بريطانيا" },
                { name: "Devex", scope: "دولي/عالمي", tier: "Tier 1", country: "عالمي" },
                { name: "Project Syndicate", scope: "دولي/عالمي", tier: "Tier 1", country: "عالمي" },
                { name: "Politico", scope: "متخصصة", tier: "متخصصة", country: "الولايات المتحدة" },
                { name: "International Tax Review", scope: "متخصصة", tier: "متخصصة", country: "عالمي" },
                { name: "Aleqtisadiah", scope: "السعودية/محلي", tier: "Tier 1", country: "السعودية" },
                { name: "Okaz", scope: "السعودية/محلي", tier: "Tier 1", country: "السعودية" },
                { name: "Asharq Al-Awsat", scope: "إقليمي/الخليج", tier: "Tier 1", country: "الشرق الأوسط" },
                { name: "SPA (Saudi Press Agency)", scope: "السعودية/محلي", tier: "Tier 1", country: "السعودية" },
                { name: "Al Arabiya Business", scope: "إقليمي/الخليج", tier: "Tier 1", country: "الشرق الأوسط" },
                { name: "Sky News Arabia", scope: "إقليمي/الخليج", tier: "Tier 1", country: "الإمارات" },
                { name: "Gulf News", scope: "إقليمي/الخليج", tier: "Tier 1", country: "الإمارات" },
                { name: "Forbes Middle East", scope: "إقليمي/الخليج", tier: "Tier 2", country: "الإمارات" },
                { name: "MEED", scope: "إقليمي/الخليج", tier: "Tier 2", country: "بريطانيا" },
                { name: "Al Bayan", scope: "إقليمي/الخليج", tier: "Tier 1", country: "الإمارات" },
                { name: "Al Khaleej", scope: "إقليمي/الخليج", tier: "Tier 2", country: "الإمارات" }
            ],

            get filteredPlatforms() {
                const scope = this.selectedScope;
                const tier = this.selectedTier;

                if (!scope || !tier) return [];

                return this.mediaMasterList.filter(m =>
                    m.scope === scope &&
                    m.tier === tier
                );
            },

            weeks: [],
            startDate: new Date('2025-12-01'),

            init() {
                this.generateWeeks(16);
                this.fetchNews();
            },

            normalizeDate(date) {
                if (!date) return '';
                const d = new Date(date);
                return d.toISOString().split('T')[0];
            },

            formatDateDisplay(dateStr) {
                if (!dateStr) return '';
                const date = new Date(dateStr);
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
            },

            generateWeeks(count = 16) {
                let current;
                let startIndex = this.weeks.length;

                if (startIndex === 0) {
                    current = new Date(this.startDate);
                } else {
                    const lastWeek = this.weeks[startIndex - 1];
                    current = new Date(lastWeek.end);
                    current.setDate(current.getDate() + 1);
                }

                const today = new Date();
                const options = { month: 'short', day: 'numeric', year: 'numeric' };

                for (let i = 0; i < count; i++) {
                    let end = new Date(current);
                    end.setDate(current.getDate() + 6);

                    const isCurrentWeek = today >= current && today <= end;
                    const label = current.toLocaleDateString('en-US', options);

                    this.weeks.push({
                        id: startIndex + i,
                        start: new Date(current),
                        end: new Date(end),
                        label: label,
                        isCurrent: isCurrentWeek,
                        startDateStr: this.normalizeDate(current)
                    });
                    current.setDate(current.getDate() + 7);
                }
            },

            loadMoreWeeks() {
                this.generateWeeks(4);
            },

            fetchNews() {
                const q = collection(db, "news_items");
                onSnapshot(q, (snapshot) => {
                    this.newsItems = snapshot.docs.map(doc => {
                        const data = doc.data();
                        return {
                            id: doc.id,
                            ...data,
                            platformName: data.platformName || data.platform || '',
                            country: data.country || 'السعودية',
                            impactTier: data.impactTier || 'Tier 1',
                            time: data.time || '09:00',
                            newsLink: data.newsLink || '',
                            clientApproved: data.clientApproved || false,
                            details: data.details || ''
                        };
                    });
                });
            },

            getNewsForWeek(week) {
                return this.newsItems.filter(item => {
                    const itemDate = new Date(item.date);
                    return itemDate >= week.start && itemDate <= week.end;
                });
            },

            // --- Secure PIN Logic ---
            openPinModal(title, description, expectedPin, callback) {
                this.pinModal = {
                    isOpen: true,
                    title: title,
                    description: description,
                    input: '',
                    expectedPin: expectedPin,
                    onConfirm: callback
                };
                // Focus input on next tick
                setTimeout(() => {
                    const input = document.getElementById('pinInput');
                    if (input) input.focus();
                }, 100);
            },

            closePinModal() {
                this.pinModal.isOpen = false;
                this.pinModal.input = '';
                this.pinModal.onConfirm = null;
            },

            confirmPin() {
                if (this.pinModal.input === this.pinModal.expectedPin) {
                    if (this.pinModal.onConfirm) {
                        this.pinModal.onConfirm();
                    }
                    this.closePinModal();
                } else {
                    alert("الرمز غير صحيح. تم رفض الوصول.");
                    this.pinModal.input = ''; // Clear input for retry
                }
            },

            // --- CRUD Operations ---
            openModal(item = null, dateOverride = null) {
                if (item) {
                    this.currentItem = { ...item };

                    // Initialize filters from item data
                    if (this.currentItem.scope) {
                        this.selectedScope = this.currentItem.scope;
                    } else {
                        // Legacy support: try to find scope/tier from platform name
                        const match = this.mediaMasterList.find(m => m.name === this.currentItem.platformName);
                        this.selectedScope = match ? match.scope : 'السعودية/محلي';
                        this.currentItem.scope = this.selectedScope; // Update item
                    }

                    if (this.currentItem.impactTier) {
                        this.selectedTier = this.currentItem.impactTier;
                    } else {
                        const match = this.mediaMasterList.find(m => m.name === this.currentItem.platformName);
                        this.selectedTier = match ? match.tier : 'Tier 1';
                        this.currentItem.impactTier = this.selectedTier; // Update item
                    }

                    // Determine if manual entry
                    const isKnown = this.mediaMasterList.some(m => m.name === this.currentItem.platformName);
                    this.isManualPlatform = !isKnown && this.currentItem.platformName !== '';

                } else {
                    // New Item: Reset to defaults
                    this.selectedScope = 'السعودية/محلي';
                    this.selectedTier = 'Tier 1';
                    this.isManualPlatform = false;

                    this.currentItem = {
                        id: null,
                        title: '',
                        platformName: '',
                        scope: 'السعودية/محلي',
                        impactTier: 'Tier 1',
                        country: 'السعودية',
                        time: new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }),
                        date: dateOverride || new Date().toISOString().split('T')[0],
                        status: 'scheduled',
                        clientApproved: false,
                        newsLink: '',
                        details: ''
                    };
                }
                this.isModalOpen = true;
            },

            closeModal() {
                this.isModalOpen = false;
            },

            async saveNews() {
                if (!this.currentItem.title || !this.currentItem.date) {
                    alert('يرجى تعبئة العنوان والتاريخ');
                    return;
                }

                // Map scope to country for backward compatibility if needed, or just save scope
                if (this.currentItem.scope.includes('السعودية')) this.currentItem.country = 'السعودية';
                else if (this.currentItem.scope.includes('إقليمي')) this.currentItem.country = 'إقليمي';
                else if (this.currentItem.scope.includes('دولي')) this.currentItem.country = 'دولي';
                else this.currentItem.country = 'دولي';

                try {
                    if (this.currentItem.id) {
                        await updateDoc(doc(db, "news_items", this.currentItem.id), this.currentItem);
                    } else {
                        await addDoc(collection(db, "news_items"), {
                            ...this.currentItem,
                            createdAt: new Date().toISOString()
                        });
                    }
                    this.closeModal();
                    this.fetchNews();
                } catch (e) {
                    console.error("Error saving document: ", e);
                    alert("حدث خطأ أثناء الحفظ");
                }
            },

            deleteNews(id) {
                this.openPinModal("تأكيد الحذف", "أدخل الرمز السري لحذف هذا الخبر.", "1221", async () => {
                    try {
                        await deleteDoc(doc(db, "news_items", id));
                        // If modal is open for this item, close it
                        if (this.isModalOpen && this.currentItem.id === id) {
                            this.closeModal();
                        }
                        this.fetchNews();
                    } catch (e) {
                        console.error("Error deleting document: ", e);
                        alert("خطأ في حذف الخبر");
                    }
                });
            },

            async toggleApproval(item) {
                // If turning ON, require PIN
                if (!item.clientApproved) {
                    this.openPinModal("اعتماد المالك", "أدخل الرمز السري للموافقة.", "53100", async () => {
                        try {
                            const docRef = doc(db, "news_items", item.id);
                            await updateDoc(docRef, {
                                clientApproved: true
                            });
                            this.fetchNews();
                        } catch (e) {
                            console.error("Error updating approval: ", e);
                            alert("خطأ في تحديث حالة الاعتماد");
                        }
                    });
                } else {
                    // Turning OFF - No PIN required (or add if needed)
                    try {
                        const docRef = doc(db, "news_items", item.id);
                        await updateDoc(docRef, {
                            clientApproved: false
                        });
                        this.fetchNews();
                    } catch (e) {
                        console.error("Error updating approval: ", e);
                        alert("خطأ في تحديث حالة الاعتماد");
                    }
                }
            },

            handleDragStart(event, item) {
                event.dataTransfer.setData('text/plain', item.id);
                event.dataTransfer.effectAllowed = 'move';
            },

            handleDrop(event, week) {
                const itemId = event.dataTransfer.getData('text/plain');
                if (!itemId) return;

                this.openPinModal("نقل الخبر", "أدخل الرمز السري لنقل الخبر.", "1221", async () => {
                    try {
                        const newDate = week.startDateStr;
                        const docRef = doc(db, "news_items", itemId);
                        await updateDoc(docRef, {
                            date: newDate
                        });
                    } catch (e) {
                        console.error("Error moving item: ", e);
                        alert("خطأ في نقل العنصر");
                    }
                });
            },

            // --- AI Integration ---
            openAIModal() {
                this.isAIModalOpen = true;
            },

            closeAIModal() {
                this.isAIModalOpen = false;
                this.aiPrompt = '';
            },

            async processAIImport() {
                if (!this.aiApiKey) {
                    alert("الرجاء إدخال مفتاح API.");
                    return;
                }

                const fileInput = this.$refs.fileInput;
                const file = fileInput ? fileInput.files[0] : null;

                if (!this.aiPrompt && !file) {
                    alert("الرجاء إدخال نص أو رفع ملف.");
                    return;
                }

                this.isProcessingAI = true;

                const systemPrompt = `
                    You are a News Calendar Assistant. 
                    Analyze the provided content (text or file) and extract news items.
                    If a file is provided (CSV, TXT, PDF, etc.), analyze its structure to extract the data.
                    Infer the 'country' (default 'السعودية'), 'impactTier' ('Tier 1' or 'Tier 2'), and 'platformName'.
                    Distribute dates logically starting from Dec 1, 2025 if not specified.
                    Return ONLY a JSON array of objects with keys: title, platformName, country, impactTier, time, newsLink, date (YYYY-MM-DD), status (default 'scheduled').
                `;

                try {
                    let parts = [{ text: systemPrompt + "\n\nContext/Instructions:\n" + this.aiPrompt }];

                    if (file) {
                        // Read file as Base64
                        const base64Data = await new Promise((resolve, reject) => {
                            const reader = new FileReader();
                            reader.onload = () => {
                                // Remove Data URL prefix (e.g., "data:application/pdf;base64,")
                                const result = reader.result;
                                const base64 = result.split(',')[1];
                                resolve(base64);
                            };
                            reader.onerror = error => reject(error);
                            reader.readAsDataURL(file);
                        });

                        parts.push({
                            inlineData: {
                                mimeType: file.type || 'application/octet-stream',
                                data: base64Data
                            }
                        });
                    }

                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${this.aiApiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: parts }]
                        })
                    });

                    const data = await response.json();

                    if (data.error) {
                        throw new Error(data.error.message);
                    }

                    const text = data.candidates[0].content.parts[0].text;
                    const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || text.match(/```\n([\s\S]*?)\n```/) || [null, text];
                    const jsonStr = jsonMatch[1] || text;

                    this.aiStagingData = JSON.parse(jsonStr);
                    this.isAIModalOpen = false;
                    this.isStagingOpen = true;

                } catch (e) {
                    console.error("AI Error: ", e);
                    alert("فشلت المعالجة بالذكاء الاصطناعي: " + e.message);
                } finally {
                    this.isProcessingAI = false;
                }
            },

            saveStagingData() {
                this.openPinModal("استيراد بيانات", "أدخل الرمز السري لحفظ البيانات.", "1221", async () => {
                    try {
                        const batch = writeBatch(db);
                        this.aiStagingData.forEach(item => {
                            const docRef = doc(collection(db, "news_items"));
                            batch.set(docRef, {
                                ...item,
                                createdAt: new Date().toISOString(),
                                clientApproved: false
                            });
                        });
                        await batch.commit();
                        this.isStagingOpen = false;
                        this.aiStagingData = [];
                        alert("تم استيراد " + this.aiStagingData.length + " عنصر بنجاح.");
                    } catch (e) {
                        console.error("Batch save error: ", e);
                        alert("خطأ في حفظ البيانات المستوردة.");
                    }
                });
            }
        };
    };

    container.innerHTML = `
        <div x-data="newsManagerLogic()" class="p-6 bg-gray-50 min-h-screen font-sans text-right" dir="rtl">
            <!-- Top Bar (Simplified & Right Aligned) -->
            <div class="flex items-center gap-3 mb-6">
                <!-- View Toggles (Icons) -->
                <div class="bg-white rounded-lg shadow p-1 flex">
                    <button @click="viewMode = 'calendar'" :class="{'bg-blue-100 text-blue-600': viewMode === 'calendar'}" class="w-10 h-10 flex items-center justify-center rounded-md transition text-xl" title="عرض الروزنامة">📅</button>
                    <button @click="viewMode = 'table'" :class="{'bg-blue-100 text-blue-600': viewMode === 'table'}" class="w-10 h-10 flex items-center justify-center rounded-md transition text-xl" title="عرض الجدول">📄</button>
                </div>

                <!-- Add News -->
                <button @click="openModal()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg shadow transition flex items-center gap-2 font-medium">
                    <span>+ إضافة خبر جديد</span>
                </button>

                <!-- Smart Import -->
                <button @click="openAIModal()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg shadow transition flex items-center gap-2 font-medium">
                    <span>🤖 استيراد ذكي</span>
                </button>
            </div>

            <!-- Calendar View -->
            <div x-show="viewMode === 'calendar'">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <template x-for="week in weeks" :key="week.id">
                        <div class="bg-white rounded-xl shadow-lg min-h-[250px] border border-gray-100 overflow-hidden flex flex-col transition-colors"
                             :class="{'ring-2 ring-blue-400': week.isCurrent}"
                             @dragover.prevent
                             @drop="handleDrop($event, week)">
                            
                            <!-- Week Header -->
                            <div class="p-3 border-b flex justify-between items-center" 
                                 :class="week.isCurrent ? 'bg-blue-50 border-blue-100' : 'bg-green-50 border-green-100'">
                                <h3 class="font-semibold text-gray-700 text-sm" x-text="week.label"></h3>
                                <button @click="openModal(null, week.startDateStr)" class="text-gray-400 hover:text-green-600 transition text-lg leading-none" title="إضافة لهذا الأسبوع">+</button>
                            </div>

                            <!-- Drop Zone / Items -->
                            <div class="p-3 flex-1 space-y-3">
                                <template x-for="item in getNewsForWeek(week)" :key="item.id">
                                    <div draggable="true" @dragstart="handleDragStart($event, item)"
                                         @click="openModal(item)" 
                                         dir="rtl"
                                         class="p-3 rounded-lg border-r-4 bg-white shadow-md cursor-pointer hover:shadow-lg hover:scale-[1.02] transition-all duration-200 group relative text-right"
                                         :class="{
                                            'border-green-500': item.status === 'published',
                                            'border-yellow-500': item.status === 'scheduled',
                                            'border-gray-400': item.status === 'draft'
                                         }">
                                        
                                        <!-- Card Header -->
                                        <div class="flex justify-between items-start mb-2">
                                            <div class="flex items-center gap-2">
                                                <span class="text-xs font-bold px-1.5 py-0.5 rounded text-white"
                                                      :class="item.impactTier === 'Tier 1' ? 'bg-red-500' : 'bg-gray-400'"
                                                      x-text="item.impactTier === 'Tier 1' ? 'T1' : 'T2'"></span>
                                                <span class="text-xs text-gray-500" x-text="item.country"></span>
                                            </div>
                                            <!-- Delete Button with @click.stop -->
                                            <button @click.stop="deleteNews(item.id)" class="text-red-300 hover:text-red-600 opacity-0 group-hover:opacity-100 transition px-1">×</button>
                                        </div>

                                        <!-- Title -->
                                        <h4 class="font-bold text-gray-800 text-sm mb-2 line-clamp-2 leading-tight" x-text="item.title"></h4>

                                        <!-- Footer -->
                                        <div class="flex justify-between items-center text-xs text-gray-500 border-t border-gray-100 pt-2 mt-1">
                                            <div class="flex items-center gap-1">
                                                <span class="font-medium text-gray-700" x-text="item.platformName"></span>
                                                <span class="text-gray-300">|</span>
                                                <span x-text="item.time"></span>
                                            </div>
                                            
                                            <!-- Approval Toggle with @click.stop -->
                                            <button @click.stop="toggleApproval(item)" 
                                                    class="w-8 h-4 rounded-full relative transition-colors duration-200 focus:outline-none"
                                                    :class="item.clientApproved ? 'bg-green-500' : 'bg-gray-300'">
                                                <span class="absolute right-0.5 top-0.5 w-3 h-3 bg-white rounded-full shadow transform transition-transform duration-200"
                                                      :class="item.clientApproved ? '-translate-x-4' : 'translate-x-0'"></span>
                                            </button>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Load More Button -->
                <div class="flex justify-center mt-8 pb-8">
                    <button @click="loadMoreWeeks()" class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 px-6 py-3 rounded-lg shadow-sm transition font-medium flex items-center gap-2">
                        <span>+ أضف 4 أسابيع أخرى</span>
                    </button>
                </div>
            </div>

            <!-- Table View -->
            <div x-show="viewMode === 'table'" class="bg-white rounded-xl shadow overflow-hidden">
                <table class="w-full text-right">
                    <thead class="bg-gray-50 border-b border-gray-200">
                        <tr>
                            <th class="p-4 font-semibold text-gray-600 text-sm">العنوان</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">المنصة</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">الدولة</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">التأثير</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">التاريخ</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">الحالة</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">موافقة مالك المشروع</th>
                            <th class="p-4 font-semibold text-gray-600 text-sm">إجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        <template x-for="item in newsItems" :key="item.id">
                            <tr class="border-b border-gray-100 hover:bg-gray-50 transition">
                                <td class="p-4 font-medium text-gray-800 text-sm" x-text="item.title"></td>
                                <td class="p-4 text-gray-600 text-sm" x-text="item.platformName"></td>
                                <td class="p-4 text-gray-600 text-sm" x-text="item.country"></td>
                                <td class="p-4 text-gray-600 text-sm">
                                    <span class="px-2 py-1 rounded text-xs font-bold text-white"
                                          :class="item.impactTier === 'Tier 1' ? 'bg-red-500' : 'bg-gray-400'"
                                          x-text="item.impactTier === 'Tier 1' ? 'T1' : 'T2'"></span>
                                </td>
                                <td class="p-4 text-gray-600 text-sm" x-text="formatDateDisplay(item.date)"></td>
                                <td class="p-4">
                                    <span class="px-2 py-1 rounded-full text-xs font-semibold"
                                          :class="{
                                            'bg-green-100 text-green-700': item.status === 'published',
                                            'bg-yellow-100 text-yellow-700': item.status === 'scheduled',
                                            'bg-gray-100 text-gray-700': item.status === 'draft'
                                          }" x-text="item.status"></span>
                                </td>
                                <td class="p-4">
                                    <button @click="toggleApproval(item)" 
                                            class="w-10 h-5 rounded-full relative transition-colors duration-200 focus:outline-none"
                                            :class="item.clientApproved ? 'bg-green-500' : 'bg-gray-300'">
                                        <span class="absolute right-0.5 top-0.5 w-4 h-4 bg-white rounded-full shadow transform transition-transform duration-200"
                                              :class="item.clientApproved ? '-translate-x-5' : 'translate-x-0'"></span>
                                    </button>
                                </td>
                                <td class="p-4 flex gap-2">
                                    <button @click="openModal(item)" class="text-blue-600 hover:text-blue-800 text-sm font-medium">تعديل</button>
                                    <button @click="deleteNews(item.id)" class="text-red-600 hover:text-red-800 text-sm font-medium">حذف</button>
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>

            <!-- Add/Edit Modal -->
            <div x-show="isModalOpen" class="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm" style="display: none;">
                <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg p-6 transform transition-all max-h-[90vh] overflow-y-auto" @click.away="closeModal()">
                    <h3 class="text-xl font-bold text-gray-800 mb-4" x-text="currentItem.id ? 'تعديل الخبر' : 'إضافة خبر جديد'"></h3>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div class="col-span-2">
                            <label class="block text-sm font-medium text-gray-700 mb-1">العنوان</label>
                            <input type="text" x-model="currentItem.title" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>
                        
                        <!-- Cascading Filters -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">نطاق التغطية</label>
                            <select x-model="selectedScope" 
                                    @change="currentItem.scope = selectedScope; currentItem.platformName = ''; isManualPlatform = false;"
                                    class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                <option value="السعودية/محلي">السعودية/محلي</option>
                                <option value="إقليمي/الخليج">إقليمي/الخليج</option>
                                <option value="دولي/عالمي">دولي/عالمي</option>
                                <option value="معتمدة من البنك الدولي">معتمدة من البنك الدولي</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">مستوى التأثير</label>
                            <select x-model="selectedTier" 
                                    @change="currentItem.impactTier = selectedTier; currentItem.platformName = ''; isManualPlatform = false;"
                                    class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                <option value="Tier 1">Tier 1</option>
                                <option value="Tier 2">Tier 2</option>
                                <option value="متخصصة">متخصصة</option>
                            </select>
                        </div>

                        <div class="col-span-2">
                            <label class="block text-sm font-medium text-gray-700 mb-1">المنصة</label>
                            
                            <!-- Dropdown Mode -->
                            <div x-show="!isManualPlatform" class="relative">
                                <select x-model="currentItem.platformName" 
                                        @change="if($event.target.value === 'other') { isManualPlatform = true; currentItem.platformName = ''; }"
                                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                    <option value="">اختر المنصة</option>
                                    <template x-for="media in filteredPlatforms" :key="media.name">
                                        <option :value="media.name" x-text="media.name"></option>
                                    </template>
                                    <option value="other" class="font-bold text-blue-600">أخرى (إدخال يدوي)...</option>
                                </select>
                            </div>

                            <!-- Manual Input Mode -->
                            <div x-show="isManualPlatform" class="flex gap-2" style="display: none;">
                                <input type="text" x-model="currentItem.platformName" placeholder="أدخل اسم المنصة يدوياً" class="flex-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                <button @click="isManualPlatform = false; currentItem.platformName = '';" class="px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-gray-600" title="عودة للقائمة">
                                    ↩
                                </button>
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">الوقت</label>
                            <input type="time" x-model="currentItem.time" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">التاريخ</label>
                            <input type="date" x-model="currentItem.date" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">الحالة</label>
                            <select x-model="currentItem.status" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                <option value="draft">مسودة</option>
                                <option value="scheduled">مجدول</option>
                                <option value="published">منشور</option>
                            </select>
                        </div>

                        <!-- Modal Toggle Switch -->
                        <div class="flex items-center justify-between bg-gray-50 p-2 rounded-lg border border-gray-200">
                            <span class="text-sm font-medium text-gray-700">موافقة مالك المشروع</span>
                            <button @click="if(!currentItem.clientApproved) { 
                                        openPinModal('اعتماد المالك', 'أدخل الرمز السري للموافقة.', '53100', () => { currentItem.clientApproved = true; });
                                    } else { 
                                        currentItem.clientApproved = false; 
                                    }" 
                                    type="button"
                                    class="w-10 h-5 rounded-full relative transition-colors duration-200 focus:outline-none"
                                    :class="currentItem.clientApproved ? 'bg-green-500' : 'bg-gray-300'">
                                <span class="absolute right-0.5 top-0.5 w-4 h-4 bg-white rounded-full shadow transform transition-transform duration-200"
                                      :class="currentItem.clientApproved ? '-translate-x-5' : 'translate-x-0'"></span>
                            </button>
                        </div>

                        <div class="col-span-2">
                            <label class="block text-sm font-medium text-gray-700 mb-1">رابط الخبر</label>
                            <input type="url" x-model="currentItem.newsLink" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                        </div>

                        <!-- Details Textarea -->
                        <div class="col-span-2">
                            <label class="block text-sm font-medium text-gray-700 mb-1">التفاصيل</label>
                            <textarea x-model="currentItem.details" rows="4" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"></textarea>
                        </div>
                    </div>

                    <div class="flex justify-between items-center mt-6 pt-4 border-t border-gray-100">
                        <!-- Delete Button (Only if editing) -->
                        <div>
                            <button x-show="currentItem.id" @click="deleteNews(currentItem.id)" class="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition font-medium">حذف</button>
                        </div>
                        <div class="flex gap-3">
                            <button @click="closeModal()" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition font-medium">إلغاء</button>
                            <button @click="saveNews()" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition shadow font-medium">حفظ</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PIN Verification Modal (High Z-Index) -->
            <div x-show="pinModal.isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm" style="display: none;">
                <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm p-6 transform transition-all scale-100" @click.away="closePinModal()">
                    <div class="text-center mb-6">
                        <div class="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                            <span class="text-2xl">🔒</span>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800" x-text="pinModal.title"></h3>
                        <p class="text-gray-500 text-sm mt-1" x-text="pinModal.description"></p>
                    </div>
                    
                    <div class="mb-6">
                        <input type="password" id="pinInput" x-model="pinModal.input" 
                               @keydown.enter="confirmPin()"
                               placeholder="أدخل الرمز السري" 
                               class="w-full text-center text-2xl tracking-widest p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                    </div>

                    <div class="flex gap-3">
                        <button @click="closePinModal()" class="flex-1 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition font-medium">إلغاء</button>
                        <button @click="confirmPin()" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition shadow font-medium">تأكيد</button>
                    </div>
                </div>
            </div>

            <!-- AI Import Modal -->
            <div x-show="isAIModalOpen" class="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm" style="display: none;">
                <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg p-6" @click.away="closeAIModal()">
                    <h3 class="text-xl font-bold text-gray-800 mb-4">🤖 استيراد ذكي بالذكاء الاصطناعي</h3>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">مفتاح Gemini API</label>
                            <div class="flex gap-2">
                                <input type="password" x-model="aiApiKey" placeholder="الصق مفتاح API هنا" class="flex-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none">
                                <button @click="saveApiKey()" class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm font-medium">حفظ المفتاح</button>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">رفع ملف الروزنامة (CSV, TXT, PDF)</label>
                            <input type="file" x-ref="fileInput" class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">المحتوى / التوجيه</label>
                            <textarea x-model="aiPrompt" rows="4" placeholder="الصق نص الأخبار أو تعليمات إضافية..." class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"></textarea>
                        </div>
                    </div>

                    <div class="flex justify-end gap-3 mt-6">
                        <button @click="closeAIModal()" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition font-medium">إلغاء</button>
                        <button @click="processAIImport()" :disabled="isProcessingAI" class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition shadow font-medium flex items-center gap-2">
                            <span x-show="isProcessingAI" class="animate-spin">↻</span>
                            <span x-text="isProcessingAI ? 'جاري المعالجة...' : 'تحليل واستيراد'"></span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- AI Staging Review Modal -->
            <div x-show="isStagingOpen" class="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm" style="display: none;">
                <div class="bg-white rounded-xl shadow-2xl w-full max-w-4xl p-6 max-h-[90vh] overflow-y-auto">
                    <h3 class="text-xl font-bold text-gray-800 mb-4">مراجعة البيانات المستوردة</h3>
                    
                    <div class="overflow-x-auto border rounded-lg">
                        <table class="w-full text-right text-sm">
                            <thead class="bg-gray-50 border-b">
                                <tr>
                                    <th class="p-3">العنوان</th>
                                    <th class="p-3">المنصة</th>
                                    <th class="p-3">التاريخ</th>
                                    <th class="p-3">المستوى</th>
                                    <th class="p-3">الدولة</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="(item, index) in aiStagingData" :key="index">
                                    <tr class="border-b hover:bg-gray-50">
                                        <td class="p-2">
                                            <input type="text" x-model="item.title" class="w-full p-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none text-sm">
                                        </td>
                                        <td class="p-2">
                                            <input type="text" x-model="item.platformName" class="w-full p-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none text-sm">
                                        </td>
                                        <td class="p-2">
                                            <input type="date" x-model="item.date" class="w-full p-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none text-sm">
                                        </td>
                                        <td class="p-2">
                                            <select x-model="item.impactTier" class="w-full p-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none text-sm">
                                                <option value="Tier 1">Tier 1</option>
                                                <option value="Tier 2">Tier 2</option>
                                                <option value="Devex">Devex</option>
                                            </select>
                                        </td>
                                        <td class="p-2">
                                            <select x-model="item.country" class="w-full p-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none text-sm">
                                                <option value="السعودية">السعودية</option>
                                                <option value="إقليمي">إقليمي</option>
                                                <option value="دولي">دولي</option>
                                            </select>
                                        </td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>

                    <div class="flex justify-end gap-3 mt-6">
                        <button @click="isStagingOpen = false" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition font-medium">تجاهل</button>
                        <button @click="saveStagingData()" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition shadow font-medium">تأكيد وحفظ (يتطلب رمز)</button>
                    </div>
                </div>
            </div>

        </div>
    `;

    console.log("NewsManager Modal & Data Structure Updated");
}
