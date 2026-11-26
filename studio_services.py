"""Local trend and narration services for Studio v0.2; no Facebook scraping."""
import json, subprocess, sys, os, datetime, wave, struct, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FEED="https://trends.google.com/trending/rss?geo=ID"
def trends():
    req=urllib.request.Request(FEED,headers={"User-Agent":"AI Content Production Engine/0.2 (RSS reader)"})
    with urllib.request.urlopen(req,timeout=15) as r:
        if not r.geturl().startswith("https://trends.google.com/"):raise ValueError("Unexpected trend feed origin")
        blob=r.read(2_000_001)
    if len(blob)>2_000_000:raise ValueError("RSS exceeds limit")
    tree=ET.fromstring(blob)
    items=[]
    for i in tree.findall("./channel/item")[:20]:
        title=(i.findtext("title") or "").strip()[:180]
        if title:items.append({"title":title,"published":(i.findtext("pubDate") or "")[:100],"link":(i.findtext("link") or "")[:500]})
    if not items:raise ValueError("RSS returned no trends")
    return {"status":"live","source":FEED,"retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"items":items,"limitation":"Google search interest, not Facebook engagement or proof of facts; verify relevance and source before publication."}
def plan(action, payload=None, timeout=35):
    env=os.environ.copy()
    for k in ("OPENAI_API_KEY","OPENAI_CUSTOM_HEADERS","OPENAI_BASE_URL","OPENAI_ORGANIZATION","OPENAI_PROJECT","OPENAI_LOG"):
        env.pop(k,None)
    result=subprocess.run(["node",str(ROOT/"chatgpt-plan.mjs"),action],input=json.dumps(payload or {},ensure_ascii=False),encoding="utf-8",capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),timeout=timeout,cwd=ROOT,env=env)
    try:data=json.loads(result.stdout.strip())
    except ValueError:raise RuntimeError("ChatGPT adapter unavailable") from None
    if result.returncode or data.get("error"):raise RuntimeError("ChatGPT adapter: "+str(data.get("error","failed"))[:100])
    return data
def piper_ready():
    return (ROOT/"vendor"/"piper"/"piper").is_dir() and (ROOT/"vendor"/"voice-id"/"id_ID-news_tts-medium.onnx").is_file()
def local_voice(folder,scenes):
    if not piper_ready():raise RuntimeError("Indonesian Piper model missing; install with INSTALL-VOICE-ID.cmd")
    env=os.environ.copy();env["PYTHONPATH"]=str(ROOT/"vendor"/"piper")
    model=ROOT/"vendor"/"voice-id"/"id_ID-news_tts-medium.onnx"
    durations=[]
    for i,s in enumerate(scenes):
        p=folder/f"voice-{i:02d}.wav"
        r=subprocess.run([sys.executable,"-B","-m","piper","--model",str(model),"--output-file",str(p)],input=s["text"],encoding="utf-8",capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),env=env,cwd=ROOT,timeout=100)
        if r.returncode or not p.is_file():raise RuntimeError("Piper synthesis failed")
        with wave.open(str(p),"rb") as w:
            n=w.getnframes();dur=n/w.getframerate()
            if w.getsampwidth()!=2 or dur<.25:raise RuntimeError("Invalid voice output")
            samples=w.readframes(min(n,500000))
            peak=max(abs(v[0]) for v in struct.iter_unpack("<h",samples))
            if peak<100:raise RuntimeError("Audio is silent")
            durations.append(dur)
    return durations,"Piper Indonesian neural voice (local preview; review voice dataset license before monetization)"
if __name__=="__main__":
    if "--trends" in sys.argv:print(json.dumps(trends(),ensure_ascii=False))
    elif "--voice" in sys.argv:
        d=ROOT/"tmp";dur,p=local_voice(d,[{"text":"Selamat datang. Ini adalah uji narasi bahasa Indonesia di studio agen AI."}]);print(json.dumps({"duration":dur,"provider":p}))
