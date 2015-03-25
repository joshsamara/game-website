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

function updateTotalRatings() {
    $.get(total_ratings_url, function (data) {
        console.log(data);
        $("#number-ratings").text(data.total_ratings);
    });
}

$(updateTotalRatings());

$.ajax(ratings_url, {
    type: 'GET',
    dataType: 'application/json',
    statusCode: {
        200: function (data) {
            var response = JSON.parse(data.responseText);
            console.log(response);
            $("#gameRating").rateit('value', response.value)
        },
        401: function () {
            $("#gameRating").rateit('value', avg_rating)
        }
    }
});

$("#gameRating")
    .bind('rated', function (event, value) {
        var data = {
            'value': value
        };

        $.ajax(ratings_url, {
                type: 'PUT',
                dataType: 'application/json',
                data: JSON.stringify(data),
                statusCode: {
                    201: function () {
                        updateTotalRatings(213);
                    },
                    401: function () {
                        alert('You must be logged in to rate a game!');
                    }
                },
                complete: updateTotalRatings()
            }
        );
    })
    .bind('reset', function () {
        $.ajax(ratings_url, {
                type: 'DELETE',
                dataType: 'application/json',
                statusCode: {
                    204: function () {
                        // For some reason 'complete' is firing before the success, so I
                        // moved the update into here
                        updateTotalRatings()
                    },
                    401: function () {
                        alert('You must be logged in to rate a game!');
                    }
                }
            }
        )
    });