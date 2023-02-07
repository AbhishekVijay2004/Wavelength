/*
         Colour           Dark Mode Light Mode
 --background-colour       #1E1E1E   #E9EAEA
 --background-highlight-1  #333333   #
 --background-highlight-2  #474747
 --primary-colour
 --primary-highlight-1
 --primary-highlight-2

*/

var darkMode = true;

var colourDict = {
  
}

function SwitchMode(){
  darkMode = !darkMode;
  if (darkMode){
    document.documentElement.style.setProperty("--background-colour", "#1E1E1E")
  }
  else{
    document.documentElement.style.setProperty("--background-colour", "#FFFFFF")
  }
}
