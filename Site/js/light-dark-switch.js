var darkMode = true;

function SwitchMode(){
  darkMode = !darkMode;
  if (darkMode){
    document.documentElement.style.setProperty("--background-colour", "#1E1E1E")
  }
  else{
    document.documentElement.style.setProperty("--background-colour", "#FFFFFF")
  }
}
