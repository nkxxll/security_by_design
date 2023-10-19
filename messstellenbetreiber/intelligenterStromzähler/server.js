const fetch = require("node-fetch");

const id = 3427824;

const startingPower = 324803;
let addingPower = 349;

const body = {};
body["timestamp"] = Date.now();
body["stromzaehler_id"] = id;
body["consumtion"] = startingPower;

function sendData() {
    console.log("sending Data");
    body["timestamp"] = Date.now();
    body["power"] = body["power"] + addingPower;
    // TODO: make addingPower random and sometimes negativ 
    fetch('http://localhost:3000/api/v1/stromverbrauch/save_consumtion', {
        method: 'POST', body: JSON.stringify(body),
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

sendData();
setTimeout(sendData, 15 * 60 * 1000);