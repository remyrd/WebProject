$(document).ready(function() {

  var inbox = new ReconnectingWebSocket("ws://"+ location.host + "/receive");
  var outbox = new ReconnectingWebSocket("ws://"+ location.host + "/submit");

  inbox.onmessage = function(message) {
    var data = JSON.parse(message.data);
    switch (data.id) {
      case "message":
        if (data.room == $("#roomname").attr("value")) {
        $("#chat-text").append("<div class='panel-body'>" + $('<span/>').text(data.handle).html() +" : "+$('<span/>').text(data.text).html() + "</div>");
        $("#chat-text").stop().animate({
          scrollTop: $('#chat-text')[0].scrollHeight
          }, 100);
        }

    }
    
  };

  inbox.onclose = function(){
      console.log('inbox closed');
      this.inbox = new WebSocket(inbox.url);

  };

  outbox.onclose = function(){
      console.log('outbox closed');
      this.outbox = new WebSocket(outbox.url);
  };

  $("#input-form").on("submit", function(event) {
    event.preventDefault();
    var handle = $("#input-handle").attr("value");
    var text   = $("#input-text")[0].value;
    var room = $("#roomname").attr("value");
    var id = "message";
    if (text != "") {
      outbox.send(JSON.stringify({ 
        handle: handle, 
        text: text, 
        room: room, 
        id: id
      }));
    }
    $("#input-text")[0].value = "";
  });

  $("#click-me").click(function(){
    $("#people-in-room").toggle();

  })
})
