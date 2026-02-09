import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { isAuthenticated, getAuth, getCurrentUser } from '../lib/auth';

// Add global styles for animations
const ChatStyles = () => (
  <style jsx global>{`
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Scrollbar styling */
    div::-webkit-scrollbar {
      width: 6px;
    }

    div::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 10px;
    }

    div::-webkit-scrollbar-thumb {
      background: #c5c5c5;
      border-radius: 10px;
    }

    div::-webkit-scrollbar-thumb:hover {
      background: #a8a8a8;
    }
  `}</style>
);

export default function ChatPage() {
  const [user, setUser] = useState(null);
  const [isPending, setIsPending] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const router = useRouter();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  // Check and set dark mode preference
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode) {
      const isDark = JSON.parse(savedDarkMode);
      setDarkMode(isDark);
      if (isDark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }
  }, []);

  useEffect(() => {
    // Check authentication status
    if (!isAuthenticated()) {
      router.push('/login');
    } else {
      const currentUser = getCurrentUser();
      setUser(currentUser);
      setIsPending(false);
    }
  }, [router]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), role: 'user', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const token = localStorage.getItem('access_token');

      // Ensure we have both token and user_id before making the API call
      if (!token || !user?.user_id) {
        throw new Error('Authentication required');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'}/${encodeURIComponent(user.user_id)}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: inputValue,
        }),
      });

      const data = await response.json();
      console.log('Response:', data);

      if (response.ok) {
        setConversationId(data.conversation_id);
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.response,
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Handle different error types
        const errorMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.message || 'Sorry, I encountered an error. Please try again.',
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Chat API error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: error.message || 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (isPending) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!user) {
    return <div className="flex justify-center items-center h-screen">Redirecting to login...</div>;
  }

  return (
    <>
      <ChatStyles />
      <div className={`min-h-screen flex flex-col transition-all duration-500 ${
        darkMode
          ? 'bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900'
          : 'bg-gradient-to-br from-blue-50 via-purple-50/50 to-emerald-50'
      }`}>
        {/* Subtle particle background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]"></div>
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>

        <div className="relative z-10 flex flex-col min-h-screen pt-16"> {/* Add padding for fixed navbar */}
          {/* Main Content */}
          <div className="flex-1 flex items-center justify-center p-4">
            <div className={`w-full max-w-3xl rounded-xl overflow-hidden flex flex-col h-[70vh] backdrop-blur-lg border ${
              darkMode
                ? 'bg-white/10 border-white/20'
                : 'bg-white rounded-xl shadow-lg border-slate-200'
            }`}>
              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-4 max-h-[70vh]">
                {messages.map((message, index) => (
                  <div
                    key={`${message.id}-${index}`}
                    className={`flex mb-3 transition-all duration-300 ease-out transform ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className="mr-2 mt-1 flex-shrink-0">
                        <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
                          darkMode ? 'bg-blue-500' : 'bg-blue-500'
                        }`}>
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 005 10a6 6 0 0012 0c0-.35-.036-.687-.101-1.016A5 5 0 0010 11z" clipRule="evenodd" />
                          </svg>
                        </div>
                      </div>
                    )}
                    <div
                      className={`text-sm px-3 py-2 rounded-lg max-w-[80%] transition-all duration-200 ease-out transform ${
                        message.role === 'user'
                          ? `${darkMode ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-br-none hover:from-purple-600 hover:to-blue-600 cursor-pointer' : 'bg-blue-500 text-white rounded-br-none hover:bg-blue-600 cursor-pointer'}`
                          : `${darkMode ? 'bg-white/20 text-white rounded-bl-none' : 'bg-gray-100 text-gray-800 rounded-bl-none'}`
                      }`}
                      style={{ animation: 'fadeInUp 0.3s ease-out forwards' }}
                    >
                      {message.content}
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex justify-start mb-3">
                    <div className="mr-2 mt-1 flex-shrink-0">
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
                        darkMode ? 'bg-blue-500' : 'bg-blue-500'
                      }`}>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 005 10a6 6 0 0012 0c0-.35-.036-.687-.101-1.016A5 5 0 0010 11z" clipRule="evenodd" />
                        </svg>
                      </div>
                    </div>
                    <div className={`text-sm px-3 py-2 rounded-lg ${
                      darkMode ? 'bg-white/20 text-white rounded-bl-none' : 'bg-gray-100 text-gray-800 rounded-bl-none'
                    }`}>
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-100"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area - Sticky at bottom */}
              <div className={`p-3 backdrop-blur-lg border-t ${
                darkMode
                  ? 'bg-white/10 border-white/20'
                  : 'bg-gray-50 border-slate-200'
              }`}>
                <div className="flex items-center space-x-2">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your command... (e.g., 'Add buy groceries', 'Show my tasks')"
                    className={`flex-1 rounded-full px-4 py-2 focus:outline-none resize-none text-sm ${
                      darkMode
                        ? 'bg-white/10 border border-white/20 text-white placeholder-slate-400 focus:ring-2 focus:ring-purple-500'
                        : 'border border-gray-300 focus:ring-2 focus:ring-blue-500'
                    }`}
                    rows="1"
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={isLoading || !inputValue.trim()}
                    className={`px-4 py-2 rounded-full text-sm disabled:opacity-50 disabled:cursor-not-allowed ${
                      darkMode
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600'
                        : 'bg-blue-500 hover:bg-blue-600 text-white'
                    }`}
                  >
                    Send
                  </button>
                </div>
                <div className={`mt-2 text-xs text-center ${
                  darkMode ? 'text-slate-400' : 'text-gray-500'
                }`}>
                  Examples: "Add buy groceries", "Show my tasks", "Mark task 1 as done", "Delete task 2"
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}