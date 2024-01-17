function statusProcess() {
    let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
    const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/status/'

    StatusSocket = {
        socket: new WebSocket(socketUrl),
        url: socketUrl,
        shouldClose: false
    };
    
    StatusSocket.socket.onopen = () => console.log('Connection opened');
    StatusSocket.socket.onerror = error => console.log('WebSocket error:', error);
    StatusSocket.socket.onmessage = event => console.log('Message from server:', event.data);
    // Check WebSocket connection status
    StatusSocket.socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened:', event);
    });

    StatusSocket.socket.addEventListener('error', function (event) {
        console.error('WebSocket error:', event);
    });

    StatusSocket.socket.onmessage = function(event) {
        console.log('Message from server:', event.data);

        var message = JSON.parse(event.data);

        if (message.type === 'status_update') {
            console.log('status_update');
            var userElement = document.querySelector('.container[data-user-id="' + message.id + '"]');
            console.log(userElement);

            if (userElement) {
                var statusElement = userElement.querySelector('.status');
                if (statusElement) {
                    statusElement.textContent = message.status === 'online' ? '🟢' : '🔴';
                }
            }
        }
    }
}