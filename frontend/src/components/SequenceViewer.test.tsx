import {render,screen,fireEvent,cleanup} from '@testing-library/react'
import {afterEach,it,expect,vi} from 'vitest'
import SequenceViewer from './SequenceViewer'
import type {Sequence} from '../lib/types'
afterEach(cleanup)
it('paginates a large sequence and disables invalid region extraction',()=>{
 const s={id:'x',identifier:'test',description:'test',sequence:'A'.repeat(1201),kind:'DNA'} as Sequence
 const extract=vi.fn()
 const {container}=render(<SequenceViewer sequence={s} region={[5,2]} onRegion={()=>{}} onExtract={extract}/>)
 expect(container.querySelectorAll('.base').length).toBe(600)
 expect((screen.getByRole('button',{name:'Extract copy'}) as HTMLButtonElement).disabled).toBe(true)
 fireEvent.click(screen.getByRole('button',{name:'Next sequence page'}))
 expect(screen.getByText('601–1200 of 1,201 nt')).toBeTruthy()
})
