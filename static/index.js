/* =================== PHOTO GALLERY SLIDER =================== */
let slideIndex = 1;
showSlides(slideIndex);
function plusSlides(n) {
  showSlides(slideIndex += n);
}
function currentSlide(n) {
  showSlides(slideIndex = n);
}
function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("demo");
  let captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}

/* =================== DISPLAYING AND REMOVING CHATBOX =================== */
const message_bot_btn=document.getElementById("message-bot");
message_bot_btn.addEventListener("click",()=>{
  const chat_box=document.getElementsByClassName("boxed")[0];
  chat_box.style.right="15px";
})
const close_chat_box_btn=document.getElementsByClassName('close-icon')[0];
close_chat_box_btn.addEventListener("click",()=>{
  const chat_box=document.getElementsByClassName("boxed")[0];
  chat_box.style.right="-535px";
})

/* =================== CHAT BOT RESPONSES =================== */
// function getBotResponse() {
//   var userInput = document.getElementById("userInput");
//     var rawText = $("#textInput").val();
//     var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
//     $("#textInput").val("");
//     $("#chatbox").append(userHtml);
//     userInput.scrollIntoView({
//             block: "start",
//             behavior: "smooth"
//         });
//  if( rawText == ""){
//     var emp = "Can't read Empty text";
//     var botHtml = '<p class="botText"><span><i class="fas fa-robot"></i>&nbsp;' + emp + "</span></p>";
//     $("#chatbox").append(botHtml);
//         userInput.scrollIntoView({
//                 block: "start",
//                 behavior: "smooth"
//     });
//   }
//   else{
//     $.get("/get", { msg: rawText
//     }).done(function (data) {
//         var botHtml = '<p class="botText"><span><i class="fas fa-robot"></i>&nbsp;' + data +  "</span></p>";
//         $("#chatbox").append(botHtml);
//         userInput.scrollIntoView({
//                 block: "start",
//                 behavior: "smooth"
//             });
//     });
//   }
// }

/* =================== AFTER ENTER SUBMIT QUERY =================== */
// $("#textInput").keypress(function (e) {
//     if (e.which == 13) {
//         getBotResponse();
//     }
// });
