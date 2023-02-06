var darkMode = true;

function SwitchMode(){
  darkMode = !darkMode;
  if (darkMode){
    alert("Switching to dark mode.");
  }
  else{
    document.documentElement.style.setProperty("--background-colour", "#FFFFFF")
  }
}
