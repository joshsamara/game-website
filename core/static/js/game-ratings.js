/**
 * This file handles the AJAX required to use the star ratings
 */

function updateTotalRatings() {
    $.get(total_ratings_url, function (data) {
        $("#number-ratings").text(data.total_ratings);
    });
}

function resetRating() {
    $.get(total_ratings_url, function (data) {
        $("#gameRating").rateit('value', data.avg_rating).rateit('ispreset', true);
    });
}

$.ajax(ratings_url, {
    type: 'GET',
    dataType: 'json'
}).success(function (data) {
    $("#gameRating").rateit('value', data.value).rateit('ispreset', false);
}).error(function () {
    // An error means that either the user is not
    // authenticated or they haven't rated the game
    resetRating();
});

$("#gameRating")
    .bind('rated', function (event, value) {
        var data = {
            'value': value
        };

        $.ajax(ratings_url, {
                type: 'PUT',
                data: JSON.stringify(data),
                success: updateTotalRatings(),
                statusCode: {
                    401: function () {
                        alert('You must be logged in to rate a game!');
                        resetRating();
                    }
                }
            }
        ).always(updateTotalRatings());
    })
    .bind('reset', function () {
        $.ajax(ratings_url, {
                type: 'DELETE',
                dataType: 'json',
                statusCode: {
                    401: function () {
                        alert('You must be logged in to rate a game!');
                    }
                }
            }
        ).always(function () {
                updateTotalRatings();
                resetRating();
            });
    });