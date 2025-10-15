import {
  Conversation,
  ConversationWithMessages,
  ChatResponse,
  MessageRequest,
} from "@/types/chat";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendMessage(
  conversationId: string,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message,
    } as MessageRequest),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}

export async function createConversation(
  title: string = "New Chat"
): Promise<Conversation> {
  const response = await fetch(`${API_URL}/api/chat/new`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error("Failed to create conversation");
  }

  return response.json();
}

export async function getConversations(): Promise<Conversation[]> {
  const response = await fetch(`${API_URL}/api/chat/conversations`);

  if (!response.ok) {
    throw new Error("Failed to fetch conversations");
  }

  const data = await response.json();
  return data.conversations;
}

export async function getConversationHistory(
  id: string
): Promise<ConversationWithMessages> {
  const response = await fetch(`${API_URL}/api/chat/conversations/${id}`);

  if (!response.ok) {
    throw new Error("Failed to fetch conversation history");
  }

  return response.json();
}

export async function deleteConversation(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/chat/conversations/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete conversation");
  }
}

