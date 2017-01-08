function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  document.getElementById('googleID').innerHTML = profile.getId();
  document.getElementById('googleName').innerHTML = profile.getName();
  document.getElementById('googleEmail').innerHTML = profile.getEmail();
  document.getElementById('googleImage').src = profile.getImageUrl();
}

function onSignInFailure(googleUser) {
  //doSomething
  alert('FALLOOO');
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    //alert('User signed out.');
  });
}
