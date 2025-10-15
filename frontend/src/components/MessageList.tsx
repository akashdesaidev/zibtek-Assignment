import { useEffect, useRef } from "react";
import { useChatStore } from "@/lib/store";
import Message from "./Message";
import { Loader2, Bot } from "lucide-react";

export default function MessageList() {
  const messages = useChatStore((state) => state.messages);
  const isLoading = useChatStore((state) => state.isLoading);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <Bot className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h2 className="text-2xl font-semibold mb-2">Welcome to Zibtek AI</h2>
          <p>Ask me anything about Zibtek!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      {isLoading && (
        <div className="flex gap-3 p-4">
          <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gray-700">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1">
            <div className="font-semibold text-sm mb-1">Zibtek AI</div>
            <div className="flex items-center gap-2 text-gray-600">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
