// Cross Site Request Forgery protection
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = (cookies[i]).replace(/^\s+|\s+$/g, '');
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Create API object
API = {};

API.domain = 'http://127.0.0.1:8000';
      
API.call = function(type, url, data, auth, onSuccess, onError) {
  var r;
  xhr = new XMLHttpRequest();
  xhr.addEventListener('readystatechange', onSuccess);

  if (type == null) {
    type = 'get';
  }
  if (url == null) {
    url = '/';
  }
  if (data == null) {
    data = null;
  }
  if (auth == null) {
    auth = true;
  }
  if (onSuccess == null) {
    onSuccess = null;
  }
  if (onError == null) {
    onError = null;
  }


  url = "" + this.domain + url + "?format=json";
  switch (type) {
    case 'get':
      xhr.open('GET', url);
      break;
    case 'post':
      xhr.open('POST', url);
      break;
    case 'put':
      xhr.open('PUT', url);
      break;
    case 'patch':
      xhr.open('PATH', url);
      break;
    case 'delete':
      xhr.open('DELETE', url);
      break;
    default:
      console.log("Request type " + type + " is not supported");
  }

  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  
  if (data) {
    xhr.send(data);
  }
};