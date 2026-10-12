import { useRef,useState } from 'react'
import { Upload, X, FileCode2 } from 'lucide-react'
import { typeSuggestion } from '../lib/api'
import type { Kind } from '../lib/types'
export default function ImportDialog({onClose,onImport}:{onClose:()=>void;onImport:(text:string,kind:Kind,normalize:boolean,name:string)=>Promise<void>}) {
 const [text,setText]=useState(''),[kind,setKind]=useState<Kind|''>(''),[normalize,setNormalize]=useState(true),[name,setName]=useState('sequence'),[busy,setBusy]=useState(false),[error,setError]=useState('')
 const file=useRef<HTMLInputElement>(null)
 async function load(f?:File){if(!f)return;if(f.size>1_000_000){setError('Import files up to 1 MB.');return}if(!/\.(fa|fasta|fna|ffn|faa|frn|txt)$/i.test(f.name)){setError('Choose a FASTA or plain text file.');return}setText(await f.text());setName(f.name.replace(/\.[^.]+$/,''));setError('')}
 async function submit(){if(!kind){setError('Choose DNA, RNA, or Protein.');return}setBusy(true);setError('');try{await onImport(text,kind,normalize,name);onClose()}catch(e){setError((e as Error).message)}finally{setBusy(false)}}
 return <div className="overlay" onKeyDown={e=>{if(e.key==='Escape'&&!busy)onClose()}}><section role="dialog" aria-modal="true" aria-labelledby="import-title" className="dialog">
 <div className="section-heading"><div><p className="eyebrow">BRING YOUR DATA</p><h2 id="import-title">Import sequences</h2></div><button aria-label="Close import" className="icon-button" onClick={onClose} disabled={busy}><X size={20}/></button></div>
 <p className="muted">Paste raw sequence or multi-record FASTA. Original input is preserved.</p>
 <div className="dropzone" onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault();void load(e.dataTransfer.files[0])}}><FileCode2 size={24}/><span>Drop a FASTA file here</span><button onClick={()=>file.current?.click()}>Browse files</button><input ref={file} type="file" hidden accept=".fa,.fasta,.fna,.ffn,.faa,.frn,.txt" onChange={e=>void load(e.target.files?.[0])}/></div>
 <label>Record name <input value={name} onChange={e=>setName(e.target.value)} maxLength={120}/></label>
 <label>Sequence or FASTA <textarea autoFocus value={text} onChange={e=>setText(e.target.value)} placeholder={'>my_sequence\nATGAAATGA'} rows={7} spellCheck={false}/></label>
 <p className="hint">{typeSuggestion(text)}</p><label>Molecule type <select value={kind} onChange={e=>setKind(e.target.value as Kind)}><option value="">Select explicitly…</option><option>DNA</option><option>RNA</option><option>Protein</option></select></label>
 <label className="check-label"><input type="checkbox" checked={normalize} onChange={e=>setNormalize(e.target.checked)}/> Normalize lowercase to uppercase and remove whitespace</label>
 <p className="hint">No bases are replaced. Limits: 100,000 symbols per record, 100 records per import.</p>
 {error&&<p role="alert" className="error">{error}</p>}<div className="dialog-actions"><button onClick={onClose} disabled={busy}>Cancel</button><button className="primary" disabled={busy||!text.trim()||!kind} onClick={()=>void submit()}><Upload size={16}/>{busy?'Importing…':'Import sequences'}</button></div>
 </section></div>
}
