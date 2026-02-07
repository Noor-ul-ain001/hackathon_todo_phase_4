import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '@/contexts/AuthContext';
import { authService } from '@/services/auth';

// Loading state component
const LoadingState = () => (
  <div className="flex-1 flex items-center justify-center bg-gradient-to-br from-cyan-50 via-teal-50 to-white">
    <div className="text-center animate-fadeIn">
      <div className="loading-spinner mx-auto mb-4"></div>
      <p className="text-gray-500">Loading chat...</p>
    </div>
  </div>
);

export default function Chatkit() {
  // Auth and routing
  const { user, isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [conversationId, setConversationId] = useState(null);

  // Chat state
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Fetch conversation history from backend
  const loadConversationHistory = async (convId) => {
    if (!convId || !user) return;

    try {
      const response = await fetch(`${API_BASE_URL}/api/${user.id}/chat/history?conversation_id=${convId}&limit=50`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authService.getAccessToken()}`,
        },
      });

      if (!response.ok) {
        console.warn('Failed to load conversation history');
        return;
      }

      const data = await response.json();

      // Transform backend format to our format
      const formattedMessages = data.messages.map(msg => ({
        id: msg.id,
        text: msg.content,
        sender: msg.role === 'user' ? 'user' : 'ai',
        timestamp: new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }));

      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  // Auth protection - redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  // Load conversation history on mount or restore from localStorage
  useEffect(() => {
    if (!user) return;

    // Try to restore conversation from localStorage
    const savedConvId = localStorage.getItem('taskflow_current_conversation');

    if (savedConvId) {
      const convId = parseInt(savedConvId);
      setConversationId(convId);
      loadConversationHistory(convId);
    } else {
      // Show welcome message only for new conversations
      setMessages([{
        id: 'welcome-message',
        text: "Hello! I'm your TaskFlow AI Assistant. I can help you create, manage, and organize your tasks using natural language. Try typing 'Add a new task', 'Update task 1 to high priority', or 'Delete task 5'!",
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }]);
    }
  }, [user]);

  // Save conversation ID to localStorage when it changes
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem('taskflow_current_conversation', conversationId.toString());
    }
  }, [conversationId]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Show loading while auth initializes
  if (loading) {
    return <LoadingState />;
  }

  if (!user) {
    return null; // Will redirect to login
  }

  // Handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await callBackendAPI(inputMessage);

      // Add AI response to UI
      const aiMessage = {
        id: response.metadata?.message_id || `ai-${Date.now()}`,
        text: response.response,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        tasksAffected: response.tasks_affected || [],
      };

      setMessages(prev => [...prev, aiMessage]);

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Fetch updated tasks if any tasks were affected
      if (response.tasks_affected && response.tasks_affected.length > 0) {
        // In a real implementation, you would fetch updated tasks here
        console.log('Tasks affected:', response.tasks_affected);
      }
    } catch (error) {
      console.error('API Error:', error);

      // More descriptive error message
      let errorMessageText = 'Sorry, I encountered an error. ';
      if (error.message.includes('401') || error.message.includes('403')) {
        errorMessageText += 'Please make sure you are logged in and your session is valid.';
      } else if (error.message.includes('500')) {
        errorMessageText += 'The server encountered an error. Please try again later.';
      } else if (error.message.includes('Failed to fetch')) {
        errorMessageText += 'Unable to connect to the server. Please check if the backend is running.';
      } else {
        errorMessageText += error.message || 'Please try again later.';
      }

      const errorMessage = {
        id: `error-${Date.now()}`,
        text: errorMessageText,
        sender: 'system',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const callBackendAPI = async (message) => {
    const response = await fetch(`${API_BASE_URL}/api/${user.id}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authService.getAccessToken()}`,
      },
      body: JSON.stringify({
        message: message,
        modality: 'text',
        conversation_id: conversationId,
        metadata: {}
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  };

  // Handle key press (Enter to send, Shift+Enter for new line)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-cyan-50 via-teal-50 to-white">
      <Head>
        <title>ChatKit - TaskFlow</title>
        <meta name="description" content="TaskFlow AI Assistant with ChatKit" />
      </Head>

      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-teal-100 p-4 shadow-sm">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-teal-600 rounded-xl flex items-center justify-center mr-3">
            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">TaskFlow AI Assistant</h1>
            <div className="flex items-center space-x-2">
              <div className="relative flex h-2 w-2">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isLoading ? 'bg-amber-400' : 'bg-emerald-400'}`}></span>
                <span className={`relative inline-flex rounded-full h-2 w-2 ${isLoading ? 'bg-amber-500 shadow-[0_0_8px_#fbbf24]' : 'bg-emerald-500 shadow-[0_0_8px_#10b981]'}`}></span>
              </div>
              <span className={`text-xs font-medium ${isLoading ? 'text-amber-600' : 'text-emerald-600'}`}>
                {isLoading ? "Thinking..." : "Online"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 pb-20">
        <div className="max-w-3xl mx-auto">
          {messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex mb-6 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.sender !== 'user' && (
                <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-teal-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                  <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
              
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${
                  message.sender === 'user'
                    ? 'bg-gradient-to-br from-teal-500 to-teal-600 text-white rounded-tr-none'
                    : message.sender === 'system'
                    ? 'bg-red-100 text-red-800 border border-red-200 rounded-tl-none'
                    : 'bg-white border border-teal-100 rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.text}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-teal-100' : 'text-gray-500'
                  }`}
                >
                  {message.timestamp}
                </div>
              </div>
              
              {message.sender === 'user' && (
                <div className="w-8 h-8 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-full flex items-center justify-center ml-3 flex-shrink-0">
                  <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          ))}
          
          {isTyping && (
            <div className="flex mb-6 justify-start">
              <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-teal-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="bg-white border border-teal-100 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white/80 backdrop-blur-sm border-t border-teal-100 p-4 fixed bottom-0 left-0 right-0">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSendMessage} className="flex items-end gap-2">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a command... (e.g., 'Add task: Complete project proposal')"
                disabled={isLoading}
                rows="1"
                className="w-full px-4 py-3 pr-12 bg-white border border-teal-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none max-h-32"
              />
              <button
                type="button"
                className="absolute right-3 bottom-3 text-gray-400 hover:text-teal-600"
                onClick={() => document.getElementById('file-upload').click()}
                disabled={isLoading}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
              </button>
            </div>
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="px-5 py-3 bg-gradient-to-br from-teal-500 to-teal-600 text-white rounded-2xl hover:from-teal-600 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 disabled:opacity-50 transition-all shadow-md hover:shadow-lg"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              </svg>
            </button>
          </form>
          
          {/* Hidden file input */}
          <input
            id="file-upload"
            type="file"
            onChange={(e) => {
              if (e.target.files && e.target.files.length > 0) {
                // Handle file attachment
                console.log('File attached:', e.target.files[0].name);
              }
            }}
            style={{ display: 'none' }}
            accept="image/*,.pdf,.doc,.docx,.txt"
          />
        </div>
      </div>
    </div>
  );
}