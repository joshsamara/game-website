var app = angular.module("HomePage", ['ngAnimate']);

app.controller("ListController", function($scope, $http){
  // Do a search, set the field in the scope to the response
  function search(params, field){
    $http({url: "/games/api", method: "GET", params: params})
      .success(function(response){
        $scope[field] = response;
      }
      );
  }

  // Initial setup
  search({featured: true}, 'featured');
  search({term: ''}, 'games');
  search({top: true}, 'top_games');
  search({recent: true}, 'recent');


  // Make a search function available to the scope
  $scope.search = function(){
    search({term: $scope.search_term}, 'games');
  };

});

// Add a filter to cut down super long strings
app.filter('summarize', function () {
  return function (input) {
    if (input.length > 100){
        input = input.substring(0,100) + '...';
    }
      return input;
    };
});

app.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  };
});

// constructs the suggestion engine
var games = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // `states` is an array of state names defined in "The Basics"
  remote: {
    url: '/games/api',
    replace: function(url, query) {
      return url + "?term=" + query;
    },
  }
});

$('.typeahead').typeahead({
  hint: true,
  highlight: true,
},
{
  name: 'games',
  display: 'name',
  source: games
});
