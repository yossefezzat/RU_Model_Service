import { expect } from "chai";
import chai from "chai";
import config from "config";
import request from "supertest";
import service from "../service.js";
require("babel-polyfill");


// Extend Chai to check json
chai.use(require('chai-json'));

/*
// Testing server port
describe("Server", ()=>{
    it("tests that server is running in the current port", ()=>{
        expect(service.port).to.equal(parseInt(config.get("app.port")));
    })
});
*/


// Testing api end point
describe("API end points", () => {
    // Testing api end point working with prefix
    it(`Should work with the prefix in config file (${config.get("api.prefix")})`, async()=>{
        const response = await request(service).get("/api/v1/login/");
        expect(response.status).to.equal(200);
        console.log(response.body + "  " + typeof response.body);
        expect(response.body).to.be.jsonObj();
    })
});
