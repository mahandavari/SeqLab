import { chromium, expect } from '../frontend/node_modules/@playwright/test/index.mjs'
const browser = await chromium.launch({channel:'msedge',headless:true})
try {
 const page=await browser.newPage({viewport:{width:1512,height:1100}})
 await page.goto('http://127.0.0.1:8765')
 await page.getByRole('button',{name:/Analysis History/}).click()
 await page.getByRole('button',{name:'Open',exact:true}).first().click()
 await expect(page.getByText('Analysis saved',{exact:true})).toBeVisible()
 await expect(page.locator('.js-plotly-plot').first().locator('.main-svg').first()).toBeVisible()
 await page.screenshot({path:'artifacts/preview.png',fullPage:true})
 console.log('Restarted production app and saved example results verified; preview saved.')
} finally { await browser.close() }
