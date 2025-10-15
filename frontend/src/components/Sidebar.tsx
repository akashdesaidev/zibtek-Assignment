import { useEffect } from "react";
import { useChatStore } from "@/lib/store";
import {
  getConversations,
  deleteConversation,
  getConversationHistory,
} from "@/lib/api";
import { MessageSquarePlus, Trash2, MessageSquare } from "lucide-react";

interface SidebarProps {
  onNewChat: () => void;
  onSelectConversation: (id: string) => void;
}

export default function Sidebar({
  onNewChat,
  onSelectConversation,
}: SidebarProps) {
  const conversations = useChatStore((state) => state.conversations);
  const setConversations = useChatStore((state) => state.setConversations);
  const currentConversationId = useChatStore(
    (state) => state.currentConversationId
  );

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const convs = await getConversations();
      setConversations(convs);
    } catch (error) {
      console.error("Failed to load conversations:", error);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm("Are you sure you want to delete this conversation?")) {
      try {
        await deleteConversation(id);
        await loadConversations();
        if (currentConversationId === id) {
          onNewChat();
        }
      } catch (error) {
        console.error("Failed to delete conversation:", error);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return "Today";
    if (diffDays === 2) return "Yesterday";
    if (diffDays <= 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-screen">
      <div className="p-4">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          <MessageSquarePlus className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2">
        <div className="text-xs font-semibold text-gray-400 px-3 py-2">
          Recent Conversations
        </div>
        {conversations.length === 0 ? (
          <div className="text-sm text-gray-500 px-3 py-4">
            No conversations yet
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => onSelectConversation(conv.id)}
              className={`group px-3 py-2 mb-1 rounded-lg cursor-pointer transition-colors flex items-center justify-between ${
                currentConversationId === conv.id
                  ? "bg-gray-800"
                  : "hover:bg-gray-800"
              }`}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 flex-shrink-0 text-gray-400" />
                  <div className="text-sm truncate">{conv.title}</div>
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {formatDate(conv.updated_at)}
                </div>
              </div>
              <button
                onClick={(e) => handleDelete(conv.id, e)}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-700 rounded transition-opacity"
              >
                <Trash2 className="w-4 h-4 text-red-400" />
              </button>
            </div>
          ))
        )}
      </div>

      <div className="p-4 border-t border-gray-800">
        <div className="text-xs text-gray-500">Zibtek AI Chatbot v1.0</div>
      </div>
    </div>
  );
}

