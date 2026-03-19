document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

function initDashboard() {
    const data = DASHBOARD_DATA;
    
    // Injects summary cards
    renderStats(data.summary);
    
    // Config Chart globally
    Chart.defaults.color = '#8b949e';
    Chart.defaults.font.family = "'Inter', 'Outfit', sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.borderColor = 'rgba(48, 54, 61, 1)';

    // Render Charts
    renderTimeSeries(data.timeSeries);
    renderSeasonal(data.seasonal);
    renderWeekly(data.weekly);
}

function renderStats(summary) {
    const grid = document.getElementById('stats-grid');
    const stats = [
        { label: 'Avg Daily Sales', value: summary.avg_sales, unit: 'units', color: 'blue' },
        { label: 'Avg Temp', value: summary.avg_temp, unit: '°C', color: 'orange' },
        { label: 'Rainy Days', value: summary.rainy_days, unit: 'days', color: 'teal' },
        { label: 'Correlation', value: summary.temp_sales_corr, unit: 'r', color: 'red' },
        { label: 'Peak Sales', value: summary.max_sales, unit: 'units', color: 'green' }
    ];

    grid.innerHTML = stats.map((s, i) => `
        <div class="stat-card" style="animation-delay: ${i * 0.1}s">
            <div class="stat-label">${s.label}</div>
            <div class="stat-value">${s.value} <span>${s.unit}</span></div>
        </div>
    `).join('');
}

function renderTimeSeries(tsData) {
    const ctx = document.getElementById('timeSeriesChart').getContext('2d');
    
    // Prepare data
    const labels = tsData.map(d => d.date);
    const sales = tsData.map(d => d.sRoll);
    const temps = tsData.map(d => d.tRoll);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sales (7d Avg)',
                data: sales,
                borderColor: '#2f81f7',
                backgroundColor: 'rgba(47, 129, 247, 0.08)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                yAxisID: 'y'
            }, {
                label: 'Temp (7d Avg)',
                data: temps,
                borderColor: '#d29922',
                borderWidth: 2,
                borderDash: [5, 4],
                tension: 0.4,
                pointRadius: 0,
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { position: 'top', align: 'end' }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 12 }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Sales (units)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Temperature (°C)' }
                }
            }
        }
    });
}

function renderSeasonal(seasonalData) {
    const ctx = document.getElementById('seasonalChart').getContext('2d');
    
    // Sort logic to match order if needed
    const labels = seasonalData.map(d => d.Season);
    const values = seasonalData.map(d => d.Total_Sales);
    
    const colors = {
        'Winter': '#2f81f7',
        'Spring': '#3fb950',
        'Summer': '#d29922',
        'Autumn': '#f85149'
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Avg Daily Units',
                data: values,
                backgroundColor: labels.map(l => colors[l] || '#2f81f7'),
                borderRadius: 12,
                borderWidth: 0,
                barThickness: 50
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true, grid: { color: 'rgba(48, 54, 61, 1)' } }
            }
        }
    });
}

function renderWeekly(weeklyData) {
    const ctx = document.getElementById('weeklyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: weeklyData.map(d => d.DayName),
            datasets: [{
                label: 'Avg Sales',
                data: weeklyData.map(d => d.Total_Sales),
                borderColor: '#2f81f7',
                backgroundColor: 'rgba(47, 129, 247, 0.15)',
                borderWidth: 2,
                pointBackgroundColor: '#2f81f7'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            elements: { line: { tension: 0.1 } },
            scales: {
                r: {
                    angleLines: { color: 'rgba(48, 54, 61, 1)' },
                    grid: { color: 'rgba(48, 54, 61, 1)' },
                    suggestedMin: Math.min(...weeklyData.map(d => d.Total_Sales)) * 0.9,
                    ticks: { display: false }
                }
            }
        }
    });
}
