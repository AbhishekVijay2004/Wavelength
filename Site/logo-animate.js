Expand();
function Expand(){
  document.getElementById("logo-container").classList.add("expanded");
  setTimeout(Contract, 2000);
}

function Contract(){
  document.getElementById("logo-container").classList.remove("expanded");
  setTimeout(Expand, 2000);
}
