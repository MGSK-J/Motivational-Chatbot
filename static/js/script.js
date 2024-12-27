document.getElementById('chat-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;

    // Display user message
    const messages = document.getElementById('messages');
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerText = userInput;
    messages.appendChild(userMessage);

    // Send input to the server
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ user_input: userInput })
    });

    // Display bot message
    const botMessage = document.createElement('div');
    botMessage.className = 'bot-message';
    botMessage.innerText = (await response.json()).response;
    messages.appendChild(botMessage);

    // Scroll chatbox
    messages.scrollTop = messages.scrollHeight;

    // Clear input
    document.getElementById('user-input').value = '';
});
