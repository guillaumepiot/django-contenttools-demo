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

(function() {
	window.onload = function() {
	    var editor;
		ContentTools.StylePalette.add([
			new ContentTools.Style('By-line', 'article__by-line', ['p']), 
			new ContentTools.Style('Caption', 'article__caption', ['p']), 
			new ContentTools.Style('Example', 'example', ['pre']), 
			new ContentTools.Style('Example + Good', 'example--good', ['pre']), 
			new ContentTools.Style('Example + Bad', 'example--bad', ['pre'])]);

		editor = ContentTools.EditorApp.get();
		editor.init('.editable', 'data-name');

		editor.bind('save', function (regions) {
		    var name, onStateChange, payload, xhr;
		    var data = JSON.stringify(regions)

		    // Set the editor as busy while we save our changes
		    this.busy(true);

		    // Send the update content to the server to be saved
		    onStateChange = function(ev) {
		        // Check if the request is finished
		        if (ev.target.readyState == 4) {
		            editor.busy(false);
		            if (ev.target.status == '201') {
		                // Save was successful, notify the user with a flash
		                new ContentTools.FlashUI('ok');
		            } else {
		                // Save failed, notify the user with a flash
		                new ContentTools.FlashUI('no');
		            }
		        }
		    };

		    console.log(typeof(data))

			API.call('post', '/api/add/', data, true, onStateChange)

		});
	}
}).call(this);