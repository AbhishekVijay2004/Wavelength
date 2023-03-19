$.ajax({
  url: '/fetchPosts',
  data: {startIndex: 0, numToReturn: 0, userProfile: document.getElementById("username").innerHTML},
  type: 'GET',
  success: function(data) {
    for (var i = 0; i < data.length; i++){
      post = data[i];
      for (var val in post){
        if (post[val] == null){
          post[val] = "0";
        }
      }
      //Order: album_art, song_title, artist_name, preview_mp3, postAuthorLink, postAuthorPic, postAuthorName, postTime, postText, posReactCount, negReactCount, commentCount
      container.replaceChild(loadPost(post["songImage"], post["songTitle"], post["artistName"], post["songPreview"], post["posterUsername"], post["posterPic"], post["posterName"], post["postTime"], post["postCaption"], post["postLikes"], post["postDislikes"], post["postComments"], post["postID"]),container.childNodes[3 + i])
    }
  },
  error: function(error) {
  console.error(error);
  }
});
