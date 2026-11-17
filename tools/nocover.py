# The cover for a game without one: the retro horizon in the system's colour, NO COVER over it (nocover/)
import os,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
OUT,SYSLIST=sys.argv[1:3]
os.makedirs(OUT+'/nocover',exist_ok=True)
F=lambda n,px:ImageFont.truetype(f'{OUT}/fonts/{n}.ttf',px)
BLUE=(29,79,196); RED=(200,16,46); GOLD=(255,199,44)
def brand(name,full):
    s=(name+' '+full).lower()
    for keys,c in [(('sega','megadrive','genesis','mastersystem','gamegear','32x','segacd','dreamcast','saturn','sg-1000','sg1000','msumd','pico','naomi','atomiswave','vmu'),BLUE),
        (('nes','snes','famicom','nintendo','gb','gba','gbc','n64','nds','virtualboy','pokemon','sgb','sufami','satellaview','fds'),RED),
        (('psx','psp','playstation','sony'),(110,120,150)),(('pcengine','tg16','tg-cd','supergrafx','pcfx','turbografx','nec','pc98'),(230,110,20)),
        (('neogeo','ngp','snk'),GOLD),(('atari','lynx','jaguar'),(205,70,30)),(('cps','mame','arcade','fba','fbneo','capcom','alg','daphne'),(150,50,190))]:
        if any(k in s for k in keys): return c
    return (20,140,130)
def chrome(txt,font):
    b=font.getbbox(txt); w,h=b[2]-b[0]+8,b[3]-b[1]+8
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).text((4-b[0],4-b[1]),txt,font=font,fill=255)
    g=Image.new('RGB',(w,h)); d=ImageDraw.Draw(g)
    for y in range(h): t=y/max(1,h-1); v=int(255-105*t); d.line([(0,y),(w,y)],fill=(v,v,min(255,v+15)))
    d.line([(0,h//2),(w,h//2)],fill=(110,115,130))
    o=Image.new('RGBA',(w,h),(0,0,0,0)); o.paste(g,(0,0),m)
    sh=Image.new('RGBA',(w+6,h+4),(0,0,0,0)); sh.paste((0,0,0,255),(3,3),m); sh=sh.filter(ImageFilter.GaussianBlur(1.5)); sh.alpha_composite(o,(0,0))
    s=0.18; return sh.transform((int(sh.width+s*sh.height),sh.height),Image.AFFINE,(1,s,-s*sh.height,0,1,0),Image.BICUBIC)
PAL={}    # tools/system_info.txt: the system's three colours
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'system_info.txt'),encoding='utf-8'):
    line=line.strip()
    if line and not line.startswith('#'):
        f=(line.split('|')+['']*5)[:5]
        if f[4]: PAL[f[0]]=[tuple(int(h[i:i+2],16) for i in (0,2,4)) for h in f[4].split(',')]
def mix(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def lift(c,k=1.08,add=18): return tuple(min(255,int(v*k+add)) for v in c)
def nocover(col,theme=''):
    cs=PAL.get(theme,[col,lift(col,1.2,40),col])
    sky,grid=cs[0],cs[1] if sum(cs[1])>90 else lift(cs[1],1,80)
    W,H=210,294; im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    hz=int(H*0.56)
    for y in range(hz): t=y/hz; d.line([(0,y),(W,y)],fill=tuple(int(c*(0.08+0.5*t)) for c in sky))
    r=52; sun=Image.new('RGB',(2*r+1,2*r+1)); sd=ImageDraw.Draw(sun)
    for x in range(2*r+1):
        t=x/(2*r); sd.line([(x,0),(x,2*r)],fill=lift(mix(cs[0],cs[1],t*2) if t<0.5 else mix(cs[1],cs[2],(t-0.5)*2)))
    m=Image.new('L',sun.size,0); ImageDraw.Draw(m).ellipse([0,0,2*r,2*r],fill=255); im.paste(sun,(W//2-r,hz-r),m)
    for i in range(5): d.line([(0,hz-10-i*9),(W,hz-10-i*9)],fill=tuple(int(c*0.2) for c in sky),width=3)
    d.rectangle([0,hz,W,H],fill=(6,6,10))
    for x in range(-W*2,W*3,20): d.line([(W/2+(x-W/2)*0.12,hz),(x,H)],fill=grid)
    for i in range(1,12): y=hz+(i**1.8)*1.7; d.line([(0,y),(W,y)],fill=grid)
    im=im.convert('RGBA')
    t=chrome('NO',F('Orbitron-Black',40)); im.alpha_composite(t,((W-t.width)//2,22))
    t=chrome('COVER',F('Orbitron-Black',40)); im.alpha_composite(t,((W-t.width)//2,66))
    d=ImageDraw.Draw(im); d.rectangle([0,0,W-1,H-1],outline=(200,202,212),width=2)
    return im
rows=[l.split('|') for l in open(SYSLIST).read().splitlines() if l.count('|')==2]
seen=set()
for name,full,theme in rows+[('default','','default')]+[(t,'arcade',t) for t in ('auto-allgames','all','auto-favorites','favorites','auto-lastplayed','recent','custom-collections','collections','options')]:
    if theme and theme not in seen:
        seen.add(theme); nocover(brand(name,full),theme).save(f'{OUT}/nocover/{theme}.png')
print('nocover:',len(seen))
