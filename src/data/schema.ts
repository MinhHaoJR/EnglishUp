import { z } from 'zod';
export const levelSchema = z.enum(['A1','A2','B1','B2','C1']);
export const skillSchema = z.enum(['vocabulary','listening','speaking','reading','writing']);
export const wordSchema = z.object({id:z.string().min(1),word:z.string().min(1),ipa:z.string(),pos:z.string().min(1),meaning:z.string().min(1),definition:z.string().min(1),examples:z.array(z.string()).min(1).max(2),level:levelSchema,topic:z.string().min(1),custom:z.boolean().optional()});
export type Word = z.infer<typeof wordSchema>;
export type Skill = z.infer<typeof skillSchema>;
export type Level = z.infer<typeof levelSchema>;
