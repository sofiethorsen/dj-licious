// Search for songs from Spotify
function searchSong(search_string) {
	$.mobile.showPageLoadingMsg();
	// String to lower case and UTF-8 format
	needle = encodeURIComponent(search_string.toLowerCase());
	// Sends the request to spotify and handle the result with the function onSpotifyResult
	$.getJSON("http://ws.spotify.com/search/1/track.json?q="+needle,
		function(data){onSpotifyResult(data);});
}

// Runs when data from Spotify Web API is loaded
function onSpotifyResult(result) {
	data = parseSpotifyData(result);
	console.log(data);

	$.mobile.hidePageLoadingMsg();
}


function parseSpotifyData(result) {
	data = {};
	data.tracks = [];

	data.total_num_results = result.info.num_results;
	data.num_results = Math.min(data.total_num_results, 100);

	for (var i=0;i<data.num_results;i++)
	{ 
		track = {};
		track.artist = result.tracks[i].artists[0].name;
		track.name = result.tracks[i].name;
		data.tracks[i] = track;
	}
	return data;
}

//TODO: Have a cache?
// search_string = $("#searchinput1").val();
// searchSong(search_string);




