function hist(ctx, label, data, xlabel, ylabel,title){
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: label,
            datasets: [{
                label: title,
                data: data,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    display:true,
                    scaleLabel: {
                        display:true,
                        labelString: ylabel
                    }
                }],
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: xlabel
                    }
                }]
            },
            title: {
                text:title,
                display:true,
            }
        },
    });
    }