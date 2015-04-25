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
