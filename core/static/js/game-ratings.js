/**
 * This file handles the AJAX required to use the star ratings
 */

var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#gameRating").bind('rated', function (event, value) {
    var data = {
        'value': value
    };

    $.ajax(ratings_url, {
            type: 'PUT',
            dataType: 'application/json',
            data: JSON.stringify(data),
            statusCode: {
                204: function (response) {
                    alert('204');
                },
                401: function (response) {
                    alert('You must be logged in to rate a game!');
                }
            }
        }
    )
});