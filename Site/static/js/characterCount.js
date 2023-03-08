document.querySelector('textarea').addEventListener('keyup', function(){
  var characterCount = this.value.length;
  var current = document.querySelector('#current');
  var maximum = document.querySelector('#maximum');
  var theCount = document.querySelector('#the-count');

  current.textContent = characterCount;
});