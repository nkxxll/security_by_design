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

    console.log(randomDate.getTime());
    return randomDate.getTime()
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



function add_verbrauch_for_stromzahler(stromzahlerID, max_verbrauch_Wh, start_date, timeinterval_min = 15) {
    increment = timeinterval_min * 60
    current_date = new Date().getTime();
    verbrauch = 0
    for (i = start_date; i += increment; i < current_date) {
        verbrauch += Math.floor(Math.random() * (max_verbrauch_Wh / 4))
        dbConnection.fill_verbrauch_db(stromzahlerID, verbrauch, random_date + i)
    }
}

dbConnection.db_connection.serialize(function () {
    let id_array = [];
    for (let i = 0; i < 100; i++) {
        id = generate_random_id() + i;
        key = generate_key(15) + i;
        console.log(id, key)
        dbConnection.fill_location_db(id);
        dbConnection.fill_id_key_realtion_db(id, key);
        random_date = generate_random_date(2022, 2023);
        add_verbrauch_for_stromzahler(id, 1000, random_date, 15)
        id_array.push(id)
    }
    console.log(id_array);
    dbConnection.close_connection();
});

// generate Date = new_date
// now do 15min Increments till curernt Date is reached
// every increment, add data to verbrauchstabelle