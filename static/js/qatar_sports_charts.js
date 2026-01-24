/**
 * مخططات تقرير السمعة الإعلامية
 * وزارة الرياضة والشباب - قطر
 * 
 * تاريخ الإنشاء: يناير 2026
 */

// ألوان قطر الرسمية
const QatarColors = {
    maroon: '#8B1538',
    maroonDark: '#6A1029',
    gold: '#D4AF37',
    goldLight: '#E5C76B',
    white: '#FFFFFF',
    black: '#1A1A1A',
    gray: '#F5F5F5',
    positive: '#27AE60',
    negative: '#E74C3C',
    neutral: '#F39C12'
};

// إعدادات Chart.js العامة
Chart.defaults.font.family = "'Tajawal', sans-serif";
Chart.defaults.font.size = 14;
Chart.defaults.color = '#333';

// تهيئة المخططات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initSentimentChart();
    initMediaTypeChart();
    initEventsReachChart();
    initSourcesChart();
    initGeoChart();
    initPlatformsChart();
    initHashtagsChart();
    
    // تفعيل الأنيميشن للأشرطة عند الظهور
    initAnimatedBars();
});

/**
 * مخطط توزيع المشاعر (Donut Chart)
 */
function initSentimentChart() {
    const ctx = document.getElementById('sentimentChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['إيجابي', 'محايد', 'سلبي'],
            datasets: [{
                data: [28.0, 66.2, 5.8],
                backgroundColor: [
                    QatarColors.positive,
                    QatarColors.neutral,
                    QatarColors.negative
                ],
                borderColor: QatarColors.white,
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 16,
                            weight: '600'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.raw + '%';
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true
            }
        }
    });
}

/**
 * مخطط توزيع نوع الإعلام (Pie Chart)
 */
function initMediaTypeChart() {
    const ctx = document.getElementById('mediaTypeChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['منصات التواصل الاجتماعي', 'الإعلام التقليدي'],
            datasets: [{
                data: [69.5, 30.5],
                backgroundColor: [
                    '#9B59B6',
                    '#3498DB'
                ],
                borderColor: QatarColors.white,
                borderWidth: 3,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 16,
                            weight: '600'
                        },
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const count = context.label.includes('التواصل') ? '104,835' : '46,003';
                            return context.label + ': ' + context.raw + '% (' + count + ')';
                        }
                    }
                }
            }
        }
    });
}

/**
 * مخطط ترتيب الفعاليات حسب الوصول (Horizontal Bar)
 */
