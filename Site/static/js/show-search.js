function ShowSearch(){
  var searchContainer = document.getElementById("search-container");
  //searchContainer.style.boxShadow = "0vw 0vw 2vw 0.5vw rgba(0, 0, 0, 0.5)";
  searchContainer.style.height = "62vh";
}

function HideSearch(){
  var searchContainer = document.getElementById("search-container");
  //searchContainer.style.boxShadow = "none";
  searchContainer.style.height = "0";
}

// Implimented my own (Jonny) mini search function for settings and creation page so
// that I didnt break anything you were doing

function ShowMiniSearch(){
  var searchContainer = document.getElementById("search-container");
  searchContainer.style.height = "26vw";
}

function HideMiniSearch(){
  var searchContainer = document.getElementById("search-container");
  searchContainer.style.height = "0";
}
