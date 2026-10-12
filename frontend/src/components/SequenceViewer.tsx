import { useState } from 'react'
import { ChevronLeft,ChevronRight,Download,Scissors } from 'lucide-react'
import { downloadText } from '../lib/api'
import type { Sequence } from '../lib/types'
export default function SequenceViewer({sequence,region,onRegion,onExtract}:{sequence:Sequence;region:[number,number];onRegion:(region:[number,number])=>void;onExtract:()=>void}) {
 const [page,setPage]=useState(0);const chunk=600,n=sequence.sequence.length,offset=Math.min(page*chunk,Math.floor((n-1)/chunk)*chunk)
 const lines=sequence.sequence.slice(offset,offset+chunk).match(/.{1,60}/g)||[]
 const valid=region[0]>=1&&region[1]>=region[0]&&region[1]<=n
 return <section className="card sequence-card"><div className="section-heading"><div><h3>Sequence viewer <span className="tag">{sequence.kind}</span></h3><p className="hint">Click a symbol to select a position. Coordinates are 1-based, inclusive.</p></div><a className="button small" href={'/api/sequences/'+sequence.id+'/fasta'}><Download size={14}/> FASTA</a></div>
 <div className="sequence-ruler"><span>POSITION</span><span>01　　　 10　　　 20　　　 30　　　 40　　　 50　　 60</span></div>
 <div className="sequence-lines">{lines.map((line,i)=><div className="sequence-line" key={i}><span className="position">{offset+i*60+1}</span><code>{[...line].map((char,j)=>{const pos=offset+i*60+j+1;return <span key={j} title={char+' · '+pos} onClick={()=>onRegion([pos,pos])} className={'base base-'+char+((pos>=region[0]&&pos<=region[1])?' selected':'')}>{char}</span>})}</code></div>)}</div>
 <div className="viewer-footer"><span className="hint">{offset+1}–{Math.min(offset+chunk,n)} of {n.toLocaleString()} {sequence.kind==='Protein'?'aa':'nt'}</span><div className="row"><button className="icon-button" aria-label="Previous sequence page" disabled={offset===0} onClick={()=>setPage(Math.max(0,page-1))}><ChevronLeft size={16}/></button><button className="icon-button" aria-label="Next sequence page" disabled={offset+chunk>=n} onClick={()=>setPage(page+1)}><ChevronRight size={16}/></button></div></div>
 <div className="region-controls"><label>Region start<input type="number" min={1} max={n} value={region[0]} onChange={e=>onRegion([Number(e.target.value),region[1]])}/></label><label>Region end<input type="number" min={1} max={n} value={region[1]} onChange={e=>onRegion([region[0],Number(e.target.value)])}/></label><button disabled={!valid} onClick={onExtract}><Scissors size={14}/> Extract copy</button><button disabled={!valid} onClick={()=>downloadText('>'+sequence.identifier+':'+region.join('-')+'\n'+sequence.sequence.slice(region[0]-1,region[1])+'\n','region.fasta')}><Download size={14}/> Region</button></div>
 </section>
}
