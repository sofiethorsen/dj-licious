
var _lastestupdate = "";


function callAPI(api_function, callback_function) {
	var request = "http://10.48.18.111/api/"+api_function;

	console.log("Called function: " + api_function);

//	$.getJSON(request, function(data, textStatus, xhr){
//		console.log(data);
//		console.log("Status: " + xhr.status);
//		callback_function(data);
//	});


	$.ajax({
	    url: request,
	    dataType: 'json',
	    success: function( data ) {
	      	console.log(data);
		  	callback_function(data);
	    },
	    error: function( data ) {
	    	console.log("ERROR!");
	    	console.log(data);
	    }
  	});
}

function checkServer(){
	getPlaylist();
}



function vote(href, vote) {
	//API bok.alexanderheldt.se:8080/api/vote/<playlist_id>/<track_id>/<facebook_id>/<vote>
	callAPI("vote/?playlist_hash="+_playlistId+"&uri="+href+"&facebook_id="+FB.user.id+"&vote="+vote, onVoteResult);
}

function onVoteResult(data){
	checkServer();
}

function addSong(href) {
	var track = _TRACKS[getSpotifyId(href)];
	callAPI("add-track/?playlist_hash="+_playlistId+"&facebook_id="+FB.user.id+"&artist="+encodeURIComponent(track.artist)+"&album="+encodeURIComponent(track.album)+"&uri="+href+"&track="+encodeURIComponent(track.name), onResultAddsong);
}

function onResultAddsong(data){
	console.log("onResultAddsong");
	checkServer();
}

function removeSong(href) {
   
}


function getPlaylist() {
	callAPI("get-playlist/?playlist_hash="+_playlistId, onResultPlaylist);
}

function onResultPlaylist(data) {
	var imgSrc = "";

	if (data.result.currently_playing.adder === null) {
		imgSrc = "http://www.landinst.com/images/placeholder-100x100.png";
	}
	else {
		imgSrc = "https://graph.facebook.com/"+data.result.currently_playing.adder+"/picture?width=100&height=100";
	}




    $("#mainImgContainer").html('<img style="background:url('+imgSrc+')" src="'+"http://10.48.18.111/static/img/play.png"+'" alt="" />');
	$("#mainTextContainer").html(data.result.currently_playing.track + " </br> " + data.result.currently_playing.artist);
	$("#queueList").html(generateQueue(data));
}
