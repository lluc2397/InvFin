
(function($) {
    'use strict'

    $(function() {
        $('[data-toggle="sweet-alert"]').on('click', function(){
            var type = $(this).data('sweet-alert');

            switch (type) {
                case 'basic':
                    swal({
                        title: "Here's a message!",
                        text: 'A few words about this sweet alert ...',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-primary'
                    })
                break;

                case 'info':
                    swal({
                        title: 'Info',
                        text: 'A few words about this sweet alert ...',
                        type: 'info',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-info'
                    })
                break;

                case 'info':
                    swal({
                        title: 'Info',
                        text: 'A few words about this sweet alert ...',
                        type: 'info',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-info'
                    })
                break;

                case 'success':
                    swal({
                        title: 'Success',
                        text: 'A few words about this sweet alert ...',
                        type: 'success',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-success'
                    })
                break;

                case 'warning':
                    swal({
                        title: 'Warning',
                        text: 'A few words about this sweet alert ...',
                        type: 'warning',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-warning'
                    })
                break;

                case 'question':
                    swal({
                        title: 'Are you sure?',
                        text: 'A few words about this sweet alert ...',
                        type: 'question',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-default'
                    })
                break;

                case 'confirm':
                    swal({
                        title: 'Are you sure?',
                        text: "You won't be able to revert this!",
                        type: 'warning',
                        showCancelButton: true,
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-danger',
                        confirmButtonText: 'Yes, delete it!',
                        cancelButtonClass: 'btn btn-secondary'
                    }).then((result) => {
                        if (result.value) {
                            // Show confirmation
                            swal({
                                title: 'Deleted!',
                                text: 'Your file has been deleted.',
                                type: 'success',
                                buttonsStyling: false,
                                confirmButtonClass: 'btn btn-primary'
                            });
                        }
                    })
                break;

                case 'image':
                    swal({
                        title: 'Sweet',
                        text: "Modal with a custom image ...",
                        imageUrl: '../../assets/img/ill/ill-1.svg',
                        buttonsStyling: false,
                        confirmButtonClass: 'btn btn-primary',
                        confirmButtonText: 'Super!'
                });
                break;

                case 'timer':
                    swal({
                        title: 'Auto close alert!',
                        text: 'I will close in 2 seconds.',
                        timer: 2000,
                        showConfirmButton: false
                    });
                break;
            }
        });

    });
}(jQuery))



function colorize() {
    var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
  }

  chartFields = [
      field = {
        label: 'Net margin',
        dataName : 'revenue',
        data: [],
        backgroundColor: colorize(),
        borderColor: colorize(),
    
        yAxisID:"right",
        order: 1,
        type: 'line'
  },]

function generateChart(companyData, chartFields, chartType, chartTitle){
    let dates = companyData.map(function(data){return data.date})
    let dataChart = []
    chartFields.forEach((field, index) => {
        if (index > 0){
            let pastOrder = chartFields[index - 1].order;
            field['order'] = pastOrder + 1;
        }    
        
        companyData.forEach((data, index) => {
            field['data'].push(data[dataName])
        
        });
        dataChart.push(field)
    });
    const config = {
        type: chartType,
        data: dataChart,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: chartTitle
            },
            zoom: {
                pan:{
                  enabled:true
                },
                zoom: {
                  wheel: {
                    enabled: true,
                  },
                  pinch: {
                    enabled: true
                  },
                  mode: 'x',
                }
            }
          }
        },
      };
}

function displayTable(chartDatasets, companyData, tableID){
    let keys = companyData[0]
    let currency = keys.reported_currency
    let firstRows = Object.keys(keys)
    let table = '<table class="table table-striped table-hover">';
    let tableHead = '<thead class="card-header text-center"><tr><th scope="col" class="border-0">En ' + currency +'</th>';
    let tableBody = '<tbody>';


    companyData.forEach((data, index) => {
        tableHead += '<th scope="col" class="border-0">'+ data['date'] +'</th>';
    });

    chartDatasets.forEach((title, index) => {    
        tableBody += '<tr><th scope="row"><a href="#">'+title.label+'</a></th>';
        let position = index + 2;
        let term = firstRows[position];
        companyData.forEach((data, index) => {
            tableBody += '<td>'+data[term]+'</td>';
        });
        tableBody += '<td id="blur">6462465462466</td></tr>';
    });
    tableHead += '<th scope="col" class="border-0"><button data-bs-toggle="modal" data-bs-target="#NecesitasMembresiaModal" class="btn btn-danger btn-sm">Más años</button></th></tr></thead>'
    table += tableHead
    tableBody += '</tbody>';
    table += tableBody
    table += "</table>";
    tableID.innerHTML = table;
}


function pr(d){
    console.log(d)
};

function createContent(url, chartDatasets, tableID, loaderID){
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        result = response.json()
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting brand info!')
            return false;
        }
        
        return result
    })
    .then(result => {
        loaderID.remove();
        displayTable(chartDatasets, result, tableID);
        let chartDatasets = chartDatasets.map(
            function(data){
                if (data.dataName != false){
                    return data
                }
            });
        pr(chartDatasets)
    })    
    .catch(error => {
        console.log(error)
    })
    
}