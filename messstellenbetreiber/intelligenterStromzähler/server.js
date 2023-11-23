const fetch = require("node-fetch");
const configuration = require("./configuration");
const customMath = require("./customMath");
const myConfig = new configuration();
const myMath = new customMath();
console.log(myConfig.getAllConfig())

const id = myConfig.getId();

const startingPower = 0;
const minAdd = myConfig.getSimulationMinAdd();
const maxAdd = myConfig.getSimulationMaxAdd();;
let totalConsumption = startingPower;


/**
 * creates and returns the Data Array needed for sendData for a running Simulation
 * 0: id (int)
 * 1: timestamp (int)
 * 2: totalPowerConsumption (int)
 */
function calcData() {
    const timestamp = Date.now();
    const totalPowerConsumption = totalConsumption + myMath.getRandomInt(minAdd, maxAdd);
    return [id, timestamp, totalPowerConsumption]
}

/**
 * Sends Data (id,timestamp,powerconsumption) to msb db
 * data needs to be an array:
 * 0: id (int)
 * 1: timestamp (int)
 * 2: totalPowerConsumption (int)
 */
function sendData(data) {
    console.log("sending Data");
    let newBody = {};
    newBody[myConfig.getSaveIdName()] = data[0];
    newBody[myConfig.getSaveTimestampName()] = data[1];
    newBody[myConfig.getSaveConsumptionName()] = data[2];
    fetch(myConfig.getSaveURL(), {
        method: 'POST', body: JSON.stringify(newBody),
        headers: { 'Content-Type': 'application/json' }
    }).then((result) => {
        console.log("Success with sending Data:", result);
    }).catch((err) => {
        console.log(err)
        if (err.name === "FetchError") {
            console.error("CONNECTION REFUSED");
        }
        else {
            console.error("PROBLEM: ", err);
        }
    });
}

function sendpopulatedData() {
    sendData(calcData())
}

function call_send_Data() {
    // const Interval = 
    setInterval(sendpopulatedData, myConfig.getTimeInterval() * 1000);
}

function stop_send_Data() {
    clearInterval(Interval);
}

call_send_Data()