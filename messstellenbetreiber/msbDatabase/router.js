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

router.get("/api/v1/stromverbrauch/hello", (request, response) => {
    data = dbConnection.read_Stromverbrauch_all("1");
    response.send(data);
});
module.exports = router