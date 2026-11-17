# Name:        gen16.py
# Description: 16-Bit-Minigen's art, drawn from nothing but its fonts: the backgrounds (art/), a cartridge for each system
#              (carts/, its own illustration from src-art/ if there is one) and the game lists' headers (headers/)
# Usage:       python3 tools/gen16.py . fonts tools/systems.txt    (from the theme's folder)
import os,sys,shutil,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
OUT,FONTS,SYSLIST=sys.argv[1:4]
W,H=640,480
os.makedirs(OUT+'/art',exist_ok=True); os.makedirs(OUT+'/carts',exist_ok=True); os.makedirs(OUT+'/headers',exist_ok=True); os.makedirs(OUT+'/stripes',exist_ok=True); os.makedirs(OUT+'/fonts',exist_ok=True)
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

# ---- the horizon in a cartridge (and in NO COVER): the sky in the system's first colour, the sun a gradient through
# its three colours left to right, the grid in its second; or an icon of its own for what is not a console
def mix(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def lift(c,k=1.15,add=30): return tuple(min(255,int(v*k+add)) for v in c)
def gradient3(cs,t): return mix(cs[0],cs[1],t*2) if t<0.5 else mix(cs[1],cs[2],(t-0.5)*2)
ICONS={'retropie':'gear','options':'gear','retroarch':'pad','ports':'joystick','auto-allgames':'stack','all':'stack',
 'auto-favorites':'star','favorites':'star','auto-lastplayed':'clock','recent':'clock','custom-collections':'folder',
 'collections':'folder','vhs':'tape'}
def icon(d,kind,cx,cy,r,c,bg):
    import math as m
    if kind=='gear':
        pts=[]
        for k in range(48):
            a=k*m.pi/24; rr=r if (k//3)%2==0 else r*0.78; pts.append((cx+rr*m.cos(a),cy+rr*m.sin(a)))
        d.polygon(pts,fill=c); d.ellipse([cx-r*0.36,cy-r*0.36,cx+r*0.36,cy+r*0.36],fill=bg)
    elif kind=='pad':
        d.rounded_rectangle([cx-r*1.2,cy-r*0.55,cx+r*1.2,cy+r*0.55],radius=int(r*0.5),fill=c)
        for dx,dy,ww,hh in ((-0.72,0,0.42,0.14),(-0.72,0,0.14,0.42)): d.rectangle([cx+(dx-ww/2)*r,cy+(dy-hh/2)*r,cx+(dx+ww/2)*r,cy+(dy+hh/2)*r],fill=bg)
        for dx,dy in ((0.55,-0.15),(0.85,0.12)): d.ellipse([cx+(dx-0.12)*r,cy+(dy-0.12)*r,cx+(dx+0.12)*r,cy+(dy+0.12)*r],fill=bg)
    elif kind=='joystick':
        d.rounded_rectangle([cx-r,cy+r*0.25,cx+r,cy+r*0.75],radius=int(r*0.2),fill=c)
        d.rectangle([cx-r*0.09,cy-r*0.5,cx+r*0.09,cy+r*0.3],fill=c); d.ellipse([cx-r*0.32,cy-r*0.95,cx+r*0.32,cy-r*0.3],fill=c)
        d.ellipse([cx+r*0.45,cy+r*0.02,cx+r*0.75,cy+r*0.3],fill=c)
    elif kind=='star':
        pts=[(cx+(r if k%2==0 else r*0.42)*m.cos(-m.pi/2+k*m.pi/5),cy+(r if k%2==0 else r*0.42)*m.sin(-m.pi/2+k*m.pi/5)) for k in range(10)]
        d.polygon(pts,fill=c)
    elif kind=='clock':
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c); d.ellipse([cx-r*0.8,cy-r*0.8,cx+r*0.8,cy+r*0.8],fill=bg)
        d.line([(cx,cy),(cx,cy-r*0.6)],fill=c,width=max(2,int(r*0.14))); d.line([(cx,cy),(cx+r*0.45,cy+r*0.15)],fill=c,width=max(2,int(r*0.14)))
    elif kind=='stack':
        for k in range(3):
            o=(1-k)*r*0.28; d.rounded_rectangle([cx-r*0.55+o,cy-r*0.75+o,cx+r*0.45+o,cy+r*0.75+o],radius=3,fill=c,outline=bg,width=2)
    elif kind=='folder':
        d.rounded_rectangle([cx-r,cy-r*0.55,cx-r*0.1,cy-r*0.3],radius=3,fill=c); d.rounded_rectangle([cx-r,cy-r*0.4,cx+r,cy+r*0.65],radius=4,fill=c)
    elif kind=='tape':
        d.rounded_rectangle([cx-r*1.2,cy-r*0.65,cx+r*1.2,cy+r*0.65],radius=4,fill=c)
        for dx in (-0.55,0.55): d.ellipse([cx+(dx-0.28)*r,cy-r*0.28,cx+(dx+0.28)*r,cy+r*0.28],fill=bg)
        d.rectangle([cx-r*0.27,cy-r*0.12,cx+r*0.27,cy+r*0.12],fill=bg)
def horizon(aw,ah,theme,col,big=1.0):
    cs=stripes(theme) if theme in INFO and INFO[theme][1] else [col,lift(col),col]
    sky,grid=cs[0],cs[1] if sum(cs[1])>90 else lift(cs[1],1,80)
    art=Image.new('RGB',(aw,ah),(0,0,0)); ad=ImageDraw.Draw(art)
    hz=int(ah*0.45)
    for y in range(hz): t=y/hz; ad.line([(0,y),(aw,y)],fill=tuple(int(sky[i]*(0.10+0.5*t)) for i in range(3)))
    if theme in ICONS:    # an icon of its own over the horizon, in the third colour
        icon(ad,ICONS[theme],aw/2,hz*0.55,min(aw,hz)*0.33*big,lift(cs[2],1,0) if sum(cs[2])>200 else lift(cs[2]),tuple(int(sky[i]*0.3) for i in range(3)))
    else:                 # the sun: the three colours left to right
        r=int(38*big); sun=Image.new('RGB',(2*r+1,2*r+1)); sd=ImageDraw.Draw(sun)
        for x in range(2*r+1): sd.line([(x,0),(x,2*r)],fill=lift(gradient3(cs,x/(2*r)),1.08,18))
        m=Image.new('L',sun.size,0); ImageDraw.Draw(m).ellipse([0,0,2*r,2*r],fill=255); art.paste(sun,(aw//2-r,hz-r),m)
        for i in range(4): ad.line([(0,hz-int(14*big)-i*int(7*big)),(aw,hz-int(14*big)-i*int(7*big))],fill=tuple(int(sky[j]*0.2) for j in range(3)),width=max(2,int(2*big)))
    ad.rectangle([0,hz,aw,ah],fill=(6,6,10))
    for x in range(-aw*2,aw*3,22): ad.line([(aw/2+(x-aw/2)*0.12,hz),(x,ah)],fill=grid)
    for i in range(1,9): y=hz+(i**1.8)*2.4*ah/206; ad.line([(0,y),(aw,y)],fill=grid)
    return art
def stripe_band(theme):    # the console top's corners: the system's three stripes (stripes/, over the background)
    im=Image.new('RGBA',(W,40),(0,0,0,0)); d=ImageDraw.Draw(im); cs=stripes(theme)
    for i,c in enumerate(cs): d.polygon([(18+i*14,10),(28+i*14,10),(20+i*14,32),(10+i*14,32)],fill=c)
    for i,c in enumerate(reversed(cs)): d.polygon([(W-30-i*14,10),(W-20-i*14,10),(W-28-i*14,32),(W-38-i*14,32)],fill=c)
    return im
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
    art=horizon(w-48,h-130,theme,col)
    aw,ah=art.size
    src=os.path.join(OUT,'src-art',theme+'.png')    # an illustration of its own (src-art/), else the drawn horizon
    if theme and os.path.isfile(src):
        a=Image.open(src).convert('RGB'); s=max(aw/a.width,ah/a.height)
        a=a.resize((round(a.width*s),round(a.height*s)),Image.LANCZOS)
        art=a.crop(((a.width-aw)//2,(a.height-ah)//2,(a.width-aw)//2+aw,(a.height-ah)//2+ah))
    im.paste(art,(40,76)); d=ImageDraw.Draw(im)
    d.rectangle([40,h-52,w-8,h-10],fill=(0,0,0)); d.rectangle([40,h-52,w-8,h-49],fill=stripes(theme)[0])
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
    stripe_band(theme).save(f'{OUT}/stripes/{theme}.png')
    cart(full,col,theme).save(f'{OUT}/carts/{theme}.png'); header(full).save(f'{OUT}/headers/{theme}.png')
print('sistemas:',len(seen))
