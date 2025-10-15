import { Message as MessageType } from "@/types/chat";
import { Bot, User } from "lucide-react";

interface MessageProps {
  message: MessageType;
}

export default function Message({ message }: MessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 p-4 ${isUser ? "bg-gray-50" : "bg-white"}`}>
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-primary-600" : "bg-gray-700"
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>
      <div className="flex-1">
        <div className="font-semibold text-sm mb-1">
          {isUser ? "You" : "Zibtek AI"}
        </div>
        <div className="text-gray-800 whitespace-pre-wrap">
          {message.content}
        </div>
      </div>
    </div>
  );
}

