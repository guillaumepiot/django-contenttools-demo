# django-contenttools-demo

This is a basic integration of the [ContentTools](http://getcontenttools.com/) content editor into a Django application using Django REST Framework. It would be interesting to have a look at the original project before diving into this tutorial. You will have a better understanding of what we are doing here.

## Installation

First of all, you will need to download the code from Github [Django ContentTools](https://github.com/Cotidia/django-contenttools-demo).

```
git clone https://github.com/Cotidia/django-contenttools-demo.git
cd contenttools_django
pip install -r requirements.txt
```

## Getting started

The application is divided in two main folders:
* home - Where we are displaying the HTML of the app
* api - We are using Django REST Framework to serve and store the content

The original project is written completely in javascript with no dependencies. We just place it into our static files. 
We copy content-tools.js and create editor.js and image-uploader.js following [ContentTools](http://getcontenttools.com/) and add few tweaks to handle the necessary ajax requests to communicate with the backend.

As we are handling ajax requests, Django asks to add the following piece of code for [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/1.8/ref/csrf/).
This is how our api.js file looks like

### api.js

```javascript
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
```

```javascript

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
```

It will be called from the different files like this, depending on the kind of the request `(GET,POST,PUT,PATCH,DELETE)`.
```javascript
API.call('post', '/api/add/', payload, true, onStateChange)
```

### editor.js

We barely change this file. Just append to the payload on save the different fields for our ajax request.
```javascript
payload = new FormData();
payload.append('page', window.location.pathname);
payload.append('images', JSON.stringify(getImages()));
payload.append('regions', JSON.stringify(regions));
```

### image-uploader.js

This file requires more work as we need to implement the code not only to save the image, but also to update it (rotation and crop) in the server.
For that purpose, we change how the alreader built methods `fileReady` and `save` in *imageUploader* work. We will save the image through `fileReady` and once saved, we will update it with the `save` method.
```javascript
ImageUploader = function(dialog) {
     var image, xhr, xhrComplete, xhrProgress;

    // ... We are skipping code here to make it more legible
```

Let's start with `fileReady`. Keep in mind that on fileReady, we already save the image.

```javascript
    dialog.bind('imageUploader.fileReady', function (file) {
        // Upload a file to the server
        var formData;
```

```javascript
        // Build the form data to post to the server
        formData = new FormData()
        formData.append('image', file)
        // Set the width of the image when it's inserted, this is a default
        // the user will be able to resize the image afterwards.
        formData.append('width', 600);
        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', xhrProgress);
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        API.call('post', '/api/images/add/', formData, true, xhrComplete)
```

Now we need to handle the ajax response. This will require a bit of explanation. 


```javascript
        xhrComplete = function (ev) {
            // Check the request is complete
            if (ev.target.readyState != 4) {
                return;
            }

            // Clear the request
            xhr = null
            xhrProgress = null
            xhrComplete = null

            // Handle the result of the upload
            if (parseInt(ev.target.status) == 201) {
                // Unpack the response (from JSON)
                var response = JSON.parse(ev.target.responseText);
                // Store the image details
                image = {
                    id: response.id,
                    name: response.name,
                    size: getImageSize(response),
                    width: response.edited_width,
                    url: response.image
                    };
                console.log(image.size)
                // Populate the dialog
                dialog.populate(image.url, image.size);

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }
```

We want the user to keep the original size of the image they are uploading, so we will store the full-size image in the backed. 
What we are doing here is taking a generic width (600px) and create a function to display the image with this size in the browser.

```javascript
function getImageSize(response) {
    coef = response.edited_width / response.size[0]
    for(var i=0; i<response.size.length; i++) {
        response.size[i] *= coef;
    }
    return response.size
}
```

Now, let's talk about saving, or updating in our case. The `insert` button will trigger it.

```javascript
	dialog.bind('imageUploader.save', function () {
        var crop, cropRegion, formData;
```

```javascript
        // Build the form data to post to the server
        formData = new FormData();

        // Check if a crop region has been defined by the user
        if (dialog.cropRegion()) {
            formData.append('crop', dialog.cropRegion());
        }

        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        API.call('put', '/api/images/update/' + image.id, formData, true, xhrComplete)
```

The callback is as expected. It only takes into account if we have cropped the image. 
The rotation method will make an ajax call separately every time we rotate the image.

```javascript
        // Define a function to handle the request completion
        xhrComplete = function (ev) {
            // Check the request is complete
            if (ev.target.readyState !== 4) {
                return;
            }

            // Clear the request
            xhr = null
            xhrComplete = null

            // Free the dialog from its busy state
            dialog.busy(false);

            // Handle the result of the rotation
            if (parseInt(ev.target.status) === 200) {
                // Unpack the response (from JSON)
                var response = JSON.parse(ev.target.responseText);

                // Trigger the save event against the dialog with details of the
                // image to be inserted.
                dialog.save(
                    response.image,
                    getImageSize(response),
                    {
                        'alt': response.name,
                        'data-ce-max-width': image.size[0]
                    });

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }
```

The ajax call for the rottion method is the same as the above, but appending `direction` instead of `crop` to `formData`

```javascript
	function rotateImage(direction) {
        // Request a rotated version of the image from the server
        var formData;

        // Define a function to handle the request completion
        xhrComplete = function (ev) {
            // Check the request is complete
            if (ev.target.readyState != 4) {
                return;
            }

            // Clear the request
            xhr = null
            xhrComplete = null

            // Free the dialog from its busy state
            dialog.busy(false);

            // Handle the result of the rotation
            if (parseInt(ev.target.status) == 200) {
                // Unpack the response (from JSON)
                var response = JSON.parse(ev.target.responseText);

                // Store the image details
                image.size = getImageSize(response),
                image.url = response.image

                // Populate the dialog
                dialog.populate(image.url, image.size[0]);

              

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }

        // Set the dialog to busy while the rotate is performed
        dialog.busy(true);

        // Build the form data to post to the server
        formData = new FormData();
        formData.append('direction', direction);

        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        API.call('put', '/api/images/update/' + image.id, formData, true, xhrComplete)
    }

    dialog.bind('imageUploader.rotateCCW', function () {
        rotateImage('CCW');
    });

    dialog.bind('imageUploader.rotateCW', function () {
        rotateImage('CW');
    });

}

