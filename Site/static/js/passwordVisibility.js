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
  var passwordInput3 = document.getElementById("password3");
  if (passwordInput3.type === "password") {
    passwordInput3.type = "text";
  } else {
    passwordInput3.type = "password";
  }
}