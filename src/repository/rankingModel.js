import mongoose from "mongoose";

const CVSchema = mongoose.Schema({
    jobID: {
        type: String,
        required: true
    },
    CVs: [{
        path: {
            type: String,
            required: true
        },
        weight: {
            type: Number,
            required: true
        },
        name: {
            type: String,
            required: true
        },
        email: {
            type: String,
            required: false
        },
        class: {
            type: String,
                required: false
        },
    }],
    created_date: {
        type: Date,
        default: Date.now
    }
});

const rankingModel = mongoose.model('jobs_cvs', CVSchema);

module.exports = rankingModel;
