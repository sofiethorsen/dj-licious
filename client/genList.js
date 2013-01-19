var builder = "";
var imgSrc = "http://www.beatmyday.com/wp-content/uploads/2012/07/Florence-+-The-Machine-Spectrum-Say-My-Name.jpeg";
var name = "Spectrum (Say My Name)";
var artist = "Florence + The Machine";

for(var i=0; i < 4; i++) {
	builder += "<div class=\"queueContainer\">";
	builder += "<div class=\"queueImgContainer\">";
	builder += "<img style=\"width: 100px; height: 100px\" src=\" ";
	builder += imgSrc;
	builder += "\"></div>";

	builder += "<div class=\"queueTextContainer\">";
    builder += name;
    builder += "</br>"
    builder += artist;
    builder += "</div>";

    builder += "<div class=\"queueVoteContainer\">";
    builder += "<img src=\"img/upvote.png\" width=\"30\" height=\"30\"/>";
    builder += "<img src=\"img/downvote.png\" width=\"30\" height=\"30\">";
    builder += "</div>";
    builder += "</div>";
}



$(function() {
	$("#queueList").append(builder);
});