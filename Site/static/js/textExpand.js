
	window.addEventListener('resize', onResizeOrLoad);
	window.addEventListener('load', onResizeOrLoad);

	function clickOnText() {
		let elmnt = this;
		let i = arrayOfPosts.indexOf(this);
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
		let i = arrayOfPosts.indexOf(this);
		    expandedComments[i] = !expandedComments[i];
		    if (expandedComments[i]) {
		    	console.log(commSec.scrollHeight);
		      commSec.style.maxHeight = '250px';
		      commSec.style.display = 'inline';
		      loadComment(commSec);
	    	} else {
		      commSec.style.maxHeight = '0px';
		      commSec.style.display = 'none';
	    	}
	}

	function loadComment(parnt) {
		const comment = document.createElement('div');
		comment.classList.add('commentContainer');
		comment.innerHTML = `
			<div class="commentProfilePic">
          
      </div>
      <div class="commentText">
          eipit vehicula. Vestibulum ultricies odio non eros posuere aliquam. Aliquam ac vulputate mi, nec rhoncus justo. Suspendisse vel ultricies eros. Vivamus bibendum non elit eget facilisis. Suspendisse condimentum odio ut purus convallis, vel pretium mauris varius. Donec rutrum eleifend mi scelerisque accumsan.
<br><br>
Nunc eu mollis elit. Nulla non ligula at dui rhoncus dapibus sit amet cursus nibh. Nam maximus tempor eros, id lobortis augue imperdiet non. Morbi maximus pharetra imperdiet. Proin accumsan sit amet lorem eget accumsan. Nulla facilisi. Nulla facilisi. Mauris elit quam, mollis a enim in, pharetra ornare massa. In quis convallis urna.
      </div>
	`;
		parnt.appendChild(comment);
	} //creates a template at the bottom of the page


	function onResizeOrLoad(e) {
	    for (var i = 0; i < arrayOfPosts.length; i++) {
	    	currentTextbox = arrayOfPosts[i].getElementsByClassName('text')[0]
			if (currentTextbox.scrollHeight > 150 && expandedPosts[i] == false) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'linear-gradient(180deg, #000 60%, transparent)'; 

			} else if (currentTextbox.scrollHeight > 150) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			} else {
			    currentTextbox.style.cursor = 'default';
			    currentTextbox.style.maxHeight = '150px';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			    expandedPosts[i] = false;
			}
		}
    }; //checks if the text gets smaller/larger than 150px when resized, so toggle for textboxes can be disabled/enabled