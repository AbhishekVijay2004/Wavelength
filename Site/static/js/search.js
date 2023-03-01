function Search(){
  var query = document.getElementById("search-box").value;
  window.location.href = "{{url_for('search_song')}}";
  var NUM_RESULTS = 5;
  for (var i = 0; i < NUM_RESULTS; i++){
    var indexString = i.toString();
    document.getElementById("search-image-" + indexString).src = "{{images[" + indexString + "]}}";
    document.getElementById("search-title-" + indexString).src = "{{titles[" + indexString + "]}} - {{artists[" + indexString + "]}}";
  }
}
