function ShowSearch(){
  var searchContainer = document.getElementById("search-container");
  searchContainer.style.boxShadow = "0vw 0vw 1vw 0.5vw black";
  searchContainer.style.height = "62vh";
}

function HideSearch(){
  var searchContainer = document.getElementById("search-container");
  searchContainer.style.boxShadow = "none";
  searchContainer.style.height = "0";
}
