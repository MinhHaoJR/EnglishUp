import { z } from 'zod';
import { fetchJson, authFetch, ApiError } from './auth';

const citationSchema = z.object({
  n: z.number().int().positive(),
  sourceType: z.string(),
  sourceId: z.string(),
  title: z.string(),
  score: z.number(),
});
export type Citation = z.infer<typeof citationSchema>;

const replySchema = z.object({
  conversationId: z.string().uuid(),
  answer: z.string(),
  citations: z.array(citationSchema),
  questionsLeft: z.number().int().nonnegative(),
});
export type AssistantReply = z.infer<typeof replySchema>;

const conversationsSchema = z.array(
  z.object({ id: z.string().uuid(), title: z.string(), updatedAt: z.string() }),
);
export type ConversationSummary = z.infer<typeof conversationsSchema>[number];

const messagesSchema = z.array(
  z.object({
    role: z.enum(['user', 'assistant']),
    content: z.string(),
    createdAt: z.string(),
    citations: z.array(citationSchema),
  }),
);
export type ChatMessage = z.infer<typeof messagesSchema>[number];

export const MAX_QUESTION_LENGTH = 1000;

/** Rejects with ApiError 429 when today's questions are used up, 503 when the AI quota is. */
export const ask = (question: string, conversationId: string | null) =>
  fetchJson(replySchema, '/api/assistant/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: question.trim(), conversationId }),
  });

export const fetchConversations = () =>
  fetchJson(conversationsSchema, '/api/assistant/conversations');

export const fetchConversation = (id: string) =>
  fetchJson(messagesSchema, `/api/assistant/conversations/${id}`);

export async function deleteConversation(id: string) {
  const response = await authFetch(`/api/assistant/conversations/${id}`, { method: 'DELETE' });
  if (!response.ok) throw new ApiError(response.status);
}

/** Where a cited source can be practised in the app. */
export const sourcePath = (sourceType: string) =>
  ({
    word: '/vocabulary',
    reading: '/reading',
    listening: '/listening',
    writing: '/writing',
    grammar: '/grammar',
    guide: '/',
    roadmap: '/roadmap',
  })[sourceType] ?? '/';
