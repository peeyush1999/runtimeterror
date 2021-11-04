
//const toggleChatboxBtn = document.querySelector(".js-chatbox-toggle");
//const chatbox = document.querySelector(".js-chatbox");

//const chatboxForm = document.querySelector(".js-chatbox-form");

// Use to create chat bubble when user submits text
// Appends to display
/*const createChatBubble = input => {
  const chatSection = document.createElement("p");
  chatSection.textContent = input;
  chatSection.classList.add("chatbox__display-chat");

  chatboxMsgDisplay.appendChild(chatSection);
};
*/
// Toggle the visibility of the chatbox element when clicked
// And change the icon depending on visibility
var toggle1=document.querySelector(".js-chatbox-toggle");
var cbox=document.querySelector(".js-chatbox");
var cmd= document.querySelector(".js-chatbox-display");



uid=1;
workshopid=1;
gid=1;

window.addEventListener('load', (event) => {
var today = new Date();
var time = today.getHours() + ":" + today.getMinutes();

$.get("/getmsg", { wid:workshopid, grpid:gid }).done(function(data) {
    
    

    for(i=0;i<data.length;i++)
    {
    console.log(data[i]["text"]);
    const chatSection = document.createElement("p");
    chatSection.textContent = data[i]["text"];
    chatSection.classList.add("chatbox__display-chat");
    cmd.appendChild(chatSection);
    
    }
    //document
      //.getElementById("userInput")
      //.scrollIntoView({ block: "start", behavior: "smooth" });
      $('#chat').animate({
      scrollTop: $('#chat')[0].scrollHeight}, 5000);
  });

});


toggle1.addEventListener("click", () => {

  console.log("Executed");
  document.querySelector(".js-chatbox").classList.toggle("chatbox--is-visible");

  if (cbox.classList.contains("chatbox--is-visible")) {
    toggle1.innerHTML = '<i class="fas fa-chevron-down"></i>';
  } else {
    toggle1.innerHTML = '<i class="fas fa-chevron-up"></i>';
  }

});

function getBotResponse() 
{
  //var rawText = $("#textInput").val();
  var rawText = document.querySelector(".js-chatbox-input").value;
    console.log(rawText);
    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes()
    if(today.getHours() >=12)
    {
        time+=" PM";
    }
    else
    {
        time+=" AM";   
    }

  /*var userHtml = '<li class="me"><div class="entete"><span class="status green"></span></div><div class="triangle"></div><div class="message">' + rawText + "</div></li>";
  $("#textInput").val("");
  $("#chat").append(userHtml);
  */
  $("#text").val("");
  const chatSection = document.createElement("p");
  chatSection.textContent = rawText;
  chatSection.classList.add("chatbox__display-chat");
  cmd.appendChild(chatSection);
  $('#chat').animate({
  scrollTop: $('#chat')[0].scrollHeight}, 1000);


  $.get("/addMessage", { msg: rawText, userid: uid, wid:workshopid, grpid:gid }).done(function(data) {
    /*    
    var botHtml = '<li class="you"><div class="entete"><h3>'+time+', Today &nbsp;</h3><h2>Travis</h2><span class="status blue"></span></div><div class="triangle"></div><div class="message">' + data + "</div></li>";
    $("#chat").append(botHtml);    
      $('#chat').animate({
      scrollTop: $('#chat')[0].scrollHeight}, 1000);
      */
  });


}


$("#textInput").keypress(function(e) {
  console.log("input pressed");
if (e.which == 13 && $("#textInput").val()!="" ) {
getBotResponse();
}
});


// Form input using method createChatBubble
// To append any user message to display
/*chatboxForm.addEventListener("submit", e => {
  const chatInput = document.querySelector(".js-chatbox-input").value;

  createChatBubble(chatInput);

  e.preventDefault();
  chatboxForm.reset();
});
*/



