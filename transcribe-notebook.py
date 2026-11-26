"""Transcribe owner-provided Notebook media locally. No cloud audio upload."""
import os,sys,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ.update(HF_HOME=str(ROOT/'vendor'/'asr-cache'),TEMP=str(ROOT/'tmp'),TMP=str(ROOT/'tmp'),HF_HUB_OFFLINE='1')
sys.path.insert(0,str(ROOT/'vendor'/'asr'))
from faster_whisper import WhisperModel
def main():
 project=sys.argv[1]
 import re
 if not re.fullmatch('[a-zA-Z0-9_-]{1,64}',project):raise ValueError('Invalid project')
 folder=ROOT/'notebook-workspace'/project
 manifest=json.loads((folder/'integrated-media.json').read_text(encoding='utf-8'))
 m=WhisperModel('base',device='cpu',compute_type='int8',download_root=str(ROOT/'vendor'/'asr-cache'),local_files_only=True,cpu_threads=4,num_workers=1)
 reports={}
 for kind in ('video','audio'):
  x=manifest['media'][kind];source=folder/x['source']
  if source.resolve().parent!=folder.resolve():raise ValueError('Invalid source')
  seg,info=m.transcribe(str(source),language='id',beam_size=1,vad_filter=True,condition_on_previous_text=False)
  rows=[]
  for s in seg:rows.append({'start':round(s.start,2),'end':round(s.end,2),'text':s.text.strip(),'avg_logprob':round(s.avg_logprob,3)})
  if not rows:raise ValueError('Empty transcription')
  result={'kind':kind,'source':source.name,'language':'id (specified)','duration_seconds':info.duration,'segments':rows,'limitations':'ASR may mistranscribe technical terms, names and numbers; human listening still needed for pronunciation.'}
  (folder/f'transcript-{kind}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  (folder/f'transcript-{kind}.txt').write_text('\n'.join(f"[{s['start']:.1f}–{s['end']:.1f}] {s['text']}" for s in rows),encoding='utf-8')
  reports[kind]={'duration':info.duration,'segments':len(rows),'last_speech':rows[-1]['end']}
  print(kind+' TRANSCRIBED '+json.dumps(reports[kind]),flush=True)
 (folder/'transcription-status.json').write_text(json.dumps({'status':'transcribed','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'media':reports,'publication_approved':False},indent=2),encoding='utf-8')
if __name__=='__main__':main()
