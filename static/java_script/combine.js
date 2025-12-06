document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const messageForm = document.getElementById('messageForm');
    const themeToggle = document.getElementById('themeToggle');

    // Theme toggle functionality
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }

    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Initialize theme
    initTheme();

    // Auto-scroll to bottom
    function scrollToBottom() {
        if (chatMessages) {
            setTimeout(() => {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 0);
        }
    }

    // Auto-resize textarea
    if (messageInput) {
        messageInput.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 80) + 'px';
        });
    }

    // Scroll to bottom on page load
    scrollToBottom();

    // Handle form submission
    if (messageForm) {
        messageForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Check if message is not empty
            if (messageInput.value.trim() !== '') {
                // Submit the form
                this.submit();

                // Reset the input field
                setTimeout(() => {
                    if (messageInput) {
                        messageInput.value = '';
                        messageInput.style.height = 'auto';
                    }
                    scrollToBottom();
                }, 100);
            }
        });
    }

    // Add Enter key support (Shift+Enter for new line)
    if (messageInput) {
        messageInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (messageForm) {
                    // Trigger form submission
                    messageForm.dispatchEvent(new Event('submit'));
                }
            }
        });
    }

    // Prevent going back to previous page
    history.pushState(null, null, location.href);
    window.onpopstate = function () {
        history.pushState(null, null, location.href);
    };
});

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the main messages page (no active chat)
    const isEmptyChat = document.querySelector('.empty-chat') !== null;
    
    if (isEmptyChat) {
        // Get the first conversation from the inbox (most recent)
        const firstConversation = document.querySelector('.conversation-item');
        const mobileFirstConversation = document.querySelector('.mobile-conversation-btn');
        
        if (firstConversation) {
            // Redirect to the most recent conversation
            window.location.href = firstConversation.href;
        } else if (mobileFirstConversation) {
            // For mobile, use the mobile conversation button
            window.location.href = mobileFirstConversation.href;
        }
    }
});

