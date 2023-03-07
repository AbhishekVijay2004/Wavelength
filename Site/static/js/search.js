function Search(){
  var userQuery = document.getElementById("search-box").value;
  fetch("{{url_for('song')}}", {
    method: "POST",
    body: JSON.stringify({
      query: userQuery
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
  .then((response) => response.text())
  .then((json) => console.log(json));
  var NUM_RESULTS = 5;
  for (var i = 0; i < NUM_RESULTS; i++){
    var indexString = i.toString();
    document.getElementById("search-image-" + indexString).src = "{{images[" + indexString + "]}}";
    document.getElementById("search-title-" + indexString).src = "{{titles[" + indexString + "]}} - {{artists[" + indexString + "]}}";
  }
}
