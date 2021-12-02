function createChart(chartId, chartTitle, chartData) {
    const ctx = document.getElementById(chartId).getContext('2d');
    const data = {
        labels: chartData.labels,
        datasets: [{
            data: chartData.values,
            borderWidth: 1,
            backgroundColor: chartData.colors,
        }]
    };
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {legend: {position: 'left'}, title: {display: true, text: chartTitle}}
        }
    };
    return new Chart(ctx, config)
}

axios.get('/api/chart').then(response => {
    createChart('chart1', 'Продажи', response.data.chart1)
    createChart('chart2', 'Выручка', response.data.chart2)
});