#!/bin/bash
# 76 sayfayı 390 px genişlikte yükler, yatay taşmaları raporlar
R="$(cd "$(dirname "$0")/.." && pwd)"; S="${TMPDIR:-/tmp}/anahtar-mt"; mkdir -p "$S"
python3 - "$R" "$S" <<'PY'
import os,json,sys
R,S=sys.argv[1:3]
names=sorted(f[:-5] for f in os.listdir(R+'/pages') if f.endswith('.html') and f!='Kiraci-Ana-Sayfa.html')
s=open(R+'/tools/mobile_test.html').read().replace('PAGES',json.dumps(names)).replace("'../pages/'","'file://"+R+"/pages/'")
open(S+'/mt.html','w').write(s)
PY
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --allow-file-access-from-files --virtual-time-budget=120000 --dump-dom file://$S/mt.html 2>/dev/null > $S/out.html
python3 - "$S" <<'PY'
import re,json,html,sys
t=open(sys.argv[1]+'/out.html').read()
d=json.loads(html.unescape(re.search(r'<pre id="out">(.*?)</pre>',t,re.S).group(1)))
bad=[x for x in d if x.get('err') or x['w']>391]
print(len(d),'sayfa,',len(bad),'taşan')
for x in bad: print(x['n'],x.get('w'),x.get('nb'),x.get('bad') or x.get('err'))
PY
