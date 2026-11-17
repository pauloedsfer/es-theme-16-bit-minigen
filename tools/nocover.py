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
def nocover(col):
    W,H=210,294; im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    hz=int(H*0.56)
    for y in range(hz): t=y/hz; d.line([(0,y),(W,y)],fill=tuple(int(c*(0.08+0.55*t)) for c in col))
    d.ellipse([W/2-52,hz-52,W/2+52,hz+52],fill=tuple(min(255,int(c*1.2+50)) for c in col))
    for i in range(5): d.line([(0,hz-10-i*9),(W,hz-10-i*9)],fill=(0,0,0),width=3)
    d.rectangle([0,hz,W,H],fill=(6,6,10))
    for x in range(-W*2,W*3,20): d.line([(W/2+(x-W/2)*0.12,hz),(x,H)],fill=col)
    for i in range(1,12): y=hz+(i**1.8)*1.7; d.line([(0,y),(W,y)],fill=col)
    im=im.convert('RGBA')
    t=chrome('NO',F('Orbitron-Black',40)); im.alpha_composite(t,((W-t.width)//2,22))
    t=chrome('COVER',F('Orbitron-Black',40)); im.alpha_composite(t,((W-t.width)//2,66))
    d=ImageDraw.Draw(im); d.rectangle([0,0,W-1,H-1],outline=(200,202,212),width=2)
    return im
rows=[l.split('|') for l in open(SYSLIST).read().splitlines() if l.count('|')==2]
seen=set()
for name,full,theme in rows+[('default','','default')]+[(t,'arcade',t) for t in ('auto-allgames','all','auto-favorites','favorites','auto-lastplayed','recent','custom-collections','collections','options')]:
    if theme and theme not in seen:
        seen.add(theme); nocover(brand(name,full)).save(f'{OUT}/nocover/{theme}.png')
print('nocover:',len(seen))
