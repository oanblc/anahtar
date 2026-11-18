#!/bin/bash
# Her sayfanın gerçek 390 px mobil görünümünü PNG olarak alır: tools/mobile_shots.sh <çıktı klasörü> [sayfa adları...]
R="$(cd "$(dirname "$0")/.." && pwd)"; O="${1:?çıktı klasörü}"; shift; mkdir -p "$O"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ $# -gt 0 ]; then L="$@"; else L=$(ls "$R/pages" | sed 's/\.html$//'); fi
for n in $L; do
  [ "$n" = Kiraci-Ana-Sayfa ] && continue
  echo "<!doctype html><body style='margin:0;background:#fff'><iframe src='file://$R/pages/$n.html' style='width:390px;height:1600px;border:0;display:block'></iframe>" > "$O/_w.html"
  "$CH" --headless --disable-gpu --hide-scrollbars --window-size=500,1600 --virtual-time-budget=4000 --screenshot="$O/$n.png" "file://$O/_w.html" >/dev/null 2>&1
done
