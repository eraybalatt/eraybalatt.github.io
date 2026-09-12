#!/usr/bin/env python3
"""_a.html'den yildizi cikarip iki alternatif kabuk uretir.

  A1  Sade Kunye   — yildiz gider, yerine hicbir sey gelmez. Kelime markasi buyur.
  A2  Konusan Ayrac — yildiz gider, ayraclar bolum adini tasir. Susleme bilgiye doner.
"""
import re, sys, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
SRC  = ROOT / '_a.html'
s0   = SRC.read_text(encoding='utf-8')

def one(old, new, t, label=''):
    n = t.count(old)
    assert n == 1, 'ESLESME %d (%s): %r' % (n, label, old[:70])
    return t.replace(old, new, 1)

# ---------------------------------------------------------------- ortak
def strip_star(s):
    # 1) header'daki dokuma yildiz SVG'si
    m = re.search(r'<span class="brand-mark" aria-hidden="true">[\s\S]*?</span>', s)
    assert m, 'brand-mark bulunamadi'
    s = s[:m.start()] + s[m.end():]

    # 2) acilis ekranindaki yildiz
    s = one('<div class="wel-star" aria-hidden="true"></div>', '', s, 'wel-star')

    # 3) loader motifi -> kelime markasi
    m = re.search(r'<svg class="loader-motif"[\s\S]*?</svg>', s)
    assert m, 'loader-motif bulunamadi'
    s = s[:m.start()] + '<div class="loader-word" aria-hidden="true">ERAY BALAT</div>' + s[m.end():]

    # 4) ayraclardaki yildiz span'i
    s = s.replace('<span class="slj-star"></span>', '')

    # 5) footer yildizi
    s = re.sub(r'<[^>]*class="[^"]*foot-star[^"]*"[^>]*>\s*</[a-z]+>', '', s)
    s = re.sub(r'<[^>]*class="[^"]*foot-star[^"]*"[^>]*/?>', '', s)
    return s

def add_css(s, css, tag):
    # son </style>'dan once — bu dosyada sonra gelen kazaniyor
    i = s.rfind('</style>')
    assert i > 0, 'style kapanisi yok'
    return s[:i] + '\n/* ===== %s ===== */\n' % tag + css + '\n' + s[i:]

def noindex_title(s, name):
    return one('<title>', '<!-- KABUK: %s -->\n<title>' % name, s, 'title')

# ---------------------------------------------------------------- A1
CSS_A1 = """
/* Yildiz gitti. Kelime markasi markanin kendisi oldu: isim buyur, altina rol. */
header.nav .brand{ gap:0 }
header.nav .brand-wm{ gap:6px }
header.nav .brand-wm b{
  font-size:19px; letter-spacing:.2em; font-weight:700;
}
header.nav .brand-wm i{ font-size:9.5px; letter-spacing:.24em; opacity:.8 }
@media(min-width:880px){
  header.nav .brand-wm b{ font-size:27px; letter-spacing:.22em }
  header.nav .brand-wm i{ font-size:10.5px; letter-spacing:.28em }
}
@media(max-width:600px){
  header.nav .brand-wm b{ font-size:15px; letter-spacing:.14em }
  header.nav .brand-wm i{ display:none }
}

/* Ayrac: tek ince cizgi, ortasi bos. Sus yok. */
.slj-divider{ gap:0; max-width:190px; margin:36px auto 30px }
.slj-divider .slj-line{
  height:1px; animation:none;
  background:linear-gradient(90deg,transparent,rgba(120,205,255,.32),transparent);
}
.slj-divider .slj-line:last-child{ display:none }

/* Loader: donen yildiz yerine isim */
.loader-word{
  font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:20px;
  letter-spacing:.34em; color:#a8dcff; text-align:center; opacity:.9;
  animation:lwfade 2.2s ease-in-out infinite;
}
@keyframes lwfade{0%,100%{opacity:.35}50%{opacity:1}}
@media(prefers-reduced-motion:reduce){.loader-word{animation:none;opacity:.9}}
"""

