document.addEventListener('DOMContentLoaded', function () {
    // Init the socket
    let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let websocketPort = window.location.protocol === 'https:' ? ':8443' : ':8000';
    const notificationSocketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/notifications/';

    let notificationSocket = {
        socket: new WebSocket(notificationSocketUrl),
        url: notificationSocketUrl,
        shouldClose: false
    };

    // Update the notification count
    notificationSocket.socket.onmessage = function(e) {
        renderHeader();
    };

    // Close the socket
    notificationSocket.socket.onclose = function(e) {
        if (!this.shouldClose) {
            // Reconnect if the socket is unexpectedly closed
            notificationSocket.socket = new WebSocket(notificationSocket.url);
        }
    };

    // Close the socket when the user leaves the page
    window.onbeforeunload = function() {
        if (notificationSocket !== null) {
            notificationSocket.shouldClose = true;
            notificationSocket.socket.close();
        }
    };
});