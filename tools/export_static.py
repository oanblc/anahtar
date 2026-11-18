#!/usr/bin/env python3
"""Tasarım kaynaklarını (.dc.html) düz, bağımsız HTML sayfalarına çevirir.

Kullanım: python3 tools/export_static.py <kaynak klasör> <hedef klasör (pages)>
- <x-dc>, <helmet> ve tasarım betiği kaldırılır, helmet içeriği <head>'e taşınır
- /_blob/<id> görsel yolları yerel assets/img dosyalarına çevrilir
- *.dc.html bağlantıları *.html olur
- Ücretler sayfasındaki hesaplayıcı düz JavaScript ile çalışır hale getirilir
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
DST.mkdir(parents=True, exist_ok=True)

BLOB = {
    "5af7ea009f2e3492396a86b7cd33cde8": "hero-cift-telefon.jpg",
    "b025703cc6f8dc5f0e320b2f9d30586c": "anahtar-teslimi.jpg",
    "2f219d1fffc654a4e18a0009e32dda89": "aydinlik-salon.jpg",
    "d75cef0a2197ef879222ddf228c46ba1": "kadin-telefon-dikey.jpg",
    "a5c753507639c4f246c6935cae4693f8": "erkek-kimlik-dikey.jpg",
    "3ff4597b4b333386cc2ec2341466f25a": "cift-dizustu-dikey.jpg",
    "32fdc97c0c0064dc4dc48fd5ab76b949": "kiraci-kanepe.jpg",
    "3fca91b6ebc537abbad3ba218b622c89": "ev-sahibi-tablet.jpg",
    "8b0642bc2e19be18b02d48e78b746d0e": "kiraci-kanepe.jpg",  # kullanılmıyor, güvenli yedek
    "75a33cc9b18c7c75dd51f4a55b76dc60": "telefon-cercevesi.png",
    "3a01491201551b18160bd887e75478f9": "telefon-ekran-maskesi.png",
}
FINAL = {
    "A1": "A1_kombi.jpg", "A2": "A2_klima.jpg", "A3": "A3_buzdolabi.jpg",
    "A4": "A4_camasir_makinesi.jpg", "A5": "A5_mutfak_dolabi.jpg", "A6": "A6_anahtar_takimi.jpg",
    "B_banyo": "B_banyo.jpg", "B_elektrik": "B_elektrik_sayaci.jpg", "B_mutfak": "B_mutfak.jpg",
    "B_salon": "B_salon.jpg", "B_su": "B_su_dogalgaz_sayaclari.jpg", "B_yatak": "B_yatak_odasi.jpg",
    "C_musluk": "C_damlatan_musluk.jpg", "C_klima": "C_klima.jpg", "C_kombi": "C_kombi_basinc.jpg",
    "C_parke_cikis": "C_parke_cikis.jpg", "C_parke_giris": "C_parke_giris.jpg",
    "C_tezgah_cikis": "C_tezgah_cikis.jpg", "C_tezgah_giris": "C_tezgah_giris.jpg",
    "E_bina_1": "E_bina_1.jpg", "E_bina_2": "E_bina_2.jpg", "E_bina_3": "E_bina_3.jpg",
    "E_guvenlik": "E_guvenlik.jpg", "E_iletisim": "E_iletisim.jpg", "E_kurumsal": "E_kurumsal.jpg",
}
ids_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
if ids_path and ids_path.exists():
    for k, v in json.loads(ids_path.read_text()).items():
        if k in FINAL:
            BLOB[v] = FINAL[k]

UCRETLER_PRESETS = [10000, 15000, 18000, 25000, 40000]
BTN_BASE = ("font-family:inherit;cursor:pointer;font-size:13.5px;font-weight:600;padding:9px 12px;"
            "border-radius:999px;")
BTN_ON = BTN_BASE + "border:1.5px solid #2B5078;background:#2B5078;color:#fff;"
BTN_OFF = BTN_BASE + "border:1.5px solid #CBDDEF;background:#fff;color:#2B5078;"

CALC_JS = """<script>
(function () {
  var RATE = 0.03, VAT = 0.20;
  var BASE = %r, ON = %r, OFF = %r;
  var input = document.getElementById('kira');
  var buttons = Array.prototype.slice.call(document.querySelectorAll('[data-preset]'));
  function money(n) { return n.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ₺'; }
  function set(id, v) { var e = document.getElementById(id); if (e) e.textContent = v; }
  function render(k) {
    var fee = Math.round(k * RATE * 100) / 100;
    var tax = Math.round(fee * VAT * 100) / 100;
    var total = Math.round((k + fee + tax) * 100) / 100;
    set('c-kira', money(k)); set('c-kira2', money(k)); set('c-fee', money(fee));
    set('c-tax', money(tax)); set('c-total', money(total));
    buttons.forEach(function (b) { b.setAttribute('style', Number(b.dataset.preset) === k ? ON : OFF); });
  }
  input.addEventListener('input', function () {
    var d = String(input.value).replace(/[^0-9]/g, '');
    var n = d === '' ? 0 : Math.min(parseInt(d, 10), 1000000);
    render(n);
  });
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = Number(b.dataset.preset); input.value = String(v); render(v);
    });
  });
  render(parseInt(input.value, 10) || 0);
})();
</script>""" % (BTN_BASE, BTN_ON, BTN_OFF)


def convert(name: str, s: str) -> str:
    # 1) tasarım çalışma zamanı betikleri
    s = s.replace('<script src="./support.js"></script>\n', '').replace('<script src="./support.js"></script>', '')
    s = re.sub(r'<script type="text/x-dc" data-dc-script.*?</script>\n?', '', s, flags=re.S)
    # 2) helmet içeriği head'e
    m = re.search(r'<helmet>(.*?)</helmet>', s, re.S)
    helmet = m.group(1) if m else ''
    s = re.sub(r'<helmet>.*?</helmet>\n?', '', s, flags=re.S)
    s = s.replace('<x-dc>', '').replace('</x-dc>', '')
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    s = s.replace('</head>', helmet.strip() + '\n</head>', 1)
    # 3) Ücretler: hesaplayıcı
    if name == 'Ucretler':
        for k, v in {'kiraText': '18000', 'kiraFmt': '18.000,00 ₺', 'feeFmt': '540,00 ₺',
                     'taxFmt': '108,00 ₺', 'totalFmt': '18.648,00 ₺'}.items():
            s = s.replace('{{ %s }}' % k, v)
        s = s.replace(' onChange="{{ onKira }}"', '')
        s = re.sub(r'<sc-for list="\{\{ presets \}\}".*?</sc-for>',
                   ''.join('<button type="button" data-preset="%d" style="%s">%s ₺</button>' % (
                       p, BTN_ON if p == 18000 else BTN_OFF, f'{p:,}'.replace(',', '.')) for p in UCRETLER_PRESETS),
                   s, flags=re.S)
        # toplam ve ev sahibi satırları için id'ler
        s = s.replace('<span style="font-variant-numeric:tabular-nums">18.000,00 ₺</span></div>\n      <div style="display:flex;justify-content:space-between"><span>Hizmet bedeli (%3)</span><span style="font-variant-numeric:tabular-nums">540,00 ₺</span>',
                      '<span id="c-kira" style="font-variant-numeric:tabular-nums">18.000,00 ₺</span></div>\n      <div style="display:flex;justify-content:space-between"><span>Hizmet bedeli (%3)</span><span id="c-fee" style="font-variant-numeric:tabular-nums">540,00 ₺</span>')
        s = s.replace('<span>Vergiler</span><span style="font-variant-numeric:tabular-nums">108,00 ₺</span>',
                      '<span>Vergiler</span><span id="c-tax" style="font-variant-numeric:tabular-nums">108,00 ₺</span>', 1)
        s = s.replace('letter-spacing:-0.03em;font-variant-numeric:tabular-nums">18.648,00 ₺</span>',
                      'letter-spacing:-0.03em;font-variant-numeric:tabular-nums" id="c-total">18.648,00 ₺</span>', 1)
        s = s.replace('letter-spacing:-0.03em;color:#1D3650;font-variant-numeric:tabular-nums">18.000,00 ₺</span>',
                      'letter-spacing:-0.03em;color:#1D3650;font-variant-numeric:tabular-nums" id="c-kira2">18.000,00 ₺</span>', 1)
        s = s.replace('</body>', CALC_JS + '\n</body>')
    assert '{{' not in s, name + ': çözülmemiş {{ }} kaldı'
    # 4) görseller ve bağlantılar
    def blob(m):
        return '../assets/img/' + BLOB[m.group(1)]
    s = re.sub(r'/_blob/([0-9a-f]{32})', blob, s)
    s = s.replace('.dc.html', '.html')
    return s


count = 0
for f in sorted(SRC.glob('*.dc.html')):
    name = f.name[:-len('.dc.html')]
    if name in ('Anasayfa-Mobil',):
        continue
    out = convert(name, f.read_text(encoding='utf-8'))
    (DST / (name + '.html')).write_text(out, encoding='utf-8')
    count += 1
print(count, 'sayfa yazıldı ->', DST)
