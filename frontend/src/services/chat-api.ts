import { ChatRequest, ChatResponse } from '@/types/chat-types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Send a message to the chat endpoint
 */
export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Include authentication token if available
      ...getAuthHeaders(),
    },
    credentials: 'include', // Include cookies in the request
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Get list of conversations for the current user
 */
export const getConversations = async (): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/chat/conversations`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    credentials: 'include', // Include cookies in the request
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Get a specific conversation and its messages
 */
export const getConversation = async (conversationId: string): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/chat/conversations/${conversationId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    credentials: 'include', // Include cookies in the request
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Delete a conversation
 */
export const deleteConversation = async (conversationId: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/chat/conversations/${conversationId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    credentials: 'include', // Include cookies in the request
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
};

/**
 * Get authentication headers if available
 */
const getAuthHeaders = (): Record<string, string> => {
  // For cookie-based auth, we don't need to manually send headers
  // The fetch request will automatically include cookies when credentials: 'include' is set
  return {};
};