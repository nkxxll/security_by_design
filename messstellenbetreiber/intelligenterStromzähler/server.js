const fetch = require("node-fetch");
const configuration = require("./configuration");
const customMath = require("./customMath");
const myConfig = new configuration();
const myMath = new customMath();
console.log(myConfig.getAllConfig())

// TODO: add interval between update to Configuration
// TODO: add to Configuration
const id = myConfig.getId();

// TODO: add to simulation Config
// TODO: startingPower should be 0
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

// TODO: sendData should be called for unlimited times in an interval
// aka. every X Seconds sendData should be executed
function call_send_Data() {

}
setInterval(FetchData, 1000);
sendData(calcData());