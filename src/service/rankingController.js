const ps = require('python-shell')
const path = require('path')

import readingModel from "../repository/readingModel";
import rankingModel from "../repository/rankingModel";


const weightRanking = (req, res) => {
    let jobResumes;
    const {
        jobID,
        desc

    } = req.query;
    console.log(jobID)
    readingModel.find({
            jobID: jobID
        })
        .then((data) => {
            jobResumes = data;
            const options = {
                mode: '',
                args: [JSON.stringify(jobResumes), desc],
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: path.join(__dirname, 'Model_py'),
            }
            ps.PythonShell.run('ranking_model.py', options, function (err, results) {
                if (err) throw err;
                //res.json(results);
                const data = JSON.parse(results)
                const weighted_CVs = new rankingModel({
                    jobID: jobID,
                    CVs: data.cvs
                });
                weighted_CVs.save()
                    .then((data) => res.json(data))
                    .catch((err) => res.status(400).json(err))

            });
        })
        .catch((err) => res.status(400).json(err))
}

module.exports = {
    weightRanking
};
