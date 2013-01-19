function getFromApi(api_function, callback_function) {
	$.getJSON("http://bok.alexanderheldt.se:8080/api/"+api_function
		, function(data){callback_function(data);});
}


function test() {
	getFromApi("test", onTestResult);
}

function onTestResult(data) {
	console.log("test");
	console.log(data)
}
