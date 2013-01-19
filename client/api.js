
var _lastestupdate = "";
var _playlistId = 1;

//TODO: Remove this
var user_id = "1337";


function callAPI(api_function, callback_function) {
	request = "http://bok.alexanderheldt.se:8080/api/"+api_function + "/";
	console.log("Running the request: " + request)
	$.getJSON(request, function(data){
		console.log("Reply from server.");
		callback_function(data);
	});
}



setInterval(checkServer, 5000);
function checkServer(){
	//Check if the current timestamp is newer then _lastestupdate
  	console.log("Checking database for changes...");

	//callAPI("test", onTestResult);
}

function onTestResult(data) {
	console.log("test");
	console.log(data)
}


// Vote for a track
function vote(track_id) {
	//API -> bok.alexanderheldt.se:8080/api/vote/<playlist_id>/<track_id>/<facebook_id>
	//callAPI("vote/"+_playlistId+"/"+track_id+"/"+user_id, alert);
}

function addSong(track_id) {
	//API -> bok.alexanderheldt.se:8080/api/add-song/<playlist_id>/<track_id>

}
