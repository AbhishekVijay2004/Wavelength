function Search() {
  var userQuery = document.getElementById('search-box').value;
  $.ajax({
    url: '/song',
    data: {query: userQuery},
    type: 'GET',
    success: function(data) {
      var NUM_RESULTS = 5;
      for (var i = 0; i < NUM_RESULTS; i++){
        var indexString = i.toString();
        document.getElementById("search-result-" + indexString).setAttribute("onmousedown", "ResultSelected('" + data[i].id + "')");
        document.getElementById("search-image-" + indexString).src = data[i].image;
        document.getElementById("search-title-" + indexString).textContent = data[i].title;
      }
    },
    error: function(error) {
    console.error(error);
    }
  });
}
function ResultSelected(result){
  var pageID = document.getElementById("pageID").innerHTML;
  $.ajax({
    url: '/selectResult',
    data: {id: result, page: pageID},
    type: 'GET',
    success: function(data) {
      document.getElementById("resultBackground").style.backgroundImage = "url('" + data[0].image + "')";
      document.getElementById("resultImage").style.backgroundImage = "url('" + data[0].image + "')";
      document.getElementById("resultTitle").innerHTML = data[0].title;
      document.getElementById("resultArtist").innerHTML = data[0].artist;
      document.getElementById("resultAudio").src = data[0].audio;
      document.getElementById("resultPreview").style.display = "block";
    },
    error: function(error) {
      console.error(error);
    }
  });
  if (pageID == "newPost"){
    document.getElementById("postButton").setAttribute("onclick", "PostSong(" + result + ")");
  }
  document.getElementById("selectedSongID").value = result;
}
