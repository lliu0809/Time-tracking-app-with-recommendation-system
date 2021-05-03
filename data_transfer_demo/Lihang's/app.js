const http = require('http');
const fs = require('fs');
var file;

let obj = {
    user_activities: []
};

const server = http.createServer(function(req, res){
	let file

	try{
		file = fs.readFileSync('./index.html');
	}
	catch(e){
		res.writeHead(404, {'content-type': 'text/plain'});
		res.write('404 File Not Found!');
		res.end();
		return;
	}

	if(file){
		res.writeHead(200, {'content-type': 'text/html'});
		res.write(file);
		res.end();
	}

	req.on('data', (data)=>{
		var arr = decodeURIComponent(data).replace(/\+/g, ' ').replace('date=', '')
				.replace('start=', '').replace('end=', '').replace('activity=', '')
				.replace('preference=', '').split('&');


		let m_activity = {
				date: arr[0], 
				start: arr[1], 
				end: arr[2], 
				activity: arr[3], 
				preference: arr[4]
		};

		fs.exists('activity_log.json', function(exists) {
		    if (exists) {
		        fs.readFile('activity_log.json', function readFileCallback(err, data) {
		            if (err) {
		                console.log(err);
		            } else {
		                obj = JSON.parse(data);
		                obj.user_activities.push(m_activity);
		                let json = JSON.stringify(obj);
		                fs.writeFile('activity_log.json', json, (err)=>{
							if(err){
								throw err;
							}
						});
		            }
		        });
		    } 
		    else {
		        obj.user_activities.push(m_activity)
		        let json = JSON.stringify(obj);
		        fs.writeFile('activity_log.json', json, 'utf8', (err)=>{
					if(err){
						throw err;
					}
				});
		    }
		});
	});

}).listen(3000, ()=>{console.log('Server running on 3000');});