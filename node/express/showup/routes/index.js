var express = require('express');
var router = express.Router();

var google = require('googleapis');
var OAuth2 = google.auth.OAuth2;

var oauth2Client = new OAuth2(
  "377772959689-bcknbu9demsg3v85gbmg7t2he94593ps.apps.googleusercontent.com",
  "Q9jscTdwWHcw4LU8QcBBAuI9",
  "http://riven.zspin.com:3000/google_auth_complete"
);

// generate a url that asks permissions for Google+ and Google Calendar scopes
var scopes = [
  'https://www.googleapis.com/auth/plus.me',
  'https://www.googleapis.com/auth/calendar'
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
	  scope: scopes
	});

	res.redirect(url);
});



module.exports = router;
