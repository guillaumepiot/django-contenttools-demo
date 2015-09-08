ImageUploader = function(dialog) {
     var image, xhr, xhrComplete, xhrProgress;

    // Set up the event handlers
    dialog.bind('imageUploader.cancelUpload', function () {
        // Cancel the current upload

        // Stop the upload
        if (xhr) {
            xhr.upload.removeEventListener('progress', xhrProgress);
            xhr.removeEventListener('readystatechange', xhrComplete);
            xhr.abort();
        }

        // Set the dialog to empty
        dialog.state('empty');
    });

    dialog.bind('imageUploader.clear', function () {
        // Clear the current image
        dialog.clear();
        image = null;
    });

    dialog.bind('imageUploader.fileReady', function (file) {
    	console.log(file)
        // Upload a file to the server
        var formData;

        // Define functions to handle upload progress and completion
        xhrProgress = function (ev) {
            // Set the progress for the upload
            dialog.progress((ev.loaded / ev.total) * 100);
        }

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
            if (parseInt(ev.target.status) == 200) {
                // Unpack the response (from JSON)
                var response = JSON.parse(ev.target.responseText);

                // Store the image details
                image = {
                    size: reponse.size,
                    url: response.url
                    };

                // Populate the dialog
                dialog.populate(image.url, image.size);

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }

        // Set the dialog state to uploading and reset the progress bar to 0
        dialog.state('uploading');
        dialog.progress(0);

        // Build the form data to post to the server
        formData = new FormData()
        formData.append('image', file)

        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', xhrProgress);
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        xhr.open('POST', '/api/images/add/', true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(formData);
    });

	dialog.bind('imageUploader.save', function () {
        var crop, cropRegion, formData;

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
                    response.url,
                    response.size,
                    {
                        'alt': response.alt,
                        'data-ce-max-width': image.size[0]
                    });

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }

        // Set the dialog to busy while the rotate is performed
        dialog.busy(true);

        // Build the form data to post to the server
        formData = new FormData();
        formData.append('url', image.url);

        // Set the width of the image when it's inserted, this is a default
        // the user will be able to resize the image afterwards.
        formData.append('width', 600);

        // Check if a crop region has been defined by the user
        if (dialog.cropRegion()) {
            formData.append('crop', dialog.cropRegion());
        }

        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        xhr.open('POST', '/api/images/add/', true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(formData);
    });

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
                image = {
                    size: reponse.size,
                    url: response.url
                    };

                // Populate the dialog
                dialog.populate(image.url, image.size);

            } else {
                // The request failed, notify the user
                new ContentTools.FlashUI('no');
            }
        }

        // Set the dialog to busy while the rotate is performed
        dialog.busy(true);

        // Build the form data to post to the server
        formData = new FormData();
        formData.append('url', image.url);
        formData.append('direction', direction);

        // Make the request
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('readystatechange', xhrComplete);
        xhr.open('POST', '/rotate-image', true);
        xhr.send(formData);
    }

    dialog.bind('imageUploader.rotateCCW', function () {
        rotateImage('CCW');
    });

    dialog.bind('imageUploader.rotateCW', function () {
        rotateImage('CW');
    });

}

ContentTools.IMAGE_UPLOADER = ImageUploader;
