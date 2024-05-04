import "./chart/chart.js";

import {getDataByYear} from "./api.js";

const mainChart = document.getElementById("mainChart");
const mainChartBox = document.getElementById("newChartBox");

async function renderChart() {
    mainChart.innerHTML = "";

    let dataAll = await getDataByYear();
    let cityArray = dataAll["data"]["city"];


    let j = 0;
    for (j; j < cityArray.length; j++) {
        let curButton = `<button id="cityButton${j}" name="${j}" type="button">${cityArray[j]}</button>`;
        mainChart.innerHTML += curButton;
    }

    mainChart.childNodes.forEach(
        (x) => x.addEventListener(
            "click",
            () => showChart(x.getAttribute("name"))
        )
    );
}

async function showChart(i) {
    mainChartBox.innerHTML = "";
    console.log(i);
    let dataAll = await getDataByYear();
    let cityArray = dataAll["data"]["city"];
    let yearArray = Object.values(dataAll["data"]["year"]);

    let peopleArray = dataAll["data"]["people"];
    let pmtwoArray = dataAll["data"]["pmtwo"];
    let humidityArray = dataAll["data"]["humidity"];
    let temperatureArray = dataAll["data"]["temperature"];

    let curCity = cityArray[i];
    let curPeople = [];
    let curPmtwo = [];
    let curHumidity = [];
    let curTemperature = [];

    yearArray.forEach(
        (x) => {
            curPeople.push(peopleArray[x][i]);
            curPmtwo.push(pmtwoArray[x][i]);
            curHumidity.push(humidityArray[x][i]);
            curTemperature.push(temperatureArray[x][i]);
        }
    );

    let html = `<div><canvas id="chartBox"></canvas></div>`;
    mainChartBox.innerHTML += html;

    let ctx = document.getElementById("chartBox");
    new Chart(
        ctx,
        {
            type: 'line',
            data: {
                labels: yearArray,
                datasets: [
                    {
                        label: 'PM 2.5 Index',
                        data: curPmtwo,
                        tension: 0.3,
                        borderWidth: 1
                    },
                    {
                        label: 'Population',
                        data: curPeople,
                        tension: 0.3,
                        borderWidth: 1
                    },
                    {
                        label: 'Humidity',
                        data: curHumidity,
                        tension: 0.3,
                        borderWidth: 1
                    },
                    {
                        label: 'Temperature',
                        data: curTemperature,
                        tension: 0.3,
                        borderWidth: 1
                    },
                ]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    }
                }
            }
        }
    );
}

function main() {
    renderChart();
}

main();
