
var _lastestupdate = "";
var _playlistId = 1;


function getFromApi(api_function, callback_function) {
	request = "http://bok.alexanderheldt.se:8080/api/"+api_function;
	console.log("Running the request: " + request)
	$.getJSON(request, function(data){
		console.log("Reply from server.")
		callback_function(data);
	});
}



setInterval(checkServer, 5000);
function checkServer(){
	//Check if the current timestamp is newer then _lastestupdate
  	console.log("Checking database for changes...");

	//getFromApi("test/", onTestResult);

}

function onTestResult(data) {
	console.log("test");
	console.log(data)
}
