import React, { useState, useEffect } from 'react';
import './index.css';
import io from 'socket.io-client';

const socket = io(`http://localhost:4000`);

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    // Listen for messages from the server
    socket.on("bot_message", (botMessage) => {
        setMessages(prevMessages => [...prevMessages, { text: botMessage, sender: 'bot' }]);
    });

    // Clean up the listener
    return () => {
        socket.off("bot_message");
    };
  }, []);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const newMessages = [...messages, { text: inputMessage, sender: 'user' }];
    setMessages(newMessages);

    socket.emit('user_message', inputMessage);

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