# ---------------------------------------------------------------- A2
CSS_A2 = """
/* Yildiz gitti. Ayrac artik bolum adini tasiyor: sus degil, bilgi. */
.slj-divider{ gap:14px; max-width:min(560px,86%); margin:40px auto 28px }
.slj-divider .slj-line{
  flex:1; height:1px; animation:none;
  background:linear-gradient(90deg,transparent,rgba(120,205,255,.36));
}
.slj-divider .slj-line:last-child{
  display:block;
  background:linear-gradient(90deg,rgba(120,205,255,.36),transparent);
}
.slj-divider .slj-tag{
  flex:0 0 auto; font-family:'Space Grotesk',sans-serif;
  font-size:10.5px; font-weight:600; letter-spacing:.26em;
  text-transform:uppercase; color:rgba(168,220,255,.8); white-space:nowrap;
}
@media(max-width:600px){
  .slj-divider{ gap:10px; max-width:92% }
  .slj-divider .slj-tag{ font-size:9px; letter-spacing:.16em }
}

/* Yildizin yerine yapisal bir isaret: ince dikey kural */
header.nav .brand{ gap:11px; align-items:center }
header.nav .brand::before{
  content:""; flex:0 0 auto; width:2px; height:26px; border-radius:2px;
  background:linear-gradient(180deg,rgba(120,205,255,.95),rgba(120,205,255,.12));
}
@media(min-width:880px){ header.nav .brand::before{ height:38px; width:3px } }
@media(max-width:520px){ header.nav .brand::before{ height:20px } }
header.nav .brand-wm b{ font-size:16px; letter-spacing:.13em }
@media(min-width:880px){ header.nav .brand-wm b{ font-size:20px; letter-spacing:.16em } }

.loader-word{
  font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:20px;
  letter-spacing:.34em; color:#a8dcff; text-align:center; opacity:.9;
  animation:lwfade 2.2s ease-in-out infinite;
}
@keyframes lwfade{0%,100%{opacity:.35}50%{opacity:1}}
@media(prefers-reduced-motion:reduce){.loader-word{animation:none;opacity:.9}}
"""

def label_dividers(s):
    """Her .slj-divider'a, kendisinden SONRA baslayan ilk bolumun adini yazar.
    Pencere tahmini yok: bolum konumlari sirali cikarilir, ilk sonraki secilir."""
    NAMES = {
        'about':'About','films':'Films','ugc':'UGC Ads','shorts':'Short Films',
        'music':'Music Videos','docs':'Documentary','prodphoto':'Product Shots',
        'brands':'Brands','reviews':'Reviews','contact':'Contact',
        'flawless-feature':'Flawless','bushido':'Bushido','leather-feature':'Leather',
        'vlab':'Lab','animbb':'Animation','home':'Home',
    }
    secs = [(m.start(), m.group(1)) for m in
            re.finditer(r'<section[^>]*\sid="([^"]+)"', s)]
    secs.sort()

    divs = list(re.finditer(r'<div class="slj-divider[^"]*"[^>]*>', s))

    # Her bolumu YALNIZCA kendisinden hemen onceki ayrac tanitir.
    # Bolum icinde kalan ayraclar etiketsiz cizgi olarak durur.
    chosen = {}
    for st, key in secs:
        prev = [d for d in divs if d.start() < st]
        if not prev:
            continue
        # ayni ayrac iki bolume denk gelirse, hemen ardindan geleni tanitir
        chosen.setdefault(prev[-1].start(), key)

    out, pos, n, skipped = [], 0, 0, 0
    for m in divs:
        lab = NAMES.get(chosen.get(m.start(), ''))
        if not lab:
            skipped += 1
            continue
        tail = s[m.end(): m.end() + 400]
        ins = m.end() + tail.index('</span>') + len('</span>') if '</span>' in tail else m.end()
        out.append(s[pos:ins]); out.append('<span class="slj-tag">%s</span>' % lab)
        pos = ins; n += 1
    out.append(s[pos:])
    return ''.join(out), n, skipped



