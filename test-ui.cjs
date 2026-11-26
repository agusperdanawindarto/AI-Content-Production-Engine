// Optional acceptance test; reuses a separately installed Playwright without installing it into C:.
const assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'D:/AI-COMPUTER-CONTROL/node_modules/playwright');
(async()=>{let browser;try{
browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});let errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8899/');await page.locator('.room').nth(9).waitFor();assert.equal(await page.locator('.room').count(),10);
const prev=await page.locator('#job').innerText();await page.locator('#run').click();
await page.waitForFunction(p=>document.querySelector('#job').innerText!==p,prev);
await page.screenshot({path:path.join(__dirname,'workspace','studio-running.png'),fullPage:true});
await page.waitForFunction(()=>document.querySelector('#job').innerText.includes('review'),null,{timeout:120000});
const s=await page.evaluate(()=>fetch('/state').then(r=>r.json()));assert.equal(s.status,'review');assert.equal(s.events.length,20);assert.equal(s.quality.decode_pass,true);assert.equal(s.quality.publication_approved,false);assert.equal(await page.locator('#outputs a').count(),9);
await page.screenshot({path:path.join(__dirname,'workspace','studio-review.png'),fullPage:true});assert.equal(errors.length,0,errors.join('; '));
const api=await page.request.post('http://127.0.0.1:8899/run',{headers:{Origin:'http://127.0.0.1:8899','Content-Type':'application/json'},data:{mode:'api',confirm_cost:false}});assert.equal(api.status(),400);
const bad=await page.request.post('http://127.0.0.1:8899/run',{headers:{Origin:'https://example.invalid','Content-Type':'application/json'},data:{mode:'demo'}});assert.equal(bad.status(),403);
console.log(JSON.stringify({passed:true,job:s.id,agents:10,events:s.events.length,outputLinks:9,quality:s.quality,apiConsentGuard:true,crossOriginGuard:true,uiErrors:errors},null,2));
}catch(e){console.error(e);process.exitCode=1}finally{if(browser)await browser.close()}})();
