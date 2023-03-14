    setTimeout(replacePosts, 2000);
    function replacePosts () {
    	//container.removeChild(container.childNodes[0]);
        container.replaceChild(loadPost(),container.childNodes[3])
        container.replaceChild(loadPostTwo(),container.childNodes[4])
        onResizeOrLoad();
    }

function playPauseClick() {

  let i = arrayOfPosts.indexOf(this.parentNode.parentNode.parentNode.parentNode);
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
}

function audioTimeUpdate() {
  let i = arrayOfPosts.indexOf(this.parentNode.parentNode.parentNode.parentNode);
  const audioPlayer = document.getElementsByClassName('audio-player')[i]
  const progress = document.getElementsByClassName('spsongCircle')[i];

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
}
