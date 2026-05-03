document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBody = document.getElementById('chat-body');
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Theme toggling
    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-theme', newTheme);
        
        // Update icon
        const icon = themeToggle.querySelector('i');
        if (newTheme === 'dark') {
            icon.classList.replace('fa-sun', 'fa-moon');
        } else {
            icon.classList.replace('fa-moon', 'fa-sun');
        }
    });

    // Formatting time
    function getCurrentTime() {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; 
        minutes = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minutes} ${ampm}`;
    }

    // Add message to chat body
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text;

        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = getCurrentTime();

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);

        chatBody.appendChild(messageDiv);
        scrollToBottom();
    }

    // Typing indicator
    let typingIndicator;
    function showTypingIndicator() {
        typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'bot');
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('typing-indicator');
        contentDiv.innerHTML = '<span></span><span></span><span></span>';
        
        typingIndicator.appendChild(contentDiv);
        chatBody.appendChild(typingIndicator);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        if (typingIndicator) {
            chatBody.removeChild(typingIndicator);
            typingIndicator = null;
        }
    }

    // Scroll to bottom
    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    let lastIntent = null;

    // Handle form submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const messageText = userInput.value.trim();
        if (!messageText) return;

        // Display user message
        appendMessage('user', messageText);
        userInput.value = '';

        // Show typing indicator while fetching
        showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText, last_intent: lastIntent })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Save the intent for follow-ups
            if (data.intent && data.intent !== 'unknown' && data.intent !== 'follow_up') {
                lastIntent = data.intent;
            }
            
            // Artificial delay to make typing animation visible
            setTimeout(() => {
                removeTypingIndicator();
                appendMessage('bot', data.response);
            }, 600);

        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            const fallbacks = [
                "That's interesting! By the way, did you know that 'Avatar' is the highest-grossing film of all time?",
                "I'm here to entertain! Want to hear a fun fact or a movie recommendation?",
                "Haha, got it! Want me to suggest a great song or tell a joke?"
            ];
            const randomFallback = fallbacks[Math.floor(Math.random() * fallbacks.length)];
            appendMessage('bot', randomFallback);
        }
    });
});
