$(document).ready(function(){
    var socket = io.connect();
    socket.on('status_response', function(msg) {
        var date = new Date();
        $('#status').append('<p>status: ' + msg.data + "Time:"+ date+ '</p>');
    });
});