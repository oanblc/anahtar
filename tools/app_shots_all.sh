#!/bin/bash
# tüm app ekranlarının önizleme görüntüleri: app/onizleme/<ad>.png (birden çok .pair olanlar daha yüksek)
R="$(cd "$(dirname "$0")/.." && pwd)"; mkdir -p "$R/app/onizleme"
for f in "$R"/app/screens/*.html; do
  n=$(basename "$f" .html); c=$(grep -o 'class="pair' "$f" | wc -l | tr -d ' ')
  h=1000; [ "$c" -ge 2 ] && h=2050
  "$R/tools/app_shot.sh" "$n" "$R/app/onizleme/$n.png" $h
done
echo bitti
