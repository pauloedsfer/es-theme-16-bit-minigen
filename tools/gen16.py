# Name:        gen16.py
# Description: 16-Bit-Minigen's art, drawn from nothing but its fonts: the backgrounds (art/), a cartridge for each system
#              (carts/, its own illustration from src-art/ if there is one) and the game lists' headers (headers/)
# Usage:       python3 tools/gen16.py . fonts tools/systems.txt    (from the theme's folder)
import os,sys,shutil,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
OUT,FONTS,SYSLIST=sys.argv[1:4]
W,H=640,480
os.makedirs(OUT+'/art',exist_ok=True); os.makedirs(OUT+'/carts',exist_ok=True); os.makedirs(OUT+'/headers',exist_ok=True); os.makedirs(OUT+'/fonts',exist_ok=True)
if os.path.abspath(FONTS)!=os.path.abspath(OUT+'/fonts'):    # (the fonts are in the theme already: fonts/)
    for f in ['Orbitron-Black.ttf','Orbitron-Bold.ttf','Exo2-SemiBold.ttf','Exo2-ExtraBold.ttf','OFL-Orbitron.txt','OFL-Exo2.txt']: shutil.copy(f'{FONTS}/{f}',f'{OUT}/fonts/')
F=lambda n,px:ImageFont.truetype(f'{OUT}/fonts/{n}.ttf',px)
BLUE=(29,79,196); RED=(200,16,46); GOLD=(255,199,44); SILVER=(214,216,224)
def vgrad(w,h,top,bot):
    im=Image.new('RGB',(w,h)); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/max(1,h-1); d.line([(0,y),(w,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    return im
def chrome_text(txt,font,shear=0.18,h_target=None):
    b=font.getbbox(txt); w,h=b[2]-b[0]+8,b[3]-b[1]+8
    mask=Image.new('L',(w,h),0); ImageDraw.Draw(mask).text((4-b[0],4-b[1]),txt,font=font,fill=255)
    g=vgrad(w,h,(255,255,255),(150,155,170)); d=ImageDraw.Draw(g); d.line([(0,h//2),(w,h//2)],fill=(110,115,130))
    out=Image.new('RGBA',(w,h),(0,0,0,0)); out.paste(g,(0,0),mask)
    sh=Image.new('RGBA',(w+6,h+4),(0,0,0,0)); sh.paste((0,0,0,255),(3,3),mask); sh=sh.filter(ImageFilter.GaussianBlur(1.2)); sh.alpha_composite(out,(0,0))
    if shear: sh=sh.transform((int(sh.width+shear*sh.height),sh.height),Image.AFFINE,(1,shear,-shear*sh.height,0,1,0),Image.BICUBIC)
    return sh
# ---------- background (the console's top, a grid floor, the panels, the bottom bar)
def background(system=False,split=394):    # split: where the list's panel ends and the cover's begins
    im=vgrad(W,H,(16,16,20),(4,4,6)); d=ImageDraw.Draw(im,'RGBA')
    for x in range(-W,2*W,32): d.line([(W/2+(x-W/2)*0.35,64),(x,H)],fill=(255,255,255,10))
    for i in range(14): y=64+(i**1.6)*3.2; d.line([(0,y),(W,y)],fill=(255,255,255,9))
    d.polygon([(0,0),(W,0),(W,40),(470,40),(440,66),(200,66),(170,40),(0,40)],fill=(28,28,34))
    d.line([(0,40),(170,40),(200,66),(440,66),(470,40),(W,40)],fill=(90,92,104),width=2)
    d.line([(0,43),(168,43),(198,69),(442,69),(472,43),(W,43)],fill=(0,0,0),width=2)
    d.rounded_rectangle([262,3,378,19],radius=7,fill=(200,202,210)); f=F('Orbitron-Bold',9)
    d.text((272,6),'POWER',font=f,fill=(30,30,36)); d.ellipse([318,6,328,16],fill=RED,outline=(120,0,10)); d.line([(332,11),(342,11)],fill=(30,30,36)); d.text((345,6),'ON',font=f,fill=(30,30,36))
    for i,c in enumerate([RED,GOLD,BLUE]): d.polygon([(18+i*14,10),(28+i*14,10),(20+i*14,32),(10+i*14,32)],fill=c)
    for i,c in enumerate([BLUE,GOLD,RED]): d.polygon([(W-30-i*14,10),(W-20-i*14,10),(W-28-i*14,32),(W-38-i*14,32)],fill=c)
    if not system:
        d.rounded_rectangle([14,94,split,394],radius=6,fill=(0,0,0,150),outline=(70,72,84),width=2)
        d.rounded_rectangle([split+10,94,626,394],radius=6,fill=(0,0,0,150),outline=(70,72,84),width=2)
    pill=vgrad(612,52,(236,237,242),(176,179,190)); m=Image.new('L',(612,52),0); ImageDraw.Draw(m).rounded_rectangle([0,0,611,51],radius=26,fill=255)
    im.paste(pill,(14,406),m); d=ImageDraw.Draw(im,'RGBA'); d.rounded_rectangle([14,406,625,457],radius=26,outline=(90,92,104),width=2)
    for cx in (40,600): d.ellipse([cx-9,422,cx+9,440],fill=(250,250,252),outline=(120,122,134))
    if not system:
        d.rounded_rectangle([552,412,586,451],radius=4,fill=BLUE,outline=(255,255,255),width=2)
    return im
background().save(OUT+'/art/bg_gamelist.png'); background(False,326).save(OUT+'/art/bg_gamelist_wide.png'); background(True).save(OUT+'/art/bg_system.png')
# ---------- the systems: brand colours, a cartridge and a header each
rows=[l.split('|') for l in open(SYSLIST).read().splitlines() if l.count('|')==2]
def brand(name,full):
    s=(name+' '+full).lower()
    for keys,c in [(('sega','megadrive','genesis','mastersystem','gamegear','32x','segacd','dreamcast','saturn','sg-1000','sg1000','msumd','pico','naomi','atomiswave','vmu'),BLUE),
        (('nes','snes','famicom','nintendo','gb','gba','gbc','n64','nds','virtualboy','pokemon','sgb','sufami','satellaview','fds'),RED),
        (('psx','psp','playstation','sony'),(70,90,120)),(('pcengine','tg16','tg-cd','supergrafx','pcfx','turbografx','nec','pc98'),(230,110,20)),
        (('neogeo','ngp','snk'),GOLD),(('atari','lynx','jaguar'),(205,70,30)),(('cps','mame','arcade','fba','fbneo','capcom','alg','daphne'),(130,40,170))]:
        if any(k in s for k in keys): return c
    return (20,140,130)
BITS={'8-BIT':('nes','famicom','fds','mastersystem','gamegear','sg-1000','gb','gbc','sgb','pokemini','pokemonmini','atari2600','atari7800','colecovision','intellivision','msx','msx2','ngp','ngpc','wonderswan','wonderswancolor','supervision','megaduck','arduboy','channelf','odyssey2','videopac'),
 '16-BIT':('megadrive','genesis','snes','sfc','snes-usa','snes-hacks','snesh','pcengine','tg16','supergrafx','neogeo','neogeocd','segacd','megacd','msumd','snesmsu1','sufami','satellaview','x68000','amiga','atarist','cps1','cps2','pico','lynx','pcenginecd','tg-cd'),
 '32-BIT':('psx','saturn','sega32x','32x','3do','gba','pcfx','cps3','atarijaguar','amigacd32','virtualboy'),
 '64-BIT':('n64','n64dd'),'128-BIT':('dreamcast','naomi','atomiswave')}
INFO={}    # tools/system_info.txt: theme|bits|generation|year|three stripe colours
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'system_info.txt'),encoding='utf-8'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    t,b,g,y,c=(line.split('|')+['']*5)[:5]
    INFO[t]=([x for x in (b,g,y) if x],[tuple(int(h[i:i+2],16) for i in (0,2,4)) for h in c.split(',')] if c else None)
def side_label(theme):    # what the cartridge's side says: 16-BIT - 4TH GEN - 1989
    return ' - '.join(INFO[theme][0]) if theme in INFO else bits(theme)
def stripes(theme):
    return INFO[theme][1] if theme in INFO and INFO[theme][1] else [RED,GOLD,BLUE]
def bits(theme):
    for k,v in BITS.items():
        if theme in v: return k
    return ''
def cart(full,col,theme=''):
    w,h=240,336; im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=8,fill=(12,12,15),outline=(110,112,124),width=2)
    band=vgrad(30,h-8,(70,72,82),(30,31,36)); im.paste(band,(4,4)); d=ImageDraw.Draw(im)
    label=side_label(theme); px=17
    while px>9 and F('Orbitron-Black',px).getlength(label)>h-28: px-=1    # (the longest still fits the side)
    t=Image.new('RGBA',(h-8,30),(0,0,0,0)); ImageDraw.Draw(t).text((10,15),label,font=F('Orbitron-Black',px),fill=(200,202,212),anchor='lm')
    t=t.rotate(90,expand=True); im.alpha_composite(t,(4,4))
    d.rectangle([40,8,w-8,70],fill=(0,0,0)); 
    words=full.upper().split(); lines=[];cur=''
    for wd in words:
        if F('Orbitron-Black',22).getlength((cur+' '+wd).strip())<w-60: cur=(cur+' '+wd).strip()
        else: lines.append(cur); cur=wd
    lines.append(cur); lines=[l for l in lines if l][:3]
    px=22 if len(lines)<3 else 17
    for i,l in enumerate(lines):
        ct=chrome_text(l,F('Orbitron-Black',px),0.12)
        if ct.width>w-56: ct=ct.resize((w-56,int(ct.height*(w-56)/ct.width)),Image.LANCZOS)
        y=39-len(lines)*ct.height//2+i*ct.height; im.alpha_composite(ct,(40+(w-48-ct.width)//2,max(8,y)))
    art=Image.new('RGB',(w-48,h-130),(0,0,0)); ad=ImageDraw.Draw(art)
    aw,ah=art.size; hz=int(ah*0.45)
    for y in range(hz): t=y/hz; ad.line([(0,y),(aw,y)],fill=tuple(int(col[i]*(0.15+0.6*t)) for i in range(3)))
    ad.ellipse([aw/2-38,hz-38,aw/2+38,hz+38],fill=tuple(min(255,int(c*1.2+40)) for c in col))
    ad.rectangle([0,hz,aw,ah],fill=(6,6,10))
    for x in range(-aw*2,aw*3,22): ad.line([(aw/2+(x-aw/2)*0.12,hz),(x,ah)],fill=col)
    for i in range(1,9): y=hz+(i**1.8)*2.4; ad.line([(0,y),(aw,y)],fill=col)
    for i in range(4): ad.line([(0,hz-14-i*7),(aw,hz-14-i*7)],fill=(6,6,10),width=2)
    src=os.path.join(OUT,'src-art',theme+'.png')    # an illustration of its own (src-art/), else the drawn horizon
    if theme and os.path.isfile(src):
        a=Image.open(src).convert('RGB'); s=max(aw/a.width,ah/a.height)
        a=a.resize((round(a.width*s),round(a.height*s)),Image.LANCZOS)
        art=a.crop(((a.width-aw)//2,(a.height-ah)//2,(a.width-aw)//2+aw,(a.height-ah)//2+ah))
    im.paste(art,(40,76)); d=ImageDraw.Draw(im)
    d.rectangle([40,h-52,w-8,h-10],fill=(0,0,0)); d.rectangle([40,h-52,w-8,h-49],fill=col)
    for i,c in enumerate(stripes(theme)): d.polygon([(w-70+i*14,h-42),(w-60+i*14,h-42),(w-66+i*14,h-18),(w-76+i*14,h-18)],fill=c)
    return im
def header(full):
    ct=chrome_text(full.upper(),F('Orbitron-Black',30),0.18)
    if ct.width>300: ct=ct.resize((300,int(ct.height*300/ct.width)),Image.LANCZOS)
    return ct
seen=set()
COLLECTIONS=[(t,n,t) for t,n in [('auto-allgames','All Games'),('all','All Games'),('auto-favorites','Favorites'),('favorites','Favorites'),
 ('auto-lastplayed','Last Played'),('recent','Last Played'),('custom-collections','Collections'),('collections','Collections'),('options','Options')]]
for name,full,theme in rows+COLLECTIONS+[('default','16-Bit-Minigen','default')]:
    if theme in seen or not theme: continue
    seen.add(theme); col=brand(name,full)
    cart(full,col,theme).save(f'{OUT}/carts/{theme}.png'); header(full).save(f'{OUT}/headers/{theme}.png')
print('sistemas:',len(seen))
