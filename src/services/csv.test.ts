import { exportCSV,importCSV,parseCSV } from './csv';
import { vocabulary } from '../data/content';
test('CSV round trip preserves Unicode, commas, quotes and newlines',()=>{const word={...vocabulary[0],meaning:'nghĩa, "đẹp"\nhai dòng'};const imported=importCSV(exportCSV([word]))[0];expect(imported.meaning).toBe(word.meaning);expect(imported.examples).toEqual(word.examples);expect(imported.custom).toBe(true);});
test('CSV rejects broken rows and escapes spreadsheet formulas',()=>{expect(()=>parseCSV('"abc')).toThrow();expect(()=>importCSV('word\na')).toThrow();expect(exportCSV([{...vocabulary[0],word:'=1+1'}])).toContain("'=1+1");});
