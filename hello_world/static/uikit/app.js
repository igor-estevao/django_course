// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
  document.getElementById("formInput#search").focus();
});



let alertWrapper = document.querySelector(".alert")
let alertClose = document.querySelector(".alert__close")

if(alertWrapper){
  console.log("Closed Alert")
  alertClose.addEventListener("click", () =>
    alertWrapper.style.display = "none"
  )
}