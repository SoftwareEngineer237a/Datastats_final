// Main Chat Interface JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const messagesContainer = document.getElementById('messagesContainer');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const attachBtn = document.getElementById('attachBtn');
    const fileInput = document.getElementById('fileInput');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const uploadedFiles = document.getElementById('uploadedFiles');
    const charCount = document.getElementById('charCount');
    const clearChatBtn = document.getElementById('clearChat');
    const exportChatBtn = document.getElementById('exportChat');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    // State
    let uploadedFilesData = [];
    let conversationHistory = [];
    let isProcessing = false;

    // Initialize
    init();

    function init() {
        setupEventListeners();
        updateSendButtonState();
        autoResizeTextarea();
    }

    function setupEventListeners() {
        // Send message
        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keydown', handleKeyDown);
        
        // File upload
        attachBtn.addEventListener('click', toggleFileUpload);
        fileInput.addEventListener('change', handleFileSelect);
        fileUploadArea.addEventListener('click', () => fileInput.click());
        fileUploadArea.addEventListener('dragover', handleDragOver);
        fileUploadArea.addEventListener('dragleave', handleDragLeave);
        fileUploadArea.addEventListener('drop', handleFileDrop);
        
        // Input handling
        messageInput.addEventListener('input', handleInputChange);
        messageInput.addEventListener('paste', handlePaste);
        
        // Header actions
        clearChatBtn.addEventListener('click', clearConversation);
        exportChatBtn.addEventListener('click', exportConversation);
        
        // Click outside to close file upload
        document.addEventListener('click', handleOutsideClick);
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    function handleInputChange() {
        const text = messageInput.value;
        charCount.textContent = `${text.length}/2000`;
        
        if (text.length > 1800) {
            charCount.style.color = '#ef4444';
        } else if (text.length > 1500) {
            charCount.style.color = '#f59e0b';
        } else {
            charCount.style.color = '#64748b';
        }
        
        updateSendButtonState();
        autoResizeTextarea();
    }

    function handlePaste(e) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const file = items[i].getAsFile();
                if (file) {
                    addFileToUpload(file);
                }
            }
        }
    }

    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
    }

    function updateSendButtonState() {
        const hasText = messageInput.value.trim().length > 0;
        const hasFiles = uploadedFilesData.length > 0;
        sendBtn.disabled = (!hasText && !hasFiles) || isProcessing;
    }

    function toggleFileUpload() {
        const isHidden = fileUploadArea.classList.contains('hidden');
        if (isHidden) {
            fileUploadArea.classList.remove('hidden');
            attachBtn.classList.add('active');
        } else {
            fileUploadArea.classList.add('hidden');
            attachBtn.classList.remove('active');
        }
    }

    function handleOutsideClick(e) {
        if (!fileUploadArea.contains(e.target) && !attachBtn.contains(e.target)) {
            fileUploadArea.classList.add('hidden');
            attachBtn.classList.remove('active');
        }
    }

    function handleDragOver(e) {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
    }

    function handleFileDrop(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        files.forEach(addFileToUpload);
        fileUploadArea.classList.add('hidden');
        attachBtn.classList.remove('active');
    }

    function handleFileSelect(e) {
        const files = Array.from(e.target.files);
        files.forEach(addFileToUpload);
        fileInput.value = '';
        fileUploadArea.classList.add('hidden');
        attachBtn.classList.remove('active');
    }

    function addFileToUpload(file) {
        // File type validation
        const allowedTypes = [
            'text/csv',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel',
            'image/jpeg',
            'image/jpg',
            'image/png',
            'application/pdf',
            'text/plain',
            'application/json'
        ];
        
        if (!allowedTypes.includes(file.type)) {
            showNotification('File type not supported', 'error');
            return;
        }
        
        // File size validation (10MB max)
        if (file.size > 10 * 1024 * 1024) {
            showNotification('File size must be less than 10MB', 'error');
            return;
        }
        
        const fileData = {
            id: Date.now() + Math.random(),
            file: file,
            name: file.name,
            size: formatFileSize(file.size),
            type: file.type
        };
        
        uploadedFilesData.push(fileData);
        renderUploadedFiles();
        updateSendButtonState();
    }

    function removeFile(fileId) {
        uploadedFilesData = uploadedFilesData.filter(f => f.id !== fileId);
        renderUploadedFiles();
        updateSendButtonState();
    }

    function renderUploadedFiles() {
        if (uploadedFilesData.length === 0) {
            uploadedFiles.innerHTML = '';
            return;
        }
        
        const html = uploadedFilesData.map(file => `
            <div class="file-preview" data-file-id="${file.id}">
                <span class="file-icon">${getFileIcon(file.type)}</span>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${file.size}</div>
                </div>
                <button class="remove-file" onclick="removeFile(${file.id})">×</button>
            </div>
        `).join('');
        
        uploadedFiles.innerHTML = html;
    }

    function getFileIcon(fileType) {
        const iconMap = {
            'text/csv': '📊',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '📊',
            'application/vnd.ms-excel': '📊',
            'image/jpeg': '🖼️',
            'image/jpg': '🖼️',
            'image/png': '🖼️',
            'application/pdf': '📄',
            'text/plain': '📝',
            'application/json': '📋'
        };
        return iconMap[fileType] || '📎';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if ((!text && uploadedFilesData.length === 0) || isProcessing) return;
        
        isProcessing = true;
        updateSendButtonState();
        
        // Hide welcome message if it exists
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
        
        // Create user message
        const userMessage = {
            type: 'user',
            text: text,
            files: [...uploadedFilesData],
            timestamp: new Date()
        };
        
        // Add to conversation
        conversationHistory.push(userMessage);
        renderMessage(userMessage);
        
        // Clear input
        messageInput.value = '';
        uploadedFilesData = [];
        renderUploadedFiles();
        updateSendButtonState();
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Simulate API call (replace with actual implementation)
            const response = await simulateAPICall(userMessage);
            
            hideTypingIndicator();
            
            // Create bot response
            const botMessage = {
                type: 'bot',
                text: response,
                timestamp: new Date()
            };
            
            conversationHistory.push(botMessage);
            renderMessage(botMessage);
            
        } catch (error) {
            hideTypingIndicator();
            showNotification('Sorry, something went wrong. Please try again.', 'error');
        } finally {
            isProcessing = false;
            updateSendButtonState();
            messageInput.focus();
        }
    }

    function renderMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type}-message`;
        
        let filesHtml = '';
        if (message.files && message.files.length > 0) {
            filesHtml = `
                <div class="message-files">
                    ${message.files.map(file => `
                        <div class="message-file">
                            <span class="file-icon">${getFileIcon(file.type)}</span>
                            <span class="file-name">${file.name}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${filesHtml}
                ${message.text ? `<div class="message-text">${message.text}</div>` : ''}
            </div>
            <div class="message-time">${formatTime(message.timestamp)}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-content typing-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="message-time">AI is typing...</div>
        `;
        messagesContainer.appendChild(typingDiv);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        const typingDiv = document.getElementById('typingIndicator');
        if (typingDiv) typingDiv.remove();
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showNotification(message, type = 'info') {
        // Simple notification (could be replaced with a toast library)
        const notif = document.createElement('div');
        notif.className = `chatbox-notification ${type}`;
        notif.textContent = message;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    }

    function formatTime(date) {
        if (!(date instanceof Date)) date = new Date(date);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function clearConversation() {
        conversationHistory = [];
        messagesContainer.innerHTML = '';
        showWelcomeMessage();
    }

    function exportConversation() {
        let exportText = '';
        conversationHistory.forEach(msg => {
            const who = msg.type === 'user' ? 'You' : 'AI';
            exportText += `[${formatTime(msg.timestamp)}] ${who}: ${msg.text}\n`;
        });
        const blob = new Blob([exportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'chat_history.txt';
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    }

    function showWelcomeMessage() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    <div class="message-text">
                        👋 Hi! I can help interpret your analysis results, reports, or graphs.<br>
                        Type your question or paste your data to get started.
                    </div>
                </div>
                <div class="message-time">${formatTime(new Date())}</div>
            </div>
        `;
        messagesContainer.appendChild(welcomeDiv);
        scrollToBottom();
    }

    // Simulate API call (replace with actual API integration)
    async function simulateAPICall(userMessage) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: userMessage.text,
                context: '' // You can add more context if needed
            })
        });
        const data = await response.json();
        if (data.reply) {
            return data.reply;
        } else if (data.response) {
            return data.response;
        } else if (data.error) {
            return "Error: " + data.error;
        } else {
            return "Sorry, I couldn't interpret that.";
        }
    } catch (err) {
        return "Network error. Please try again.";
    }
}

    // Expose removeFile globally for inline onclick
    window.removeFile = removeFile;

    // Show welcome message on load if no conversation
    if (conversationHistory.length === 0) {
        showWelcomeMessage();
    }
});