document.addEventListener('DOMContentLoaded', () => {
    getMarketData(cnpjs="73.232.530/0001-39");

    document.querySelector("#search-data").addEventListener('input', function(event) {
        const query = event.target.value;
        if (query != ""){
            searchMarketData(query);
        } else {
            const searchResultsContainer = document.querySelector("#search-results");
            searchResultsContainer.innerHTML = "";
        }
    });

    document.querySelector("#menu-button").addEventListener('click', () => toggleMenu());

});

function toggleMenu() {
    const menu = document.querySelector("#menu")
    const body = document.querySelector("#body")
    if (menu.style.display === 'none' | menu.style.display === ''){
        console.log('Menu visible')
        body.classList.remove('col-12');
        body.classList.add('col-sm-6');
        body.classList.add('col-md-7');
        body.classList.add('col-lg-8');
        menu.style.display = 'block';
    } else {
        console.log('Menu hidden')
        body.classList.remove('col-sm-6');
        body.classList.remove('col-md-7');
        body.classList.remove('col-lg-8');
        body.classList.add('col-12');
        menu.style.display = 'none';
    }
}

function getMarketData(
    cnpjs,
    data_type = 'quota',
    start_dt_comptc = null,
    end_dt_comptc = null,
    normalize = true
) {
    console.log(`Request for ${cnpjs}`)
    const data = {
        cnpjs: cnpjs,
        data_type: data_type,
        start_dt_comptc: start_dt_comptc,
        end_dt_comptc: end_dt_comptc,
        normalize: normalize
    };
    fetch('/get-market-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(marketData => {
        // Handle the JSON response
        console.log(marketData);
        plotMarketData(marketData);
    });
}

MARKET_COLORS = [
    `rgb(226, 0, 0)`,
    `rgb(0, 204, 102)`,
    `rgb(255, 102, 178)`,
    `rgb(102, 178, 255)`,
    `rgb(128, 128, 128)`,
    `rgb(255, 255, 0)`,
    `rgb(255, 0, 255)`,
]

function plotMarketData(marketData) {
    const marketDatasets = [];
    const marketKeys = Object.keys(marketData.data);

    let colorIndex = 0

    for (const marketIndex of marketKeys) {

        const newDataset = {
            fill: false,
            label: marketIndex,
            borderColor: MARKET_COLORS[colorIndex],
            data: Object.values(marketData.data[marketIndex])
        };
        marketDatasets.push(newDataset);

        colorIndex += 1
    }

    const labels = Object.keys(marketData.data[marketKeys[0]]);
    const data = {
        labels: labels,
        datasets: marketDatasets
    };

    const ctx = document.getElementById('comparison-graphic-main').getContext('2d');
    const myChart = new Chart(ctx, {
        type: "line",
        data: data,
        options: {
            scales: {
                y: {
                    type: 'linear',
                    grace: '5%'
                }
            }
        }
    });
}

function searchMarketData(query) {
    const data = {
        query: query
    };
    fetch('/search-market-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(queryResults => {
        console.log(queryResults);
        const searchResultsContainer = document.querySelector("#search-results");
        searchResultsContainer.innerHTML = "";

        queryResults.query_results.forEach(function(result) {
            const indexOption = document.createElement("div");
            indexOption.textContent = result.short_name;
            indexOption.classList.add("search-result-option");
            indexOption.classList.add("form-control");
            indexOption.addEventListener('click', () => addToComparisonPlot(result.short_name, result.cnpj));
            searchResultsContainer.appendChild(indexOption);
        });
    });
}

