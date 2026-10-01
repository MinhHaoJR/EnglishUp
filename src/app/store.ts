import { create } from 'zustand';
import { defaults, db, type Settings } from '../services/storage';
import type { Level } from '../data/schema';
type State={settings:Settings;ready:boolean;error:string;level:Level|'all';topic:string;refresh:number;load:()=>Promise<void>;update:(patch:Partial<Settings>)=>Promise<void>;filter:(level:Level|'all',topic:string)=>void;bump:()=>void;};
export const useApp=create<State>((set,get)=>({settings:defaults,ready:false,error:'',level:'all',topic:'all',refresh:0,load:async()=>{try {set({settings:(await db.settings.get('main'))??defaults,ready:true,error:''});}catch{set({ready:true,error:'Không thể mở bộ nhớ / Storage unavailable. Enable browser storage and reload.'});}},update:async(patch)=>{const settings={...get().settings,...patch};await db.settings.put(settings);set({settings});},filter:(level,topic)=>set({level,topic}),bump:()=>set(s=>({refresh:s.refresh+1}))}));
