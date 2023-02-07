var darkMode = true;

var darkModeColourDict = {
  "--background-colour"      : "#1E1E1E",
  "--background-highlight-1" : "#333333",
  "--background-highlight-2" : "#474747",
  "--primary-colour"         : "#B64CFF",
  "--primary-highlight-1"    : "#CE85FF",
  "--primary-highlight-2"    : "#DEADFF"
}

var lightModeColourDict = {
  "--background-colour"      : "#E9EAEA",
  "--background-highlight-1" : "#D5D7D7",
  "--background-highlight-2" : "#C1C3C3",
  "--primary-colour"         : "#B64CFF",
  "--primary-highlight-1"    : "#AD33FF",
  "--primary-highlight-2"    : "#9D0AFF"
}

function SwitchMode(){
  darkMode = !darkMode;
  var thisDict = darkMode ? darkModeColourDict : lightModeColourDict
  for (var colourType in thisDict){
    document.documentElement.style.setProperty(colourType, thisDict[colourType])
  }
}
