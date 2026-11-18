/* Mobil menü düğmesi ve geniş tabloların kaydırılabilir hale getirilmesi */
(function () {
  function btn(target) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'mb-btn'; b.textContent = 'Menü';
    b.setAttribute('aria-expanded', 'false');
    b.addEventListener('click', function () {
      var open = target.classList.toggle('mb-open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.textContent = open ? 'Kapat' : 'Menü';
    });
    return b;
  }
  var head = document.querySelector('body header');
  if (head && head.querySelector('nav')) {
    var d = head.querySelector(':scope > div:last-child');
    head.insertBefore(btn(head), d && d !== head.querySelector('nav') ? d : null);
  }
  var side = document.querySelector('body aside');
  if (side && side.querySelector(':scope > nav')) {
    side.insertBefore(btn(side), side.querySelector(':scope > nav'));
  }
  // en az 4 sütunlu sabit genişlikli tablo satırlarını kaydırılabilir bir kapla sar
  document.querySelectorAll('main table, section table').forEach(function (t) {
    if (t.parentElement.classList.contains('mb-scroll')) return;
    var w = document.createElement('div'); w.className = 'mb-scroll';
    t.parentElement.insertBefore(w, t); w.appendChild(t);
  });
  var seen = new Set();
  document.querySelectorAll('[style*="display:grid"][style*="grid-template-columns"]').forEach(function (row) {
    var cols = (row.getAttribute('style').match(/grid-template-columns:([^;"]*)/) || [])[1] || '';
    var n = 0;
    cols.replace(/repeat\((\d+),[^)]*\)/g, function (m, k) { n += +k - 1; return ''; });
    n += cols.replace(/repeat\([^)]*\)/g, ' x ').trim().split(/\s+(?![^()]*\))/).length;
    if (/repeat\((auto)/.test(cols) || n < 4) return;
    var p = row.parentElement;
    if (p && /^(SECTION|MAIN|BODY)$/.test(p.tagName)) p = row;
    if (!p || seen.has(p) || p.classList.contains('mb-scroll')) return;
    seen.add(p);
    var wrap = document.createElement('div');
    wrap.className = 'mb-scroll';
    p.parentElement.insertBefore(wrap, p);
    wrap.appendChild(p);
  });
  // sabit genişlikli flex "tablo" satırları ve çok sütunlu grafikler de kaydırılır
  document.querySelectorAll('main [style*="display:flex"], section [style*="display:flex"]').forEach(function (row) {
    var st = row.getAttribute('style') || '';
    if (/flex-wrap:wrap|flex-direction:column/.test(st) || row.closest('.mb-scroll')) return;
    var kids = row.children, fixed = 0;
    for (var i = 0; i < kids.length; i++) if (/flex:0 0 \d+px/.test(kids[i].getAttribute('style') || '')) fixed++;
    var chart = kids.length >= 10 && /flex:1/.test(kids[0].getAttribute('style') || '');
    if (fixed < 3 && !chart) return;
    var p = chart ? row : row.parentElement;
    if (p && /^(SECTION|MAIN|BODY)$/.test(p.tagName)) p = row;
    if (!p || seen.has(p) || p.classList.contains('mb-scroll') || p.closest('.mb-scroll')) return;
    seen.add(p);
    var w = document.createElement('div'); w.className = 'mb-scroll';
    p.parentElement.insertBefore(w, p); w.appendChild(p);
  });
  document.querySelectorAll('aside > div').forEach(function (d) { if (d.querySelector('a[href="Main.html"]')) d.classList.add('mb-brand'); });
  document.querySelectorAll('main [style*="display:flex"], section [style*="display:flex"]').forEach(function (row) {
    var st = row.getAttribute('style') || '';
    if (/flex-wrap:wrap|flex-direction:column/.test(st) || row.closest('.mb-scroll') || row.children.length < 3 || row.children.length >= 10) return;
    var grow = 0;
    for (var i = 0; i < row.children.length; i++) if (/flex:1(;|"| 1)/.test(row.children[i].getAttribute('style') || '')) grow++;
    // yalnızca eşit hücrelerden oluşan satırlar (kod kutuları, adım çubuğu) olduğu gibi kalır
    if (grow > 0 && grow < row.children.length) row.classList.add('mb-row');
  });
})();
