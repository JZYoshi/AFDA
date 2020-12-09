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

function hist_2_set(ctx, label, data1,data2, xlabel, ylabel,title,airline1,airline2){
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: label,
            datasets: [{
                label: airline1,
                data: data1,
                backgroundColor: 'blue',
            },
            {
                label: airline2,
                data:data2,
                backgroundColor:'red'
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