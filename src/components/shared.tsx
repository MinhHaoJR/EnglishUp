import { useEffect, useState } from 'react';
import { liveQuery } from 'dexie';
import { useApp } from '../app/store';
import { useT, topics, topicVi } from '../i18n';
import type { Level } from '../data/schema';
export function useLive<T>(query:()=>Promise<T>,deps:unknown[]=[]){const [value,setValue]=useState<T>();const [error,setError]=useState('');useEffect(()=>{const sub=liveQuery(query).subscribe({next:setValue,error:()=>setError('Không thể đọc dữ liệu / Cannot read data')});return()=>sub.unsubscribe(); // query is intentionally driven by explicit dependencies
// eslint-disable-next-line react-hooks/exhaustive-deps
},deps);return {value,error};}
export function Filters(){const t=useT();const {level,topic,filter,settings}=useApp();return <div className="filters"><label>{t('level')}<select value={level} onChange={e=>filter(e.target.value as Level|'all',topic)}><option value="all">{t('allLevels')}</option>{['A1','A2','B1','B2','C1'].map(x=><option key={x}>{x}</option>)}</select></label><label>{t('topic')}<select value={topic} onChange={e=>filter(level,e.target.value)}><option value="all">{t('allTopics')}</option>{topics.map(x=><option key={x} value={x}>{settings.language==='vi'?topicVi[x]:x}</option>)}</select></label></div>}
export function useFiltered<T extends {level:string;topic:string}>(items:T[]){const {level,topic}=useApp();return items.filter(x=>(level==='all'||x.level===level)&&(topic==='all'||x.topic===topic));}
export function PageTitle({eyebrow,title,description,children}:{eyebrow?:string;title:string;description?:string;children?:React.ReactNode}){return <header className="page-title"><div>{eyebrow&&<p className="eyebrow">{eyebrow}</p>}<h1>{title}</h1>{description&&<p className="muted">{description}</p>}</div>{children}</header>}
export function Empty(){const t=useT();const filter=useApp(s=>s.filter);return <div className="panel empty"><span aria-hidden="true">◇</span><p>{t('empty')}</p><button onClick={()=>filter('all','all')}>{t('clearFilters')}</button></div>}
export function Notice({children,error=false}:{children:React.ReactNode;error?:boolean}){return <p role={error?'alert':'status'} className={error?'notice error':'notice'}>{children}</p>}
export function useTimer(active=true){const [start]=useState(Date.now);const [seconds,setSeconds]=useState(0);useEffect(()=>{if(!active)return;const id=setInterval(()=>setSeconds(Math.floor((Date.now()-start)/1000)),1000);return()=>clearInterval(id);},[active,start]);return {start,seconds};}
