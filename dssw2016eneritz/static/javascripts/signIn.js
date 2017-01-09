function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  //fill html values
  document.getElementById('googleID').innerHTML = profile.getId();
  document.getElementById('googleName').innerHTML = profile.getName();
  document.getElementById('googleEmail').innerHTML = profile.getEmail();
  document.getElementById('googleImage').src = profile.getImageUrl();

  //start server session
  $.ajax({
      type: "POST",
      url: "/register/googleLogin/",
      data: {'email': profile.getEmail()}
    });

  document.getElementById('loginButton').disabled = "true";
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
  document.getElementById('loginButton').disabled = "false";
}
