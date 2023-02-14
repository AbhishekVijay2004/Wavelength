
	window.addEventListener('resize', onResizeOrLoad);
	window.addEventListener('load', onResizeOrLoad);

	function clickOnText() {
		let elmnt = this.getElementsByClassName('text')[0];
		let i = arrayOfPosts.indexOf(this);
		console.log(expandedPosts);
	    if (elmnt.scrollHeight > 250) {
		    expandedPosts[i] = !expandedPosts[i];
		    if (expandedPosts[i]) {
		      elmnt.style.maxHeight = 'none';
		      elmnt.style['-webkit-mask-image'] = 'none'; 
	    	} else {
	      		elmnt.style.maxHeight = '250px';
	    		elmnt.style['-webkit-mask-image'] = 'linear-gradient(180deg, #000 60%, transparent)'; 
	    	}
	 	}
	} //toggle between expanded & not expanded text boxed
	function onResizeOrLoad(e) {
	    for (var i = 0; i < arrayOfPosts.length; i++) {
	    	currentTextbox = arrayOfPosts[i].getElementsByClassName('text')[0]
			if (currentTextbox.scrollHeight > 250 && expandedPosts[i] == false) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'linear-gradient(180deg, #000 60%, transparent)'; 

			} else if (currentTextbox.scrollHeight > 250) {
			    currentTextbox.style.cursor = 'pointer';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			} else {
			    currentTextbox.style.cursor = 'default';
			    currentTextbox.style.maxHeight = '250px';
			    currentTextbox.style['-webkit-mask-image'] = 'none'; 

			    expandedPosts[i] = false;
			}
		}
    }; //checks if the text gets smaller/larger than 250px when resized, so toggle for textboxes can be disabled/enabled