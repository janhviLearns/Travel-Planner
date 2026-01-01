import { ChatRequest, ChatResponse } from './types';

const API_BASE_URL = import.meta.env.PROD ? '' : 'http://localhost:8000';

export const sendChatMessage = async (query: string): Promise<ChatResponse> => {
  console.log('[API] Sending chat message:', query);
  console.log('[API] API endpoint:', `${API_BASE_URL}/chat`);
  
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query } as ChatRequest),
    });

    console.log('[API] Response status:', response.status, response.statusText);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[API] Error response:', errorText);
      throw new Error(`Failed to send message: ${response.status}`);
    }

    const data = await response.json();
    console.log('[API] Response data:', data);
    console.log('[API] Response.response length:', data.response?.length || 0);
    
    return data;
  } catch (error) {
    console.error('[API] Error in sendChatMessage:', error);
    throw error;
  }
};

