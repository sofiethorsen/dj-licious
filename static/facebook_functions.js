
function onFBConnected() {
	console.log("onFBConnected");
	FB.api('/me', function(response) {
		// Initiate the FB.user object
		FB.user = response;
		$.mobile.changePage( ($("#page_home")));
		$.mobile.hidePageLoadingMsg();
	});
	
	setInterval(checkServer, 2000);
}

function onFBLogin() {
	console.log("onFBLogin");
	onFBConnected();
}

function onFBCancelledLogin() {
	console.log("onFBCancelledLogin");
	$.mobile.changePage( ($("#page_login")));
	$.mobile.hidePageLoadingMsg();
}

function onFBLogout() {
	$.mobile.changePage( ($("#page_login")));
	FB.user = {};
}

function onFBNotAuthorized() {
	console.log("onFBNotAuthorized");
	$.mobile.changePage( ($("#page_login")));
	$.mobile.hidePageLoadingMsg();
}

function onFBNotLoggedIn() {
	console.log("onFBNotLoggedIn");
	$.mobile.changePage( ($("#page_login")));
	
	$.mobile.hidePageLoadingMsg();
}

function login() {
	$.mobile.showPageLoadingMsg();
	FB.getLoginStatus(function(response) {
		if (response.status === 'connected') {
			onFBConnected();
		}
		else {
			FB.login(function(response) {
				if (response.authResponse) {
					onFBLogin();
				} else {
					onFBCancelledLogin();
				}
			});
		}
	});	
}

function logout() {
	$.mobile.showPageLoadingMsg();
	FB.logout(function(response) {
		onFBLogout();
	});
}


window.fbAsyncInit = function() {
	$.mobile.showPageLoadingMsg();
	FB.init({
	    appId      : '239735496161666', // App ID
	    channelUrl : 'http://10.48.18.111/client/', // Channel File
	    status     : true, // check login status
	    cookie     : true, // enable cookies to allow the server to access the session
	    xfbml      : true  // parse XFBML
	});
	FB.getLoginStatus(function(response) {

		if (response.status === 'connected') {
			onFBConnected();
		} else if (response.status === 'not_authorized') {
			onFBNotAuthorized();
		} else {
			onFBNotLoggedIn();
		}
	});
};

// Load the SDK Asynchronously
(function(d){
	var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "http://connect.facebook.net/en_US/all.js";
	ref.parentNode.insertBefore(js, ref);
}(document));