export async function api<T>(path:string, method='GET', body?:unknown):Promise<T> {
  const response = await fetch('/api'+path,{method,headers:body !== undefined?{'Content-Type':'application/json'}:undefined,body:body !== undefined?JSON.stringify(body):undefined})
  if(!response.ok) { const data = await response.json().catch(()=>({detail:'Server unavailable'})); throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail)) }
  return response.json()
}
export function downloadText(text:string,name:string,type='text/plain') {
  const url=URL.createObjectURL(new Blob([text],{type})); const a=document.createElement('a'); a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)
}
export function fmt(value:number|null|undefined,digits=2){return value == null?'—':value.toLocaleString('en-US',{maximumFractionDigits:digits})}
export function typeSuggestion(text:string):string {
  const symbols = text.split(/\r?\n/).filter(line=>!line.startsWith('>')).join('').replace(/\s/g,'').toUpperCase()
  if (!symbols) return 'Select the molecule type before importing.'
  if (/^[ACGTRYSWKMBDHVN]+$/.test(symbols)) return 'Compatible with DNA; alphabet alone cannot exclude a protein. Confirm the type.'
  if (/^[ACGURYSWKMBDHVN]+$/.test(symbols)) return 'Compatible with RNA; confirm the type.'
  return 'May be protein or invalid nucleotide input. Confirm the type.'
}
