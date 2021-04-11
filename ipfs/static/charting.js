function addData(chart, labels, data) {
    $.each(labels, (idx, item) => {
        if ($.inArray(item, chart.data.labels) === -1){
            chart.data.labels.push(item)
        }

    })
    
    chart.data.datasets.forEach((dataset) => {
        $.each(data, (idx, item) => {
            if ($.inArray(item, dataset.data) === -1) {
                dataset.data.push(item)
            }
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