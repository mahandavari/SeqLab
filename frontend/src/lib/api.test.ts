import { describe,it,expect } from 'vitest'
import {fmt,typeSuggestion} from './api'
describe('scientific presentation',()=>{
 it('does not replace undefined scientific ratios with zero',()=>{expect(fmt(null)).toBe('—');expect(fmt(0)).toBe('0');expect(fmt(200/9)).toBe('22.22')})
 it('keeps alphabet ambiguity explicit',()=>{expect(typeSuggestion('>id\nACGT')).toContain('cannot exclude a protein');expect(typeSuggestion('AUG')).toContain('RNA')})
})
