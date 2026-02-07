import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '@/contexts/AuthContext';
import { authService } from '@/services/auth';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
  Avatar,
  ConversationHeader,
  MessageSeparator,
  MessageGroup
} from '@chatscope/chat-ui-kit-react';

// Loading state component
const LoadingState = () => (
  <div className="flex-1 flex items-center justify-center bg-gradient-to-br from-cyan-50 via-teal-50 to-white">
    <div className="text-center animate-fadeIn">
      <div className="loading-spinner mx-auto mb-4"></div>
      <p className="text-gray-500">Loading chat...</p>
    </div>
  </div>
);

export default function Chat() {
  // Auth and routing
  const { user, isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [conversationId, setConversationId] = useState(null);

  // Chat state
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Tasks state
  const [tasks, setTasks] = useState([]);
  const [isLoadingTasks, setIsLoadingTasks] = useState(false);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Fetch tasks for the user
  const fetchTasks = async () => {
    if (!user) return;

    setIsLoadingTasks(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/${user.id}/tasks`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authService.getAccessToken()}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const tasksData = await response.json();
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
      setTasks([]);
    } finally {
      setIsLoadingTasks(false);
    }
  };

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

      // Transform backend format to ChatUI Kit format
      const formattedMessages = data.messages.map(msg => ({
        id: msg.id,
        message: msg.content,
        sentTime: msg.created_at,
        sender: msg.role === 'user' ? 'You' : 'TaskFlow AI',
        direction: msg.role === 'user' ? 'outgoing' : 'incoming',
        position: 'single'
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
        message: "Hello! I'm your TaskFlow AI Assistant. I can help you create, manage, and organize your tasks using natural language. Try typing 'Add a new task', 'Update task 1 to high priority', or 'Delete task 5'!",
        sentTime: new Date().toISOString(),
        sender: 'TaskFlow AI',
        direction: 'incoming',
        position: 'single'
      }]);
    }
  }, [user]);

  // Fetch tasks when user changes
  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  // Save conversation ID to localStorage when it changes
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem('taskflow_current_conversation', conversationId.toString());
    }
  }, [conversationId]);

  // Show loading while auth initializes
  if (loading) {
    return <LoadingState />;
  }

  if (!user) {
    return null; // Will redirect to login
  }

  // Handle back button - clear conversation and show welcome
  const handleBackToConversations = () => {
    localStorage.removeItem('taskflow_current_conversation');
    setConversationId(null);
    setMessages([{
      id: 'welcome-message',
      message: "Hello! I'm your TaskFlow AI Assistant. I can help you create, manage, and organize your tasks using natural language. Try typing 'Add a new task', 'Update task 1 to high priority', or 'Delete task 5'!",
      sentTime: new Date().toISOString(),
      sender: 'TaskFlow AI',
      direction: 'incoming',
      position: 'single'
    }]);
  };

  // Handle send message
  const handleSend = async (message) => {
    if (!message.trim() || isLoading) return;

    const currentInput = typeof message === 'string' ? message : message.trim();

    // Add user message to UI immediately
    const userMessage = {
      id: `user-${Date.now()}`, // Add unique ID for user messages
      message: currentInput,
      sentTime: new Date().toISOString(),
      sender: 'You',
      direction: 'outgoing',
      position: 'single'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await callBackendAPI(currentInput, tasks);

      // Add AI response to UI
      const aiMessage = {
        id: response.metadata?.message_id,
        message: response.response,
        sentTime: new Date().toISOString(),
        sender: 'TaskFlow AI',
        direction: 'incoming',
        position: 'single',
        metadata: response.metadata,
        tasksAffected: response.tasks_affected || [],
      };

      setMessages(prev => [...prev, aiMessage]);

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Fetch updated tasks if any tasks were affected
      if (response.tasks_affected && response.tasks_affected.length > 0) {
        await fetchTasks(); // Fetch updated tasks after changes
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
        message: errorMessageText,
        sentTime: new Date().toISOString(),
        sender: 'System',
        direction: 'incoming',
        position: 'single',
        type: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const callBackendAPI = async (message, currentTasks) => {
    // Format tasks into a readable string for the AI
    const tasksContext = currentTasks.length > 0
      ? `Current tasks:\n${currentTasks.map(task =>
          `- ID: ${task.id}, Title: "${task.title}", Description: "${task.description || 'No description'}", ` +
          `Status: ${task.completed ? 'Completed' : 'Pending'}, Priority: ${task.priority}, ` +
          `Due: ${task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date'}`
        ).join('\n')}`
      : 'No tasks available.';

    // Create a comprehensive message that includes the user's query and the current tasks context
    const fullMessage = `${tasksContext}\n\nUser query: ${message}`;

    const response = await fetch(`${API_BASE_URL}/api/${user.id}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authService.getAccessToken()}`,
      },
      body: JSON.stringify({
        message: fullMessage,
        modality: 'text',
        conversation_id: conversationId,
        metadata: {
          original_message: message, // Keep the original message for reference
          tasks: currentTasks // Include current tasks in the request
        }
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-black via-[#1a1a1a] to-[#330033] relative">
      <Head>
        <title>Chat - TaskFlow</title>
        <meta name="description" content="TaskFlow AI Assistant" />
      </Head>

      {/* Background Decorative Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-20 z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-gradient-to-br from-[#000000] to-[#C459E0] rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-gradient-to-br from-[#C459E0] to-[#000000] rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="flex flex-col h-full relative z-10">
        <MainContainer className="flex-1 border-none shadow-none">
          <ChatContainer className="px-2 md:px-4 flex flex-col h-full">
            <ConversationHeader className="bg-black/80 backdrop-blur-sm border-b border-[#C459E0] py-3 z-30 sticky top-0 shadow-sm">
              <ConversationHeader.Back onClick={handleBackToConversations} className="hover:text-[#C459E0] transition-colors mr-2" />
              <Avatar
                src="https://ui-avatars.com/api/?name=TF&background=C459E0&color=fff&bold=true"
                name="TaskFlow AI"
                className="ring-1 ring-[#C459E0]/30"
              />
              <ConversationHeader.Content
                userName={<span className="font-bold text-white tracking-tight text-lg">TaskFlow AI Assistant</span>}
                info={
                  <div className="flex items-center space-x-2.5 mt-1">
                    <div className="relative flex h-2 w-2">
                      <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isLoading ? 'bg-amber-400' : 'bg-emerald-400'}`}></span>
                      <span className={`relative inline-flex rounded-full h-2 w-2 ${isLoading ? 'bg-amber-500 shadow-[0_0_8px_#fbbf24]' : 'bg-emerald-500 shadow-[0_0_8px_#10b981]'}`}></span>
                    </div>
                    <span className={`text-[10px] font-medium uppercase tracking-[0.2em] ${isLoading ? 'text-amber-400' : 'text-emerald-400'}`}>
                      {isLoading ? "Thinking..." : "Online"}
                    </span>
                  </div>
                }
              />
            </ConversationHeader>

            <MessageList
              className="flex-1 mt-2 mb-2"
              typingIndicator={isLoading && (
                <TypingIndicator
                  content="Thinking..."
                  className="text-white bg-black/80 backdrop-blur-md rounded-2xl px-4 py-2 border border-[#C459E0] shadow-sm"
                />
              )}
            >
              {(() => {
                const grouped = [];
                let currentGroup = null;

                messages.forEach((msg, index) => {
                  // Add date separator if needed
                  if (index === 0 || new Date(messages[index - 1].sentTime).toDateString() !== new Date(msg.sentTime).toDateString()) {
                    if (currentGroup) {
                      grouped.push({ type: 'group', ...currentGroup });
                      currentGroup = null;
                    }
                    grouped.push({ type: 'separator', date: new Date(msg.sentTime).toLocaleDateString() });
                  }

                  // Group consecutive messages from same sender
                  if (currentGroup && currentGroup.sender === msg.sender) {
                    currentGroup.messages.push(msg);
                  } else {
                    if (currentGroup) {
                      grouped.push({ type: 'group', ...currentGroup });
                    }
                    currentGroup = {
                      sender: msg.sender,
                      direction: msg.direction,
                      messages: [msg]
                    };
                  }
                });

                if (currentGroup) {
                  grouped.push({ type: 'group', ...currentGroup });
                }

                return grouped.map((item, index) => {
                  if (item.type === 'separator') {
                    return (
                      <MessageSeparator
                        key={`sep-${index}`}
                        className="text-white"
                        content={item.date}
                      />
                    );
                  }

                  return (
                    <MessageGroup
                      key={`group-${index}`}
                      direction={item.direction}
                      className="bg-transparent"
                    >
                      <MessageGroup.Messages>
                        {item.messages.map((msg, msgIndex) => {
                          const isLastInGroup = msgIndex === item.messages.length - 1;
                          const isFirstInGroup = msgIndex === 0;

                          return (
                            <Message
                              key={msg.id || `msg-${index}-${msgIndex}`}
                              model={{
                                message: msg.message,
                                sentTime: new Date(msg.sentTime).toLocaleTimeString(),
                                sender: msg.sender,
                                direction: msg.direction,
                                position: isFirstInGroup && isLastInGroup ? 'single' :
                                         isFirstInGroup ? 'first' :
                                         isLastInGroup ? 'last' : 'normal'
                              }}
                              className={`${
                                item.direction === 'incoming'
                                  ? 'bg-black/80 backdrop-blur-sm border border-[#C459E0] rounded-2xl shadow-sm'
                                  : 'bg-gradient-to-br from-[#C459E0] to-[#9c27b0] text-white rounded-2xl rounded-tr-none'
                              } mb-3`}
                            >
                              {isFirstInGroup && item.direction === 'incoming' && (
                                <Avatar
                                  src={msg.sender === 'System'
                                    ? "https://ui-avatars.com/api/?name=S&background=ef4444&color=fff"
                                    : "https://ui-avatars.com/api/?name=TF&background=C459E0&color=fff"
                                  }
                                  name={msg.sender}
                                  className="ring-1 ring-[#C459E0]/20"
                                />
                              )}
                              {isFirstInGroup && (
                                <Message.Header
                                  sender={msg.sender}
                                  sentTime={new Date(msg.sentTime).toLocaleTimeString()}
                                  className={`${item.direction === 'incoming' ? 'text-white' : 'text-white'}`}
                                />
                              )}
                            </Message>
                          );
                        })}
                      </MessageGroup.Messages>
                    </MessageGroup>
                  );
                });
              })()}
            </MessageList>

            {/* ChatUI Kit Message Input */}
            <MessageInput
              placeholder="Type a command... (e.g., 'Update task 1 to completed')"
              onSend={handleSend}
              disabled={isLoading}
              attachButton={false}
            />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
}