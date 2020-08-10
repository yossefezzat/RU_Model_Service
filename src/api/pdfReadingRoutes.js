import express from "express";
import {
    pdfReader
} from "../service/pdfReadingController";

const router = express.Router();

router.route("/readPdf")
    .get(pdfReader);


module.exports = router;
