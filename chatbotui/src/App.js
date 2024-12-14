import React, { useState } from 'react';
import './index.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const newMessages = [...messages, { text: inputMessage, sender: 'user' }];
    setMessages(newMessages);

    // Simulate bot response
    setTimeout(() => {
      setMessages([
        ...newMessages,
        { text: `Bot: I received your message: "${inputMessage}"`, sender: 'bot' }
      ]);
    }, 1000);

    setInputMessage('');
  };

  return (
    <div className="container">
      <div className="chat-container">
        <div className="chat-header">GenAI Chatbot</div>
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <form className="input-form" onSubmit={handleSendMessage}>
          <input
            className="input"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type a message..."
          />
          <button className="send-button" type="submit">Send</button>
        </form>
      </div>
    </div>
  );
};

export default App; 