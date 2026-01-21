console.log("hello world");
const headerSection = document.querySelector(".header-section");
const navBar = document.querySelector(".nav-bar");
const searchContainer = document.querySelector(".search-container");
const searchInput = document.querySelector(".search-input");
const searchButton = document.querySelector(".search-container");
const pageContent = document.querySelector(".page-content");
const footerSection = document.querySelector(".page-footer");
const connectWithUs = document.querySelector(".connect");
const policies = document.querySelector(".must-read");
const btnSignUp = document.querySelector(".sign-up-button");
const btnLogin = document.querySelector(".sign-in-button");
//let's Design header
// Django URL template (replace 'registration' with your Django URL name)


if (btnLogin) {
  btnLogin.addEventListener("click", function() {
    console.log("Login button clicked");
    window.location.href = "/login/";
  });
}

if (btnSignUp) {
  btnSignUp.addEventListener("click",function() {
    console.log("sign up button clicked");
    window.location.href = "/register/";
  } );
}