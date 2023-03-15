const input = document.getElementById('profile-pic-input');
const span = document.querySelector('.profile-picture-span');
input.addEventListener('change', function() {
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = function() {
    span.style.backgroundImage = `url(${reader.result})`;
    }
    reader.readAsDataURL(file);
});