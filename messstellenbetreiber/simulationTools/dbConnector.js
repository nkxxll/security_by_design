const sqlite3 = require('sqlite3');

class dbConnector {
    constructor(db_type, db_location) {
        if (db_type == "sqlite" || db_type == "sqlite3") {
            this.db_connection = new sqlite3.Database(db_location, (err) => {
                if (err) {
                    console.error(err.message);
                }
                console.log('Connected to the sqlite database.');
            });
        }
        else if (db_type == "mysql" || db_type == "Mysql") {
            this.db_connection = "NOT IMPLEMENTED";
        }
    }

    // TODO: add  a Stromzähler 
    // 1. add id  and location to position tabelle



    fill_location_db(random_id) {
        let city_names = ["Aberdeen", "Abilene", "Akron", "Albany", "Albuquerque", "Alexandria", "Allentown", "Amarillo", "Anaheim", "Anchorage", "Ann Arbor", "Antioch", "Apple Valley", "Appleton", "Arlington", "Arvada", "Asheville", "Athens", "Atlanta", "Atlantic City", "Augusta", "Aurora", "Austin", "Bakersfield", "Baltimore", "Barnstable", "Baton Rouge", "Beaumont", "Bel Air", "Bellevue", "Berkeley", "Bethlehem", "Billings", "Birmingham", "Bloomington", "Boise", "Boise City", "Bonita Springs", "Boston", "Boulder", "Bradenton", "Bremerton", "Bridgeport", "Brighton", "Brownsville", "Bryan", "Buffalo", "Burbank", "Burlington", "Cambridge", "Canton", "Cape Coral", "Carrollton", "Cary", "Cathedral City", "Cedar Rapids", "Champaign", "Chandler", "Charleston", "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista", "Cincinnati", "Clarke County", "Clarksville", "Clearwater", "Cleveland", "College Station", "Colorado Springs", "Columbia", "Columbus", "Concord", "Coral Springs", "Corona", "Corpus Christi", "Costa Mesa", "Dallas", "Daly City", "Danbury", "Davenport", "Davidson County", "Dayton", "Daytona Beach", "Deltona", "Denton", "Denver", "Des Moines", "Detroit", "Downey", "Duluth", "Durham", "El Monte", "El Paso", "Elizabeth", "Elk Grove", "Elkhart", "Erie", "Escondido", "Eugene", "Evansville", "Fairfield", "Fargo", "Fayetteville", "Fitchburg", "Flint", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Smith", "Fort Walton Beach", "Fort Wayne", "Fort Worth", "Frederick", "Fremont", "Fresno", "Fullerton", "Gainesville", "Garden Grove", "Garland", "Gastonia", "Gilbert", "Glendale", "Grand Prairie", "Grand Rapids", "Grayslake", "Green Bay", "GreenBay", "Greensboro", "Greenville", "Gulfport-Biloxi", "Hagerstown", "Hampton", "Harlingen", "Harrisburg", "Hartford", "Havre de Grace", "Hayward", "Hemet", "Henderson", "Hesperia", "Hialeah", "Hickory", "High Point", "Hollywood", "Honolulu", "Houma", "Houston", "Howell", "Huntington", "Huntington Beach", "Huntsville", "Independence", "Indianapolis", "Inglewood", "Irvine", "Irving", "Jackson", "Jacksonville", "Jefferson", "Jersey City", "Johnson City", "Joliet", "Kailua", "Kalamazoo", "Kaneohe", "Kansas City", "Kennewick", "Kenosha", "Killeen", "Kissimmee", "Knoxville", "Lacey", "Lafayette", "Lake Charles", "Lakeland", "Lakewood", "Lancaster", "Lansing", "Laredo", "Las Cruces", "Las Vegas", "Layton", "Leominster", "Lewisville", "Lexington", "Lincoln", "Little Rock", "Long Beach", "Lorain", "Los Angeles", "Louisville", "Lowell", "Lubbock", "Macon", "Madison", "Manchester", "Marina", "Marysville", "McAllen", "McHenry", "Medford", "Melbourne", "Memphis", "Merced", "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mission Viejo", "Mobile", "Modesto", "Monroe", "Monterey", "Montgomery", "Moreno Valley", "Murfreesboro", "Murrieta", "Muskegon", "Myrtle Beach", "Naperville", "Naples", "Nashua", "Nashville", "New Bedford", "New Haven", "New London", "New Orleans", "New York", "New York City", "Newark", "Newburgh", "Newport News", "Norfolk", "Normal", "Norman", "North Charleston", "North Las Vegas", "North Port", "Norwalk", "Norwich", "Oakland", "Ocala", "Oceanside", "Odessa", "Ogden", "Oklahoma City", "Olathe", "Olympia", "Omaha", "Ontario", "Orange", "Orem", "Orlando", "Overland Park", "Oxnard", "Palm Bay", "Palm Springs", "Palmdale", "Panama City", "Pasadena", "Paterson", "Pembroke Pines", "Pensacola", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh", "Plano", "Pomona", "Pompano Beach", "Port Arthur", "Port Orange", "Port Saint Lucie", "Port St. Lucie", "Portland", "Portsmouth", "Poughkeepsie", "Providence", "Provo", "Pueblo", "Punta Gorda", "Racine", "Raleigh", "Rancho Cucamonga", "Reading", "Redding", "Reno", "Richland", "Richmond", "Richmond County", "Riverside", "Roanoke", "Rochester", "Rockford", "Roseville", "Round Lake Beach", "Sacramento", "Saginaw", "Saint Louis", "Saint Paul", "Saint Petersburg", "Salem", "Salinas", "Salt Lake City", "San Antonio", "San Bernardino", "San Buenaventura", "San Diego", "San Francisco", "San Jose", "Santa Ana", "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Cruz", "Santa Maria", "Santa Rosa", "Sarasota", "Savannah", "Scottsdale", "Scranton", "Seaside", "Seattle", "Sebastian", "Shreveport", "Simi Valley", "Sioux City", "Sioux Falls", "South Bend", "South Lyon", "Spartanburg", "Spokane", "Springdale", "Springfield", "St. Louis", "St. Paul", "St. Petersburg", "Stamford", "Sterling Heights", "Stockton", "Sunnyvale", "Syracuse", "Tacoma", "Tallahassee", "Tampa", "Temecula", "Tempe", "Thornton", "Thousand Oaks", "Toledo", "Topeka", "Torrance", "Trenton", "Tucson", "Tulsa", "Tuscaloosa", "Tyler", "Utica", "Vallejo", "Vancouver", "Vero Beach", "Victorville", "Virginia Beach", "Visalia", "Waco", "Warren", "Washington", "Waterbury", "Waterloo", "West Covina", "West Valley City", "Westminster", "Wichita", "Wilmington", "Winston", "Winter Haven", "Worcester", "Yakima", "Yonkers", "York", "Youngstown"];
        let more_stree_name = ["Aldegrever Siedlung", "Alte Dorfstraße", "Alter Rennweg ", "Am Friedhof", "Am Waldweg", "Anton-Brune-Weg ", "Auf der Heide ", "Augustin-Schulte-Weg", "Bischofshaar", "Bittinger Haarweg", "Bittinger Straße ", "Bördestraße ", "Bootszufahrt", "Breitenbrucher Straße", "Breiter Weg ", "Büecker Weg", "Deckmannstraße", "Dickelweg ", "Diebesweg", "Dinscheder Weg", "Donnerscher Weg", "Enze-Brück", "Espadweg ", "Felgenweg ", "Forsthausweg", "Freienohler Weg", "Fuchsweg ", "Giegelnpfad", "Griesenbrink ", "Haarholz", "Heideweg", "Herringser Höfe", "Hewingser Straße", "Hohenweg", "Huerweg", "Hüsten-Delecker-Weg", "Im Bruch", "Kanzelbrücke", "Kellersiepen Trail", "Kellersiepenweg", "Kiepenkerlweg", "Körbecker Weg", "Köttersweg", "Kuehlbruecke", "Max Schulze-Sölde Weg", "Meister-Stütting-Straße ", "Möhneweg", "Mühlenhof", "Mühlenweg", "Münstermannweg", "Nelkenweg", "Neuengeseker Heide", "Neuer Rennweg", "Neuhauser Weg ", "Neuhaus Panoramaweg", "Oberer Kreesweg", "Ostpreußendamm", "Pankratius Platz", "Pastorenweg", "Randweg", "Regenweg", "Rennweg", "Rilkeweg", "Ringstraße ", "Rissmecke", "Rottland", "Rüthener Weg", "Sassendorfer Weg", "Schillingsweg ", "Schlibbeckeweg", "Schlickmannsweg", "Schlotweg ", "Seepark ", "Seeweg", "Sommerfeld ", "St.-Josef-Weg", "Südlicher Randweg", "Trellenweg", "Trimmpfad", "Ullrich-Prigge-Weg ", "Unterer Kreesweg", "Vogelsänger Weg", "Wildbachbrücke", "Wilmes Kamp", "Zum Scharfenberg"];
        let street_names = ["Mündener Straße", "Gomadinger Straße", "Hölzlberg", "Emmastraße", "Steinmauerweg", "Pfarrer-Steeg-Straße", "Schief-Schaten-Redder", "Langensalzaer Straße", "Spechtgrund", "Schleifenfelsweg", "Birkenstraße", "Albin Langer-Weg", "Fichtenweg", "Aussiedlerhof", "Ziegelfeld", "Blaumeisenweg", "Erzgebirgsblick", "Haldenweg", "Edith-Stein-Straße", "Lindenplatz", "Altsteigersweg", "Aidenbacher Straße"];
        let random_street = street_names[Math.round(Math.random() * (street_names.length - 1))]
        let random_housenumber = Math.floor(Math.random() * 71)
        let random_plz = Math.floor(Math.random() * 10000)
        let random_city = city_names[Math.round(Math.random() * (city_names.length - 1))]
        this.db_connection.each(`INSERT INTO Position_Stromzahler (StromzahlerID,Straße, Hausnummer, Postleitzahl, Stadname) 
            VALUES (?, ?, ?, ?, ?)`,
            [random_id, random_street, random_housenumber, random_plz, random_city],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }


    fill_id_key_realtion_db(random_id, random_key) {
        this.db_connection.each(`INSERT INTO StromzahlerAuth (StromzahlerID, Auth_Key) 
            VALUES (?, ?)`,
            [random_id, random_key],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    // Abstand Jahre Eichung: 8
    // Abstand Jahre Wartung: 1
    fill_wartung_db(random_id, random_letztesEichungsDatum, random_einbaudatum, random_letztesWartungsDatum) {
        this.db_connection.each(`INSERT INTO StromzahlerWartung (StromzahlerID,	Einbaudatum, letztesEichungsDatum, letzesWartungsDatum) 
            VALUES (?, ?, ?, ?)`,
            [random_id, random_einbaudatum, random_letztesEichungsDatum, random_letztesWartungsDatum],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    //to do 
    fill_verbrauch_db(stromzahlerID, stromverbrauchGesamt, stromverbrauchJetzt) {
        this.db_connection.each(`INSERT INTO StromzahlerVerbrauch (StromzahlerID, StromverbrauchGesamt, StromverbrauchJetzt) 
            VALUES (?, ?, ?)`,
            [stromzahlerID, stromverbrauchGesamt, stromverbrauchJetzt],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    // 2. add key and id to auth tabelle
    // 3.0 run kirschalls python script
    // 3.1 kirschall: python script which takes as args: [zahlerKey, Street, Housenumber, PLZ, City]
    // 3.2 kirschall: python script adds this data to his db and randomly generates names and all other necessary data

    delete_db() {
        this.db_connection.each(`DROP DATABASE msb`,
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    create_db() {
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

        this.db_connection.serialize(function () {
            commands.forEach(function (command, index) {
                this.db_connection.run(command, function (err) {
                    if (err) {
                        console.error(`Error executing command ${index + 1}: ${command}\n${err.message}`);
                    } else {
                        console.log(`Command ${index + 1} executed successfully: ${command}`);
                    }
                });
            });
        });
    }


    close_connection() {
        this.db_connection.close((err) => {
            if (err) {
                console.error(err.message);
            }
            console.log('Close the database connection.');
        });
    }

    ////////////////////////////////fill database for test///////////////////////////////////////////////////


    fill_location_db_test(random_id) {
        let city_names = ["Aberdeen", "Abilene", "Akron", "Albany", "Albuquerque", "Alexandria", "Allentown", "Amarillo", "Anaheim", "Anchorage", "Ann Arbor", "Antioch", "Apple Valley", "Appleton", "Arlington", "Arvada", "Asheville", "Athens", "Atlanta", "Atlantic City", "Augusta", "Aurora", "Austin", "Bakersfield", "Baltimore", "Barnstable", "Baton Rouge", "Beaumont", "Bel Air", "Bellevue", "Berkeley", "Bethlehem", "Billings", "Birmingham", "Bloomington", "Boise", "Boise City", "Bonita Springs", "Boston", "Boulder", "Bradenton", "Bremerton", "Bridgeport", "Brighton", "Brownsville", "Bryan", "Buffalo", "Burbank", "Burlington", "Cambridge", "Canton", "Cape Coral", "Carrollton", "Cary", "Cathedral City", "Cedar Rapids", "Champaign", "Chandler", "Charleston", "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista", "Cincinnati", "Clarke County", "Clarksville", "Clearwater", "Cleveland", "College Station", "Colorado Springs", "Columbia", "Columbus", "Concord", "Coral Springs", "Corona", "Corpus Christi", "Costa Mesa", "Dallas", "Daly City", "Danbury", "Davenport", "Davidson County", "Dayton", "Daytona Beach", "Deltona", "Denton", "Denver", "Des Moines", "Detroit", "Downey", "Duluth", "Durham", "El Monte", "El Paso", "Elizabeth", "Elk Grove", "Elkhart", "Erie", "Escondido", "Eugene", "Evansville", "Fairfield", "Fargo", "Fayetteville", "Fitchburg", "Flint", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Smith", "Fort Walton Beach", "Fort Wayne", "Fort Worth", "Frederick", "Fremont", "Fresno", "Fullerton", "Gainesville", "Garden Grove", "Garland", "Gastonia", "Gilbert", "Glendale", "Grand Prairie", "Grand Rapids", "Grayslake", "Green Bay", "GreenBay", "Greensboro", "Greenville", "Gulfport-Biloxi", "Hagerstown", "Hampton", "Harlingen", "Harrisburg", "Hartford", "Havre de Grace", "Hayward", "Hemet", "Henderson", "Hesperia", "Hialeah", "Hickory", "High Point", "Hollywood", "Honolulu", "Houma", "Houston", "Howell", "Huntington", "Huntington Beach", "Huntsville", "Independence", "Indianapolis", "Inglewood", "Irvine", "Irving", "Jackson", "Jacksonville", "Jefferson", "Jersey City", "Johnson City", "Joliet", "Kailua", "Kalamazoo", "Kaneohe", "Kansas City", "Kennewick", "Kenosha", "Killeen", "Kissimmee", "Knoxville", "Lacey", "Lafayette", "Lake Charles", "Lakeland", "Lakewood", "Lancaster", "Lansing", "Laredo", "Las Cruces", "Las Vegas", "Layton", "Leominster", "Lewisville", "Lexington", "Lincoln", "Little Rock", "Long Beach", "Lorain", "Los Angeles", "Louisville", "Lowell", "Lubbock", "Macon", "Madison", "Manchester", "Marina", "Marysville", "McAllen", "McHenry", "Medford", "Melbourne", "Memphis", "Merced", "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mission Viejo", "Mobile", "Modesto", "Monroe", "Monterey", "Montgomery", "Moreno Valley", "Murfreesboro", "Murrieta", "Muskegon", "Myrtle Beach", "Naperville", "Naples", "Nashua", "Nashville", "New Bedford", "New Haven", "New London", "New Orleans", "New York", "New York City", "Newark", "Newburgh", "Newport News", "Norfolk", "Normal", "Norman", "North Charleston", "North Las Vegas", "North Port", "Norwalk", "Norwich", "Oakland", "Ocala", "Oceanside", "Odessa", "Ogden", "Oklahoma City", "Olathe", "Olympia", "Omaha", "Ontario", "Orange", "Orem", "Orlando", "Overland Park", "Oxnard", "Palm Bay", "Palm Springs", "Palmdale", "Panama City", "Pasadena", "Paterson", "Pembroke Pines", "Pensacola", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh", "Plano", "Pomona", "Pompano Beach", "Port Arthur", "Port Orange", "Port Saint Lucie", "Port St. Lucie", "Portland", "Portsmouth", "Poughkeepsie", "Providence", "Provo", "Pueblo", "Punta Gorda", "Racine", "Raleigh", "Rancho Cucamonga", "Reading", "Redding", "Reno", "Richland", "Richmond", "Richmond County", "Riverside", "Roanoke", "Rochester", "Rockford", "Roseville", "Round Lake Beach", "Sacramento", "Saginaw", "Saint Louis", "Saint Paul", "Saint Petersburg", "Salem", "Salinas", "Salt Lake City", "San Antonio", "San Bernardino", "San Buenaventura", "San Diego", "San Francisco", "San Jose", "Santa Ana", "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Cruz", "Santa Maria", "Santa Rosa", "Sarasota", "Savannah", "Scottsdale", "Scranton", "Seaside", "Seattle", "Sebastian", "Shreveport", "Simi Valley", "Sioux City", "Sioux Falls", "South Bend", "South Lyon", "Spartanburg", "Spokane", "Springdale", "Springfield", "St. Louis", "St. Paul", "St. Petersburg", "Stamford", "Sterling Heights", "Stockton", "Sunnyvale", "Syracuse", "Tacoma", "Tallahassee", "Tampa", "Temecula", "Tempe", "Thornton", "Thousand Oaks", "Toledo", "Topeka", "Torrance", "Trenton", "Tucson", "Tulsa", "Tuscaloosa", "Tyler", "Utica", "Vallejo", "Vancouver", "Vero Beach", "Victorville", "Virginia Beach", "Visalia", "Waco", "Warren", "Washington", "Waterbury", "Waterloo", "West Covina", "West Valley City", "Westminster", "Wichita", "Wilmington", "Winston", "Winter Haven", "Worcester", "Yakima", "Yonkers", "York", "Youngstown"];
        let more_stree_name = ["Aldegrever Siedlung", "Alte Dorfstraße", "Alter Rennweg ", "Am Friedhof", "Am Waldweg", "Anton-Brune-Weg ", "Auf der Heide ", "Augustin-Schulte-Weg", "Bischofshaar", "Bittinger Haarweg", "Bittinger Straße ", "Bördestraße ", "Bootszufahrt", "Breitenbrucher Straße", "Breiter Weg ", "Büecker Weg", "Deckmannstraße", "Dickelweg ", "Diebesweg", "Dinscheder Weg", "Donnerscher Weg", "Enze-Brück", "Espadweg ", "Felgenweg ", "Forsthausweg", "Freienohler Weg", "Fuchsweg ", "Giegelnpfad", "Griesenbrink ", "Haarholz", "Heideweg", "Herringser Höfe", "Hewingser Straße", "Hohenweg", "Huerweg", "Hüsten-Delecker-Weg", "Im Bruch", "Kanzelbrücke", "Kellersiepen Trail", "Kellersiepenweg", "Kiepenkerlweg", "Körbecker Weg", "Köttersweg", "Kuehlbruecke", "Max Schulze-Sölde Weg", "Meister-Stütting-Straße ", "Möhneweg", "Mühlenhof", "Mühlenweg", "Münstermannweg", "Nelkenweg", "Neuengeseker Heide", "Neuer Rennweg", "Neuhauser Weg ", "Neuhaus Panoramaweg", "Oberer Kreesweg", "Ostpreußendamm", "Pankratius Platz", "Pastorenweg", "Randweg", "Regenweg", "Rennweg", "Rilkeweg", "Ringstraße ", "Rissmecke", "Rottland", "Rüthener Weg", "Sassendorfer Weg", "Schillingsweg ", "Schlibbeckeweg", "Schlickmannsweg", "Schlotweg ", "Seepark ", "Seeweg", "Sommerfeld ", "St.-Josef-Weg", "Südlicher Randweg", "Trellenweg", "Trimmpfad", "Ullrich-Prigge-Weg ", "Unterer Kreesweg", "Vogelsänger Weg", "Wildbachbrücke", "Wilmes Kamp", "Zum Scharfenberg"];
        let street_names = ["Mündener Straße", "Gomadinger Straße", "Hölzlberg", "Emmastraße", "Steinmauerweg", "Pfarrer-Steeg-Straße", "Schief-Schaten-Redder", "Langensalzaer Straße", "Spechtgrund", "Schleifenfelsweg", "Birkenstraße", "Albin Langer-Weg", "Fichtenweg", "Aussiedlerhof", "Ziegelfeld", "Blaumeisenweg", "Erzgebirgsblick", "Haldenweg", "Edith-Stein-Straße", "Lindenplatz", "Altsteigersweg", "Aidenbacher Straße"];
        let random_street = street_names[Math.round(Math.random() * (street_names.length - 1))]
        let random_housenumber = Math.floor(Math.random() * 71)
        let random_plz = Math.floor(Math.random() * 10000)
        let random_city = city_names[Math.round(Math.random() * (city_names.length - 1))]
        this.db_connection.each(`INSERT INTO Position_Stromzahler (StromzahlerID,Straße, Hausnummer, Postleitzahl, Stadname) 
            VALUES (?, ?, ?, ?, ?)`,
            [random_id, random_street, random_housenumber, random_plz, random_city],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }


    fill_id_key_realtion_db_test(random_id, random_key) {
        this.db_connection.each(`INSERT INTO StromzahlerAuth (StromzahlerID, Auth_Key) 
            VALUES (?, ?)`,
            [random_id, random_key],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    // Abstand Jahre Eichung: 8
    // Abstand Jahre Wartung: 1
    fill_wartung_db(random_id, random_letztesEichungsDatum, random_einbaudatum, random_letztesWartungsDatum) {
        this.db_connection.each(`INSERT INTO StromzahlerWartung (StromzahlerID,	Einbaudatum, letztesEichungsDatum, letzesWartungsDatum) 
            VALUES (?, ?, ?, ?)`,
            [random_id, random_einbaudatum, random_letztesEichungsDatum, random_letztesWartungsDatum],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

    //to do 
    fill_verbrauch_db(stromzahlerID, stromverbrauchGesamt, stromverbrauchJetzt) {
        this.db_connection.each(`INSERT INTO StromzahlerVerbrauch (StromzahlerID, StromverbrauchGesamt, StromverbrauchJetzt) 
            VALUES (?, ?, ?)`,
            [stromzahlerID, stromverbrauchGesamt, stromverbrauchJetzt],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row);
            });
    }

}

module.exports = dbConnector