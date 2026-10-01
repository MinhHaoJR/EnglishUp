import { vocabulary } from './content';
test('original vocabulary meets quantity, topic and schema requirements',()=>{expect(vocabulary.length).toBeGreaterThanOrEqual(150);expect(new Set(vocabulary.map(w=>w.topic)).size).toBeGreaterThanOrEqual(8);expect(new Set(vocabulary.map(w=>w.word)).size).toBe(vocabulary.length);expect(vocabulary.every(w=>['A2','B1','B2'].includes(w.level))).toBe(true);});
