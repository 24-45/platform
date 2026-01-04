/**
 * Current Status Tab - Interactive Charts & Animations
 * مخططات تفاعلية وأرقام متحركة لتاب الوضع الراهن
 */

// Wait for DOM
document.addEventListener('DOMContentLoaded', function() {
    // Initialize when tab becomes visible
    initCurrentStatusTab();
});

function initCurrentStatusTab() {
    const tabLink = document.querySelector('a[data-tab="current-status"]');
    if (tabLink) {
        tabLink.addEventListener('click', function() {
            setTimeout(() => {
                initAllCharts();
                initAnimatedCounters();
                initAmmanMap();
            }, 300);
        });
    }
    
    // Also check if already on the tab
    const currentTab = document.getElementById('current-status');
    if (currentTab && currentTab.classList.contains('active')) {
        setTimeout(() => {
            initAllCharts();
            initAnimatedCounters();
            initAmmanMap();
        }, 500);
    }
}

// =============================================
// ANIMATED COUNTERS
// =============================================
function initAnimatedCounters() {
    const counters = document.querySelectorAll('.cs-animated-number');
    
    counters.forEach(counter => {
        if (counter.dataset.animated === 'true') return;
        
        const target = parseFloat(counter.dataset.target);
        const suffix = counter.dataset.suffix || '';
        const duration = 2000;
        const startTime = performance.now();
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = target * easeOutQuart;
            
            if (Number.isInteger(target)) {
                counter.textContent = Math.floor(current) + suffix;
            } else {
                counter.textContent = current.toFixed(1) + suffix;
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + suffix;
                counter.dataset.animated = 'true';
            }
        }
        
        // Start animation when element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    requestAnimationFrame(updateCounter);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });
}

// =============================================
// CHART.JS CONFIGURATIONS
// =============================================
const chartColors = {
    primary: '#dc1f27',
    secondary: '#00D46A',
    blue: '#3b82f6',
    orange: '#f59e0b',
    purple: '#8b5cf6',
    pink: '#ec4899',
    cyan: '#06b6d4',
    gray: '#64748b'
};

const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            rtl: true,
            labels: {
                color: '#e2e8f0',
                padding: 20,
                font: {
                    family: 'Cairo, Tajawal, sans-serif',
                    size: 12
                }
            }
        },
        tooltip: {
            rtl: true,
            titleFont: {
                family: 'Cairo, Tajawal, sans-serif'
            },
            bodyFont: {
                family: 'Cairo, Tajawal, sans-serif'
            },
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            borderColor: 'rgba(220, 31, 39, 0.3)',
            borderWidth: 1,
            padding: 12
        }
    }
};

function initAllCharts() {
    initGeographicChart();
    initChallengesChart();
    initSatisfactionChart();
    initPriceRangeChart();
    initFacilitiesChart();
    initDesignPreferenceChart();
}

// Geographic Distribution Donut Chart
function initGeographicChart() {
    const ctx = document.getElementById('geographicChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['طبربور', 'رأس العين والجاردنز', 'المدينة الرياضية', 'ماركا', 'الجويدة ويادودة', 'وادي السير', 'مناطق أخرى'],
            datasets: [{
                data: [35.2, 28.7, 10.5, 10.2, 3.4, 2.6, 9.4],
                backgroundColor: [
                    chartColors.primary,
                    chartColors.secondary,
                    chartColors.blue,
                    chartColors.orange,
                    chartColors.purple,
                    chartColors.pink,
                    chartColors.gray
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            ...chartDefaults,
            cutout: '60%',
            plugins: {
                ...chartDefaults.plugins,
                legend: {
                    ...chartDefaults.plugins.legend,
                    position: 'right'
                }
            }
        }
    });
    ctx.dataset.initialized = 'true';
}

// Market Challenges Horizontal Bar Chart
function initChallengesChart() {
    const ctx = document.getElementById('challengesChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['التغيير المستمر في القوانين', 'ضعف الطلب', 'تغير طلب العملاء', 'ارتفاع الإيجارات', 'المنافسة', 'التسويق'],
            datasets: [{
                data: [49.4, 41.5, 32.4, 18.8, 17.6, 13.4],
                backgroundColor: [
                    chartColors.primary,
                    chartColors.orange,
                    chartColors.blue,
                    chartColors.purple,
                    chartColors.secondary,
                    chartColors.cyan
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            ...chartDefaults,
            indexAxis: 'y',
            plugins: {
                ...chartDefaults.plugins,
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' },
                    max: 60
                },
                y: {
                    grid: { display: false },
                    ticks: { 
                        color: '#e2e8f0',
                        font: { family: 'Cairo, Tajawal, sans-serif' }
                    }
                }
            }
        }
    });
    ctx.dataset.initialized = 'true';
}

// Satisfaction Pie Chart
function initSatisfactionChart() {
    const ctx = document.getElementById('satisfactionChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['راضٍ جداً', 'راضٍ', 'محايد', 'غير راضٍ', 'غير راضٍ إطلاقاً'],
            datasets: [{
                data: [8, 38.1, 1.7, 33, 19.3],
                backgroundColor: [
                    chartColors.secondary,
                    '#34d399',
                    chartColors.gray,
                    chartColors.orange,
                    chartColors.primary
                ],
                borderWidth: 0
            }]
        },
        options: {
            ...chartDefaults,
            plugins: {
                ...chartDefaults.plugins
            }
        }
    });
    ctx.dataset.initialized = 'true';
}

