
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
		let elmnt = this.parentNode.parentNode.parentNode;
		commSec = elmnt.querySelector('.commentSection');
		let i = arrayOfPosts.indexOf(elmnt);
		if (commentsOpened[i] == '0') {
			commentsOpened[i] = 1;
		    loadCommentsSection(commSec);		//needs variables passing
}
		    expandedComments[i] = !expandedComments[i];
		    if (expandedComments[i]) {
		      commSec.style.maxHeight = '250px';
		      commSec.style.display = 'flex';
	    	} else {
		      commSec.style.maxHeight = '0px';
		      commSec.style.display = 'none';
	    	}
	}

	function loadCommentsSection(parnt) {
		$.ajax({
		  url: '/getComments',
			data: {postID: parnt.id},
		  type: 'GET',
		  success: function(data) {
		    var user_pic = data[0].userPic;
				const newComment = document.createElement('div');
				newComment.classList.add('groupHorizontal');
				newComment.innerHTML = `
<textarea rows="1" maxlength="200" class="newCommentText"></textarea>
<button class="commentSubmitButton">Submit</button>
		<br>
			`;

				parnt.appendChild(newComment);
				const submitButton = parnt.querySelector('.commentSubmitButton');
				submitButton.addEventListener('click', submitComment);
				for (var i = 1; i < data.length; i++){
					var thisComment = data[i];
					var commentAuthorLink = thisComment["commentUsername"];
					var commentAuthorPic = thisComment["commentPic"];
					var commentAuthorName = thisComment["commentUsername"];
					var commentText = thisComment["commentText"];
					var commentDate = thisComment["commentDate"];
					loadComment(parnt, commentAuthorLink, commentAuthorPic, commentAuthorName, commentText, commentDate);
				}
		  },
		  error: function(error) {
		  console.error(error);
		  }
		});
	}
	function submitComment() {
		textbox = this.parentNode.querySelector('.newCommentText').value;
		this.parentNode.querySelector('.newCommentText').value = "";
		if (textbox.length > 0) {
			$.ajax({
		    url: '/postComment',
		    data: {postID: this.parentNode.parentNode.id, text: textbox},
		    type: 'GET',
		    success: function(data) {
				location.reload()
		    	loadCommentsSection(this.parentNode.parentNode);
		    },
		    error: function(error) {
		    console.error(error);
		    }
		  });
		}
	}
	function newCommentText(elem) {  /* javascript */
    elem.style.height = "1px";
    elem.style.height = (elem.scrollHeight)+"px";
}

	function loadComment(parnt, commentAuthorLink, commentAuthorPic, commentAuthorName, commentText, commentDate) {
		const comment = document.createElement('div');
		comment.classList.add('groupHorizontalComments');
		comment.innerHTML = `

		<div class="profilePic" style="background-image:url('`+commentAuthorPic+`');" onclick="navigateToProfilePage('`+commentAuthorLink+`')"></div>

		<div class="commentText">`+commentText+`</div>

		<div class="timeNameContainer">
			<div class="profileName" onclick="navigateToProfilePage('`+commentAuthorLink+`')" style="font-size:1.25vw; margin:0; line-height:1;">`+commentAuthorName+`</div>
	      	<div class="timeComments">`+commentDate+`</div>
	    </div>


	`;

		parnt.appendChild(comment);
	} //creates a template at the bottom of the page


	function onResizeOrLoad(e) {
    	arrayOfMusic = document.getElementsByClassName('spsongTitle');
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
          if (loop2 == false) {
            arrayOfMusic[i].style.fontSize = Math.min(parseInt(arrayOfMusic[i].style.fontSize.substring(0,2)),bigvw) - 2 + "px";
          arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize = Math.min(parseInt(arrayOfMusic[i].parentNode.querySelector('.spartistTitle').style.fontSize.substring(0,2)),smallvw) - 1 + "px";

          }
    		}
    	}

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
			    currentTextbox.style.minHeight = '0px';
			    currentTextbox.style['-webkit-mask-image'] = 'none';

			    expandedPosts[i] = false;
			}
		}
    }; //checks if the text gets smaller/larger than 150px when resized, so toggle for textboxes can be disabled/enabled
