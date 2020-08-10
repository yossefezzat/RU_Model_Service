'use strict';
require('dotenv').config();
module.exports = {
    app: {
        name: "RankingService",
        baseUrl: `http://localhost:`,
        port: process.env.PORT || 3000
    },
    api: {
        prefix: '^/api/v[1-9]',
        version: [1],
    },
    database: {
        url: process.env.DB_URL || "mongodb://localhost:27017/RUModelDB",
    }
};
