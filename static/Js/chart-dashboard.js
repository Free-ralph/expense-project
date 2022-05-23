const renderChart = (labels, data, target,  type, label_text)=> {
    const ctx = document.getElementById(target).getContext('2d');
    const myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label_text,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    '#343a40'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 0.2)',
                    '#343a40'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title : {
                    display : true , 
                    text : label_text
                }
            }
        }
    });
    let is_empty = true
    for (let week of data){
        if(week != 0){
            is_empty = false 
        }
    }

    if (is_empty){
        $(`#${target}NoData`).removeClass('d-none')
    }

}

$(document).ready(() => {
    $.ajax({
        type : 'get', 
        url : '/dashboard-endpoint',
        beforeSend : () => {
            $('#ChartContainer').addClass('request')
        } ,
        success : (res) => {
            const [labels_prev_week, data_prev_week] = [Object.keys(res.prev_week_analysis), Object.values(res.prev_week_analysis)]
            const [labels_prev_month, data_prev_month] = [Object.keys(res.prev_month_analysis), Object.values(res.prev_month_analysis)]
            renderChart(labels_prev_week , data_prev_week, 'First',  'doughnut', "Income For previous Week")
            renderChart(labels_prev_month, data_prev_month, 'Second', 'line',   'Income for the previous Year',)
        },
        complete : () => {
            $('#ChartContainer').removeClass('request')
        } ,
        error : (err) => {
            console.log(err)
        }
    })
})