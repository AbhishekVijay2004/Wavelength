function togglePasswordVisibility() {
  var passwordInput1 = document.getElementById("password1");
  if (passwordInput1.type === "password") {
    passwordInput1.type = "text";
  } else {
    passwordInput1.type = "password";
  }
  var passwordInput2 = document.getElementById("password2");
  if (passwordInput2.type === "password") {
    passwordInput2.type = "text";
  } else {
    passwordInput2.type = "password";
  }
}