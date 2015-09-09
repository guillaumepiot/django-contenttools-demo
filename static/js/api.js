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
  // xhr.setRequestHeader('Content-Type', 'application/json');
  
  if (data) {
    xhr.send(data);
  }
};