# ---------------------------------------------------------------- hero sadelestirme
def minimal_hero(s):
    """Hero'da tekrar eden katmanlari keser, kalan iki satiri kisaltir.

    Cikan : eyebrow 'Creative AI Producer · Filmmaker' — header'da zaten yaziyor.
    Kisalan: h1 ve lead. Lead'deki kategori listesi header'in ikinci nav
             satirinda (UGC ADS / SHORT FILMS / MUSIC VIDEOS / ...) zaten var.
    """
    # 1) hero eyebrow'u kaldir (data-en degeriyle tekil)
    old_eb = ('<div class="eyebrow rin" data-en="Creative AI Producer · Filmmaker" '
              'data-tr="Creative AI Producer · Yönetmen" '
              'data-de="Creative AI Producer · Filmemacher">Creative AI Producer · Filmmaker</div>')
    assert s.count(old_eb) == 1, 'hero eyebrow tekil degil: %d' % s.count(old_eb)
    s = s.replace(old_eb, '', 1)

    # 2) h1 — 8 kelimeden 5'e
    old_h1 = ('<h1 class="rin" data-en="Cinematic stories, rebuilt frame by frame with AI." '
              'data-tr="Sinematik hikâyeler, kare kare yapay zekâ ile yeniden kurgulandı." '
              'data-de="Filmische Geschichten, Bild für Bild mit AI neu erschaffen.">'
              'Cinematic stories, rebuilt frame by frame with AI.</h1>')
    new_h1 = ('<h1 class="rin" data-en="Cinematic stories, rebuilt with AI." '
              'data-tr="Sinematik hikâyeler, yapay zekâyla yeniden kuruldu." '
              'data-de="Filmische Geschichten, mit AI neu erschaffen.">'
              'Cinematic stories, rebuilt with AI.</h1>')
    assert s.count(old_h1) == 1, 'h1 tekil degil: %d' % s.count(old_h1)
    s = s.replace(old_h1, new_h1, 1)

    # 3) lead — kategori listesi header'da var, tekrar etmesin
    import re as _re
    m = _re.search(r'<p class="lead rin" data-en="I direct music videos[\s\S]*?</p>', s)
    assert m, 'hero lead bulunamadi'
    new_lead = ('<p class="lead rin" data-en="For brands and artists worldwide." '
                'data-tr="Markalar ve sanatçılar için." '
                'data-de="Für Marken und Künstler weltweit.">'
                'For brands and artists worldwide.</p>')
    s = s[:m.start()] + new_lead + s[m.end():]
    return s


# ---------------------------------------------------------------- uret
base = minimal_hero(strip_star(s0))

a1 = add_css(base, CSS_A1, 'A1 — SADE KUNYE')
a1 = noindex_title(a1, 'A1 Sade Kunye')
(ROOT / '_a1.html').write_text(a1, encoding='utf-8')

a2, tagged, skipped = label_dividers(base)
a2 = add_css(a2, CSS_A2, 'A2 — KONUSAN AYRAC')
a2 = noindex_title(a2, 'A2 Konusan Ayrac')
(ROOT / '_a2.html').write_text(a2, encoding='utf-8')

print('A1 yazildi:', len(a1), 'bayt')
print('A2 yazildi:', len(a2), 'bayt |', tagged, 'etiketlendi,', skipped, 'etiketsiz')
for f in ('_a1.html', '_a2.html'):
    t = (ROOT / f).read_text(encoding='utf-8')
    print(f, '| slj-star:', t.count('slj-star'), '| brand-mark:', t.count('brand-mark'),
          '| foot-star:', t.count('foot-star'), '| loader-motif:', t.count('loader-motif'))
