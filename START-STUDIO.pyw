"""Windows desktop launcher: browser-only, no terminal window."""
import os,sys,json,time,subprocess,urllib.request,ctypes
from pathlib import Path
ROOT=Path(__file__).resolve().parent
URL='http://127.0.0.1:8899/'
TMP=ROOT/'tmp'
def healthy():
 try:
  with urllib.request.urlopen(URL+'health',timeout=1) as response:
   info=json.load(response)
  return info.get('ok') is True and Path(info.get('root','')).resolve()==ROOT
 except (OSError,ValueError,TypeError):return False
def main():
 TMP.mkdir(exist_ok=True)
 os.environ.update(TEMP=str(TMP),TMP=str(TMP),PYTHONDONTWRITEBYTECODE='1')
 if not healthy():
  # A Windows named mutex avoids duplicate startup when the icon is clicked twice.
  k=ctypes.windll.kernel32
  k.CreateMutexW.restype=ctypes.c_void_p
  k.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong]
  k.ReleaseMutex.argtypes=[ctypes.c_void_p]
  k.CloseHandle.argtypes=[ctypes.c_void_p]
  lock=k.CreateMutexW(None,False,'Local\\AIContentProductionEngineLauncher8899')
  if not lock:raise RuntimeError('Launcher lock unavailable')
  acquired=k.WaitForSingleObject(lock,30000) in (0,128)
  try:
   if not acquired:raise RuntimeError('Studio startup is busy')
   if not healthy():
    with (TMP/'studio-server.log').open('ab') as log:
     child=subprocess.Popen([sys.executable,'-B',str(ROOT/'app.py')],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
    deadline=time.monotonic()+25
    while time.monotonic()<deadline:
     if healthy():break
     if child.poll() is not None:raise RuntimeError('Server failed to start. Check tmp/studio-server.log on drive D.')
     time.sleep(.3)
    else:raise RuntimeError('Server did not become ready. Check tmp/studio-server.log on drive D.')
  finally:
   if acquired:k.ReleaseMutex(lock)
   k.CloseHandle(lock)
 os.startfile(URL)
if __name__=='__main__':
 try:main()
 except Exception as e:
  ctypes.windll.user32.MessageBoxW(None,str(e),'AI Content Production Engine',0x10)
  sys.exit(1)
