import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
// Remove the style import as we're using ChatbotPopup.css for all styling
// import './style.css';

const ChatWindow = ({ messages, loading }) => {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.sender === "user" ? "user-message" : "bot-message"}
          >
            {msg.sender === "user" ? "👤 " : "🤖 "}
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        ))}

        {/* Loading message */}
        {loading && (
          <div className="bot-message typing">
            🤖 <i>Bot is typing</i>
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
