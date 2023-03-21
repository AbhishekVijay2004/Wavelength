
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
				<a href url="http://google.com">
					<div class="profilePic" style="background-image:url('`+user_pic+`');">
		          	</div>
		      	</a>

<textarea rows="1" class="newCommentText" oninput="newCommentText(this)"></textarea>
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
					var commentLikeCount = thisComment["commentLikes"];
					var commentDislikeCount = thisComment["commentDislikes"];
					var commentDate = thisComment["commentDate"];
					commentLikeCount = commentLikeCount == null ? 0 : commentLikeCount;
					commentDislikeCount = commentDislikeCount == null ? 0 : commentDislikeCount;
					loadComment(parnt, commentAuthorLink, commentAuthorPic, commentAuthorName, commentText, commentLikeCount, commentDislikeCount, commentDate);
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
			console.log(textbox); //textbix
		}
	}
	function newCommentText(elem) {  /* javascript */
    elem.style.height = "1px";
    elem.style.height = (elem.scrollHeight)+"px";
}

	function loadComment(parnt, commentAuthorLink, commentAuthorPic, commentAuthorName, commentText, commentLikeCount, commentDislikeCount, commentDate) {
		const comment = document.createElement('div');
		comment.classList.add('groupHorizontal');
		comment.innerHTML = `

		<a href url="`+commentAuthorLink+`">
			<div class="profilePic" style="background-image:url('`+commentAuthorPic+`');">
          	</div>
      	</a>

      	<div class="groupVertical">
	      	<a href url="`+commentAuthorLink+`">
	      	 <div class="profileName" style="font-size:1vw;line-height:1vw;margin-bottom:5px">`+commentAuthorName+`</div>
			</a>

			<div class="commentText">
		        `+commentText+`
	      	</div>

	      	<div class="groupHorizontal">
				<div class="groupHorizontal">
						<div class = "posReact" style="width:1vw;background-size:1vw;"></div>

					<div class = "count" style="font-size:1vw;line-height:1vw;margin-left:1px">`+commentLikeCount+`</div>
				</div>
				<div class="groupHorizontal">
						<div class = "negReact" style="width:1vw;background-size:1vw;"></div>
					<div class = "count" style="font-size:1vw;line-height:1vw;margin-left:1px">`+commentDislikeCount+`</div>
				</div>
			</div>
		</div>


		<div class="groupVertical" style="gap:10px">

	      	<div class="time" style="font-size:1vw">`+commentDate+`</div>

	    </div>



	`;

		const likebutton = comment.querySelector('.posReact');
		likebutton.addEventListener('click', footerClick);
		const dislikebutton = comment.querySelector('.negReact');
		dislikebutton.addEventListener('click', footerClick);
		parnt.appendChild(comment);
	} //creates a template at the bottom of the page


	function onResizeOrLoad(e) {
		//screenSize = window.innerWidth/screen.width;
		//if (screenSize < 0.75) {
		//	minFontSize = Math.round(10 - (1-screenSize)*4)*2;
		//} else {
		//	minFontSize = 20
		//}
	    for (var i = 0; i < arrayOfPosts.length; i++) {
	    	currentTextbox = arrayOfPosts[i].getElementsByClassName('text')[0]


	    	//currentTextbox.style.fontSize="98px";
	    	//while (currentTextbox.scrollHeight > 150 && currentTextbox.style.fontSize.substring(0,2) > minFontSize) {
	    	//		currentTextbox.style.fontSize = parseInt(currentTextbox.style.fontSize.substring(0,2)) - 2 + "px";
	    	//}
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
