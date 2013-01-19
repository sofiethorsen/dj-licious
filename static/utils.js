var _TRACKS = [];


function generateQueue(data) {
    var builder = "";
    var imgSrc = "http://www.beatmyday.com/wp-content/uploads/2012/07/Florence-+-The-Machine-Spectrum-Say-My-Name.jpeg";
    

    tracks = data.result.tracks;

    for(var i=0; i < tracks.length; i++) {
        builder += "<div class=\"queueContainer\">";
        builder += "<div class=\"queueImgContainer\">";
        builder += "<img style=\"width: 100px; height: 100px\" src=\" ";
        builder += imgSrc;
        builder += "\"></div>";

        builder += "<div class=\"queueTextContainer\">";
        builder += tracks[i].track;
        builder += "</br>"
        builder += tracks[i].artist;
        builder += "</div>";

        builder += "<div class=\"queueVoteContainer\">";
        builder += "<img src=\"{{ url_for('static', filename='img/upvote.png') }}\" width=\"30\" height=\"30\"/>";
        builder += "<img src=\"{{ url_for('static', filename='img/downvote.png') }}\" width=\"30\" height=\"30\">";
        builder += "</div>";
        builder += "</div>";



    }

    return builder;
}

function genGrid(data) {
    var print_num = Math.min(20, data.num_results);
    var builder = "";

    builder += "Showing " + print_num + " of a total of " + data.total_num_results + " tracks. </br>";


    for(var i=0; i < print_num; i++) {
        builder += "<div id=\"item_"+ getSpotifyId(data.tracks[i].href) +"\" onClick=\"onSongClick(\'"+data.tracks[i].href+"\')\" class=\"ui-grid-a\">";
        builder += "<div class=\"ui-block-a\">";
        builder += data.tracks[i].name;
        builder += "</div>";
        builder += "<div class=\"ui-block-b\">";
        builder += data.tracks[i].artist;
        builder += "</div>";
        builder += "</div>";
    }

    return builder;
}

function onSongClick(href) {
    div_id = "#item_"+getSpotifyId(href);
    // Remove song
    if ($(div_id).css("opacity") === "0.5") {
        $(div_id).css("background-color", "rgba(0, 0, 0, 0)");
        $(div_id).css("opacity", "1.0");
    }
    // Add song
    else { 
        addSong(href);
        $(div_id).css("background-color", "lightgreen");
        $(div_id).css("opacity", "0.5");
    }
}



$(function() {

      console.log("HASH:" + window.location.hash);
    



    $("#searchBar").submit(
        function (e) {
        e.preventDefault(); // this will prevent from submitting the form.
        $.mobile.changePage($("#page_search"),{ transition: "fade"});
        search_string = $("#searchinput1").val();
        // Reset the search bar
        $("#searchinput1").val("");
        searchSong(search_string);

        return false;
    });



});


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
    $("#searchResult").html("");
    $("#searchResult").append(genGrid(data));
    $.mobile.hidePageLoadingMsg();
}


function parseSpotifyData(result) {
    data = {};
    data.tracks = [];

    data.total_num_results = result.info.num_results;
    data.num_results = Math.min(data.total_num_results, 100);

    console.log(result);
    for (var i=0;i<data.num_results;i++)
    { 
        track = {};
        track.artist = result.tracks[i].artists[0].name;
        track.name = result.tracks[i].name;

        track.album = result.tracks[i].album.name;
        track.href = result.tracks[i].href;

        data.tracks[i] = track;

        _TRACKS[getSpotifyId(track.href)] = track;
    }



    return data;
}

function getSpotifyId(href) {
    return href.substring(14);
}

//TODO: Have a cache?
// search_string = $("#searchinput1").val();
// searchSong(search_string);




