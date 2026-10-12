import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'
class Boundary extends React.Component<{children:React.ReactNode},{error:boolean}> {
 state={error:false}
 static getDerivedStateFromError(){return {error:true}}
 render(){return this.state.error?<main className="fatal"><h1>The workspace could not render.</h1><p>Your saved projects remain on this computer.</p><button onClick={()=>location.reload()}>Reload workspace</button></main>:this.props.children}
}
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><Boundary><App/></Boundary></React.StrictMode>)
