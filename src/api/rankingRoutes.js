import express from "express";
import {
    weightRanking
} from "../service/rankingController";

const router = express.Router();

router.route("/rank")
    .get(weightRanking);


module.exports = router;
