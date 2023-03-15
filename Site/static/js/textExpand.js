
	window.addEventListener('resize', onResizeOrLoad);
	window.addEventListener('load', onResizeOrLoad);

	function clickOnText() {
		let elmnt = this;
		let i = arrayOfPosts.indexOf(this.parentNode);
	    if (elmnt.scrollHeight > 150) {
		    expandedPosts[i] = !expandedPosts[i];
		    if (expandedPosts[i]) {
		      elmnt.style.maxHeight = 'none';
		      elmnt.style['-webkit-mask-image'] = 'none'; 
	    	} else {
	      		elmnt.style.maxHeight = '150px';
	    		elmnt.style['-webkit-mask-image'] = 'linear-gradient(180deg, #000 60%, transparent)'; 
	    	}
	 	}
	} //toggle between expanded & not expanded text boxed

	function clickOnComments() {
		let elmnt = this;
		commSec = elmnt.parentNode.parentNode.querySelector('.commentSection');	
		let i = arrayOfPosts.indexOf(this.parentNode.parentNode);
		if (commentsOpened[i] == '0') {
			commentsOpened[i] = 1;
		    loadCommentsSection(commSec);
}
		    expandedComments[i] = !expandedComments[i];
		    if (expandedComments[i]) {
		      commSec.style.maxHeight = '250px';
		      commSec.style.display = 'inline';
	    	} else {		    	
		      commSec.style.maxHeight = '0px';
		      commSec.style.display = 'none';
	    	}
	}

	function loadCommentsSection(parnt) {
		const newComment = document.createElement('div');
		newComment.classList.add('newComment');
		newComment.innerHTML = `
		<a href url="http://google.com">
			<div class="commentProfilePic" style="background-image:url('./static/media/avatar.jpg');">
          	</div>
      	</a>
      	<input type="text" id="fname" name="fname" class="bigText">
        <input type="submit" value="Submit">

	`;
		parnt.appendChild(newComment);
		loadComment(parnt);
		loadComment(parnt);
		loadComment(parnt);
		loadComment(parnt);
		loadComment(parnt);
	}

	function loadComment(parnt) {
		const comment = document.createElement('div');
		comment.classList.add('commentContainer');
		comment.innerHTML = `
		<a href url="http://google.com">
			<div class="commentProfilePic" style="background-image:url('./static/media/avatar.jpg');">
          	</div>
      	</a>
      <div class="commentText">
      <b><u><a href url="http://google.com">John Bishop</a></b></u>
      <br>
          eipit vehicula. Vestibulum ultricies odio non eros posuere aliquam. Aliquam ac vulputate mi, nec rhoncus justo. Suspendisse vel ultricies eros. Vivamus bibendum non elit eget facilisis. Suspendisse condimentum odio ut purus convallis, vel pretium mauris varius. Donec rutrum eleifend mi scelerisque accumsan.
<br><br>
Nunc eu mollis elit. Nulla non ligula at dui rhoncus dapibus sit amet cursus nibh. Nam maximus tempor eros, id lobortis augue imperdiet non. Morbi maximus pharetra imperdiet. Proin accumsan sit amet lorem eget accumsan. Nulla facilisi. Nulla facilisi. Mauris elit quam, mollis a enim in, pharetra ornare massa. In quis convallis urna.
      </div>
	`;
		parnt.appendChild(comment);
	} //creates a template at the bottom of the page


	function onResizeOrLoad(e) {
		screenSize = window.innerWidth/screen.width;
		if (screenSize < 0.75) {
			minFontSize = Math.round(10 - (1-screenSize)*4)*2;
		} else {
			minFontSize = 20
		}
	    for (var i = 0; i < arrayOfPosts.length; i++) {
	    	currentTextbox = arrayOfPosts[i].getElementsByClassName('text')[0]
	    	

	    	currentTextbox.style.fontSize="98px";
	    	while (currentTextbox.scrollHeight > 150 && currentTextbox.style.fontSize.substring(0,2) > minFontSize) {
	    			currentTextbox.style.fontSize = parseInt(currentTextbox.style.fontSize.substring(0,2)) - 2 + "px";
	    	}
			if (currentTextbox.scrollHeight > 150 && expandedPosts[i] == false) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'linear-gradient(180deg, #000 60%, transparent)'; 

			} else if (currentTextbox.scrollHeight > 150) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			} else {
			    currentTextbox.style.cursor = 'default';
			    currentTextbox.style.maxHeight = '150px';
			    currentTextbox.style.minHeight = '0px';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			    expandedPosts[i] = false;
			}
		}
    }; //checks if the text gets smaller/larger than 150px when resized, so toggle for textboxes can be disabled/enabled


    
