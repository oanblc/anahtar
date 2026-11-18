#!/usr/bin/env python3
"""tools/pages.json -> index.html (site haritası)"""
import json, html
from pathlib import Path
root = Path(__file__).resolve().parent.parent
data = json.loads((root/'tools/pages.json').read_text())
total = sum(len(g['pages']) for g in data)
def card(p):
    tags = ''.join('<span class="tag">%s</span>' % html.escape(t) for t in p['tags'])
    q = html.escape((p['title']+' '+p['desc']+' '+' '.join(p['tags'])).lower())
    return ('<a class="card" href="pages/%s.html" data-q="%s"><span class="thumb"><img loading="lazy" src="assets/thumbs/%s.jpg" alt=""></span>'
            '<span class="body"><span class="t">%s</span><span class="d">%s</span><span class="tags">%s</span></span></a>') % (
            p['file'], q, p['file'], html.escape(p['title']), html.escape(p['desc']), tags)
secs = ''
nav = ''
for i,g in enumerate(data):
    sid = 'g%d'%i
    nav += '<a href="#%s">%s <b>%d</b></a>' % (sid, html.escape(g['title']), len(g['pages']))
    secs += '<section id="%s"><div class="sh"><h2>%s</h2><p>%s</p></div><div class="grid">%s</div></section>' % (
        sid, html.escape(g['title']), html.escape(g['note']), ''.join(card(p) for p in g['pages']))
out = '''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anahtar Site Haritası</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<style>
*{box-sizing:border-box}body{margin:0;background:#EAF2FA;font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:#1D3650}
a{color:inherit;text-decoration:none}
.wrap{max-width:1368px;margin:0 auto;padding:24px}
header.top{display:flex;justify-content:space-between;align-items:center;padding:8px 8px 24px}
.logo{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:28px;letter-spacing:-.03em;color:#2B5078}.logo i{font-style:normal;color:#5489C6}
.hero{background:#2B5078;color:#fff;border-radius:40px;padding:48px;display:flex;flex-direction:column;gap:14px}
.hero h1{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:44px;line-height:1.08;letter-spacing:-.035em;max-width:760px}
.hero p{margin:0;font-size:16px;line-height:1.65;color:#D3E3F2;max-width:760px}
.hero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}
.btn{background:#D3F26A;color:#1D3650;font-weight:700;padding:14px 22px;border-radius:999px;font-size:15px}
.btn.alt{background:transparent;border:1.5px solid #A8CBE8;color:#fff}
.bar{position:sticky;top:0;z-index:5;background:#EAF2FA;padding:16px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.bar input{flex:1;min-width:240px;font:inherit;font-size:15px;padding:13px 18px;border-radius:999px;border:1.5px solid #CBDDEF;background:#fff;color:#1D3650;outline:none}
.bar input:focus{border-color:#2B5078}
.nav{display:flex;gap:8px;flex-wrap:wrap}
.nav a{font-size:13px;font-weight:600;color:#2B5078;background:#fff;border:1.5px solid #CBDDEF;padding:9px 14px;border-radius:999px}
.nav a b{color:#5489C6;font-weight:700;margin-left:4px}
section{margin-top:28px;scroll-margin-top:90px}
.sh{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:14px}
.sh h2{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:26px;letter-spacing:-.02em;color:#2B5078}
.sh p{margin:0;font-size:14px;color:#536C87}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.card{background:#fff;border-radius:24px;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s;border:1.5px solid transparent}
.card:hover{transform:translateY(-3px);box-shadow:0 24px 40px -28px rgba(43,80,120,.6);border-color:#A8CBE8}
.thumb{display:block;aspect-ratio:16/10;background:#DCE8F3;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.body{display:flex;flex-direction:column;gap:6px;padding:14px 16px 16px}
.t{font-weight:700;font-size:15px;color:#1D3650}.d{font-size:13px;line-height:1.5;color:#536C87}
.tags{display:flex;gap:6px;flex-wrap:wrap}.tag{font-size:11.5px;font-weight:600;color:#1D3650;background:#D3F26A;padding:3px 9px;border-radius:999px}
.hidden{display:none!important}.empty{display:none;padding:40px;text-align:center;color:#536C87}
footer{padding:36px 8px;font-size:13px;line-height:1.7;color:#536C87}
@media(max-width:700px){.hero{padding:28px;border-radius:28px}.hero h1{font-size:30px}}
</style></head><body><div class="wrap">
<header class="top"><a class="logo" href="index.html">anahtar<i>.</i></a><span style="font-size:14px;font-weight:600;color:#536C87">Site haritası · @@TOTAL@@ sayfa</span></header>
<div class="hero"><h1>Tüm sayfalar tek yerde.</h1>
<p>Kiracı, ev sahibi, yönetim ve kurumsal paneller dahil @@TOTAL@@ sayfa aşağıda gruplandı. Bir karta tıklayarak sayfayı açabilirsiniz. Sayfalar telefon genişliğinde de çalışır; tarayıcı pencerenizi daraltarak ya da telefondan açarak mobil görünümü inceleyebilirsiniz.</p>
<div class="row"><a class="btn" href="pages/Main.html">Anasayfayı aç</a><a class="btn alt" href="app/index.html">Mobil uygulama ekranları</a><a class="btn alt" href="pages/Ucretler.html">Ücret hesaplayıcı</a></div></div>
<div class="bar"><input id="q" type="search" placeholder="Sayfa ara: ödeme, depozito, sözleşme…" aria-label="Sayfa ara"><nav class="nav">@@NAV@@</nav></div>
@@SECS@@
<div class="empty" id="empty">Aramanızla eşleşen sayfa bulunamadı.</div>
<footer>Sayfalar bağımsız HTML dosyalarıdır (masaüstü ve mobil düzen aynı dosyada); yazı tipleri için internet bağlantısı gerekir. Yönetim ve kurumsal sayfalar iç kullanım içindir, genel sitede yer almaz. Yasal metinler taslaktır.</footer>
</div>
<script>
var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card')),secs=[].slice.call(document.querySelectorAll('section'));
q.addEventListener('input',function(){var v=q.value.trim().toLocaleLowerCase('tr-TR'),n=0;
cards.forEach(function(c){var ok=!v||c.dataset.q.indexOf(v)>-1;c.classList.toggle('hidden',!ok);if(ok)n++});
secs.forEach(function(s){s.classList.toggle('hidden',!s.querySelector('.card:not(.hidden)'))});
document.getElementById('empty').style.display=n?'none':'block'});
</script></body></html>'''
out = out.replace('@@TOTAL@@', str(total)).replace('@@NAV@@', nav).replace('@@SECS@@', secs)
(root/'index.html').write_text(out, encoding='utf-8')
print('index.html yazıldı', total)
