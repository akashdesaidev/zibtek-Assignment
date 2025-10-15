"use client";

import { useEffect } from "react";
import { useChatStore } from "@/lib/store";
import {
  sendMessage,
  createConversation,
  getConversationHistory,
  getConversations,
} from "@/lib/api";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import Sidebar from "./Sidebar";

export default function ChatInterface() {
  const {
    currentConversationId,
    setCurrentConversation,
    messages,
    setMessages,
    addMessage,
    setIsLoading,
    clearMessages,
    setConversations,
  } = useChatStore();

  useEffect(() => {
    // Load conversations on mount
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const convs = await getConversations();
      setConversations(convs);

      // If there are existing conversations, load the most recent one
      if (convs.length > 0) {
        const mostRecent = convs[0];
        setCurrentConversation(mostRecent.id);
        const conv = await getConversationHistory(mostRecent.id);
        setMessages(conv.messages);
      } else {
        // Only create new conversation if none exist
        handleNewChat();
      }
    } catch (error) {
      console.error("Failed to load conversations:", error);
      // If loading fails, create a new conversation as fallback
      handleNewChat();
    }
  };

  const handleNewChat = async () => {
    try {
      const newConv = await createConversation();
      setCurrentConversation(newConv.id);
      clearMessages();

      // Refresh conversation list
      const convs = await getConversations();
      setConversations(convs);
    } catch (error) {
      console.error("Failed to create conversation:", error);
    }
  };

  const handleSelectConversation = async (id: string) => {
    try {
      setCurrentConversation(id);
      const conv = await getConversationHistory(id);
      setMessages(conv.messages);
    } catch (error) {
      console.error("Failed to load conversation:", error);
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!currentConversationId) return;

    // Add user message optimistically
    addMessage({
      role: "user",
      content: message,
      timestamp: new Date().toISOString(),
    });

    setIsLoading(true);

    try {
      const response = await sendMessage(currentConversationId, message);

      // Add assistant response with sources
      addMessage({
        role: "assistant",
        content: response.message,
        timestamp: new Date().toISOString(),
        sources: response.sources,
      });

      // Update conversation title if it's the first message
      if (messages.length === 0) {
        // Use first message as title (truncated)
        const title =
          message.length > 50 ? message.substring(0, 50) + "..." : message;
        try {
          await fetch(
            `${
              process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
            }/api/chat/conversations/${currentConversationId}/title`,
            {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ title }),
            }
          );
        } catch (err) {
          console.error("Failed to update title:", err);
        }

        // Refresh conversation list
        const convs = await getConversations();
        setConversations(convs);
      }
    } catch (error) {
      console.error("Failed to send message:", error);
      // Add error message
      addMessage({
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
      />
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-800">
            Zibtek AI Assistant
          </h1>
          <p className="text-sm text-gray-600">Ask me anything about Zibtek</p>
        </header>
        <MessageList />
        <ChatInput
          onSend={handleSendMessage}
          disabled={!currentConversationId}
        />
      </div>
    </div>
  );
}
