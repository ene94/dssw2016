function asyncValidation()
{
  var XMLHttpRequestObject = new XMLHttpRequest();
  var response;
  var email = document.getElementById("email");

  var params = "?email2=" + email.value;
  if(XMLHttpRequestObject)
  {
    XMLHttpRequestObject.onreadystatechange = function()
    {
      if (XMLHttpRequestObject.readyState==4)
      {
        response = XMLHttpRequestObject.responseText;
        if (response == ""){
          document.getElementById("emailCorrect").innerHTML = "OK =)";
          document.getElementById("emailError").innerHTML= "";
        }
        else{
          document.getElementById("emailCorrect").innerHTML = "";
          document.getElementById("emailError").innerHTML= response;
        }
      }
    }
    XMLHttpRequestObject.open("get","/register/asyncValidation/" + params, true);
    XMLHttpRequestObject.send(null);
  }

}

function checkingEmailMessage()
{
  var text = document.getElementById("emailError");
  text.innerHTML= "";
  var good = document.getElementById("emailCorrect");
  good.innerHTML = "loading ...";
}
