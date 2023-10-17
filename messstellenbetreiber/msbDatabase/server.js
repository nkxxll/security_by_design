const express = require('express');
const router = require("./router");
const server = express();
const port = 3000;

function main() {
    server.get('/', (req, res) => {
        res.send('Hello World!');
    });

    server.use(router);

    server.listen(port, () => {
        console.log(`Example server listening on port ${port}`);
    });
}

main();