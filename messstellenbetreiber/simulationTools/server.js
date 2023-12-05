// TODO: autoamtically populate database with kunden und stormzählern und allem scheiß und das mit variabel vielen
// TODO: give niklas the kunden data for his database
// TODO: give the kunden den auth key

const dbConnector = require("./dbConnector");

const db_type = "sqlite3";
const sqlite_file = "./..\\msbDatabase\\msb.db";
const dbConnection = new dbConnector(db_type, sqlite_file);


// https://www.helpster.de/ist-ihr-stromzaehler-noch-geeicht-die-zeit-bis-zum-ablauf-der-gueltigkeit-feststellen_169681
function generate_random_date(start_year, end_year) {
    const year = Math.floor(Math.random() * (end_year - start_year + 1) + start_year);
    const month = Math.floor(Math.random() * 12);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const day = Math.floor(Math.random() * daysInMonth) + 1;
    const randomDate = new Date(year, month, day);
    return randomDate.getTime();
}


function generate_random_id() {
    let random_id = Math.floor(Math.random() * 10000000000);
    return random_id;
}


function generate_key(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}


function add_verbrauch_for_stromzahler(stromzahlerID, max_verbrauch_Wh, start_date) {
    increment = 60 * 60 * 1000;
    current_date = new Date().getTime();
    verbrauch = 0
    change = 0
    for (i = start_date; i < current_date; i += increment) {
        still_required = (current_date - i) / increment;
        if (still_required < 20000 && change < 1) {
            increment = 30 * 60 * 1000;
            change += 1;
        }
        if (still_required < 10000 && change < 2) {
            increment = 15 * 60 * 1000;
            change += 1;
        }
        verbrauch += Math.floor(Math.random() * (max_verbrauch_Wh / 4))
        dbConnection.fill_verbrauch_db(stromzahlerID, verbrauch, random_date + i)
    }
    time_taken = new Date().getTime() - current_date
    console.log(stromzahlerID, "took", time_taken, "ms aka.", time_taken / 1000, "s")
}

function add_verbrauch_for_stromzahler_test(stromzahlerID) {
    verbrauch = 0;
    for (i = 10000; i < 100000; i += 15 * 60 * 1000) {
        verbrauch += i;
        dbConnection.fill_verbrauch_db(stromzahlerID, verbrauch, i)
    }
}




function add_stromzahler(stromzahler_id, auth_key) {
    console.log("creating new stromzahler", id, "with auth key:", key)
    dbConnection.fill_location_db(id);
    dbConnection.fill_id_key_realtion_db(id, key);
    random_date = generate_random_date(2022, 2023);
    add_verbrauch_for_stromzahler(id, 1000, random_date, 60);
    einbau = generate_random_date(2006, 2023);
    einbau_year = new Date(einbau).getFullYear();
    if (einbau_year < 2023) {
        wartung = generate_random_date(2023, 2023);
    }
    else {
        wartung = einbau;
    }
    dbConnection.fill_wartung_db(id, einbau, einbau, wartung);
}

dbConnection.db_connection.serialize(function () {
    let id_array = [];

    console.log("resetting db")
    const commands = [
        `DROP DATABASE msb`,
        `CREATE TABLE Position_Stromzahler (
            StromzahlerID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            Straße TEXT, 
            Hausnummer INTEGER,
            Hausnummerzusatz TEXT,
            Postleitzahl INTEGER,
            Stadtname TEXT);`,
        `CREATE TABLE StromzahlerAuth  (
            StromzahlerID INTEGER,
            Auth_Key TEXT UNIQUE PRIMARY KEY,
            FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));`,
        `CREATE TABLE StromzahlerWartung (
            StromzahlerID INTEGER,
            Einbaudatum INTEGER,
            letztesEichungsDatum INTEGER,
            letzesWartungsDatum INTEGER,
            FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));`,
        `CREATE TABLE StromzahlerVerbrauch (
            StromzahlerID INTEGER,
            StromverbrauchGesamt INTEGER,
            StromverbrauchJetzt INTEGER,
            Uhrzeit INTEGER,
            FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));`,
    ];
    commands.forEach(function (command, index) {
        dbConnection.db_connection.run(command, function (err) {
            console.log("creating", command)
            if (err) {
                console.error(`Error executing command ${index + 1}: ${command}\n${err.message}`);
            } else {
                console.log(`Command ${index + 1} executed successfully: ${command}`);
            }
        });
    });
    console.log("db resetted")
    dbConnection.fill_id_key_realtion_db("testid", "testkey");
    add_verbrauch_for_stromzahler_test("testid");
    for (let i = 0; i < 100; i++) {
        id = generate_random_id() + i;
        key = generate_key(15) + i;
        add_stromzahler(id, key);
        id_array.push(id);
    }
    console.log("added stromzähler:", id_array);
    dbConnection.close_connection();
});

// generate Date = new_date
// now do 15min Increments till curernt Date is reached
// every increment, add data to verbrauchstabelle