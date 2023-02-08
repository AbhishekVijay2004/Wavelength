function backendTest(){
  alert("Working.");
}
var xhr = null;
  getXmlHttpRequestObject = function () {
      if (!xhr) {
          // Create a new XMLHttpRequest object
          xhr = new XMLHttpRequest();
      }
      return xhr;
  };
  function dataCallback() {
      // Check response is ready or not
      if (xhr.readyState == 4 && xhr.status == 200) {
          console.log("Info received!");
          dataDiv = document.getElementById('result-container');
          // Set current data text
          dataDiv.innerHTML = xhr.responseText;
      }
  }
  function getInfo() {
      console.log("Get info...");
      xhr = getXmlHttpRequestObject();
      xhr.onreadystatechange = dataCallback;
      // asynchronous requests
      xhr.open("GET", "http://localhost:6969/users", true);
      // Send the request over the network
      xhr.send(null);
  }
