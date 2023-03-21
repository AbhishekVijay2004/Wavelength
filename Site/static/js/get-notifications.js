$.ajax({
  url: '/fetchNotification',
  type: 'GET',
  success: function(data) {
    var newHTML = "<h2 class='notifications-title'>Notifications</h2>";
    for (var i = 0; i < data.length; i++){
      if (data[i].type == "Follow Request"){
        newHTML += "<div class='notification-box id" + data[i].notificationID + "' id='notification-" + i.toString() + "' style='height:13vw;'><h3 class='notification-type'>" + data[i].type + "<img class='notification-close' onclick='CloseNotification(\"" + i.toString() + "\")'></h3><img class='notification-picture' src='" + data[i].senderPic + "'><p class='notification-name'>" + data[i].sender + "</p><div class='follow-accept-button' onclick='AcceptRequest(\"" + data[i].sender + "\",\"" + i.toString() + "\")'>Accept</div></div>";
      }
      else{
        newHTML += "<div class='notification-box id" + data[i].notificationID + "' id='notification-" + i.toString() + "'><h3 class='notification-type'>" + data[i].type + "<img class='notification-close' onclick='CloseNotification(\"" + i.toString() + "\")'></h3><img class='notification-picture' src='" + data[i].senderPic + "'><p class='notification-name'>" + data[i].sender + "</p></div>";
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
  $.ajax({
    url: '/clearNotification',
    data: {notificationID: elem.classList[1].slice(2)},
    type: 'GET',
    success: function (data) {
      elem.remove();
    },
    error: function(error) {
      console.error(error);
    }
  });
}

function AcceptRequest(username, notificationNum){
  CloseNotification(notificationNum);
}
