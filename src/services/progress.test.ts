import { getProgress } from './progress';
import type { Attempt } from './storage';
const attempt=(date:string,skill:Attempt['skill']='reading'):Attempt=>({id:date,skill,score:80,duration:120,timestamp:+new Date(date),label:'test'});
test('streak includes yesterday if today has no attempt, and stops at gaps',()=>{const now=+new Date(2026,9,4,12);expect(getProgress([attempt('2026-10-03T09:00:00'),attempt('2026-10-02T09:00:00')],now).streak).toBe(2);expect(getProgress([attempt('2026-10-01T09:00:00')],now).streak).toBe(0);});
test('aggregates today and skill results independent of order',()=>{const now=+new Date(2026,9,4,12);const result=getProgress([attempt('2026-10-04T09:00:00'),attempt('2026-10-04T10:00:00','writing'),attempt('2026-10-03T09:00:00')],now);expect(result.todaySeconds).toBe(240);expect(result.streak).toBe(2);expect(result.perSkill.find(s=>s.skill==='reading')?.count).toBe(2);expect(result.week).toHaveLength(7);});
