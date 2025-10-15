import { create } from "zustand";
import { Message, Conversation } from "@/types/chat";

interface ChatStore {
  currentConversationId: string | null;
  messages: Message[];
  conversations: Conversation[];
  isLoading: boolean;

  setCurrentConversation: (id: string) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  setConversations: (conversations: Conversation[]) => void;
  setIsLoading: (isLoading: boolean) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  currentConversationId: null,
  messages: [],
  conversations: [],
  isLoading: false,

  setCurrentConversation: (id) => set({ currentConversationId: id }),
  setMessages: (messages) => set({ messages }),
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setConversations: (conversations) => set({ conversations }),
  setIsLoading: (isLoading) => set({ isLoading }),
  clearMessages: () => set({ messages: [] }),
}));

