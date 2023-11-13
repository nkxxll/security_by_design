const express = require('express');
const dbConnector = require("./dbConnector");
const router = express.Router();
const endpoints = {};
endpoints["stromverbrauch"] = "/api/v1/stromverbrauch/";
endpoints["current_consumption"] = endpoints["stromverbrauch"] + "current";
const db_type = "sqlite3";
const sqlite_file = "msb.db";
const dbConnection = new dbConnector(db_type, sqlite_file);


// middleware to check authentification
router.use((request, response, next) => {
    // this is fine, weil wir cookies ausserhalb der sim mit der "secure" flag schicken würden 
    // secure flag stellt 100% sicher das cookies über tls geschickt werden
    const zaehlerKey = request.cookies["stromzähler_key"];
    dbConnection.test(response);
    if (dbConnection.exists_ZaehlerKey(zaehlerKey)) {
        next();
    } else {
        //return response.send("Nö du hast kein access");
    }
});


router.get(endpoints["stromverbrauch"], (request, response) => {
    response.send('Soll alle Stromverbrauchsdaten eines Kunden zurückgeben');
});

router.get(endpoints["current_consumption"], (request, response) => {
    data = dbConnection.read_Stromverbrauch_all("");
    response.send('Soll die Stromverbrauchsdaten eines Kunden zurückgeben');
});

router.get(endpoints["stromverbrauch"] + "/:year", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " eines Kunden zurückgeben");
});

router.get(endpoints["stromverbrauch"] + "/:year/:month", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " und Monats " + request.params.month + " eines Kunden zurückgeben");
});

router.get("/api/v1/stromverbrauch/read_Stromverbrauch_all", (request, response) => {
    data = dbConnection.read_Stromverbrauch_all(request.cookies["kunde"]);
    response.send(data);
});

router.get("/api/v1/stromverbrauch/read_Stromverbrauch_timeframe", (request, response) => {
    // TODO: use signed  cookies
    data = dbConnection.read_Stromverbrauch_timeframe(request.cookies["kunde"], request.cookies["timeframe_start"], request.cookies["timeframe_end"]);
    response.send(data);
});

router.post("/api/v1/stromverbrauch/save_consumtion", (request, response) => {
    console.log("Stromzähler", request.body["id"], "saved its data:", request.body["power"])
    data = dbConnection.Dateneingabe_Stromzaehler(request.body["id"], request.body["power"], request.body["timestamp"]);
    response.send(data);
});

module.exports = router