
function RoundNum(number, maxPlaces, forcePlaces, forceLetter) {
  number = Number(number)
  forceLetter = forceLetter || false
  if(forceLetter !== false) {
    return annotate(number, maxPlaces, forcePlaces, forceLetter)
  }
  var abbr
  if(number >= 1e12) {
    abbr = 'T'
  }
  else if(number >= 1e9) {
    abbr = 'B'
  }
  else if(number >= 1e6) {
    abbr = 'M'
  }
  else if(number >= 1e3) {
    abbr = 'K'
  }
  else {
    abbr = ''
  }
  return annotate(number, maxPlaces, forcePlaces, abbr)
}

function annotate(number, maxPlaces, forcePlaces, abbr) {
  // set places to false to not round
  var rounded = 0
  switch(abbr) {
    case 'T':
      rounded = number / 1e12
      break
    case 'B':
      rounded = number / 1e9
      break
    case 'M':
      rounded = number / 1e6
      break
    case 'K':
      rounded = number / 1e3
      break
    case '':
      rounded = number
      break
  }
  if(maxPlaces !== false) {
    var test = new RegExp('\\.\\d{' + (maxPlaces + 1) + ',}$')
    if(test.test(('' + rounded))) {
      rounded = rounded.toFixed(maxPlaces)
    }
  }
  if(forcePlaces !== false) {
    rounded = Number(rounded).toFixed(forcePlaces)
  }
  return rounded + abbr
}


function colorize() {
    var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
  }

function generateChart(chartDatasets, chartTitle, chartID, chartLoaderID){

    let datasets = chartDatasets['fields']
    datasets.forEach((data, index) => {
        if (index > 0){
            let pastOrder = datasets[index - 1].order;
            data['order'] = pastOrder + 1;
        }
        data['backgroundColor'] = colorize()
        data['borderColor'] = colorize();
    });
    
    let info = {
        labels: chartDatasets.labels,
        datasets: datasets
        };
        
        chartLoaderID.remove();

        new Chart(chartID, {
            
        data: info,
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
                    enabled:false
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
        });
}

function displayTable(tableDatasets, tableID, loaderID){
    let currency = ''

    if (tableDatasets['currency']){
      currency = "En " + tableDatasets['currency']
    }
    let lables = tableDatasets['labels']
    let tableData = tableDatasets['fields']

    let table = '<table class="table table-striped table-hover">';
    let tableHead = '<thead class="card-header text-center"><tr><th scope="col" class="border-0">' + currency +'</th>';
    let tableBody = '<tbody>';
    

    lables.forEach((data, index) => {
        tableHead += '<th scope="col" class="border-0">'+ data +'</th>';
    });

    tableData.forEach((data, index) => {
        tableBody += '<tr><th scope="row"><a href="'+data.url+'">'+data.title+'</a></th>';

        let financialData = data['values']
        let percent = data.percent
        let short = data.short
        
        financialData.forEach((data, index) => {
          let extra = ""
          let amount = data

          if(short === 'true'){
            amount = RoundNum(amount, 2, false, false)
            }
          if(percent === 'true'){
            extra = "%"
          }
          tableBody += '<td>'+amount + extra +'</td>';
        });
        tableBody += '<td id="blur">67466</td></tr>';
    });

    tableHead += '<th scope="col" class="border-0"><button data-bs-toggle="modal" data-bs-target="#NecesitasMembresiaModal" class="btn btn-danger btn-sm">Más años</button></th></tr></thead>'
    table += tableHead
    tableBody += '</tbody>';
    table += tableBody
    table += "</table>";
    loaderID.remove();
    tableID.innerHTML = table;
}

function createContent(tableDatasets, tableID, loaderID, chartDatasets, chartTitle, chartID, chartLoaderID){
   
    // if (chartID) {chartID.destroy();}
    displayTable(tableDatasets, tableID, loaderID);

    generateChart(chartDatasets, chartTitle, chartID, chartLoaderID);
    
}


function createGauge(chartID, minValue, medValue, maxValue, needleValue){
  new Chart(chartID, {
    type: 'doughnut',
    plugins: [{
      afterDraw: chart => {
        var needleValue = chart.config.data.datasets[0].needleValue;
        var dataTotal = chart.config.data.datasets[0].data.reduce((a, b) => a + b, 0);
        var angle = Math.PI + (1 / dataTotal * needleValue * Math.PI);
        var ctx = chart.ctx;
        var cw = chart.canvas.offsetWidth;
        var ch = chart.canvas.offsetHeight;
        var cx = cw / 2;
        var cy = ch - 6;
  
        ctx.translate(cx, cy);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.moveTo(0, -3);
        ctx.lineTo(ch - 20, 0);
        ctx.lineTo(0, 3);
        ctx.fillStyle = 'rgb(0, 0, 0)';
        ctx.fill();
        ctx.rotate(-angle);
        ctx.translate(-cx, -cy);
        ctx.beginPath();
        ctx.arc(cx, cy, 5, 0, Math.PI * 2);
        ctx.fill();
      }
    }],
    data: {
      labels: [],
      datasets: [{
        data: [minValue, medValue, maxValue],
        needleValue: needleValue,
        backgroundColor: [
          'rgba(63, 191, 63, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(255, 99, 132, 0.2)'  
        ]
      }]
    },
    options: {
      responsive: false,
      aspectRatio: 2,
      layout: {
        padding: {
          bottom: 3
        }
      },
      rotation: -90,
      cutout: '50%',
      circumference: 180,
      legend: {
        display: false
      },
      animation: {
        animateRotate: false,
        animateScale: true
      }
    }
  });
}