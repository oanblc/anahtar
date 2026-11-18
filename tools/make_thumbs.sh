#!/bin/bash
# Her sayfanın ilk ekranından küçük önizleme üretir (Google Chrome gerekir).
# Kullanım: tools/make_thumbs.sh [sayfa adı ...]   (boşsa hepsi)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ $# -gt 0 ]; then LIST="$@"; else LIST=$(ls pages | sed 's/\.html$//'); fi
for n in $LIST; do
  W=1440; H=900
  [ "$n" = "Kiraci-Ana-Sayfa" ] && { W=390; H=844; }
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=$W,$H --virtual-time-budget=6000 \
    --screenshot="/tmp/thumb-$n.png" "file://$ROOT/pages/$n.html" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 70 --resampleWidth 560 "/tmp/thumb-$n.png" --out "assets/thumbs/$n.jpg" >/dev/null 2>&1
  rm -f "/tmp/thumb-$n.png"
done
echo "tamam: $(ls assets/thumbs | wc -l) önizleme"
