const express = require('express');
const dbConnector = require("./dbConnector");
const router = express.Router();
const api_location = "/api/v1/";
const endpoints = {
    "stromverbrauch": api_location + "stromverbrauch/",
    "current_consumption": endpoints["stromverbrauch"] + "current",
};
const db_type = true;
const sqlite_file = "msb.db";
const dbConnection = new dbConnector(db_type, sqlite_file);

// middleware to check authentification
router.use((request, response, next) => {
    // TODO: check authnetification
    dbConnection.read_db()
    response.send("Nö du hast kein access");
});

router.get(endpoints["stromverbrauch"], (request, response) => {
    response.send('Soll die Stromverbrauchsdaten eines Kunden zurückgeben');
});

router.get(endpoints["current_consumption"], (request, response) => {
    response.send('Soll die Stromverbrauchsdaten eines Kunden zurückgeben');
});

router.get(endpoints["stromverbrauch"] + "/:year", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " eines Kunden zurückgeben");
});

router.get(endpoints["stromverbrauch"] + "/:year/:month", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " und Monats " + request.params.month + " eines Kunden zurückgeben");
});
module.exports = router