
var _lastestupdate = "";


function callAPI(api_function, callback_function) {
	request = "http://bok.alexanderheldt.se:8080/api/"+api_function;
	console.log("Called function: " + api_function);
	$.getJSON(request, function(data){
		console.log(data);
		callback_function(data);
	});
}



function checkServer(){
	//Check if the current timestamp is newer then _lastestupdate
  	console.log("Checking database for changes...");
	getPlaylist();
}



function addSong(href) {
	track = TRACKS[getSpotifyId(href)];
	callAPI("add-track/?playlist_id"+_playlistId+"=&facebook_id="+FB.user.id+"&artist="+track.artist+"&album="+track.album+"&uri="+href+"&track="+track.name, onResultAddsong);
}

function onResultAddsong(data){
	console.log("onResultAddsong");
}

function removeSong(href) {
    
}


function getPlaylist() {
	callAPI("get-playlist/?playlist_id="+_playlistId, onResultPlaylist);
}

function onResultPlaylist(data) {
	imgSrc = "https://graph.facebook.com/"+data.result.currently_playing.adder+"/picture?width=100&height=100";
    $("#mainImgContainer").html('<img style="width: 100px; height: 100px" src="'+imgSrc+'"/>');
	$("#mainTextContainer").html(data.result.currently_playing.track + " </br> " + data.result.currently_playing.artist);
	$("#queueList").html(generateQueue(data));
}
