import { useEffect, useRef, useState } from 'react'
import type { Data, Layout, PlotlyHTMLElement } from 'plotly.js'
export default function Chart({title,data,dark=false,xLabel='',yLabel='',onRegion}:{title:string;data:Data[];dark?:boolean;xLabel?:string;yLabel?:string;onRegion?:(start:number,end:number)=>void}) {
 const ref=useRef<HTMLDivElement>(null); const [error,setError]=useState('')
 useEffect(()=>{
  let disposed=false; let cleanup=()=>{}
  import('plotly.js-dist-min').then(async module=>{
   if(disposed||!ref.current)return
   const Plotly=module.default||module; const node=ref.current
   const layout:Partial<Layout>={autosize:true,height:285,margin:{l:56,r:20,t:24,b:48},paper_bgcolor:'transparent',plot_bgcolor:'transparent',font:{family:'Segoe UI, sans-serif',color:dark?'#9fb1c5':'#617383',size:11},colorway:['#119a94','#6578d9','#dc9653','#ca6592'],xaxis:{title:{text:xLabel},gridcolor:dark?'#243447':'#edf0f2',zeroline:false},yaxis:{title:{text:yLabel},gridcolor:dark?'#243447':'#edf0f2',zeroline:false},showlegend:data.length>1,legend:{orientation:'h',y:1.16},hovermode:'closest',dragmode:onRegion?'select':'zoom'}
   await Plotly.react(node,data,layout,{responsive:true,displaylogo:false,toImageButtonOptions:{format:'png',filename:title.toLowerCase().replaceAll(' ','-'),scale:2},modeBarButtonsToAdd:[{name:'Download SVG',title:'Download SVG',icon:Plotly.Icons.camera,click:()=>{void Plotly.downloadImage(node,{format:'svg',filename:title.toLowerCase().replaceAll(' ','-'),width:1000,height:420})}}]})
   if(disposed){Plotly.purge(node);return}
   if(onRegion)(node as unknown as PlotlyHTMLElement).on('plotly_selected',(event)=>{const xs=event?.points?.map(p=>Number(p.x))||[];if(xs.length)onRegion(Math.max(1,Math.floor(Math.min(...xs))),Math.ceil(Math.max(...xs)))})
   const resize=new ResizeObserver(()=>{void Plotly.Plots.resize(node)});resize.observe(node)
   cleanup=()=>{resize.disconnect();Plotly.purge(node)}
  }).catch(e=>setError(String(e)))
  return()=>{disposed=true;cleanup()}
 },[data,dark,title,xLabel,yLabel,onRegion])
 return <div className="plot-wrap">{error?<p role="alert">{error}</p>:<div ref={ref} aria-label={title} className="plot"/>}</div>
}
