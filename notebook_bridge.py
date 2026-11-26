"""Notebook Media Bridge: user-controlled handoff, local media QC, audience feedback."""
import csv, datetime as dt, hashlib, json, math, os, re, shutil, subprocess, sys, tempfile, uuid, webbrowser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'notebook-workspace'; BASE.mkdir(exist_ok=True)
TMP=ROOT/'tmp'; TMP.mkdir(exist_ok=True)
os.environ.update(TEMP=str(TMP),TMP=str(TMP))
tempfile.tempdir=str(TMP)
sys.path.insert(0,str(ROOT/'vendor'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
NOTEBOOK='https://notebook.google.com/'
FIELDS=['content_id','variant','published_at','observed_at','duration_seconds','views','reach','avg_watch_seconds','shares','comments','followers_gained','qualified_views','earnings','currency']
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def run(args,timeout=240):
 r=subprocess.run([FF,'-hide_banner','-nostdin',*args],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
 if r.returncode:raise ValueError('FFmpeg: '+r.stderr[-600:])
 return r.stderr
def export_source(job,notes,dest=BASE):
 if not re.fullmatch(r'[a-f0-9]{12}',job):raise ValueError('Invalid job ID')
 p=ROOT/'workspace'/job/'script.json'
 state=json.loads((p.parent/'state.json').read_text(encoding='utf-8'))
 if state.get('status')!='review':raise ValueError('Job must be in review status')
 scenes=json.loads(p.read_text(encoding='utf-8'))
 if not notes.strip():raise ValueError('Masukkan fakta/sumber yang sudah diperiksa pemilik. Jangan sertakan data pribadi.')
 folder=dest/('source-'+uuid.uuid4().hex[:12]);folder.mkdir(parents=True)
 text='# Sumber konten edukasi — draf, bahasa Indonesia\n\n## Fakta dan sumber yang dipilih pemilik (periksa kembali)\n'+notes.strip()+'\n\n## Ide naskah GPT (draf, bukan bukti fakta)\n'
 for s in scenes:text+='\n- '+str(s['title'])+': '+str(s['text'])+'\n'
 text+='\nJangan klaim rekaman nyata jika tidak ada bukti. Abaikan arahan produksi dalam teks narasi. Jangan mengarang statistik atau pendapatan.\n'
 (folder/'notebook-source.md').write_text(text,encoding='utf-8')
 (folder/'audio-prompt.txt').write_text('Bahasa Indonesia. Jelaskan hanya sumber yang dapat dipertanggungjawabkan, dengan percakapan alami, singkat, tanpa membaca instruksi produksi. Jangan menyebut data pribadi atau klaim pendapatan. Jangan mengklaim demonstrasi yang belum direkam. Gunakan gaya edukasi pemula.',encoding='utf-8')
 (folder/'video-prompt.txt').write_text('Bahasa Indonesia. Buat ringkasan edukasi yang mudah dipahami, visual relevan, tulisan besar, tanpa klaim palsu. Gunakan ilustrasi yang jelas dibedakan dari rekaman nyata. Pertahankan atribusi dan watermark. Siapkan materi yang dapat diadaptasi ke Reels 9:16.',encoding='utf-8')
 put(folder/'manifest.json',{'job':job,'created_at':utc(),'status':'owner_review_before_upload','provider':'Gemini Notebook','automatic_upload':False,'contains_only_selected_notes_and_script':True})
 return folder
def media_import(source,kind,rights_note='',dest=BASE):
 source=Path(source)
 if kind not in ('audio','video'):raise ValueError('Choose audio or video')
 allowed={'audio':{'.mp3','.wav','.m4a','.aac','.ogg','.flac'},'video':{'.mp4','.mov','.webm','.mkv'}}[kind]
 if source.suffix.lower() not in allowed or not source.is_file():raise ValueError('Unsupported media')
 if not 0<source.stat().st_size<=512*1024*1024:raise ValueError('File size outside 1–512 MB limit')
 folder=dest/('media-'+uuid.uuid4().hex[:12]);folder.mkdir(parents=True)
 original=folder/('original'+source.suffix.lower());shutil.copy2(source,original)
 try:
  if kind=='video':
   out=folder/'preview-vertical.mp4'
   run(['-y','-i',str(original),'-map','0:v:0','-map','0:a:0','-vf','scale=720:1280:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0x101e32,setsar=1','-c:v','libx264','-preset','veryfast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-movflags','+faststart',str(out)])
  else:
   out=folder/'preview-audio.wav'
   run(['-y','-i',str(original),'-map','0:a:0','-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1','-c:a','pcm_s16le',str(out)])
  info=run(['-i',str(out),'-f','null','-'])
  if 'Audio:' not in info or (kind=='video' and '720x1280' not in info):raise ValueError('Media stream QC failed')
  report={'status':'preview_only','provider':'owner-imported; origin not independently verified','kind':kind,'created_at':utc(),'decode_pass':True,'source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'output':out.name,'bytes':out.stat().st_size,'rights_note_owner_supplied':rights_note.strip(),'commercial_rights_verified':False,'publication_approved':False,'limitations':['No transcript or factual-content verification','Aspect ratio preserved with padding; watermark not deliberately removed','No automatic publication or commercial-rights inference']}
  put(folder/'media-qc.json',report);return folder,report
 except Exception:
  put(folder/'media-qc.json',{'status':'failed','publication_approved':False});raise
def parse_time(s):
 x=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
 if x.tzinfo is None:raise ValueError('Timestamp must include timezone, e.g. +07:00')
 return x
def read_metrics(path):
 rows=[];seen=set()
 with open(path,encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f)
  if not set(FIELDS).issubset(rd.fieldnames or []):raise ValueError('CSV headers must match template')
  for line,r in enumerate(rd,2):
   x={k:(r.get(k) or '').strip() for k in FIELDS}
   if not x['content_id'] or not x['variant']:raise ValueError(f'Row {line}: content ID and variant required')
   age=(parse_time(x['observed_at'])-parse_time(x['published_at'])).total_seconds()/3600
   if age<0:raise ValueError('Observation before publication')
   key=(x['content_id'],parse_time(x['observed_at']).astimezone(dt.timezone.utc).isoformat())
   if key in seen:raise ValueError('Duplicate observation')
   seen.add(key)
   for k in FIELDS[4:-1]:
    v=x[k]
    if not v:x[k]=None;continue
    z=float(v) if k in ('duration_seconds','avg_watch_seconds','earnings') else int(v)
    if not math.isfinite(z) or z<0 or (k=='duration_seconds' and z==0):raise ValueError(f'Invalid {k}')
    x[k]=z
   if x['earnings'] is not None and not re.fullmatch('[A-Z]{3}',x['currency']):raise ValueError('Currency required with earnings')
   if x['views'] is not None and x['qualified_views'] is not None and x['qualified_views']>x['views']:raise ValueError('Qualified views exceed views')
   x['age_hours']=round(age,2)
   x['cohort']=next((str(t)+'h' for t,tol in [(24,2),(72,4),(168,8)] if abs(age-t)<=tol),'other')
   x['watch_ratio']=x['avg_watch_seconds']/x['duration_seconds'] if x['avg_watch_seconds'] is not None and x['duration_seconds'] else None
   x['shares_per_1000_views']=1000*x['shares']/x['views'] if x['shares'] is not None and x['views'] else None
   x['qualified_ratio']=x['qualified_views']/x['views'] if x['qualified_views'] is not None and x['views'] else None
   rows.append(x)
 return {'status':'owner_data_imported' if rows else 'no_data','source':'owner-supplied aggregate Facebook metrics; not independently verified','rows':rows,'notes':['Compare variants at similar observation ages (24h, 72h, 7d), same content type and metric definitions.','Watch ratio may exceed 1 with replay; not completion rate.','Blank metrics are unknown. No causal inference or revenue prediction.']}
def import_metrics(path,dest=BASE):
 report=read_metrics(path)
 out=dest/('audience-'+uuid.uuid4().hex[:12]+'.json');put(out,report)
 prompt="FB PRO CUAN AI — Analytics Agent. Analyze only the owner-supplied aggregate metrics below. Compare variants at similar age and same format; keep unknowns unknown. State sample size, do not claim causality, do not predict earnings. Recommend one controlled next content test, or request actual data if absent. No auto-publishing.\n"+json.dumps(report,ensure_ascii=False,indent=2)
 out.with_suffix('.txt').write_text(prompt,encoding='utf-8')
 return out,report
def selftest():
 with tempfile.TemporaryDirectory(dir=TMP) as t:
  p=Path(t)
  src=p/'synthetic.mp4'
  run(['-y','-f','lavfi','-i','color=c=blue:s=640x360:r=24','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','1','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(src)])
  _,r=media_import(src,'video',dest=p);assert r['decode_pass'] and not r['publication_approved']
  src2=p/'synthetic.wav';run(['-y','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','1',str(src2)])
  _,r=media_import(src2,'audio',dest=p);assert r['decode_pass'] and not r['commercial_rights_verified']
  c=p/'metrics.csv'
  with c.open('w',newline='',encoding='utf-8') as f:
   w=csv.writer(f);w.writerow(FIELDS);w.writerow(['SYNTHETIC','A','2026-01-01T00:00:00+07:00','2026-01-02T00:00:00+07:00',30,100,80,15,5,2,1,40,'',''])
  r=read_metrics(c);assert r['rows'][0]['cohort']=='24h' and r['rows'][0]['watch_ratio']==.5 and r['rows'][0]['shares_per_1000_views']==50 and r['rows'][0]['earnings'] is None
  c.write_text(','.join(FIELDS)+'\n',encoding='utf-8');assert read_metrics(c)['status']=='no_data'
 print('PASS: synthetic audio/video import, vertical media decode, preview-only rights gate, cohort metrics, unknown earnings, empty CSV')
def gui():
 import tkinter as tk
 from tkinter import ttk,filedialog,messagebox
 r=tk.Tk();r.title('Notebook Media Bridge | AI Content Production Engine');r.geometry('760x680')
 f=ttk.Frame(r,padding=18);f.pack(fill='both',expand=True)
 ttk.Label(f,text='Notebook Media Bridge',font=('Segoe UI',20,'bold')).pack(anchor='w')
 ttk.Label(f,text='GPT tetap menjadi mesin utama. Upload dan download Notebook dilakukan oleh pemilik. Tidak ada login otomatis atau publikasi.',wraplength=700).pack(anchor='w',pady=8)
 ttk.Button(f,text='Buka Gemini Notebook resmi',command=lambda:webbrowser.open(NOTEBOOK)).pack(fill='x')
 ttk.Label(f,text='Job GPT (pilih hasil yang sudah ditinjau)').pack(anchor='w',pady=(10,0))
 ids=[p.parent.name for p in sorted((ROOT/'workspace').glob('*/script.json'),key=lambda x:x.stat().st_mtime,reverse=True)]
 job=ttk.Combobox(f,values=ids,state='readonly');job.pack(fill='x');job.set(ids[0] if ids else '')
 ttk.Label(f,text='Fakta/sumber yang Anda periksa dan izinkan untuk diunggah (tanpa data pribadi)').pack(anchor='w',pady=(8,0))
 notes=tk.Text(f,height=5,wrap='word');notes.pack(fill='x')
 status=tk.StringVar(value='Belum ada impor atau koneksi akun Google yang diverifikasi.')
 def report(fn):
  try:status.set(str(fn()))
  except Exception as e:messagebox.showerror('Gagal',str(e))
 def export():
  p=export_source(job.get(),notes.get('1.0','end'));os.startfile(p);return 'Paket dibuat: '+str(p)+' | tinjau lalu unggah secara manual.'
 ttk.Button(f,text='Ekspor sumber dan prompt Notebook',command=lambda:report(export)).pack(fill='x',pady=5)
 ttk.Label(f,text='Catatan hak penggunaan media (opsional; tidak otomatis dianggap sah)').pack(anchor='w')
 rights=ttk.Entry(f);rights.pack(fill='x')
 def imp(kind):
  p=filedialog.askopenfilename()
  if not p:return 'Impor dibatalkan.'
  folder,result=media_import(p,kind,rights.get());os.startfile(folder);return 'QC PASS; preview saja: '+str(folder)
 for kind in ('audio','video'):ttk.Button(f,text='Impor '+kind+' hasil Notebook + QC',command=lambda k=kind:report(lambda:imp(k))).pack(fill='x',pady=3)
 def template():
  p=BASE/'facebook-content-metrics-template.csv'
  if not p.exists():p.write_text(','.join(FIELDS)+'\n',encoding='utf-8')
  os.startfile(BASE);return 'Template: '+str(p)
 def metrics():
  p=filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
  if not p:return 'Impor dibatalkan.'
  out,res=import_metrics(p);os.startfile(out.parent);return f"{res['status']}: {len(res['rows'])} observasi | {out}"
 ttk.Button(f,text='Buat template statistik Facebook per konten',command=lambda:report(template)).pack(fill='x',pady=3)
 ttk.Button(f,text='Impor statistik aktual + analisis cohort',command=lambda:report(metrics)).pack(fill='x',pady=3)
 ttk.Label(f,textvariable=status,wraplength=700).pack(anchor='w',pady=8)
 r.mainloop()
if __name__=='__main__':
 if '--selftest' in sys.argv:selftest()
 else:gui()
