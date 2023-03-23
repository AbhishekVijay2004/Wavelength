const audioPlayer = document.getElementsByClassName('audio-player')[0];
const playPauseBtn = document.getElementsByClassName('spplay-pause-btn')[0];
const progress = document.getElementsByClassName('spsongCircle')[0];

playPauseBtn.addEventListener('click', playMusic);


  function playMusic() {
  const audioPlayer = document.getElementsByClassName('audio-player');
  const playPauseBtn = document.getElementsByClassName('spplay-pause-btn');
  
  if (audioPlayer[i].paused) {
    for (let index = 0; index < audioPlayer.length; ++index) {
      audioPlayer[index].pause()
      playPauseBtn[index].classList.remove('playing');
    }
    audioPlayer[i].play();
    playPauseBtn[i].classList.add('playing');
  } else {
    audioPlayer[i].pause();
    playPauseBtn[i].classList.remove('playing');
  }
};

audioPlayer.addEventListener('timeupdate', function() {
  const degreesComplete = audioPlayer.currentTime / audioPlayer.duration * 360;
  if (degreesComplete <= 45) {
    progress.style.
  clipPath= `polygon(50% 50%, 50% 0, ${50+(degreesComplete/45*50)}% 0)`;    
  } else if (degreesComplete <= 135) {
    progress.style.
  clipPath= `polygon(50% 50%, 50% 0, 100% 0 , 100% ${((degreesComplete-45)/90*100)}%)`; 
  }else if (degreesComplete <= 225) {
    progress.style.
  clipPath= `polygon(50% 50%, 50% 0, 100% 0 , 100% 100%, ${100-((degreesComplete-135)/90*100)}% 100%)`; 
  }else if (degreesComplete <= 315) {
    progress.style.
  clipPath= `polygon(50% 50%, 50% 0, 100% 0 , 100% 100%, 0 100%, 0 ${100-((degreesComplete-225)/90*100)}%)`;    
  }else if (degreesComplete <= 360) {
    progress.style.
  clipPath= `polygon(50% 50%, 50% 0, 100% 0 , 100% 100%, 0 100%, 0 0, ${((degreesComplete-315)/45*50)}% 0)`;    
  }
});
window.addEventListener('resize', onResizeOrLoad);
window.addEventListener('load', onResizeOrLoad);
function onResizeOrLoad(e) {
      arrayOfMusic = document.getElementsByClassName('spsongTitle');
      console.log(arrayOfMusic);
      const bigvw = Math.round(0.03*Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0));
      const smallvw = Math.round(0.015*Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0));
      i = 0;
      for (let i = 0; i < arrayOfMusic.length; i++) {
        arrayOfMusic[i].style.fontSize = "1vw";
        arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize = "0.5vw";
        
        loop2 = arrayOfMusic[i].parentNode.scrollHeight*1.5 < arrayOfMusic[i].parentNode.parentNode.scrollHeight;
        while (loop2) {
          arrayOfMusic[i].style.fontSize = Math.min(parseInt(arrayOfMusic[i].style.fontSize.substring(0,2)),bigvw) + 2 + "px";
          arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize = Math.min(parseInt(arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize.substring(0,2)),smallvw) + 1 + "px";
          if (parseInt(arrayOfMusic[i].style.fontSize.substring(0,2)) - 2 == bigvw && parseInt(arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize.substring(0,2)) - 1== smallvw) {
            break;
          }
          loop2 = arrayOfMusic[i].parentNode.scrollHeight*1.5 < arrayOfMusic[i].parentNode.parentNode.scrollHeight;
          if (loop2 ==false) {
            arrayOfMusic[i].style.fontSize = Math.min(parseInt(arrayOfMusic[i].style.fontSize.substring(0,2)),bigvw) - 2 + "px";
          arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize = Math.min(parseInt(arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize.substring(0,2)),smallvw) - 1 + "px";
          
          }
        } 
      }
    }