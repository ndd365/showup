var express = require('express');
var router = express.Router();

var google = require('googleapis');
var OAuth2 = google.auth.OAuth2;
var plus = google.plus('v1');
var calendar = google.calendar('v3');

var oauth2Client = new OAuth2(
  "377772959689-bcknbu9demsg3v85gbmg7t2he94593ps.apps.googleusercontent.com",
  "Q9jscTdwWHcw4LU8QcBBAuI9",
  "http://riven.zspin.com:3000/google_auth_complete"
);

// generate a url that asks permissions for Google+ and Google Calendar scopes
var scopes = [
  'https://www.googleapis.com/auth/calendar',
  'https://www.googleapis.com/auth/userinfo.email',
	'https://www.googleapis.com/auth/userinfo.profile'

];



/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index.html');
});


router.get('/google_auth', function(req, res, next) {

	var url = oauth2Client.generateAuthUrl({
	  // 'online' (default) or 'offline' (gets refresh_token)
	  access_type: 'offline',

	  // If you only need one scope you can pass it as string
	  scope: scopes,
	  state: req.query.calid
	});

	res.redirect(url);
});


router.get('/google_auth_complete', function(req, res, next) {

	console.log("in google google_auth_complete");

	var code = req.query.code;

	// This is bad. Storing calid from state
	var calid = req.query.state;

	console.log(calid);

	oauth2Client.getToken(code, function (err, tokens) {

	  // Now tokens contains an access_token and an optional refresh_token. Save them.
	  if (!err) {	  	
	    oauth2Client.setCredentials(tokens);

	    console.log(tokens);

			// Retrieve tokens via token exchange explained above or set them:
			oauth2Client.setCredentials({
			  access_token: tokens['access_token']
			});

			console.log(oauth2Client);

			calendar_list_entry = {
		    'id': calid
			}

			var greq = calendar.calendarList.insert({
				'resource': calendar_list_entry,
				'auth': oauth2Client
			}, function(err, resp) {

			    if (err) {
			      console.log('The API returned an error: ' + err);
			    }

					console.log(resp);
				  res.redirect("/?calAdded");
			});

	  }
	  else {
	  	console.log(err);
	  	res.redirect("/");
	  }


	});

});





module.exports = router;
