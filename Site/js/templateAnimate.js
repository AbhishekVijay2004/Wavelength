const getRandomColor = () => {
    return `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
  }; //gets a random colour
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
	const scrollContent = document.querySelector('.clsScroll'); // store in a variable so we can reference the element in multiple locations
	scrollContent.addEventListener('scroll', () => {
	  const scrolled = scrollContent.scrollTop; // reuse `scrollContent` innstead of querying the DOM again
	  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
	  const contnr = document.getElementsByClassName("clsScroll")[0];

	if(scrolled + clientHeight	>= contnr.scrollHeight) {
			addPost();
		}
	}, {passive: true}); //calls addPost when the user gets to the bottom of the page
	function addPost() {
		const postElement = document.createElement('div');
		postElement.classList.add('postTemplate');
		postElement.innerHTML = `
		<div class = "spotifyTemplate">
			<div class="photoTemplate"></div>
		</div>
	  	<div id="textTemplate" class="textTemplate"></div>
		<div class = "footerTemplate">
				<div class = "reactionsTemplate">................</div>
				<div class = "commentsTemplate">Comments</div>
		</div>
	`;
		arrayOfPlaceholders.push(postElement)
		const randomColorOne = getRandomColor();
		spotifyColours.push(randomColorOne);
		postElement.getElementsByClassName('spotifyTemplate')[0].style.backgroundColor = randomColorOne;
		postElement.getElementsByClassName('photoTemplate')[0].style.backgroundColor = pSBC( -.8, randomColorOne);
		container.appendChild(postElement);
	} //creates a template at the bottom of the page
	function loadPost() {
		const postElement = document.createElement('div');
		postElement.classList.add('post');
		postElement.innerHTML = `
			<!-- ------------------- song player --------------- -->
      <div class="spcontainer">
    <div class="spplayer">
      <div class="spblurrer">
        <div class="sprepeating-image" style="background-image:url('https://i1.sndcdn.com/artworks-000142105824-y39ojb-t500x500.jpg')"></div>  
      </div>
    </div>
    <div class="spsongInfo">
      <div class="spitem spalbumImage" style="  background-image:url('https://i1.sndcdn.com/artworks-000142105824-y39ojb-t500x500.jpg');"></div>
      <div class="spitem spsongDetails">
        <div class="spsongTitle">Matadora</div>
        <div class="spartistTitle">Sofi Tukker</div>
      </div>
      <div id="spAudiocontainer">    
        <audio class="audio-player" src="https://p.scdn.co/mp3-preview/77f3d7ea6be27d21fdbf489e01011012c044ebbf?cid=774b29d4f13844c495f206cafdad9c86"></audio>
        <div class="spsongCircle"></div>
      <button class="spplay-pause-btn"></button>
      </div>
    </div>
  </div> 

      <!-- ------------------- end of song player --------------- --> 
	  	<div id="text" class="text">
	  		Lorem  ipsum dolor sit amet, consectetur adipiscing elit. Cras id lacus non purus malesuada hendrerit. Morbi aliquet vel lorem at vulputate. Mauris ex nisi, ornare eu ligula non, lobortis dapibus nisi. Donec eu volutpat lacus. Phasellus leo lacus, sodales id tempus vel, tincidunt vitae justo. Sed non rutrum sapien, vitae convallis augue. Morbi felis justo, laoreet sed elit vel, placerat fringilla velit. Quisque purus dui, ullamcorper eget suscipit eget, finibus nec ex. Phasellus tempor fringilla magna eget imperdiet. Sed viverra diam sit amet erat venenatis volutpat. Praesent suscipit enim sit amet lobortis viverra. Donec vitae faucibus sapien. Sed elementum magna in lectus accumsan ullamcorper id eget leo. Maecenas porttitor ligula at laoreet lobortis.
	  		<br><br>
				Donec quis ultrices nibh. Fusce blandit mi ut ex ultrices, vitae pellentesque lorem finibus. Integer iaculis varius fermentum. Mauris a urna nibh. Nullam efficitur pretium eros nec gravida. Pellentesque sodales ex dolor, sit amet pharetra leo porta at. Quisque molestie mollis enim, et rhoncus dui imperdiet at. Maecenas commodo ligula eu elit bibendum auctor. Cras ultrices accumsan varius. Aliquam erat volutpat. Morbi mattis lacus vitae est posuere pellentesque. Vivamus egestas quis mauris a efficitur. Nulla fringilla nulla ligula, luctus interdum quam congue ut. Nulla et mauris eget urna consequat euismod ut eu metus. Nullam a mollis massa.
		</div>
		<div class = "footer">
				<div class = "reactions">😎👀🤗</div>
				<div class = "comments">Comments</div>
		</div>
	`;
		arrayOfPosts.push(postElement);
		expandedPosts.push(false);
		console.log();
		const textBit = postElement.querySelector('.text');
		textBit.addEventListener('click', clickOnText);

		const audio = postElement.querySelector('.audio-player');
		audio.addEventListener('timeupdate', audioTimeUpdate);
		const playbutton = postElement.querySelector('.spplay-pause-btn');
		playbutton.addEventListener('click', playPauseClick);
		
		return (postElement);
	} //returns a post

	function loadPostTwo() {
		const postElement = document.createElement('div');
		postElement.classList.add('post');
		postElement.innerHTML = `
			<!-- ------------------- song player --------------- -->
      <div class="spcontainer">
    <div class="spplayer">
      <div class="spblurrer">
        <div class="sprepeating-image" style="background-image:url('https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595')"></div>  
      </div>
    </div>
    <div class="spsongInfo">
      <div class="spitem spalbumImage" style="  background-image:url('https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595');"></div>
      <div class="spitem spsongDetails">
        <div class="spsongTitle">Californication (Deluxe Edition)</div>
        <div class="spartistTitle">Red Hot Chilli Peppers</div>
      </div>
      <div id="spAudiocontainer">    
        <audio class="audio-player" src="https://p.scdn.co/mp3-preview/9acb29dd77bbaa50e13e655b68ef5c0a99549a38?cid=774b29d4f13844c495f206cafdad9c86"></audio>
        <div class="spsongCircle"></div>
      <button class="spplay-pause-btn"></button>
      </div>
    </div>
  </div> 

      <!-- ------------------- end of song player --------------- --> 
	  	<div id="text" class="text">
	  		Lorem  ipsum dolor sit amet, consectetur adipiscing elit. Cras id lacus non purus malesuada hendrerit. Morbi aliquet vel lorem at vulputate. Mauris ex nisi, ornare eu ligula non, lobortis dapibus nisi. Donec eu volutpat lacus. Phasellus leo lacus, sodales id tempus vel, tincidunt vitae justo. Sed non rutrum sapien, vitae convallis augue. Morbi felis justo, laoreet sed elit vel, placerat fringilla velit. Quisque purus dui, ullamcorper eget suscipit eget, finibus nec ex. Phasellus tempor fringilla magna eget imperdiet. Sed viverra diam sit amet erat venenatis volutpat. Praesent suscipit enim sit amet lobortis viverra. Donec vitae faucibus sapien. Sed elementum magna in lectus accumsan ullamcorper id eget leo. Maecenas porttitor ligula at laoreet lobortis.
	  		<br><br>
				Donec quis ultrices nibh. Fusce blandit mi ut ex ultrices, vitae pellentesque lorem finibus. Integer iaculis varius fermentum. Mauris a urna nibh. Nullam efficitur pretium eros nec gravida. Pellentesque sodales ex dolor, sit amet pharetra leo porta at. Quisque molestie mollis enim, et rhoncus dui imperdiet at. Maecenas commodo ligula eu elit bibendum auctor. Cras ultrices accumsan varius. Aliquam erat volutpat. Morbi mattis lacus vitae est posuere pellentesque. Vivamus egestas quis mauris a efficitur. Nulla fringilla nulla ligula, luctus interdum quam congue ut. Nulla et mauris eget urna consequat euismod ut eu metus. Nullam a mollis massa.
		</div>
		<div class = "footer">
				<div class = "reactions">😎👀🤗</div>
				<div class = "comments">Comments</div>
		</div>
	`;
		arrayOfPosts.push(postElement);
		expandedPosts.push(false);
		console.log();
		const textBit = postElement.querySelector('.text');
		textBit.addEventListener('click', clickOnText);

		const audio = postElement.querySelector('.audio-player');
		audio.addEventListener('timeupdate', audioTimeUpdate);
		const playbutton = postElement.querySelector('.spplay-pause-btn');
		playbutton.addEventListener('click', playPauseClick);
		
		return (postElement);
	} //returns a (different) post


	function breatheColour() {
		if (pos == 1) {
			change += 0.01;
		} else {
			change -= 0.01;
		}
	    if (Math.abs(change) >= 0.08) {
	    	pos = -pos;
	    } 

	    for (var i = 0; i < arrayOfPlaceholders.length; i++) {
			arrayOfPlaceholders[i].getElementsByClassName('spotifyTemplate')[0].style.backgroundColor = pSBC(change, spotifyColours[i]);
	  	arrayOfPlaceholders[i].getElementsByClassName('photoTemplate')[0].style.backgroundColor = pSBC( change, pSBC( -.8, spotifyColours[i]));
	  	const backgrColor = getComputedStyle(document.documentElement).getPropertyValue('--background-highlight-1');
			arrayOfPlaceholders[i].style.backgroundColor = pSBC(change, backgrColor);
		}

	    setTimeout(breatheColour, 20);
	} //changes the colours of the templates to add a loading animation



	const container = document.getElementsByClassName('clsScroll')[0];
    var spotifyColours = [];
	var	arrayOfPlaceholders = [];
	var arrayOfPosts = [];
	var expandedPosts = [];
	var change = 0.01;
	var pos = 1;

	addPost();
	addPost();
	addPost();
	addPost();
	breatheColour();
