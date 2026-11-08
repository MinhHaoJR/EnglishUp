import { z } from 'zod';
import { fetchJson } from './auth';

const profileSchema = z.object({ displayName: z.string(), showOnLeaderboard: z.boolean() });
export type Profile = z.infer<typeof profileSchema>;

const achievementsSchema = z.array(
  z.object({
    code: z.string(),
    points: z.number().int().nonnegative(),
    // The API omits earnedAt for badges not yet earned.
    earnedAt: z.string().optional(),
  }),
);
export type Achievement = z.infer<typeof achievementsSchema>[number];

export type Period = 'week' | 'all';
const leaderboardSchema = z.object({
  period: z.enum(['week', 'all']),
  entries: z.array(
    z.object({
      rank: z.number().int().positive(),
      displayName: z.string(),
      points: z.number().int().nonnegative(),
      isMe: z.boolean(),
    }),
  ),
  myPoints: z.number().int().nonnegative(),
  myRowShown: z.boolean(),
});
export type Leaderboard = z.infer<typeof leaderboardSchema>;

export const fetchProfile = () => fetchJson(profileSchema, '/api/profile');

export const saveProfile = (profile: Profile) =>
  fetchJson(profileSchema, '/api/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...profile, displayName: profile.displayName.trim() }),
  });

export const fetchAchievements = () => fetchJson(achievementsSchema, '/api/achievements');

export const fetchLeaderboard = (period: Period) =>
  fetchJson(leaderboardSchema, `/api/leaderboard?period=${period}`);
