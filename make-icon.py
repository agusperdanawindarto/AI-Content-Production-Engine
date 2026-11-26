from pathlib import Path
import sys
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'vendor'))
from PIL import Image,ImageDraw
im=Image.new('RGBA',(256,256),(0,0,0,0));d=ImageDraw.Draw(im)
d.rounded_rectangle((10,10,246,246),radius=48,fill='#14263e',outline='#65d9be',width=8)
for x,y in [(72,74),(184,74),(72,182),(184,182)]:
 d.line((128,128,x,y),fill='#65d9be',width=8)
 d.rounded_rectangle((x-24,y-19,x+24,y+19),radius=8,fill='#4a7593')
 d.rectangle((x-15,y-9,x+15,y+9),fill='#c9f5e9')
d.rounded_rectangle((92,93,164,163),radius=20,fill='#65d9be')
d.ellipse((107,113,117,123),fill='#14263e');d.ellipse((139,113,149,123),fill='#14263e')
d.line((113,140,143,140),fill='#14263e',width=5)
im.save(root/'studio.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print('Studio icon generated')
