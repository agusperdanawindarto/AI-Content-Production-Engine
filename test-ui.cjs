// Real browser test with optional pre-existing Playwright installation.
const assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'D:/AI-COMPUTER-CONTROL/node_modules/playwright');
(async()=>{let browser;try{
browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});let errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:8899/');await page.locator('.floor-avatar').nth(9).waitFor();assert.equal(await page.locator('.room').count(),10);assert.equal(await page.locator('#meeting').count(),1);
const h=await page.request.get('http://127.0.0.1:8899/health');assert.equal((await h.json()).voice_ready,true);
const run=async(mode,manual)=>{
 await page.selectOption('#mode',mode);await page.locator('#trends').setChecked(mode==='demo');
 if(manual)await page.locator('#scenes').fill(JSON.stringify(manual));
 const previous=await page.locator('#job').innerText();await page.locator('#run').click();
 await page.waitForFunction(p=>document.querySelector('#job').innerText!==p,previous);
 await page.waitForFunction(()=>document.querySelector('#job').innerText.includes('review')||document.querySelector('#job').innerText.includes('failed'),null,{timeout:180000});
 const s=await page.evaluate(()=>fetch('/state').then(r=>r.json()));assert.equal(s.status,'review',s.error);assert.equal(s.events.filter(e=>e.status==='handoff').length,10);assert.equal(s.quality.decode_pass,true);assert.equal(s.quality.publication_approved,false);assert.match(s.quality.audio,/Piper Indonesian/);assert.equal(await page.locator('#outputs a').count(),11);
 const t=await page.request.get('http://127.0.0.1:8899/file/'+s.id+'/trends.json');const trends=await t.json();
 if(mode==='demo'){assert.equal(trends.status,'live');assert.ok(trends.items.length>0)}
 await page.locator('#replay').click();await page.waitForFunction(()=>document.querySelector('#meeting').classList.contains('active'));assert.equal(await page.locator('.floor-avatar.meeting').count(),2);await page.waitForTimeout(750);
 await page.screenshot({path:path.join(__dirname,'workspace','studio-v02-'+mode+'-meeting.png'),fullPage:true});await page.locator('#live').click();assert.equal(await page.locator('.floor-avatar.meeting').count(),0);
 await page.screenshot({path:path.join(__dirname,'workspace','studio-v02-'+mode+'-review.png'),fullPage:true});
 return {mode,id:s.id,events:s.events.length,handoffs:10,trends:trends.status,quality:s.quality}
};
const results=[];results.push(await run('demo'));results.push(await run('manual',[{title:'Belajar AI',text:'Mulailah dengan satu masalah sederhana.'},{title:'Berikan konteks',text:'Jelaskan tujuan dan batasan tugas dengan jelas.'},{title:'Periksa jawaban',text:'Pastikan informasi benar sebelum digunakan.'}]));
const opts={headers:{Origin:'http://127.0.0.1:8899','Content-Type':'application/json'}};
const plan=await page.request.post('http://127.0.0.1:8899/run',{...opts,data:{mode:'plan',confirm_plan:false}});assert.equal(plan.status(),400);
const api=await page.request.post('http://127.0.0.1:8899/run',{...opts,data:{mode:'api',confirm_cost:false}});assert.equal(api.status(),400);
const bad=await page.request.post('http://127.0.0.1:8899/chatgpt/signin',{headers:{Origin:'https://example.invalid','Content-Type':'application/json'},data:{}});assert.equal(bad.status(),403);
const invalid=await page.request.post('http://127.0.0.1:8899/run',{...opts,data:{mode:'manual',scenes:[]}});assert.equal(invalid.status(),400);
assert.equal(errors.length,0,errors.join('; '));
const out={passed:true,agents:10,meetingReplay:true,modelConsentGuard:true,apiConsentGuard:true,crossOriginGuard:true,invalidInputGuard:true,uiErrors:errors,results};
fs.writeFileSync(path.join(__dirname,'workspace','acceptance-v02.json'),JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));
}catch(e){console.error(e);process.exitCode=1}finally{if(browser)await browser.close()}})();