function initEventsReachChart() {
    const ctx = document.getElementById('eventsReachChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'UFC قطر',
                'كأس القارات',
                'فورمولا 1',
                'كأس العالم U17',
                'كأس العرب'
            ],
            datasets: [{
                label: 'الوصول (مليار)',
                data: [41.7, 31.5, 28.7, 16.5, 14.3],
                backgroundColor: [
                    QatarColors.maroon,
                    QatarColors.gold,
                    QatarColors.maroon,
                    QatarColors.gold,
                    QatarColors.maroon
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' مليار وصول';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: QatarColors.white,
                        callback: function(value) {
                            return value + 'B';
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: QatarColors.white,
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

/**
 * مخطط المصادر الإعلامية (Horizontal Bar)
 */
function initSourcesChart() {
    const ctx = document.getElementById('sourcesChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'X (Twitter)',
                'الراية',
                'Qatar News',
                'بوابة الشرق',
                'وكالة الأنباء القطرية',
                'الاستاد',
                'MENAFN',
                'YouTube',
                'Snapchat',
                'The Peninsula'
            ],
            datasets: [{
                label: 'عدد المواد',
                data: [2118, 264, 259, 246, 224, 123, 103, 90, 69, 68],
                backgroundColor: QatarColors.maroon,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        color: QatarColors.black
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: QatarColors.black,
                        font: {
                            size: 13,
                            weight: '500'
                        }
                    }
                }
            }
        }
    });
}

/**
 * مخطط التوزيع الجغرافي (Horizontal Bar)
 */
function initGeoChart() {
    const ctx = document.getElementById('geoChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'قطر 🇶🇦',
                'مصر 🇪🇬',
                'الإمارات 🇦🇪',
                'السعودية 🇸🇦',
                'الأردن 🇯🇴',
                'أمريكا 🇺🇸',
                'الكويت 🇰🇼',
                'البحرين 🇧🇭',
                'عُمان 🇴🇲',
                'لبنان 🇱🇧'
            ],
            datasets: [{
                label: 'عدد المواد',
                data: [2913, 430, 390, 259, 90, 75, 70, 51, 27, 25],
                backgroundColor: function(context) {
                    const gradient = context.chart.ctx.createLinearGradient(0, 0, context.chart.width, 0);
                    gradient.addColorStop(0, QatarColors.maroon);
                    gradient.addColorStop(1, QatarColors.gold);
                    return gradient;
                },
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: QatarColors.white
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: QatarColors.white,
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

/**
 * مخطط منصات التواصل (Doughnut)
 */
function initPlatformsChart() {
    const ctx = document.getElementById('platformsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['X (Twitter)', 'Facebook', 'Instagram', 'YouTube', 'TikTok', 'أخرى'],
            datasets: [{
                data: [45, 25, 15, 8, 5, 2],
                backgroundColor: [
                    '#1DA1F2',
                    '#4267B2',
                    '#E1306C',
                    '#FF0000',
                    '#000000',
                    '#95a5a6'
                ],
                borderColor: QatarColors.white,
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '55%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 14,
                            weight: '500'
                        },
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

/**
 * مخطط الهاشتاقات (Horizontal Bar)
 */
function initHashtagsChart() {
    const ctx = document.getElementById('hashtagsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                '#Qatar',
                '#قطر',
                '#كأس_العرب',
                '#ArabCup',
                '#F1Qatar',
                '#Doha',
                '#UFCQatar',
                '#U17WorldCup',
                '#قنوات_الكاس',
                '#FIFA'
            ],
            datasets: [{
                label: 'عدد الاستخدامات',
                data: [40000, 35000, 25000, 22000, 18000, 15000, 12000, 10000, 8000, 20000],
                backgroundColor: function(context) {
                    const colors = [
                        QatarColors.gold,
                        QatarColors.maroon,
                        QatarColors.gold,
                        QatarColors.maroon,
                        QatarColors.gold,
                        QatarColors.maroon,
                        QatarColors.gold,
                        QatarColors.maroon,
                        QatarColors.gold,
                        QatarColors.maroon
                    ];
                    return colors[context.dataIndex];
                },
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw.toLocaleString() + ' استخدام';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: QatarColors.white,
                        callback: function(value) {
                            return (value / 1000) + 'K';
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: QatarColors.white,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

/**
 * تفعيل الأنيميشن للأشرطة عند الظهور
 */
function initAnimatedBars() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // تفعيل أشرطة المشاعر
                const sentimentBars = entry.target.querySelectorAll('.sentiment-bar__fill');
                sentimentBars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 300);
                });
                
                // تفعيل أشرطة بطاقة الأداء
                const scoreBars = entry.target.querySelectorAll('.score-item__bar-fill');
                scoreBars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 300);
                });
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.slide').forEach(slide => {
        observer.observe(slide);
    });
}

/**
 * تصدير إلى PDF
 */
function exportToPDF() {
    window.print();
}

/**
 * التنقل إلى شريحة معينة
 */
function goToSlide(slideId) {
    const slide = document.getElementById(slideId);
    if (slide) {
        slide.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * عداد الأرقام المتحركة
 */
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(progress * target);
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target.toLocaleString();
        }
    }
    
    requestAnimationFrame(update);
}

// تفعيل العدادات عند الظهور
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counters = entry.target.querySelectorAll('[data-count]');
            counters.forEach(counter => {
                if (!counter.dataset.animated) {
                    const target = parseInt(counter.dataset.count);
                    animateCounter(counter, target);
                    counter.dataset.animated = 'true';
                }
            });
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.slide').forEach(slide => {
    counterObserver.observe(slide);
});

console.log('✅ Qatar Sports Report Charts Initialized');
