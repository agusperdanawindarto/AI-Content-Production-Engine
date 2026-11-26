"""Import and assess two owner-downloaded Notebook media files, without publication."""
import argparse,json,re,hashlib,subprocess,datetime
from pathlib import Path
import notebook_bridge as nb
from PIL import Image,ImageDraw,ImageOps
def measure(p):
    raw=nb.run(['-i',str(p),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],timeout=300)
    d=re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)',raw)
    if not d:raise ValueError('Duration unknown')
    h,m,s=map(float,d.groups())
    loud=json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',raw)[-1])
    assert float(loud['input_i'])>-70,'Silent audio'
    v=re.search(r'Video:.*?\b(\d{2,5})x(\d{2,5})\b',raw)
    return {'duration_seconds':round(h*3600+m*60+s,2),'resolution':list(map(int,v.groups())) if v else None,'integrated_lufs':float(loud['input_i']),'true_peak_dbtp':float(loud['input_tp']),'audio_non_silent':True}
def contact(p,duration,out):
    im=Image.new('RGB',(960,960),'#15232f');draw=ImageDraw.Draw(im)
    for i,f in enumerate([.03,.18,.34,.50,.66,.82]):
        sec=round(duration*f,2);frame=out.parent/f'frame-{i+1}.jpg'
        nb.run(['-y','-ss',str(sec),'-i',str(p),'-frames:v','1','-vf','scale=300:440:force_original_aspect_ratio=decrease',str(frame)])
        with Image.open(frame) as x:
            x=ImageOps.contain(x.convert('RGB'),(300,440));left=(i%3)*320+(320-x.width)//2;top=(i//3)*480+12
            im.paste(x,(left,top));draw.text(((i%3)*320+12,(i//3)*480+454),f'{sec:.1f} s',fill='white')
    im.save(out)
def main():
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);a=p.parse_args()
    folder=a.folder.resolve()
    base=nb.BASE.resolve()
    if not folder.is_relative_to(base):raise ValueError('Folder must be within notebook-workspace')
    audio=list(x for x in folder.iterdir() if x.suffix.lower() in {'.m4a','.mp3','.wav','.aac','.ogg','.flac'} and x.is_file())
    video=list(x for x in folder.iterdir() if x.suffix.lower() in {'.mp4','.mov','.mkv','.webm'} and x.is_file())
    if len(audio)!=1 or len(video)!=1:raise ValueError('Exactly one original audio and video required')
    result={'status':'preview_only','project':folder.name,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider':'Owner-downloaded Notebook media; provider origin reported by owner','publication_approved':False,'commercial_rights_verified':False,'media':{}}
    for kind,source in [('audio',audio[0]),('video',video[0])]:
        dst,q=nb.media_import(source,kind,'Owner-downloaded Notebook preview; commercial rights not verified')
        original=measure(dst/('original'+source.suffix.lower()));processed=measure(dst/q['output'])
        if kind=='video':
            assert processed['resolution']==[720,1280]
            contact(dst/q['output'],processed['duration_seconds'],dst/'contact-sheet.jpg')
        assert abs(original['duration_seconds']-processed['duration_seconds'])<1.0
        assert processed['true_peak_dbtp']<0
        result['media'][kind]={'source':source.name,'folder':dst.name,'output':q['output'],'original':original,'processed':processed,'sha256':q['output_sha256'],'decode_pass':q['decode_pass']}
        print(kind+' PASS '+json.dumps(result['media'][kind]),flush=True)
    result['limitations']=['Audio waveform measurements do not establish pronunciation, factual accuracy or voice rights.','Contact sheet provides sampled visual review only.','No audience data, no publication.']
    nb.put(folder/'integrated-media.json',result)
    print('INTEGRATED '+str(folder/'integrated-media.json'),flush=True)
if __name__=='__main__':main()
