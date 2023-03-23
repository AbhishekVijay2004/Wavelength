function friendSearching() {
    hideFriends()
    var query = document.getElementById('search-box').value;
    if (query.length == 0){
        showFriends()
    }
    $.ajax({
    url: "/friendSearch/" + query,
    success: function(data) {
        displaySearchResults(data);
    }
    });
}

function displaySearchResults(string) {
    var html = '';
    const data = JSON.parse(string);
    console.log(data);
    console.log(data["usernameResults"]);
    for (var i = 0; i < data["usernameResults"].length; i++) {
        html += '<div class="profile-element">';
        html += '<div class="content-container">';
        html += '<img class="profile-image" src="' + data.profile_picResults[i] + '"></img>';
        html += '<p class="profile-text-header" onclick="navigateToProfilePage(\'' + data.usernameResults[i] + '\')">@' + data.usernameResults[i] + '</p>';
        html += '<p class="profile-text-details">Friends: ' + data.users_num_followerResults[i] + '</p>';
        html += '<p class="profile-text-details">Posts: ' + data.users_num_postResults[i] + '</p>';
        html += '<p class="profile-text-details">Likes: ' + data.users_num_likeResults[i] + '</p>';
        html += '<p class="profile-text-details">Comments: ' + data.users_num_commentResults[i] + '</p>';
        html += '<div>';
        html += '<img class="follow" onclick="followProfile(\'' + data.usernameResults[i] + '\')">';
        html += '</div>';
        html += '</div>';
        html += '</div>';
    }
    document.getElementById("searchResults").innerHTML = html;
}  

function showFriends() {
    document.getElementById("friendSearch").style.display = "block";
    document.getElementById("searchResults").style.display = "none";
}

function hideFriends() {
    document.getElementById("friendSearch").style.display = "none";
    document.getElementById("searchResults").style.display = "block";
}

function followProfile(query) {
    $.ajax({
        url: "/friendSearch/follow/" + query,
        data: {query: query},
        success: function(data) {
            console.log(data);
        }
    });
}

function unfollowProfile(query) {
    $.ajax({
        url: "/friendSearch/unfollow/" + query,
        data: {query: query},
        success: function(data) {
            console.log(data);
        }
    });
}

function navigateToProfilePage(username) {
    window.location.href = '/profile/' + username;
}