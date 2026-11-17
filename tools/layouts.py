# One small file a system in layouts/: the layout of its covers. Move a system to LANDSCAPE and run it again.
import sys,os
OUT,SYSLIST=sys.argv[1:3]
LANDSCAPE={'snes','sfc','snes-usa','snes-hacks','snesh','snesmsu1','sufami','satellaview','n64','n64dd'}
names={l.split('|')[2] for l in open(SYSLIST).read().splitlines() if l.count('|')==2 and l.split('|')[2]}
names|={'default','auto-allgames','all','auto-favorites','favorites','auto-lastplayed','recent','custom-collections','collections','retropie','options'}
for t in sorted(names):
    lay='landscape' if t in LANDSCAPE else 'portrait'
    open(os.path.join(OUT,'layouts',t+'.xml'),'w').write(f'<theme>\n\t<formatVersion>3</formatVersion>\n\t<include>./{lay}.xml</include>\n</theme>\n')
print(len(names),'systems;',len(LANDSCAPE & names),'landscape:',', '.join(sorted(LANDSCAPE & names)))
