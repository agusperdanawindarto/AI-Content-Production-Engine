// Official SIWC local DevKit adapter. Credentials are encrypted with Windows CurrentUser DPAPI.
import {createChatGPT} from './vendor/siwc-devkit/packages/local/dist/index.js';
import {spawnSync,spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
import {readFileSync} from 'node:fs';
const root=dirname(fileURLToPath(import.meta.url));
function dpapi(data,encrypt){
 const verb=encrypt?'Protect':'Unprotect';
 const ps="$ErrorActionPreference='Stop'; Add-Type -AssemblyName System.Security; $b=[Convert]::FromBase64String([Console]::In.ReadToEnd().Trim()); $o=[Security.Cryptography.ProtectedData]::"+verb+"($b,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser); [Console]::Write([Convert]::ToBase64String($o))";
 const r=spawnSync('powershell.exe',['-NoProfile','-NonInteractive','-Command',ps],{input:Buffer.from(data).toString('base64'),encoding:'utf8',windowsHide:true,timeout:15000});
 if(r.status!==0||!r.stdout.trim())throw Error('DPAPI unavailable');
 return Buffer.from(r.stdout.trim(),'base64');
}
const crypto={id:'windows-dpapi-current-user-v1',isAvailable(){try{return dpapi(dpapi(Buffer.from('check'),true),false).toString()==='check'}catch{return false}},encrypt:s=>dpapi(Buffer.from(s,'utf8'),true),decrypt:b=>dpapi(b,false).toString('utf8')};
const c=createChatGPT({appName:'AI Content Production Engine',appId:'ai-content-production-engine',redirectPort:0,storageDir:join(root,'private','chatgpt'),credentialEncryption:crypto,sendHostId:true,openBrowser(url){
 const u=new URL(url);if(u.protocol!=='https:'||u.hostname!=='auth.openai.com')throw Error('Unexpected authorization origin');
 const ps='Start-Process -FilePath $env:STUDIO_AUTH_URL';const p=spawn('powershell.exe',['-NoProfile','-NonInteractive','-Command',ps],{env:{...process.env,STUDIO_AUTH_URL:url},windowsHide:true,stdio:'ignore'});p.unref();
}});
const safe=s=>({status:s.status,sharing:!!s.sharing,identity:s.identity?{email:s.identity.email,name:s.identity.name}:null,error:s.error?{code:s.error.code}:null});
try{
 const action=process.argv[2]||'status';
 if(action==='selftest'){if(!crypto.isAvailable())throw Error('DPAPI unavailable');console.log(JSON.stringify({ok:true,dpapi:true}));}
 else if(action==='status'){console.log(JSON.stringify(safe(await c.getSession())));}
 else if(action==='signin'){console.log(JSON.stringify(safe(await c.signIn())));}
 else if(action==='disconnect'){await c.disconnect();console.log(JSON.stringify({status:'disconnected',sharing:false}));}
 else if(action==='models'){const s=await c.getSession();if(!s.sharing)throw Error('ChatGPT plan not authorized');console.log(JSON.stringify({models:await c.listModels()}));}
 else if(action==='ask'){const arg=JSON.parse(readFileSync(0,'utf8'));const s=await c.getSession();if(!s.sharing)throw Error('ChatGPT plan not authorized');const models=await c.listModels();const model=models.find(m=>m.slug===arg.model);if(!model)throw Error('Selected GPT model not available');const r=await c.streamResponse({model:model.slug,input:arg.input,instructions:arg.instructions});if(!r.text?.trim())throw Error('Empty response');console.log(JSON.stringify({text:r.text,model:model.slug}));}
 else throw Error('Unsupported command');
}catch(e){console.log(JSON.stringify({error:e.code||'local_adapter_error'}));process.exitCode=1;}
