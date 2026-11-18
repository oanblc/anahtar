#!/usr/bin/env python3
"""app/index.html: app/screens/*.html dosyalarını tarar, gruplayıp önizleme sayfası üretir.
Görseller app/onizleme/<ad>.png (tools/app_shot.sh ile alınır)."""
import re,html
from pathlib import Path
R=Path(__file__).resolve().parent.parent/'app'
def title(p):
    t=re.search(r'<title>(.*?)</title>',p.read_text(),re.S)
    t=(t.group(1) if t else p.stem).strip()
    t=re.sub(r'\s*[·|-]\s*Anahtar.*$','',t)
    return t
def clean(p):
    return html.escape(re.sub(r"^[MEA]\d+[a-z]?\s*","",title(p)))
def code(n): return re.match(r'([MEA]\d+[a-z]?)',n).group(1)
def num(n):
    m=re.match(r'([MEA])(\d+)([a-z]?)',n); return ({'M':0,'A':1,'E':2}[m.group(1)],int(m.group(2)),m.group(3),n)
GR=[("Uygulama kabuğu ve sistem",lambda c,n:c=='M' and n<=7),
("Kayıt, kimlik ve güvenlik kurulumu",lambda c,n:c=='M' and (8<=n<=20)),
("Kiracı",lambda c,n:c=='M' and (21<=n<=41 or n==62)),
("Ev sahibi",lambda c,n:c=='M' and (42<=n<=58)),
("Ortak ayarlar ve yüzeyler",lambda c,n:c=='M' and (59<=n<=70) and n!=62),
("Danışman uygulaması",lambda c,n:c=='A'),
("Danışmanlı dosya: kiracı ve ev sahibi onayları",lambda c,n:c=='M' and n>=71),
("Uç durumlar: ödeme",lambda c,n:c=='E' and n<=17),
("Uç durumlar: kayıt, hesap ve NFC",lambda c,n:c=='E' and (18<=n<=30 or 68<=n<=70)),
("Uç durumlar: sözleşme, IBAN ve davet",lambda c,n:c=='E' and 31<=n<=43),
("Uç durumlar: bildirim, cihaz ve ağ",lambda c,n:c=='E' and 44<=n<=67),
("Uç durumlar: danışman akışı",lambda c,n:c=='E' and n>=71)]
files=sorted((p for p in (R/'screens').glob('*.html')),key=lambda p:num(p.stem))
used=set();sec='';total=0
for t,f in GR:
    cards=''
    for p in files:
        c=p.stem[0]; n=num(p.stem)[1]
        if p.stem in used or not f(c,n): continue
        used.add(p.stem);total+=1
        img=f'onizleme/{p.stem}.png'
        cards+=f'<a class="c" href="screens/{p.name}"><img loading="lazy" src="{img}" alt=""><span class="t"><b>{code(p.stem)}</b> {clean(p)}</span></a>'
    if cards: sec+=f'<section><h2>{t}</h2><div class="g">{cards}</div></section>'
(R/'index.html').write_text(f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Anahtar Uygulama Ekranları</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap">
<style>*{{box-sizing:border-box}}body{{margin:0;background:#EAF2FA;font-family:'Plus Jakarta Sans',sans-serif;color:#1D3650}}a{{color:inherit;text-decoration:none}}
.w{{max-width:1368px;margin:0 auto;padding:32px 24px}}h1{{font:800 40px/1.1 'Bricolage Grotesque';letter-spacing:-.03em;color:#2B5078;margin:0 0 8px}}p{{margin:0;color:#3F5A75;line-height:1.6;max-width:760px}}
h2{{font:700 24px 'Bricolage Grotesque';color:#2B5078;margin:36px 0 14px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.c{{background:#fff;border-radius:24px;overflow:hidden;display:flex;flex-direction:column;border:1.5px solid transparent;transition:.15s}}.c:hover{{border-color:#A8CBE8;transform:translateY(-3px)}}
.c img{{width:100%;aspect-ratio:1/0.82;object-fit:cover;object-position:top;background:#C9D6E3;display:block}}.t{{padding:14px 16px 16px;font-size:14.5px;line-height:1.4}}
.back{{display:inline-block;margin-bottom:18px;font-weight:600;color:#2B5078;text-decoration:underline}}</style></head><body><div class="w">
<a class="back" href="../index.html">Site haritasına dön</a><h1>Uygulama: {total} ekran ve uç durum</h1>
<p>iOS ve Android çerçevelerinde yan yana. M kodlu kartlar ekranlar, E kodlu kartlar uç durumlardır. Karta tıklayınca ekranın canlı HTML sürümü açılır. Fotoğraf alanlarındaki açık mavi kutular, henüz üretilmemiş görsellerin yer tutucusudur.</p>{sec}</div></body></html>''')
print('ok',total,'kullanılmayan:',[p.stem for p in files if p.stem not in used])
