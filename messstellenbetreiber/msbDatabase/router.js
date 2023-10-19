const express = require('express');
const dbConnector = require("./dbConnector");
const dbConnection = new dbConnector('sqlite', 'msb.db');
const router = express.Router();
const api_location = "/api/v1/";
const endpoints = {};
endpoints["stromverbrauch"] = api_location + "stromverbrauch/";
endpoints["current_consumption"] = endpoints["stromverbrauch"] + "current";
const db_type = true;
const sqlite_file = "msb.db";


// middleware to check authentification
router.use((request, response, next) => {
    // TODO: check authnetification
    // response.send("Nö du hast kein access");
    next();
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

router.get(endpoints["stromverbrauch"] + "/hello", (request, response) => {
    dbConnection.read_Stromverbrauch_all(1, (result) => {
        response.send("Zurückgeben der Methode des Energieverbrauchs " + result);
    });
});
module.exports = router