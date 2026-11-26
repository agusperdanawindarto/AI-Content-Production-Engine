"""Read-only monetization readiness checks; no Facebook login, scraping or publishing."""
import json,csv,datetime,re,sys
from pathlib import Path
import notebook_bridge as nb
def build(project):
 if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}',project):raise ValueError('Invalid project')
 d=nb.BASE/project
 if not (d/'integrated-media.json').is_file():raise ValueError('Project missing')
 rights={'review_date':'2026-11-26','status':'conditional_pending_owner_verification','sources':[
 {'url':'https://support.google.com/gemininotebook/answer/17004255','finding':'Google does not claim ownership of original generated content; applicable terms vary by account type; copyright must be respected.'},
 {'url':'https://policies.google.com/terms','finding':'No blanket commercial prohibition identified for consumer original outputs; no guarantee of third-party asset clearance.'},
 {'url':'https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/','finding':'Meta prioritizes original creator-produced content; eligibility is not guaranteed.'},
 {'url':'https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/','finding':'Disclose realistic synthetic audio/video at publication.'}],
 'pending':['Google account type and applicable organization terms','Owner confirmation of source and third-party asset rights','Full content review and AI label at eventual publication','Meta monetization eligibility'],
 'piper_commercial_rights_verified':False,'commercial_rights_verified':False,'publication_approved':False}
 nb.put(d/'rights-review.json',rights)
 template=nb.BASE/'facebook-content-metrics-template.csv'
 if not template.exists():template.write_text(','.join(nb.FIELDS)+'\n',encoding='utf-8')
 reports=[]
 for p in sorted(nb.BASE.glob('audience-*.json')):
  try:
   x=json.loads(p.read_text(encoding='utf-8'))
   if x.get('status')=='owner_data_imported' and x.get('rows'):reports.append({'file':p.name,'observations':len(x['rows'])})
  except (OSError,ValueError):continue
 result={'status':'blocked_pending_review_and_actual_data','project':project,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audio_peak': 'pass' if (d/'true-peak-qc.json').is_file() else 'pending','transcription':'available_for_review' if (d/'transcription-status.json').is_file() else 'pending','rights':'conditional_pending_owner_verification','facebook_metrics':'owner_data_imported' if reports else 'no_data','reports':reports,'publication_approved':False,'commercial_rights_verified':False}
 nb.put(d/'monetization-readiness.json',result)
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':build(sys.argv[1])
