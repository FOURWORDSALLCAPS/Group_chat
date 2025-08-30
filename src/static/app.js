class ChatApplication {
    constructor() {
        this.username = null;
        this.emojiPickerVisible = false;
        this.isResizing = false;
        this.startX = 0;
        this.startWidth = 0;
        this.userUuid = null;
        this.ws = null;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initAuthModal();
        this.checkAuth();
        this.restoreSidebarWidth();
    }

    initAuthModal() {
        const template = document.getElementById('login-template');
        this.authModal = document.createElement('div');
        this.authModal.appendChild(template.content.cloneNode(true))
        document.body.appendChild(this.authModal);

        const form = this.authModal.querySelector('#authForm');
        form.addEventListener('submit', (e) => this.handleLogin(e));
    }

    checkAuth() {
        const savedUserUuid = localStorage.getItem('chat_user_uuid');
        if (savedUserUuid) {
            this.userUuid = savedUserUuid;
            this.isAuthenticated = true;
            this.hideAuthModal();
            this.initWebSocket();
        } else {
            this.showAuthModal();
        }
    }

    handleLogin(e) {
        e.preventDefault();

        const username = document.getElementById('login').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('authError');

        const submitButton = this.authModal.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Вход...';

        fetch('/v1/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {

            if (response.ok) {
                return response.json().then(data => {
                    this.userUuid = data.user_uuid;
                    this.isAuthenticated = true;

                    localStorage.setItem('chat_user_uuid', this.userUuid);

                    this.hideAuthModal();
                    this.initWebSocket();
                });
            } else {
                return response.json().then(errorData => {
                    errorDiv.textContent = errorData.detail || `Ошибка авторизации: ${response.status}`;
                    errorDiv.style.display = 'block';
                }).catch(() => {
                    errorDiv.textContent = `Ошибка авторизации: ${response.status}`;
                    errorDiv.style.display = 'block';
                });
            }
        })
        .catch(error => {
            errorDiv.textContent = 'Ошибка подключения к серверу';
            errorDiv.style.display = 'block';
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        });
    }

    showAuthModal() {
        this.authModal.style.display = 'flex';
    }

    hideAuthModal() {
        this.authModal.style.display = 'none';
    }

    initWebSocket() {
        try {
            this.ws = new WebSocket(`ws://${window.location.host}/v1/ws/?user_uuid=${this.userUuid}`);
            this.setupWebSocketHandlers();
        } catch (error) {
            this.addSystemMessage('Ошибка подключения к серверу');
        }
    }

    setupWebSocketHandlers() {
        this.ws.onmessage = (event) => this.handleWebSocketMessage(event);
        this.ws.onclose = () => this.handleWebSocketClose();
        this.ws.onerror = (error) => this.handleWebSocketError(error);
    }

    handleWebSocketMessage(event) {
        const data = JSON.parse(event.data);

        switch (data.type) {
            case 'connection_established':
                this.handleConnectionEstablished(data);
                this.updateUserCount(data.user_count_update);
                break;
            case 'message':
                this.handleIncomingMessage(data);
                break;
        }
    }

    handleConnectionEstablished(data) {
        if (data.username) {
            this.username = data.username;
            document.getElementById('userName').textContent = this.username;
            document.querySelector('.user-status')?.classList.add('visible');
            this.addSystemMessage('Вы подключились к чату');
        }
    }

    handleIncomingMessage(data) {
        if (data.username !== this.username) {
            this.displayMessage(data, 'incoming');
        }
    }

    handleWebSocketClose() {
        this.addSystemMessage('Соединение прервано. Попытка переподключения...');
        this.attemptReconnect();
    }

    handleWebSocketError(error) {
        this.addSystemMessage('Ошибка соединения');
    }

    attemptReconnect() {
        setTimeout(() => {
            this.initWebSocket();
        }, 3000);
    }

    setupEventListeners() {
        this.setupMessageInputListeners();
        this.setupEmojiPickerListeners();
        this.setupSidebarResizerListeners();
        this.setupGlobalListeners();
        this.setupSendButtonListener();
    }

    setupMessageInputListeners() {
        const messageInput = document.getElementById('messageInput');
        if (!messageInput) return;

        messageInput.addEventListener('keydown', (e) => this.handleMessageInputKeydown(e));
        messageInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    handleMessageInputKeydown(e) {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                setTimeout(() => this.autoResizeTextarea(), 0);
            } else {
                e.preventDefault();
                this.sendMessage();
            }
        }
    }

    setupSendButtonListener() {
        const sendButton = document.querySelector('.send-btn');
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }
    }

    setupEmojiPickerListeners() {
        const emojiButton = document.querySelector('.fa-smile')?.closest('.icon-btn');
        if (!emojiButton) return;

        emojiButton.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleEmojiPicker();
        });

        document.querySelectorAll('.emoji').forEach(emojiElement => {
            emojiElement.addEventListener('click', (e) => {
                e.stopPropagation();
                this.insertEmoji(emojiElement.textContent);
            });
        });
    }

    setupSidebarResizerListeners() {
        const resizer = document.getElementById('sidebarResizer');
        if (!resizer) return;

        resizer.addEventListener('mousedown', (e) => this.startResize(e));
        document.addEventListener('mousemove', (e) => this.handleResize(e));
        document.addEventListener('mouseup', () => this.stopResize());
    }

    setupGlobalListeners() {
        document.addEventListener('click', (e) => this.handleGlobalClick(e));
        document.addEventListener('keydown', (e) => this.handleGlobalKeydown(e));
    }

    handleGlobalClick(e) {
        this.handleEmojiPickerClose(e);
    }

    handleGlobalKeydown(e) {
        if (e.key === 'Escape' && this.emojiPickerVisible) {
            this.closeEmojiPicker();
        }
    }

    toggleEmojiPicker() {
        const emojiPicker = document.querySelector('.emoji-picker-container');
        this.emojiPickerVisible = !this.emojiPickerVisible;

        emojiPicker?.classList.toggle('show', this.emojiPickerVisible);
    }

    closeEmojiPicker() {
        if (this.emojiPickerVisible) {
            this.emojiPickerVisible = false;
            document.querySelector('.emoji-picker-container')?.classList.remove('show');
        }
    }

    handleEmojiPickerClose(e) {
        const emojiPicker = document.querySelector('.emoji-picker-container');
        const emojiBtn = document.querySelector('.fa-smile')?.closest('.icon-btn');

        if (this.emojiPickerVisible && emojiPicker && emojiBtn &&
            !emojiPicker.contains(e.target) && !emojiBtn.contains(e.target)) {
            this.closeEmojiPicker();
        }
    }

    insertEmoji(emoji) {
        const input = document.getElementById('messageInput');
        if (!input) return;

        const startPos = input.selectionStart;
        const endPos = input.selectionEnd;

        input.value = input.value.substring(0, startPos) +
                     emoji +
                     input.value.substring(endPos);

        input.selectionStart = input.selectionEnd = startPos + emoji.length;
        input.focus();
        this.autoResizeTextarea();
    }

    startResize(e) {
        this.isResizing = true;
        this.startX = e.clientX;
        this.startWidth = parseInt(getComputedStyle(document.querySelector('.sidebar')).width, 10);

        document.body.classList.add('resizing');
        document.querySelector('.app-container')?.classList.add('resizing');
        e.preventDefault();
    }

    handleResize(e) {
        if (!this.isResizing) return;

        const sidebar = document.querySelector('.sidebar');
        const newWidth = this.startWidth + (e.clientX - this.startX);
        const minWidth = 250;
        const maxWidth = 400;

        if (newWidth >= minWidth && newWidth <= maxWidth && sidebar) {
            sidebar.style.width = `${newWidth}px`;
        }
    }

    stopResize() {
        if (!this.isResizing) return;

        this.isResizing = false;
        document.body.classList.remove('resizing');
        document.querySelector('.app-container')?.classList.remove('resizing');

        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            localStorage.setItem('sidebarWidth', sidebar.style.width);
        }
    }

    restoreSidebarWidth() {
        const savedWidth = localStorage.getItem('sidebarWidth');
        const sidebar = document.querySelector('.sidebar');

        if (savedWidth && sidebar) {
            sidebar.style.width = savedWidth;
        }
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('messageInput');
        if (!textarea) return;

        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
        textarea.style.overflowY = textarea.scrollHeight > 120 ? 'auto' : 'hidden';
    }

    sendMessage() {
        if (this.emojiPickerVisible) {
            this.closeEmojiPicker();
        }

        if (!this.username) {
            this.addSystemMessage('Еще не подключены к серверу!');
            return;
        }

        const input = document.getElementById('messageInput');
        if (!input) return;

        const message = input.value.trim();
        if (!message) return;

        const messageData = {
            type: 'message',
            username: this.username,
            content: message,
            timestamp: new Date().toISOString()
        };

        this.displayMessage({
            username: this.username,
            content: message,
            timestamp: new Date().toISOString()
        }, 'outgoing');

        try {
            this.ws.send(JSON.stringify(messageData));
        } catch (error) {
            this.addSystemMessage('Ошибка отправки сообщения');
        }

        input.value = '';
        this.resetTextarea();
    }

    resetTextarea() {
        const textarea = document.getElementById('messageInput');
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.overflowY = 'hidden';
        }
    }

    displayMessage(message, messageType = 'incoming') {
        const messagesContainer = document.getElementById('messages');
        if (!messagesContainer) return;

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `message-${messageType}`);

        const formattedTime = this.formatTime(message.timestamp);

        if (messageType === 'incoming') {
            messageElement.innerHTML = `
                <div class="message-sender">${this.escapeHtml(message.username)}</div>
                <div class="message-text">${this.escapeHtml(message.content)}</div>
                <div class="message-time">${formattedTime}</div>
            `;
        } else {
            messageElement.innerHTML = `
                <div class="message-text">${this.escapeHtml(message.content)}</div>
                <div class="message-time">${formattedTime}</div>
            `;
        }

        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addSystemMessage(text) {
        const messagesContainer = document.getElementById('messages');
        if (!messagesContainer) return;

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'message-system');
        messageElement.style.cssText = `
            align-self: center;
            background-color: rgba(255, 255, 255, 0.1);
            color: #aaa;
            font-style: italic;
            max-width: 80%;
            text-align: center;
            padding: 5px 10px;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 13px;
        `;

        messageElement.textContent = text;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateUserCount(count) {
        document.getElementById('userCount').textContent = count;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApplication();
});
