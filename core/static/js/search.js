// constructs the suggestion engine
var games = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: '/games/api',
    replace: function(url, query) {
      return url + "?term=" + query;
    },
  filter: function(data){
    // Typeahead js is broken when you have 5 items
    if (data.length === 5){
      data.push({});
    }
    return data;
  }
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

$('#searchBtn').click(function(){
  term = $('.tt-input').val();
  url = '/games/search/?term=' + term;
  window.location.href = url;
});

$('.tt-input').keypress(function(e){
  if (e.which == 13){
    $("#searchBtn").click();
  }
});
