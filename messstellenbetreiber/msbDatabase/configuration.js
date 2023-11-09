const config = require("./config.json");
class configuration {
    getAllConfig() {
        return config;
    }

    getPorts() {
        return this.getAllConfig()["port"];
    }

    getAllDatabaseConfig() {
        return this.getAllConfig()["database"];
    }

    getDatabaseType() {
        return this.getAllDatabaseConfig()["type"];
    }

    getDatabaseLocation() {
        return this.getAllDatabaseConfig()["location"];
    }
}

module.exports = configuration;