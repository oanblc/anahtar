#!/usr/bin/env python3
"""app/index.html: Tur 1 ekranlarının önizleme sayfası (görseller app/onizleme/*.png)."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent/'app'
G=[("Kayıt ve kimlik doğrulama",[("M08-giris","M08","Giriş"),("M09-kayit","M09","Kayıt, adım 1"),("M10-telefon-dogrulama","M10","Telefon doğrulama"),("M11a-nfc-bilgi","M11a","Kimlik doğrulama: NFC bilgileri"),("M11b-nfc-okuma","M11b","Kimlik doğrulama: NFC okuma"),("M14-dogrulama-sonucu","M14","Doğrulama sonucu")]),
("Kiracı: ana sayfa ve ödeme",[("M21-kiraci-ana-sayfa","M21","Ana sayfa"),("M22-odeme-ozeti","M22","Ödeme özeti"),("M23-kart-secimi","M23","Kart seçimi"),("M24-3d-secure","M24","3D Secure"),("M25-odeme-sonucu","M25","Ödeme sonucu")]),
("Ev sahibi",[("M42-ev-sahibi-ana-sayfa","M42","Ana sayfa"),("M47-sozlesme-yukle","M47","Sözleşme yükleme"),("M48-sozlesme-durumu","M48","Sözleşme durumu"),("M49-iban","M49","Hesap ve IBAN")])]
sec=''
for t,items in G:
    cards=''.join(f'<a class="c" href="screens/{f}.html"><img loading="lazy" src="onizleme/{f}.png" alt=""><span class="t"><b>{n}</b> {h}</span><span class="d">iOS ve Android</span></a>' for f,n,h in items)
    sec+=f'<section><h2>{t}</h2><div class="g">{cards}</div></section>'
n=sum(len(i) for _,i in G)
(R/'index.html').write_text(f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Anahtar Uygulama Tur 1</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap">
<style>*{{box-sizing:border-box}}body{{margin:0;background:#EAF2FA;font-family:'Plus Jakarta Sans',sans-serif;color:#1D3650}}a{{color:inherit;text-decoration:none}}
.w{{max-width:1368px;margin:0 auto;padding:32px 24px}}h1{{font:800 40px/1.1 'Bricolage Grotesque';letter-spacing:-.03em;color:#2B5078;margin:0 0 8px}}p{{margin:0;color:#3F5A75;line-height:1.6;max-width:720px}}
h2{{font:700 24px 'Bricolage Grotesque';color:#2B5078;margin:36px 0 14px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.c{{background:#fff;border-radius:24px;overflow:hidden;display:flex;flex-direction:column;border:1.5px solid transparent;transition:.15s}}.c:hover{{border-color:#A8CBE8;transform:translateY(-3px)}}
.c img{{width:100%;aspect-ratio:1/0.82;object-fit:cover;object-position:top;background:#C9D6E3;display:block}}.t{{padding:14px 16px 2px;font-size:15px}}.d{{padding:0 16px 14px;font-size:13px;color:#536C87}}
.back{{display:inline-block;margin-bottom:18px;font-weight:600;color:#2B5078;text-decoration:underline}}</style></head><body><div class="w">
<a class="back" href="../index.html">Site haritasına dön</a><h1>Uygulama, Tur 1: {n} ekran</h1>
<p>iOS ve Android çerçevelerinde yan yana. Bir karta tıklayınca ekranın canlı HTML sürümü açılır. Uç durumlar ve kalan ekranlar onayınızdan sonra gelir.</p>{sec}</div></body></html>''')
print('ok',n)
