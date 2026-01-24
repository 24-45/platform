(() => {
    // Helper function to get base path for GitHub Pages
    const getBasePath = () => window.location.hostname.includes('github.io') ? '/awqaf' : '';

    const SERIES_CONFIG = [
        { key: 'Original Posts', label: 'منشورات الحساب', color: '#3498db', icon: '📝', description: 'المحتوى الأصلي المنشور' },
        { key: 'Reposts', label: 'إعادات النشر', color: '#e74c3c', icon: '🔄', description: 'المحتوى المُعاد نشره' },
        { key: 'Quote Posts', label: 'الاقتباسات', color: '#27ae60', icon: '💬', description: 'منشورات مقتبسة مع تعليق' },
        { key: 'Replies', label: 'الردود', color: '#9b59b6', icon: '↩️', description: 'ردود على المتابعين' },
        { key: 'Direct Messages', label: 'الرسائل الخاصة', color: '#95a5a6', icon: '✉️', description: 'رسائل خاصة' }
    ];

    const TYPE_MAP = {
        'social post': 'Original Posts',
        'original post': 'Original Posts',
        'social': 'Original Posts',
        'repost': 'Reposts',
        'retweet': 'Reposts',
        'quote': 'Quote Posts',
        'quote post': 'Quote Posts',
        'quote tweet': 'Quote Posts',
        'reply': 'Replies',
        'direct message': 'Direct Messages'
    };

    const rootEl = document.getElementById('post-type-trend-root');
    const cardsEl = document.getElementById('post-type-summary-cards');
    const insightsEl = document.getElementById('post-type-insights');

    if (!rootEl || typeof Plotly === 'undefined') {
        return;
    }

    const showStatus = (message, isError = false) => {
        rootEl.innerHTML = `<div class="chart-status${isError ? ' error' : ''}">${message}</div>`;
    };

    const createZeroTotals = () => SERIES_CONFIG.reduce((acc, series) => {
        acc[series.key] = 0;
        return acc;
    }, { All: 0 });

    const sanitize = (text) => text.replace(/\ufeff/g, '');

    const formatArabicDate = (isoDate) => {
        const parsed = new Date(`${isoDate}T00:00:00`);
        if (Number.isNaN(parsed.getTime())) {
            return isoDate;
        }
        return parsed.toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    };

    const formatShortDate = (isoDate) => {
        const parsed = new Date(`${isoDate}T00:00:00`);
        if (Number.isNaN(parsed.getTime())) {
            return isoDate;
        }
        return parsed.toLocaleDateString('ar-EG-u-nu-latn', {
            day: 'numeric',
            month: 'short'
        });
    };

    const parseCsv = (rawText) => {
        const rows = sanitize(rawText).split(/\r?\n/).filter(Boolean);
        if (rows.length <= 1) {
            return { data: [], totals: createZeroTotals() };
        }

        const headers = rows[0].split('\t');
        const dateIdx = headers.indexOf('Date');
        const typeIdx = headers.indexOf('Content Type');

        if (dateIdx === -1 || typeIdx === -1) {
            return { data: [], totals: createZeroTotals(), error: 'ملف البيانات يفتقد الأعمدة المطلوبة.' };
        }

        const totals = createZeroTotals();
        const aggregation = new Map();
        const peakData = {};

        // Initialize peak tracking
        SERIES_CONFIG.forEach((series) => {
            peakData[series.key] = { value: 0, date: '' };
        });

        for (let i = 1; i < rows.length; i += 1) {
            const cells = rows[i].split('\t');
            const rawDate = (cells[dateIdx] || '').trim();
            const rawType = (cells[typeIdx] || '').trim();

            if (!rawDate) {
                continue;
            }

            if (!aggregation.has(rawDate)) {
                const baseEntry = { date: rawDate };
                SERIES_CONFIG.forEach((series) => {
                    baseEntry[series.key] = 0;
                });
                baseEntry.All = 0;
                aggregation.set(rawDate, baseEntry);
            }

            const entry = aggregation.get(rawDate);
            entry.All += 1;
            totals.All += 1;

            const normalized = TYPE_MAP[rawType.toLowerCase()] || null;
            if (normalized) {
                entry[normalized] += 1;
                totals[normalized] += 1;

                // Track peak
                if (entry[normalized] > peakData[normalized].value) {
                    peakData[normalized].value = entry[normalized];
                    peakData[normalized].date = rawDate;
                }
            }
        }

        const data = Array.from(aggregation.values()).sort((a, b) => new Date(a.date) - new Date(b.date));
        return { data, totals, peakData };
    };

    const renderSummaryCards = (totals, peakData) => {
        if (!cardsEl) return;

        const grandTotal = totals.All || 1;
        
        const cardsHTML = SERIES_CONFIG.filter(series => totals[series.key] > 0).map(series => {
            const total = totals[series.key] || 0;
            const percentage = ((total / grandTotal) * 100).toFixed(1);
            const peak = peakData[series.key] || { value: 0, date: '' };
            const peakDateFormatted = peak.date ? formatShortDate(peak.date) : '-';

            return `
                <div class="post-type-card" data-type="${series.key}" style="--card-color: ${series.color}">
                    <div class="card-icon">${series.icon}</div>
                    <div class="card-content">
                        <div class="card-label">${series.label}</div>
                        <div class="card-value">${total.toLocaleString('en-US')}</div>
                        <div class="card-meta">
                            <span class="card-percentage">${percentage}%</span>
                            <span class="card-separator">•</span>
                            <span class="card-peak" title="أعلى نشاط">🔥 ${peak.value.toLocaleString('en-US')} (${peakDateFormatted})</span>
                        </div>
                    </div>
                    <div class="card-bar" style="width: ${percentage}%"></div>
                </div>
            `;
        }).join('');

        // Add total card
        const totalCard = `
            <div class="post-type-card total-card" data-type="All">
                <div class="card-icon">📊</div>
                <div class="card-content">
                    <div class="card-label">إجمالي المنشورات</div>
                    <div class="card-value">${grandTotal.toLocaleString('en-US')}</div>
                    <div class="card-meta">
                        <span class="card-percentage">100%</span>
                    </div>
                </div>
            </div>
        `;

        cardsEl.innerHTML = totalCard + cardsHTML;

        // Add click interactivity
        cardsEl.querySelectorAll('.post-type-card').forEach(card => {
            card.addEventListener('click', () => {
                const type = card.dataset.type;
                highlightSeries(type);
                
                // Toggle active state
                cardsEl.querySelectorAll('.post-type-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');
            });
        });
    };

    const renderInsights = (data, totals, peakData) => {
        if (!insightsEl || data.length < 2) return;

        // Calculate comprehensive analytics
        const recentDays = Math.min(7, data.length);
        const recentData = data.slice(-recentDays);
        const previousData = data.slice(-recentDays * 2, -recentDays);
        const firstHalf = data.slice(0, Math.floor(data.length / 2));
        const secondHalf = data.slice(Math.floor(data.length / 2));

        const insights = [];

        // 1. Content Strategy Analysis
        const sortedTypes = SERIES_CONFIG
            .filter(s => totals[s.key] > 0)
            .sort((a, b) => totals[b.key] - totals[a.key]);

        if (sortedTypes.length > 0) {
            const topType = sortedTypes[0];
            const topPercentage = ((totals[topType.key] / totals.All) * 100).toFixed(0);
            const secondType = sortedTypes[1];
            const secondPercentage = secondType ? ((totals[secondType.key] / totals.All) * 100).toFixed(0) : 0;
            
            let strategyInsight = `${topType.label} هو النوع السائد بنسبة ${topPercentage}%`;
            if (topPercentage > 70) {
                strategyInsight += ' - يُوصى بتنويع المحتوى لزيادة التفاعل';
            } else if (secondType) {
                strategyInsight += `، يليه ${secondType.label} بـ ${secondPercentage}%`;
            }
            
            insights.push({
                icon: '📊',
                title: 'استراتيجية المحتوى',
                text: strategyInsight
            });
        }

        // 2. Peak Performance Analysis
        let globalPeak = { type: '', value: 0, date: '', key: '' };
        SERIES_CONFIG.forEach(series => {
            if (peakData[series.key] && peakData[series.key].value > globalPeak.value) {
                globalPeak = {
                    type: series.label,
                    value: peakData[series.key].value,
                    date: peakData[series.key].date,
                    key: series.key
                };
            }
        });

        if (globalPeak.date) {
            const peakDateObj = new Date(globalPeak.date);
            const dayName = peakDateObj.toLocaleDateString('ar-EG-u-nu-latn', { weekday: 'long' });
            insights.push({
                icon: '🔥',
                title: 'ذروة الأداء',
                text: `أعلى نشاط في ${formatShortDate(globalPeak.date)} (${dayName}) بـ ${globalPeak.value.toLocaleString('en-US')} ${globalPeak.type}`
            });
        }

        // 3. Publishing Consistency & Frequency
        const activeDays = data.filter(d => d.All > 0).length;
        const consistencyRate = ((activeDays / data.length) * 100).toFixed(0);
        const avgPerActiveDay = (totals.All / activeDays).toFixed(1);
        
        let consistencyText = `معدل الانتظام ${consistencyRate}% - `;
        if (consistencyRate >= 80) {
            consistencyText += `نشاط منتظم ممتاز (${avgPerActiveDay} منشور/يوم نشط)`;
        } else if (consistencyRate >= 60) {
            consistencyText += `نشاط جيد مع فرص للتحسين (${avgPerActiveDay} منشور/يوم نشط)`;
        } else {
            consistencyText += `يُنصح بزيادة انتظام النشر (${avgPerActiveDay} منشور/يوم نشط)`;
        }
        
        insights.push({
            icon: '📅',
            title: 'انتظام النشر',
            text: consistencyText
        });

        // 4. Growth Trend Analysis
        if (previousData.length > 0 && recentData.length > 0) {
            const prevTotal = previousData.reduce((sum, d) => sum + d.All, 0);
            const recentTotal = recentData.reduce((sum, d) => sum + d.All, 0);
            const change = prevTotal > 0 ? ((recentTotal - prevTotal) / prevTotal * 100).toFixed(0) : 0;
            
            let trendIcon, trendText;
            if (Math.abs(change) < 5) {
                trendIcon = '➡️';
                trendText = `نشاط مستقر في آخر ${recentDays} أيام (${recentTotal.toLocaleString('en-US')} منشور)`;
            } else if (change > 0) {
                trendIcon = '📈';
                trendText = `نمو إيجابي بـ ${change}% - استمرار الزخم الحالي موصى به`;
            } else {
                trendIcon = '📉';
                trendText = `انخفاض بـ ${Math.abs(change)}% - يُنصح بمراجعة استراتيجية النشر`;
            }
            
            insights.push({
                icon: trendIcon,
                title: 'اتجاه النمو',
                text: trendText
            });
        }

        // 5. Engagement Distribution Analysis
        const engagementTypes = SERIES_CONFIG.filter(s => 
            ['Replies', 'Quote Posts', 'Reposts'].includes(s.key) && totals[s.key] > 0
        );
        
        if (engagementTypes.length > 0) {
            const engagementTotal = engagementTypes.reduce((sum, s) => sum + totals[s.key], 0);
            const engagementRate = ((engagementTotal / totals.All) * 100).toFixed(0);
            
            let engagementText = `نسبة التفاعل ${engagementRate}% من المحتوى`;
            if (engagementRate > 25) {
                engagementText += ' - مستوى تفاعل ممتاز';
            } else if (engagementRate > 15) {
                engagementText += ' - تفاعل جيد';
            } else {
                engagementText += ' - يمكن تعزيز التفاعل مع الجمهور';
            }
            
            insights.push({
                icon: '💬',
                title: 'مستوى التفاعل',
                text: engagementText
            });
        }

        // 6. Temporal Pattern Analysis
        if (firstHalf.length > 0 && secondHalf.length > 0) {
            const firstHalfTotal = firstHalf.reduce((sum, d) => sum + d.All, 0);
            const secondHalfTotal = secondHalf.reduce((sum, d) => sum + d.All, 0);
            const firstHalfAvg = (firstHalfTotal / firstHalf.length).toFixed(1);
            const secondHalfAvg = (secondHalfTotal / secondHalf.length).toFixed(1);
            
            if (secondHalfAvg > firstHalfAvg * 1.2) {
                insights.push({
                    icon: '⚡',
                    title: 'نمط النشاط',
                    text: `تسارع ملحوظ في النصف الثاني من الفترة - متوسط ${secondHalfAvg} مقابل ${firstHalfAvg} يومياً`
                });
            } else if (secondHalfAvg < firstHalfAvg * 0.8) {
                insights.push({
                    icon: '⚠️',
                    title: 'نمط النشاط',
                    text: `تباطؤ في النصف الثاني من الفترة - متوسط ${secondHalfAvg} مقابل ${firstHalfAvg} يومياً`
                });
            }
        }

        insightsEl.innerHTML = `
            <div class="insights-title">💡 نظرة عامة لتحليل أداء حساب الهيئة في منصة X</div>
            <div class="insights-grid">
                ${insights.map(insight => `
                    <div class="insight-item">
                        <span class="insight-icon">${insight.icon}</span>
                        <div class="insight-content">
                            <div class="insight-title">${insight.title}</div>
                            <div class="insight-text">${insight.text}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    };

    let currentChart = null;

    const highlightSeries = (typeKey) => {
        if (!currentChart) return;

        const gd = rootEl;
        const updates = gd.data.map((trace, idx) => {
            if (typeKey === 'All') {
                return { visible: true, 'line.width': trace.name.includes('الكل') ? 3 : 2 };
            }
            
            const seriesConfig = SERIES_CONFIG.find(s => trace.name.includes(s.label));
            if (seriesConfig && seriesConfig.key === typeKey) {
                return { visible: true, 'line.width': 4, 'fillcolor': seriesConfig.color + '40' };
            }
            return { visible: 'legendonly' };
        });

        updates.forEach((update, idx) => {
            Plotly.restyle(gd, update, [idx]);
        });
    };

    const renderChart = (data, totals, peakData) => {
        if (!data.length) {
            showStatus('لا توجد بيانات متاحة لعرض اتجاه أنواع المنشورات.');
            return;
        }

        // Render summary cards first
        renderSummaryCards(totals, peakData);
        renderInsights(data, totals, peakData);

        const customDates = data.map((entry) => formatArabicDate(entry.date));

        // Create traces with enhanced styling
        const traces = SERIES_CONFIG.map((series) => {
            const yValues = data.map((entry) => entry[series.key]);
            const hasValues = yValues.some((value) => value > 0);
            
            if (!hasValues) return null;

            return {
                x: data.map((entry) => entry.date),
                y: yValues,
                customdata: customDates,
                text: yValues.map((value) => value.toLocaleString('en-US')),
                name: `${series.label} (${(totals[series.key] || 0).toLocaleString('en-US')})`,
                mode: 'lines+markers',
                line: {
                    color: series.color,
                    width: 3,
                    shape: 'spline',
                    smoothing: 1.2
                },
                marker: {
                    color: series.color,
                    size: 4,
                    opacity: 0.8
                },
                fill: 'tonexty',
                fillcolor: series.color + '20',
                hovertemplate: 
                    '<b>%{customdata}</b><br>' +
                    `<span style="color:${series.color}">●</span> ${series.label}: <b>%{text}</b>` +
                    '<extra></extra>'
            };
        }).filter(Boolean);

        // Add "All" trace
        const allYValues = data.map((entry) => entry.All || 0);
        traces.unshift({
            x: data.map((entry) => entry.date),
            y: allYValues,
            customdata: customDates,
            text: allYValues.map((value) => value.toLocaleString('en-US')),
            name: `الكل (${totals.All.toLocaleString('en-US')})`,
            mode: 'lines+markers',
            line: {
                color: '#00502F',
                width: 4,
                shape: 'spline',
                smoothing: 1.2,
                dash: 'dashdot'
            },
            marker: {
                color: '#00502F',
                size: 6,
                opacity: 0.9,
                symbol: 'diamond'
            },
            hovertemplate: 
                '<b>%{customdata}</b><br>' +
                `<span style="color:#00502F">◆</span> الكل: <b>%{text}</b>` +
                '<extra></extra>'
        });

        if (!traces.length) {
            showStatus('لا توجد بيانات متاحة لعرض اتجاه أنواع المنشورات.');
            return;
        }

        rootEl.innerHTML = '';

        // Get container width for proper sizing
        const containerWidth = rootEl.parentElement?.offsetWidth || rootEl.offsetWidth || window.innerWidth - 100;
        const chartHeight = 500;

        const layout = {
            margin: { l: 70, r: 40, t: 30, b: 120 },
            paper_bgcolor: 'rgba(255,255,255,0)',
            plot_bgcolor: 'rgba(248,250,252,0.3)',
            font: {
                family: 'Tajawal, Arial, sans-serif',
                size: 12,
                color: '#374151'
            },
            xaxis: {
                tickangle: -45,
                tickfont: { size: 11, color: '#6b7280', family: 'Tajawal, Arial, sans-serif' },
                showgrid: true,
                gridcolor: 'rgba(229, 231, 235, 0.8)',
                gridwidth: 1,
                zeroline: false,
                tickformat: '%d/%m',
                nticks: Math.min(12, data.length),
                showline: true,
                linecolor: '#d1d5db',
                linewidth: 1,
                title: {
                    text: 'التاريخ',
                    font: { size: 12, color: '#9ca3af', family: 'Tajawal, Arial, sans-serif' },
                    standoff: 20
                }
            },
            yaxis: {
                rangemode: 'tozero',
                tickfont: { size: 11, color: '#6b7280', family: 'Tajawal, Arial, sans-serif' },
                gridcolor: 'rgba(229, 231, 235, 0.6)',
                gridwidth: 1,
                zeroline: true,
                zerolinecolor: '#e5e7eb',
                zerolinewidth: 1,
                showline: true,
                linecolor: '#d1d5db',
                linewidth: 1,
                title: {
                    text: 'عدد المنشورات',
                    font: { size: 12, color: '#9ca3af', family: 'Tajawal, Arial, sans-serif' },
                    standoff: 20
                }
            },
            legend: {
                orientation: 'h',
                x: 0.5,
                y: -0.25,
                xanchor: 'center',
                font: {
                    size: 10,
                    family: 'Tajawal, Arial, sans-serif',
                    color: '#4b5563'
                },
                bgcolor: 'rgba(255,255,255,0.95)',
                bordercolor: '#e5e7eb',
                borderwidth: 1,
                itemsizing: 'constant',
                itemwidth: 30
            },
            hovermode: 'x unified',
            hoverlabel: {
                bgcolor: 'rgba(255,255,255,0.95)',
                bordercolor: '#e5e7eb',
                borderwidth: 1,
                font: { family: 'Tajawal, Arial, sans-serif', size: 11, color: '#374151' },
                align: 'right'
            },
            showlegend: true,
            autosize: true,
            width: containerWidth,
            height: chartHeight
        };

        const config = {
            responsive: true,
            displaylogo: false,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'select2d', 'lasso2d', 'autoScale2d', 'toggleSpikelines'],
            modeBarButtonsToAdd: ['resetScale2d'],
            toImageButtonOptions: {
                format: 'png',
                filename: 'post_type_trend_awqaf',
                height: 600,
                width: 1200,
                scale: 2
            }
        };

        Plotly.newPlot(rootEl, traces, layout, config).then(() => {
            // Force resize to ensure proper display
            setTimeout(() => {
                Plotly.Plots.resize(rootEl);
            }, 100);
        });
        currentChart = rootEl;

        // Enhanced legend click behavior
        rootEl.on('plotly_legendclick', (eventData) => {
            if (!eventData || typeof eventData.curveNumber !== 'number') {
                return false;
            }

            const gd = rootEl;
            const targetIndex = eventData.curveNumber;
            const currentVisibility = gd.data.map((trace) => 
                (typeof trace.visible === 'undefined' ? true : trace.visible)
            );
            
            const isAlreadyIsolated = currentVisibility.every((value, idx) => (
                idx === targetIndex ? value !== 'legendonly' : value === 'legendonly'
            ));

            gd.data.forEach((_, idx) => {
                const shouldShowAll = isAlreadyIsolated;
                const nextVisibility = shouldShowAll ? true : (idx === targetIndex ? true : 'legendonly');
                Plotly.restyle(gd, { visible: nextVisibility }, [idx]);
            });

            // Update card states
            if (cardsEl) {
                cardsEl.querySelectorAll('.post-type-card').forEach(card => {
                    card.classList.remove('active');
                });
                
                if (!isAlreadyIsolated) {
                    const traceName = gd.data[targetIndex].name;
                    const matchingCard = Array.from(cardsEl.querySelectorAll('.post-type-card')).find(card => {
                        const cardType = card.dataset.type;
                        const series = SERIES_CONFIG.find(s => s.key === cardType);
                        return series && traceName.includes(series.label);
                    });
                    if (matchingCard) matchingCard.classList.add('active');
                }
            }

            return false;
        });

        // Add animation on hover
        rootEl.on('plotly_hover', () => {
            rootEl.style.cursor = 'crosshair';
        });

        rootEl.on('plotly_unhover', () => {
            rootEl.style.cursor = 'default';
        });
    };

    // Fetch and render
    showStatus('جارٍ تحميل البيانات...');
    
    fetch(getBasePath() + '/static/data/fromawqaf_ksa.csv?cache=' + Date.now())
        .then((res) => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.text();
        })
        .then((text) => {
            const { data, totals, peakData, error } = parseCsv(text);
            if (error) {
                showStatus(error, true);
                return;
            }
            renderChart(data, totals, peakData);
        })
        .catch((err) => {
            showStatus(`فشل تحميل بيانات اتجاه أنواع المنشورات: ${err.message}`, true);
        });
})();
