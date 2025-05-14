import React, { useState } from "react";
import ChatWindow from "./ChatWindow";
import "./ChatbotPopup.css"; // Use only this CSS file for styling

const ChatbotPopup = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const togglePopup = () => {
    setIsOpen(!isOpen);
    // Add welcome message when first opened
    if (!isOpen && messages.length === 0) {
      setMessages([
        { sender: "bot", text: "Hi there! How can I help you today?" },
      ]);
    }
  };

  const sendMessage = async (e) => {
    e?.preventDefault(); // Prevent form submission

    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    // Clear input immediately after sending
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();
      const botMessage = { sender: "bot", text: data.answer };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      // Add error message
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Sorry, I'm having trouble connecting. Please try again later.",
        },
      ]);
    }

    setLoading(false);
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage(e);
    }
  };

  return (
    <>
      {/* Floating button to open the chat */}
      {!isOpen && (
        <button className="chat-button" onClick={togglePopup}>
          💬
        </button>
      )}

      {/* Chatbot Pop-up */}
      {isOpen && (
        <div className="chat-popup">
          <div className="chat-header">
            <h3>Chatbot</h3>
            <button className="close-btn" onClick={togglePopup}>
              ✖
            </button>
          </div>
          <ChatWindow messages={messages} loading={loading} />
          <form className="chat-input" onSubmit={sendMessage}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyUp={handleKeyPress}
              placeholder="Type a message..."
              autoFocus
            />
            <button type="submit">Send</button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatbotPopup;
