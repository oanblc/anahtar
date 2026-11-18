#!/bin/bash
# app/screens/<ad>.html -> PNG: tools/app_shot.sh <ad> <çıktı.png> [yükseklik]
R="$(cd "$(dirname "$0")/.." && pwd)"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=1000,${3:-1000} --virtual-time-budget=4000 --screenshot="$2" "file://$R/app/screens/$1.html" >/dev/null 2>&1
