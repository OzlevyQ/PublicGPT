document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    var chatContainer = document.getElementById('chat-container');
    var loginForm = document.getElementById('login-form');
    var messageForm = document.getElementById('message-form');
    var usernameInput = document.getElementById('username');
    var messageInput = document.getElementById('message');

    // Hide chat container until user is logged in
    if (chatContainer) {
        chatContainer.style.display = 'none';
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var username = usernameInput.value;
            if (username) {
                socket.emit('login', { username: username });
                loginForm.style.display = 'none';
                if (chatContainer) {
                    chatContainer.style.display = 'block';
                }
            }
        });
    }

    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var message = messageInput.value;
            if (message) {
                socket.emit('message', { username: usernameInput.value, message: message });
                messageInput.value = '';
            }
        });
    }

    socket.on('message', function(data) {
        var chat = document.getElementById('chat');
        if (chat) {
            var message = document.createElement('p');
            message.textContent = data.username + ': ' + data.message;
            chat.appendChild(message);
        }
    });
});
