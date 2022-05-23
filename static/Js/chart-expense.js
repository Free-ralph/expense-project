let renderChart = (labels, data, target,  type, label_text)=> {
    const ctx = document.getElementById(target).getContext('2d');
    const myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses for the last 6months',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
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
    if (data.length < 1){
        $(`#${target}NoData`).removeClass('d-none')
    }

}


$.ajax({
    type : 'get', 
    url : 'expense-category-summary-endpoint',
    beforeSend : () => {
        $('#ChartContainer').addClass('request')
    } ,
    success : (res) => {

        const [labels_prev_month, data_prev_month] = [Object.keys(res.expenses_prev_month), Object.values(res.expenses_prev_month)]
        const [labels_prev_year, data_prev_year] = [Object.keys(res.expenses_prev_year), Object.values(res.expenses_prev_year)]
        renderChart(labels_prev_month , data_prev_month, 'First',  'doughnut', "Expenses For the a month")
        renderChart(labels_prev_year , data_prev_year, 'Second', 'line',   'Expenses for a year',)
    },
    complete : () => {
        $('#ChartContainer').removeClass('request')
    } ,
    error : (err) => {
        console.log(err)
    }
})