"""Verify a completed real ChatGPT-plan production without sending new model requests."""
import argparse,json,hashlib,sys,wave,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument("job");args=p.parse_args()
if not __import__("re").fullmatch("[a-f0-9]{12}",args.job):raise SystemExit("Invalid job id")
d=ROOT/"workspace"/args.job
def read(name):return json.loads((d/name).read_text(encoding="utf-8"))
s=read("state.json")
if s["status"]!="review":raise SystemExit("Job not ready for review: "+s["status"])
assert s["mode"]=="plan" and s["model"].startswith("gpt-6.2")
events=s["events"]
roles=["Researcher","Strategist","Script Writer","Policy Auditor"]
for role in roles:
 assert any(e["role"]==role and e["status"]=="done" for e in events),role
for name in ("research.txt","strategy.txt","script.json","policy-review.txt","caption.txt","subtitles.srt","thumbnail.png","reel.mp4"):
 assert (d/name).stat().st_size>0,name
t=read("trends.json");assert t["status"]=="live" and t["items"] and t["source"]=="https://trends.google.com/trending/rss?geo=ID"
scenes=read("script.json")
assert 3<=len(scenes)<=6
audio=[]
for i in range(len(scenes)):
 with wave.open(str(d/f"voice-{i:02d}.wav"),"rb") as w:
  duration=w.getnframes()/w.getframerate()
  assert w.getsampwidth()==2
  peak=max(abs(v[0]) for v in struct.iter_unpack("<h",w.readframes(w.getnframes())))
  assert duration>.25 and peak>100
  audio.append({"scene":i+1,"seconds":round(duration,3),"peak":peak})
q=read("quality.json")
assert q["decode_pass"] and q["publication_approved"] is False
assert q["sha256"]==hashlib.sha256((d/"reel.mp4").read_bytes()).hexdigest()
handoffs=[e for e in events if e["status"]=="handoff"]
assert len(handoffs)==10
report={"passed":True,"mode":s["mode"],"model":s["model"],"job":args.job,"trend_count":len(t["items"]),"trend_status":t["status"],"gpt_role_completion_records":roles,"event_count":len(events),"handoffs":len(handoffs),"scenes":len(scenes),"audio":audio,"quality":q,"limitations":["Records show completed role stages, not independent server-side billing verification.","Non-silent audio does not establish commercial voice rights or subjective pronunciation quality.","Content factual accuracy and publication approval require owner review."]}
(d/"plan-acceptance.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
