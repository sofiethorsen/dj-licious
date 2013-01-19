
var _lastestupdate = "";
var _playlistId = "50fae543cf1e8c48dcd6e42b";

function callAPI(api_function, callback_function) {
	request = "http://bok.alexanderheldt.se:8080/api/"+api_function;
	console.log("Running the request: " + request)
	$.getJSON(request, function(data){
		console.log("Reply from server.");
		console.log(data);
		callback_function(data);
	});
}



setInterval(checkServer, 5000);
function checkServer(){
	//Check if the current timestamp is newer then _lastestupdate
  	console.log("Checking database for changes...");

	getPlaylist();
}



function addSong(href) {
	callAPI("add-track/?playlist_id"+_playlistId+"=&facebook_id="+FB.user.id+"&artist=test&album=test&uri="+href+"&track=test", console.log);
}

function removeSong(href) {
    
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
