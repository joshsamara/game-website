var app = angular.module("HomePage", ['ngAnimate'])

app.controller("ListController", function($scope, $http){
  // Featured are consistant, set them now
  $http({url: "/games/api", method: "GET", params: {featured: true}})
    .success(function(response){
    $scope.featured = response;
  })

  function search(term){
    $http({url: "/games/api", method: "GET", params: {term: term}})
      .success(function(response){
      $scope.games = response;
    })
  }

  search('');
  $scope.search = function(){
    search($scope.search_term);
  }

})

app.filter('summarize', function () {
  return function (input) {
    if (input.length > 100){
        input = input.substring(0,100) + '...'
    }
      return input;
    };
});
