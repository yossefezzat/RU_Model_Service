import mongoose from "mongoose";

const CVSchema = mongoose.Schema({
    jobID: {
        type: String,
        required: true
    },
    path: {
        type: String,
        required: true
    },
    resumes: {
        type: Array,
        required: true
    },
    created_date: {
        type: Date,
        default: Date.now
    }
});

const readingModel = mongoose.model('Service_Cvs', CVSchema);

module.exports = readingModel;
