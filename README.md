# Anahtar Web (statik sayfalar)

Online kira ödeme platformu için 76 masaüstü sayfası (1440 px). Mobil tasarımlar henüz yok.

## Açma
- `index.html` dosyasını tarayıcıda açın (site haritası; tüm sayfalara buradan gidilir).
- İsterseniz bu klasörde `python3 -m http.server 8765` çalıştırıp http://localhost:8765 adresine gidin.
- Yazı tipleri (Bricolage Grotesque, Plus Jakarta Sans) Google Fonts'tan yüklenir, internet gerekir.

## Yapı
- `pages/` sayfalar, `assets/img/` görseller, `assets/thumbs/` site haritası önizlemeleri
- `tools/pages.json` sayfa listesi; `python3 tools/build_index.py` ile `index.html` yeniden üretilir
- `tools/export_static.py` tasarım kaynaklarından (.dc.html) sayfaları üretir
- `tools/make_thumbs.sh` önizlemeleri yeniden çeker (headless Chrome)

## Notlar
- Hizmet bedeli oranı (%3), ödeme kuruluşu, marka görselleri ve yasal metinler yer tutucu/taslaktır.
- Ücretler sayfasındaki hesaplayıcı çalışır; diğer formlar gösterim amaçlıdır.
