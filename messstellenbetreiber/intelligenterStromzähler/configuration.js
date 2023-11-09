
const config = require("./config.json");
class configuration {
    getAllConfig() {
        return config;
    }

    getId() {
        return config["id"];
    }

    getTimeInterval() {
        return this.getAllConfig()["time_interval"];
    }

    getSaveSchema() {
        return this.getAllConfig()["save_schema"];
    }

    getSaveURL() {
        return this.getSaveSchema()["url"];
    }
    getSaveIdName() {
        return this.getSaveSchema()["stromzaehler_id"];
    }
    getSaveTimestampName() {
        return this.getSaveSchema()["timestamp"];
    }

    getSaveConsumptionName() {
        return this.getSaveSchema()["totalPowerConsumption"];
    }

    getAllSimulationConfig() {
        return this.getAllConfig()["simulation"];
    }

    getSimulationMinAdd() {
        return this.getAllSimulationConfig()["minAdd"];
    }

    getSimulationMaxAdd() {
        return this.getAllSimulationConfig()["maxAdd"];
    }
}

module.exports = configuration;