// Price Range Chart
function initPriceRangeChart() {
    const ctx = document.getElementById('priceRangeChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['أقل من 15,000 دينار', '15,000 - 30,000 دينار', '30,000 - 60,000 دينار', 'أكثر من 60,000 دينار'],
            datasets: [{
                data: [56.5, 31, 11.6, 0.9],
                backgroundColor: [
                    chartColors.blue,
                    chartColors.secondary,
                    chartColors.orange,
                    chartColors.purple
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            ...chartDefaults,
            cutout: '55%'
        }
    });
    ctx.dataset.initialized = 'true';
}

// Facilities Required Chart
function initFacilitiesChart() {
    const ctx = document.getElementById('facilitiesChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['بنوك وتمويل', 'فحص السيارات', 'مطاعم ومقاهي', 'محطة وقود', 'مرافق عامة', 'مركز خدمة', 'مسار تجربة'],
            datasets: [{
                data: [96, 90.1, 87.5, 87.5, 86.9, 84.1, 81.8],
                backgroundColor: chartColors.secondary,
                borderRadius: 8
            }]
        },
        options: {
            ...chartDefaults,
            plugins: {
                ...chartDefaults.plugins,
                legend: { display: false }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' },
                    min: 70,
                    max: 100
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        color: '#e2e8f0',
                        font: { family: 'Cairo, Tajawal, sans-serif', size: 10 }
                    }
                }
            }
        }
    });
    ctx.dataset.initialized = 'true';
}

// Design Preference Chart
function initDesignPreferenceChart() {
    const ctx = document.getElementById('designChart');
    if (!ctx || ctx.dataset.initialized) return;
    
    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: ['التصميم الأول', 'التصميم الثاني', 'التصميم الثالث'],
            datasets: [{
                data: [24.1, 15.6, 59.1],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(0, 212, 106, 0.8)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            ...chartDefaults,
            scales: {
                r: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { display: false }
                }
            }
        }
    });
    ctx.dataset.initialized = 'true';
}

// =============================================
// AMMAN MAP (Leaflet)
// =============================================
function initAmmanMap() {
    const mapContainer = document.getElementById('ammanMap');
    if (!mapContainer || mapContainer.dataset.initialized) return;
    
    // Amman coordinates
    const ammanCenter = [31.9539, 35.9106];
    
    const map = L.map('ammanMap', {
        center: ammanCenter,
        zoom: 11,
        zoomControl: true,
        scrollWheelZoom: false
    });
    
    // Dark theme tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        maxZoom: 19
    }).addTo(map);
    
    // Showroom distribution data
    const locations = [
        { name: 'طبربور', coords: [31.9981, 35.9483], count: 124, percentage: 35.2 },
        { name: 'رأس العين', coords: [31.9667, 35.8833], count: 101, percentage: 28.7 },
        { name: 'المدينة الرياضية', coords: [31.9847, 35.8639], count: 37, percentage: 10.5 },
        { name: 'ماركا', coords: [31.9722, 35.9833], count: 36, percentage: 10.2 },
        { name: 'الجويدة', coords: [31.8833, 35.9333], count: 12, percentage: 3.4 },
        { name: 'وادي السير', coords: [31.9333, 35.8167], count: 9, percentage: 2.6 }
    ];
    
    // Add markers with circles
    locations.forEach(loc => {
        // Circle size based on percentage
        const radius = loc.percentage * 150;
        
        L.circle(loc.coords, {
            color: '#dc1f27',
            fillColor: '#dc1f27',
            fillOpacity: 0.4,
            radius: radius,
            weight: 2
        }).addTo(map)
        .bindPopup(`
            <div style="text-align: center; direction: rtl; font-family: Cairo, sans-serif;">
                <strong style="font-size: 14px; color: #dc1f27;">${loc.name}</strong><br>
                <span style="font-size: 20px; font-weight: bold;">${loc.count}</span> معرض<br>
                <span style="color: #666;">(${loc.percentage}%)</span>
            </div>
        `);
        
        // Add label
        L.marker(loc.coords, {
            icon: L.divIcon({
                className: 'map-label',
                html: `<div style="background: rgba(220,31,39,0.9); color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-family: Cairo; white-space: nowrap;">${loc.name}</div>`,
                iconSize: [80, 20],
                iconAnchor: [40, 10]
            })
        }).addTo(map);
    });
    
    mapContainer.dataset.initialized = 'true';
}

// =============================================
// INFOGRAPHIC ANIMATIONS
// =============================================
function initInfographicAnimations() {
    // Progress bars animation
    const progressBars = document.querySelectorAll('.cs-progress-bar');
    
    progressBars.forEach(bar => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const width = bar.dataset.width;
                    bar.style.width = width;
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(bar);
    });
}

// Initialize on tab change
document.addEventListener('click', function(e) {
    if (e.target.closest('a[data-tab="current-status"]')) {
        setTimeout(() => {
            initAllCharts();
            initAnimatedCounters();
            initAmmanMap();
            initInfographicAnimations();
        }, 400);
    }
});
