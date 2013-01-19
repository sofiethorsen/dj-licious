
var _lastestupdate = "";
var _playlistId = "50fad3edcf1e8c46163c0d7d";


//http://bok.alexanderheldt.se:8080/api/

//TODO: Remove this
var user_id = "1337";
 

function callAPI(api_function, callback_function) {
	request = "http://bok.alexanderheldt.se:8080/api/"+api_function;
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

	getPlaylist();
}



function getPlaylist() {
	callAPI("get-playlist/?playlist_id="+_playlistId, console.log);
}

// Vote for a track
function vote(track_id) {
	//API -> bok.alexanderheldt.se:8080/api/vote/<playlist_id>/<track_id>/<facebook_id>
	//callAPI("vote/"+_playlistId+"/"+track_id+"/"+user_id, alert);
}

function addSong(track_id) {
	//API -> bok.alexanderheldt.se:8080/api/add-song/<playlist_id>/<track_id>
}