function addToComparisonPlot(name, cnpj) {
    console.log(`Added ${name} to comparison`);
    const selectedMarketData = document.querySelector("#selected-market-data-container");
    const numberSelected = parseInt(selectedMarketData.getAttribute('data-numberselected'));
    const newSelectedMarketDataDiv = document.createElement('div');
    newSelectedMarketDataDiv.classList.add('selected-market-data');
    newSelectedMarketDataDiv.classList.add('col-12');
    newSelectedMarketDataDiv.classList.add('container');
    newSelectedMarketDataDiv.classList.add('d-flex');
    newSelectedMarketDataDiv.setAttribute("data-id", cnpj)
    newSelectedMarketDataDiv.setAttribute("data-color", MARKET_COLORS[numberSelected])

    const newSelectedMarketDataIconContainer = document.createElement('div');
    newSelectedMarketDataIconContainer.classList.add('col-1');
    const newSelectedMarketDataIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    newSelectedMarketDataIcon.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    newSelectedMarketDataIcon.setAttribute("height", "3em");
    newSelectedMarketDataIcon.setAttribute("viewBox", "0 0 512 512");
    const pathIcon = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathIcon.setAttribute("d", "M496 384H64V80c0-8.84-7.16-16-16-16H16C7.16 64 0 71.16 0 80v336c0 17.67 14.33 32 32 32h464c8.84 0 16-7.16 16-16v-32c0-8.84-7.16-16-16-16zM464 96H345.94c-21.38 0-32.09 25.85-16.97 40.97l32.4 32.4L288 242.75l-73.37-73.37c-12.5-12.5-32.76-12.5-45.25 0l-68.69 68.69c-6.25 6.25-6.25 16.38 0 22.63l22.62 22.62c6.25 6.25 16.38 6.25 22.63 0L192 237.25l73.37 73.37c12.5 12.5 32.76 12.5 45.25 0l96-96 32.4 32.4c15.12 15.12 40.97 4.41 40.97-16.97V112c.01-8.84-7.15-16-15.99-16z");
    pathIcon.style.fill = MARKET_COLORS[numberSelected];
    newSelectedMarketDataIcon.appendChild(pathIcon);
    newSelectedMarketDataIconContainer.appendChild(newSelectedMarketDataIcon);
    newSelectedMarketDataDiv.appendChild(newSelectedMarketDataIconContainer);

    const newSelectedMarketDataInfoContainer = document.createElement('div');
    newSelectedMarketDataInfoContainer.classList.add('col-10');
    const newSelectedMarketDataName = document.createElement('div');
    newSelectedMarketDataName.classList.add('selected-market-data-name');
    newSelectedMarketDataName.classList.add('col-12');
    newSelectedMarketDataName.classList.add('container');
    newSelectedMarketDataName.innerHTML = name;
    newSelectedMarketDataName.style.color = MARKET_COLORS[numberSelected];
    newSelectedMarketDataInfoContainer.appendChild(newSelectedMarketDataName);

    const newSelectedMarketDataId = document.createElement('div');
    newSelectedMarketDataId.classList.add('selected-market-data-id');
    newSelectedMarketDataId.classList.add('col-12');
    newSelectedMarketDataId.classList.add('container');
    newSelectedMarketDataId.innerHTML = cnpj;
    newSelectedMarketDataId.style.color = MARKET_COLORS[numberSelected];
    newSelectedMarketDataInfoContainer.appendChild(newSelectedMarketDataId);
    newSelectedMarketDataDiv.appendChild(newSelectedMarketDataInfoContainer);

    const newSelectedMarketDataRemoveIconContainer = document.createElement('div');
    newSelectedMarketDataRemoveIconContainer.classList.add('col-1');
    const newSelectedMarketDataRemoveIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    newSelectedMarketDataRemoveIcon.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    newSelectedMarketDataRemoveIcon.setAttribute("height", "1em");
    newSelectedMarketDataRemoveIcon.setAttribute("viewBox", "0 0 512 512");
    const pathRemoveIcon = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathRemoveIcon.setAttribute("d", "M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z");
    pathRemoveIcon.style.fill = MARKET_COLORS[numberSelected];
    newSelectedMarketDataRemoveIcon.appendChild(pathRemoveIcon);
    newSelectedMarketDataRemoveIconContainer.appendChild(newSelectedMarketDataRemoveIcon);
    newSelectedMarketDataDiv.appendChild(newSelectedMarketDataRemoveIconContainer);

    selectedMarketData.appendChild(newSelectedMarketDataDiv);

    selectedMarketData.setAttribute('data-numberselected', numberSelected + 1);

    const searchResultsContainer = document.querySelector("#search-results");
    searchResultsContainer.innerHTML = "";

    const searchDataContainer = document.querySelector("#search-data");
    searchDataContainer.value = "";
}

function getMarketDataIdsToPlot(){
    const selectedMarketData = document.querySelector("#selected-market-data-container");
}
