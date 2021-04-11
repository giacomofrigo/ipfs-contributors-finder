function addData(chart, labels, data) {
    $.each(labels, (idx, item) => {
        chart.data.labels.push(item)
    })
    
    chart.data.datasets.forEach((dataset) => {
        $.each(data, (idx, item) => {
            dataset.data.push(item)
        })
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels = [];
    chart.data.datasets.forEach((dataset) => {
        dataset.data = [];
    });
    chart.update();
}