"""Local production gallery and explicit editorial review. No Facebook API or posting."""
import json,re,hashlib,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'notebook-workspace'
WORK=ROOT/'workspace'
REVIEWS=BASE/'editorial-reviews.json'
def read(p):
 return json.loads(p.read_text(encoding='utf-8'))
def safe(p,base):
 return p.is_file() and p.resolve().is_relative_to(base.resolve()) and p.resolve()==p.absolute()
def entries():
 p=BASE/'pilot-001'/'READY-TO-POST'
 yield '001','AI Bisa Bantu Kerja?',p/'REEL-001-BERSUARA.mp4',p/'CAPTION-BERSUARA.txt',p/'QC-BERSUARA.json',p/'thumbnail.png'
 for n in ('002','003','004','005'):
  p=BASE/'KONTEN-002-005'/'READY-TO-REVIEW'/('KONTEN-'+n)
  yield n,'Konten '+n,p/('REEL-'+n+'-BERSUARA.mp4'),p/'DESKRIPSI-REEL.txt',p/'QC.json',p/'THUMBNAIL.png'
 for p in sorted(WORK.glob('*/state.json'),reverse=True):
  if not re.fullmatch('[a-f0-9]{12}',p.parent.name):continue
  try:
   s=read(p)
   if s.get('status')!='review':continue
   folder=p.parent
   scenes=read(folder/'script.json')
   yield 'job-'+folder.name,scenes[0]['title'],folder/'reel.mp4',folder/'caption.txt',folder/'quality.json',folder/'thumbnail.png'
  except (ValueError,OSError,KeyError,IndexError,TypeError):continue
def reviews():
 try:return read(REVIEWS)
 except (OSError,ValueError):return {}
def catalog():
 out=[];r=reviews()
 for key,title,v,c,q,t in entries():
  try:
   if not all(safe(p,ROOT) for p in (v,c,q)):continue
   data=read(q)
   if data.get('decode_pass') is not True:continue
   sha=hashlib.sha256(v.read_bytes()).hexdigest()
   if sha!=data.get('sha256'):continue
   old=r.get(key,{})
   out.append({'id':key,'title':data.get('title',title),'video':v.name,'path':str(v),'caption':c.read_text(encoding='utf-8-sig')[:10000],'duration':data.get('duration_seconds',data.get('duration_planned_seconds')),'sha256':sha,'voice':data.get('voice_provider',data.get('audio','Notebook; rights conditional')),'peak':data.get('true_peak_dbtp'),'rights_verified':data.get('commercial_rights_verified') is True,'editorial_review':old.get('status','pending') if old.get('sha256')==sha else 'pending','publication':'not_verified','thumbnail':safe(t,ROOT)})
  except (OSError,ValueError,KeyError,TypeError):continue
 return out
def asset(key,kind):
 if not re.fullmatch(r'(00[1-5]|job-[a-f0-9]{12})',key):return None
 for k,_,v,c,q,t in entries():
  if k==key:
   p={'video':v,'thumbnail':t}.get(kind)
   if p and safe(p,ROOT):return p
 return None
def approve(key,sha,status):
 if status not in ('reviewed','pending'):raise ValueError('Invalid status')
 item=next((i for i in catalog() if i['id']==key and i['sha256']==sha),None)
 if not item:raise ValueError('Video changed or not found')
 r=reviews();r[key]={'sha256':sha,'status':status,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication_approved':False,'commercial_rights_verified':False}
 BASE.mkdir(exist_ok=True)
 tmp=REVIEWS.with_suffix('.tmp');tmp.write_text(json.dumps(r,indent=2),encoding='utf-8');tmp.replace(REVIEWS)
 return r[key]
