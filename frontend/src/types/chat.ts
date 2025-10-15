export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  sources?: string[];
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationWithMessages extends Conversation {
  messages: Message[];
}

export interface ChatResponse {
  message: string;
  sources: string[];
  conversation_id: string;
}

export interface MessageRequest {
  conversation_id: string;
  message: string;
}

