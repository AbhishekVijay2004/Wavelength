const getRandomColor = () => {
    return `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
  };
  //gets a random colour
const pSBC=(p,c0,c1,l)=>{
    let r,g,b,P,f,t,h,i=parseInt,m=Math.round,a=typeof(c1)=="string";
    if(typeof(p)!="number"||p<-1||p>1||typeof(c0)!="string"||(c0[0]!='r'&&c0[0]!='#')||(c1&&!a))return null;
    if(!this.pSBCr)this.pSBCr=(d)=>{
        let n=d.length,x={};
        if(n>9){
            [r,g,b,a]=d=d.split(","),n=d.length;
            if(n<3||n>4)return null;
            x.r=i(r[3]=="a"?r.slice(5):r.slice(4)),x.g=i(g),x.b=i(b),x.a=a?parseFloat(a):-1
        }else{
            if(n==8||n==6||n<4)return null;
            if(n<6)d="#"+d[1]+d[1]+d[2]+d[2]+d[3]+d[3]+(n>4?d[4]+d[4]:"");
            d=i(d.slice(1),16);
            if(n==9||n==5)x.r=d>>24&255,x.g=d>>16&255,x.b=d>>8&255,x.a=m((d&255)/0.255)/1000;
            else x.r=d>>16,x.g=d>>8&255,x.b=d&255,x.a=-1
        }return x};
    h=c0.length>9,h=a?c1.length>9?true:c1=="c"?!h:false:h,f=this.pSBCr(c0),P=p<0,t=c1&&c1!="c"?this.pSBCr(c1):P?{r:0,g:0,b:0,a:-1}:{r:255,g:255,b:255,a:-1},p=P?p*-1:p,P=1-p;
    if(!f||!t)return null;
    if(l)r=m(P*f.r+p*t.r),g=m(P*f.g+p*t.g),b=m(P*f.b+p*t.b);
    else r=m((P*f.r**2+p*t.r**2)**0.5),g=m((P*f.g**2+p*t.g**2)**0.5),b=m((P*f.b**2+p*t.b**2)**0.5);
    a=f.a,t=t.a,f=a>=0||t>=0,a=f?a<0?t:t<0?a:a*P+t*p:0;
    if(h)return"rgb"+(f?"a(":"(")+r+","+g+","+b+(f?","+m(a*1000)/1000:"")+")";
    else return"#"+(4294967296+r*16777216+g*65536+b*256+(f?m(a*255):0)).toString(16).slice(1,f?undefined:-2)
	} //converts lots of different ways of representing colours to hex


//	const scrollContent = document.querySelector('.clsScroll'); // store in a variable so we can reference the element in multiple locations
//	scrollContent.addEventListener('scroll', () => {
//	  const scrolled = scrollContent.scrollTop; // reuse `scrollContent` innstead of querying the DOM again
//	  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
//	  const contnr = document.getElementsByClassName("clsScroll")[0];
	//if(scrolled + clientHeight	>= contnr.scrollHeight) {
	//	if (document.getElementsByClassName('postTemplate').length == 0) {
	//		addPost();
//		} else {
//			console.log("sjbfd");
//		}
//
//		}
//	}, {passive: true}); //calls addPost when the user gets to the bottom of the page

	function endOfPosts() {
		const endOfPost = document.createElement('div');
		endOfPost.classList.add('endOfPost');
		endOfPost.innerHTML = `
		Couldn't load more posts.
	`;
		document.querySelector('.clsScroll').appendChild(endOfPost);
	}

	function addPost() {
		if (document.getElementsByClassName('postTemplate').length > 1) {
			return;
		}
		const postElement = document.createElement('div');
		postElement.classList.add('postTemplate');
		postElement.innerHTML = `
		<div class="spcontainer">
    <div class="spplayer">

    </div>
    <div class="spsongInfo">
      <div class="spitem spalbumImage"></div>
      </div></div>
      	  	<div id="text" class="text" style="min-height: 85px;"></div>
      <div class = "footer">
				<div class = "posReact"></div>
				<div class = "negReact"></div>
				<div class = "comments"></div>
		</div>
	`;
		arrayOfPlaceholders.push(postElement)
		const randomColorOne = getRandomColor();
		spotifyColours.push(randomColorOne);
		postElement.getElementsByClassName('spplayer')[0].style.backgroundColor = randomColorOne;
		postElement.getElementsByClassName('spalbumImage')[0].style.backgroundColor = pSBC( -.8, randomColorOne);
		container.appendChild(postElement);
	} //creates a template at the bottom of the page
	function loadPost(album_art, song_title, artist_name, preview_mp3, postAuthorLink, postAuthorPic, postAuthorName, postTime, postText, posReactCount, negReactCount, commentCount, postID, liked, disliked, likesOn, dislikesOn, commentsAreOn) {
    var likedClicked = liked ? " clicked" : "";
    var dislikedClicked = disliked ? " clicked" : "";
    const postElement = document.createElement('div');
    var likes = 0;
    var dislikes= 0;
    var commentsYes = 0;

    if (likesOn == "1") {
   	    var likes = 1;
    }
    if (dislikesOn == "1") {
   	    var dislikes = 1;
    }
    if (commentsAreOn == "1") {
   	    var commentsYes = 1;
    }
		postElement.classList.add('post');
		postElement.innerHTML = `
			<!-- ------------------- song player --------------- -->
      <div class="spcontainer">
    <div class="spplayer">
      <div class="spblurrer">
        <div class="sprepeating-image" style="background-image:url('`+album_art+`')"></div>
      </div>
    </div>
    <div class="spsongInfo">
      <div class="spitem spalbumImage" style="  background-image:url('`+album_art+`');"></div>
      <div class="spitem spsongDetails">
        <div class="spsongTitle">`+song_title+`</div>
        <div class="spartistTitle">`+artist_name+`</div>
      </div>
      <div id="spAudiocontainer">
        <audio class="audio-player" src="`+preview_mp3+`"></audio>
        <div class="spsongCircle"></div>
      <button class="spplay-pause-btn"></button>
      </div>
    </div>
  </div>

      <!-- ------------------- end of song player --------------- -->


      <div class = "groupHorizontal">
		<div class="profilePic" style="background-image:url('`+postAuthorPic+`');" onclick="`+postAuthorLink+`">
		</div>
      	<div class="profileName" onclick="navigateToProfilePage('`+postAuthorLink+`')">`+postAuthorName+`</div>

      	 <div class="time">`+postTime+`</div>
      </div>


	  	<div id="text" class="text">
	  		`+postText+`
		</div>

`;
footerhtml = `
<div class = "footer">
				<div class="groupHorizontal" style="min-width:5vw">
					<div class = "posReact`+likedClicked+`" style="`+((likes)?``:`display:none;`)+`"></div>
					<div class = "count" style="`+((likes)?``:`display:none;`)+`">`+posReactCount+`</div>
				</div>
				
				<div class="groupHorizontal" style="min-width:5vw">
						<div class = "negReact`+dislikedClicked+`" style="`+((dislikes)?``:`display:none;`)+`"></div>
						<div class = "count" style="`+((dislikes)?``:`display:none;`)+`">`+negReactCount+`</div>
				</div>
				
				<div class="groupHorizontal" style="min-width:5vw">
					<div class = "comments" style="`+((commentsYes)?``:`display:none;`)+`"></div>
					<div class = "count" style="`+((commentsYes)?``:`display:none;`)+`">`+commentCount+`</div>
				</div>
		</div>`;
postElement.innerHTML += footerhtml;
postElement.innerHTML+=`
		<div class="commentSection" id="`+postID+`"></div>

	`;
		arrayOfPosts.push(postElement);
		expandedPosts.push(false);
		expandedComments.push(false);
		commentsOpened.push(false);
		const textBit = postElement.querySelector('.text');
		if (parseInt(commentsAreOn)) {
			const commentBit = postElement.querySelector('.comments');
			commentBit.addEventListener('click', clickOnComments);
		}
		textBit.addEventListener('click', clickOnText);

		const audio = postElement.querySelector('.audio-player');
		audio.addEventListener('timeupdate', audioTimeUpdate);
		const playbutton = postElement.querySelector('.spplay-pause-btn');
		playbutton.addEventListener('click', playPauseClick);
if (parseInt(likes)) {
			const likebutton = postElement.querySelector('.posReact');
    likebutton.classList.add("id" + postID);
		likebutton.addEventListener('click', footerClick);

}
		if (parseInt(dislikes)) {
					const dislikebutton = postElement.querySelector('.negReact');
    dislikebutton.classList.add("id" + postID);
		dislikebutton.addEventListener('click', footerClick);
		}
		if (commentsAreOn) {

		const commentbutton = postElement.querySelector('.comments');
		commentbutton.addEventListener('click', footerClick);

		}
		addPost();
		return (postElement);
	} //returns a post

  function changeLikeCount(reactElement, amount){
    var count = reactElement.parentNode.querySelector(".count");
    count.innerHTML = (parseInt(count.innerHTML) + amount).toString();
  }

  function changeLike(type, amount, postID){
    var elemName = type == "like" ? ".posReact" : ".negReact";
    var reactElement = document.querySelector(elemName + "." + postID);
    var inverseElemName = type == "like" ? ".negReact" : ".posReact";
    var inverseElement = reactElement.parentNode.parentNode.querySelector(inverseElemName);

    if (inverseElement.classList.contains('clicked')){
        changeLikeCount(inverseElement, -1);
        reactElement.parentNode.parentNode.querySelector(inverseElemName).classList.remove('clicked');
    }

    changeLikeCount(reactElement, amount);
    postID = postID.slice(2);

    $.ajax({
      url: '/changeLike',
      data: {type: type, postID: postID, amount: amount},
      type: 'GET',
      error: function(error) {
      console.error(error);
      }
    });
  }

	function footerClick(){
    reactID = this.classList[1];
    if (reactID == "clicked"){
      reactID = this.classList[2];
    }
	  if (this.classList[0] == "posReact") {
	  	if (this.classList.contains("clicked")) {
 		  this.classList.remove('clicked');
      changeLike("like", -1, reactID);
		} else {
		  	this.classList.add('clicked');
        changeLike("like", 1, reactID);
		}
	  } else if (this.classList[0] == "negReact") {
	  	if (this.classList.contains("clicked")) {
 		  this.classList.remove('clicked');
      changeLike("dislike", -1, reactID)
		} else {
		  	this.classList.add('clicked');
        changeLike("dislike", 1, reactID);
		}
	  } else {

		  if (this.classList.contains("clicked")) {
	 		  this.classList.remove('clicked');
		  } else {
		  	this.classList.add('clicked');

		  }
	  }
};

	function breatheColour() {

  	const backgrColor = getComputedStyle(document.documentElement).getPropertyValue('--background-highlight-1');
		if (pos == 1) {
			change += 0.01;
		} else {
			change -= 0.01;
		}
	    if (Math.abs(change) >= 0.08) {
	    	pos = -pos;
	    }

	    for (var i = 0; i < arrayOfPlaceholders.length; i++) {
			arrayOfPlaceholders[i].getElementsByClassName('spplayer')[0].style.backgroundColor = pSBC(change, spotifyColours[i]);
	  	arrayOfPlaceholders[i].getElementsByClassName('spalbumImage')[0].style.backgroundColor = pSBC( change, pSBC( -.8, spotifyColours[i]));
			arrayOfPlaceholders[i].style.backgroundColor = pSBC(change, "rgb(51,51,51)");
		}

	    setTimeout(breatheColour, 20);
	} //changes the colours of the templates to add a loading animation



	const container = document.getElementsByClassName('clsScroll')[0];
    var spotifyColours = [];
	var	arrayOfPlaceholders = [];
	var arrayOfPosts = [];
	var expandedPosts = [];
	var expandedComments = [];
	var commentsOpened = [];
	var change = 0.01;
	var pos = 1;

	addPost();
	breatheColour();
