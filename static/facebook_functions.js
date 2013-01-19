


function onFBConnected() {
	FB.api('/me', function(response) {
		// Initiate the FB.user object
		FB.user = response;
		console.log(FB.user);
	});

	
}

function onFBLogin() {
	onFBConnected();
}

function onFBCancelledLogin() {
}

function onFBLogout() {
}

function onFBNotAuthorized() {
}

function onFBNotLoggedIn() {
}

function login() {
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
	FB.logout(function(response) {
		onFBLogout();
	});
}


window.fbAsyncInit = function() {
	FB.init({
	    appId      : '239735496161666', // App ID
	    channelUrl : 'http://www.csc.kth.se/~jbrodi/spotify/index.htm', // Channel File
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