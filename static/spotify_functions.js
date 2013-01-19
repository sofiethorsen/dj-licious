// Search for songs from Spotify
function searchSong(search_string) {
	// String to lower case and UTF-8 format
	needle = encodeURIComponent(search_string.toLowerCase());
	// Sends the request to spotify and handle the result with the function onSpotifyResult
	$.getJSON("http://ws.spotify.com/search/1/track.json?q="+needle,
		function(data){onSpotifyResult(data);});

	//$.mobile.showPageLoadingMsg();
	//$.mobile.hidePageLoadingMsg();
}

// Runs when data from Spotify Web API is loaded
function onSpotifyResult(result) {
	console.log(result);
}

//TODO: Have a cache?