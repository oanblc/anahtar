#!/bin/bash
# usage: measure.sh file1.dc.html file2.dc.html ...  -> prints "file height" (viewport 1440 wide)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
for f in "$@"; do
  b=$(basename "$f" .dc.html)
  python3 -I - "$f" "$TMP/$b.html" <<'PY'
import sys
s=open(sys.argv[1],encoding='utf-8').read()
inj="<script>window.addEventListener('load',function(){(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){setTimeout(function(){var d=document.querySelector('x-dc > div');document.title='H='+Math.round(d.getBoundingClientRect().height)},400)})})</script>"
s=s.replace('</body>',inj+'</body>')
open(sys.argv[2],'w',encoding='utf-8').write(s)
PY
  out=$("$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1000 --virtual-time-budget=8000 --dump-dom "file://$TMP/$b.html" 2>/dev/null | grep -o '<title>H=[0-9]*' | head -1)
  echo "$b ${out#<title>H=}"
done
rm -rf "$TMP"
