const ps = require('python-shell')

const options = {
    //pythonPath: 'C:\\Users\\Joe\\AppData\\Local\\Programs\\Python\\Python37\\python.exe',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: 'Model_py/',
}

ps.PythonShell.run('clean_data.py', options, function (err, results) {
    if (err) throw err
    const data = JSON.parse(results)
    console.log(data['resumes'][0]['job_skills'])
});
