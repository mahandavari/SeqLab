import {defineConfig} from '@playwright/test'
export default defineConfig({testDir:'./e2e',workers:1,timeout:45000,use:{baseURL:'http://127.0.0.1:8765',headless:true,viewport:{width:1512,height:1100},launchOptions:{channel:'msedge'}},outputDir:'../artifacts/browser-tests',reporter:[['list'],['json',{outputFile:'../artifacts/e2e-results.json'}]]})
