import { normalize } from './diff';
export function speakingMetrics(text:string,seconds:number){const words=normalize(text);const fillers=(text.toLowerCase().match(/\b(um|uh|erm|like|you know|i mean)\b/g)??[]).length;return {words:words.length,wpm:seconds>0?Math.round(words.length/(seconds/60)):0,fillers,variety:words.length?Math.round(new Set(words).size/words.length*100):0};}
