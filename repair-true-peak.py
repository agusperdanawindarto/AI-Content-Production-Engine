"""Local true-peak correction. No modification of original Notebook exports."""
import json, re, hashlib, datetime, math
from pathlib import Path
import notebook_bridge as nb
ROOT=Path(__file__).resolve().parent
def loud(p):
 raw=nb.run(['-i',str(p),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],timeout=300)
 x=json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',raw)[-1])
 return {'integrated_lufs':float(x['input_i']),'true_peak_dbtp':float(x['input_tp'])}
def repair(p):
 data=json.loads(p.read_text(encoding='utf-8')); assert data['publication_approved'] is False
 results={}
 for kind in ('audio','video'):
  m=data['media'][kind]; folder=nb.BASE/m['folder']; src=folder/m['output']; out=folder/('review-safe.wav' if kind=='audio' else 'review-safe.mp4')
  orig=loud(src);gain=min(0,-2.0-orig['true_peak_dbtp'])
  args=['-y','-i',str(src)]
  args+=['-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k'] if kind=='video' else ['-map','0:a:0','-c:a','pcm_s16le']
  nb.run(args+['-af',f'volume={gain:.4f}dB',str(out)],timeout=300)
  final=loud(out)
  if final['true_peak_dbtp']>-1.5:
   gain-=final['true_peak_dbtp']+2.0
   nb.run(args+['-af',f'volume={gain:.4f}dB',str(out)],timeout=300);final=loud(out)
  if not all(math.isfinite(x) for x in final.values()) or final['true_peak_dbtp']>-1.5 or final['integrated_lufs']<-40:raise ValueError('Audio gate failed')
  nb.run(['-i',str(out),'-f','null','-'],timeout=300)
  results[kind]={'folder':m['folder'],'file':out.name,'before':orig,'after':final,'gain_db':gain,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'decode_pass':True}
  print(kind,json.dumps(results[kind]),flush=True)
 nb.put(p.parent/'true-peak-qc.json',{'status':'preview_only','publication_approved':False,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results})
if __name__=='__main__':
 import sys
 p=(nb.BASE/sys.argv[1]/'integrated-media.json').resolve()
 if p.parent.parent!=nb.BASE.resolve():raise ValueError('Invalid project')
 repair(p)
