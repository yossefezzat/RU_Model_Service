const ps = require('python-shell')
const path = require('path')

import readingModel from "../repository/readingModel";
// Getting cv with cvID
const pdfReader = (req, res) => {
    const {
        jobID,
        folder
    } = req.query;
    const pdfs_path = path.join(__dirname, folder);
    const ontology = path.join(__dirname, 'skill_ontologyFiltered.txt');
    const others = path.join(__dirname, 'others.txt');
    const options = {
        args: [pdfs_path, ontology, others],
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: path.join(__dirname, 'Model_py'),
    }
    ps.PythonShell.run('clean_data.py', options, function (err, results) {
        if (err) throw err;
        const data = JSON.parse(results);
        const resumesData = new readingModel({
            jobID: jobID,
            path: folder,
            resumes: data.resumes
        });
        resumesData.save()
            .then((resume) => res.json(resume))
            .catch((err) => res.status(400).json(err))
    });
}

module.exports = {
    pdfReader
};

/*
        const options = {
            //pythonPath: 'C:\\Users\\Joe\\AppData\\Local\\Programs\\Python\\Python37\\python.exe',
            pythonOptions: ['-u'], // get print results in real-time
            scriptPath: 'Model_py',
        }
        ps.PythonShell.run('clean_data.py', options, function (err, results) {
            if (err) throw err;
            const data = JSON.parse(results);
            console.log(data['resumes'][0]['job_skills']);
        });
        */
