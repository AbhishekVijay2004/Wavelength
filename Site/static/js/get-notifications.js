$.ajax({
  url: '/getNotifications',
  type: 'GET',
  success: function(data) {
    var newHTML = "<h2 class='notifications-title'>Notifications</h2>";
    for (var i = 0; i < data.length; i++){
      if (data[i].title == "Follow Request"){
        newHTML += "<div class='notification-box' id='notification-" + i.toString() + "' style='height:13vw;'><h3 class='notification-type'>" + data[i].title + "<img class='notification-close' onclick='CloseNotification(\"" + i.toString() + "\")'></h3><img class='notification-picture' src='" + data[i].profilePic + "'><p class='notification-name'>" + data[i].name + "</p><div class='follow-accept-button' onclick='AcceptRequest(\"" + data[i].name + "\")'>Accept</div></div>";
      }
      else{
        newHTML += "<div class='notification-box' id='notification-" + i.toString() + "'><h3 class='notification-type'>" + data[i].title + "<img class='notification-close' onclick='CloseNotification(\"" + i.toString() + "\")'></h3><img class='notification-picture' src='" + data[i].profilePic + "'><p class='notification-name'>" + data[i].name + "</p></div>";
      }
    }
    document.getElementById("notifications-container").innerHTML = newHTML;
  },
  error: function(error) {
  console.error(error);
  }
});

function CloseNotification(notificationNum){
  var elem = document.getElementById("notification-" + notificationNum);
  elem.remove();
}
