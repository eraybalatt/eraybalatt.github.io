#!/usr/bin/env python3
"""Dunyanin en iyilerinin yaptigini yapan dort ornek.

Arastirma (12 Eyl 2026, sitelerin kendisinden olculdu):
  MJZ  — ana sayfada ~25 kelime, hero basligi YOK, uc link: Directors/Contact/Sales
  BUCK — ustte ~15-20 kelime, hero basligi YOK, one cikan is kapagi aciyor

Ikisinde de sifat yok. Pazarlama cumlesi yok. Is ilk geliyor.

Dort ornek, dordu de bu kurallara uyuyor; ayrildiklari yer ilk ekrani
neyin doldurdugu:

  _d1 IZGARA  Ana sayfa isin kendisi. Tam genislik, kenar bosluksuz mozaik.
  _d2 KAPAK   Tek one cikan is ekrani doldurur, altinda iki tane daha. (Buck)
  _d3 DIZIN   Gorsel yok; metin dizini, satira gelince kare aciliyor.
  _d4 REEL    Tek tam ekran reel, isim, baska hicbir sey. (en uc)

ORTAK TEMIZLIK — dordunde de:
  · loader / acilis kartı yok, is ilk yukleniyor
  · hero sifatlari silindi ("Cinematic stories, rebuilt with AI." gitti)
  · sol ray yok, ustte ince cubuk
  · kunye kesin: rol · musteri · yil
  · iletisim tek tikla, her zaman gorunur
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')

HOME_RE = re.compile(r'id="home">[\s\S]*?</section>')
m0 = HOME_RE.search(s0)
assert m0, '#home bulunamadi'

ISLER = [
 ('#docs','FLAWLESS','The Antwerp Diamond Heist','Director · Writer · Editor','2026',
  'img','flawless/hero-vault.jpg'),
 ('#music','Modd','real life / yok uyku','AI Creator · Universal Music Türkiye','2026',
  'vid','dtc-1.mp4'),
 ('#docs','COLD START','XPRIZE','Editor','2026','vid','coldstart-film.mp4'),
 ('#ugc','Konfuse','Brand World Film','Director','2026','vid','konfuse.mp4'),
 ('#shorts','Tesadüf Değil','7 bölüm · 106 kare','Producer · Director','2026',
  'img','tesaduf-grid.webp'),
 ('#ugc','TennisCut','The Moment · Best of Us','Director','2026','vid','tenniscut-3.mp4'),
 ('#prodphoto','Doqu Home','Bellona','Director','2025','img','doqu-home.jpg'),
 ('#brands','Novora','Sağlık Köklerinde','Director','2026','img','novora-tr-p.webp'),
]

def media(kind, src, cls=''):
    if kind == 'vid':
        return ('<video class="%s" src="%s" muted loop playsinline preload="none"></video>'
                % (cls, src))
    return '<img class="%s" src="%s" alt="" loading="lazy" decoding="async">' % (cls, src)

# ═══════════════════════════════════════════════ ORTAK TEMIZLIK
def temizle(s):
    """Loader'i, acilis ekranini ve pazarlama cumlelerini kaldirir."""
    # loader bloğu
    s = re.sub(r'<div id="loader"[\s\S]*?</div>\s*(?=<)', '', s, count=1)
    # acilis/welcome ekrani
    s = re.sub(r'<div class="wel[^"]*"[\s\S]{0,2000}?</div>\s*(?=<section|<header|<main)',
               '', s, count=1)
    # loader'i gosteren head script'i etkisizlestir
    s = s.replace("document.documentElement.classList.add('loading')", "void 0")
    return s

ORTAK_CSS = '''
/* --- dunyanin en iyilerinin ortak kurallari --- */
#loader,.loader,.welcome,.wel{ display:none !important }
html,body{ opacity:1 !important; visibility:visible !important }
body{ background:var(--bg) }

/* ust cubuk: ince, sabit, uc link yeter */
header.nav{ border-bottom:1px solid var(--rule) }
.nav-work{ display:none }           /* ikinci nav satiri kalksin */
.avail{ font-size:10.5px; letter-spacing:.14em }

/* kunye satiri: rol · musteri · yil — her zaman ayni sirada */
.cr{ display:flex; flex-wrap:wrap; gap:0 14px; align-items:baseline }
.cr b{ font-family:'Space Grotesk',sans-serif; font-weight:600;
       font-size:clamp(1rem,2.1vw,1.35rem); letter-spacing:-.005em; color:var(--text) }
.cr i{ font-style:normal; font-size:13px; color:var(--muted) }
.cr s{ text-decoration:none; font-family:'Space Grotesk',sans-serif;
       font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:var(--muted) }
'''

# ═══════════════════════════════════════════════ 1 · IZGARA
def izgara():
    t = []
    for i,(href,ad,alt,rol,yil,k,src) in enumerate(ISLER):
        sp = ' style="--sp:2"' if i in (0,3) else ''
        t.append('<a class="gz" href="%s"%s>%s<span class="gz-c"><b>%s</b><i>%s</i><s>%s</s></span></a>'
                 % (href, sp, media(k,src,'gz-m'), ad, rol, yil))
    return ('id="home">\n    <div class="gz-wrap">\n      ' + '\n      '.join(t) +
            '\n    </div>\n  </section>')

IZGARA_CSS = ORTAK_CSS + '''
:root{ --bg:#0b0b0c; --text:#f4f4f5; --muted:#8e8e93;
       --rule:rgba(255,255,255,.11); --rule-2:rgba(255,255,255,.2);
       --plate:rgba(11,11,12,.985); --ink:#f0f0f2; --ink-2:#d4d4d8; --ink-3:#8e8e93;
       --card:rgba(255,255,255,.05); --card-brd:rgba(255,255,255,.14); }
.hero{ min-height:auto; padding:0; display:block; overflow:visible }
.gz-wrap{ display:grid; grid-template-columns:repeat(4,1fr); gap:1px;
          padding-top:var(--row1,56px); background:var(--rule) }
@media(max-width:1000px){ .gz-wrap{grid-template-columns:repeat(2,1fr)} }
@media(max-width:560px){ .gz-wrap{grid-template-columns:1fr} }
.gz{ position:relative; display:block; aspect-ratio:16/10; overflow:hidden;
     grid-column:span var(--sp,1); background:#141416; text-decoration:none }
@media(max-width:1000px){ .gz{grid-column:span 1} }
.gz-m{ width:100%; height:100%; object-fit:cover; display:block;
       transform:scale(1.001); transition:transform .8s cubic-bezier(.2,.7,.2,1) }
.gz:hover .gz-m{ transform:scale(1.04) }
.gz-c{ position:absolute; left:0; right:0; bottom:0; z-index:2; padding:18px 20px;
       background:linear-gradient(180deg,transparent,rgba(0,0,0,.82));
       display:flex; flex-wrap:wrap; gap:2px 14px; align-items:baseline }
.gz-c b{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:15px;
         letter-spacing:.02em; color:#fff; width:100% }
.gz-c i{ font-style:normal; font-size:11px; color:rgba(255,255,255,.72) }
.gz-c s{ text-decoration:none; font-size:10px; letter-spacing:.18em; color:rgba(255,255,255,.5) }
'''

# ═══════════════════════════════════════════════ 2 · KAPAK
def kapak():
    h,ad,alt,rol,yil,k,src = ISLER[0]
    ikinci = ISLER[1]; ucuncu = ISLER[3]
    def kart(x):
        href,a2,al2,r2,y2,k2,s2 = x
        return ('<a class="kp-s" href="%s">%s<span class="cr"><b>%s</b><i>%s</i><s>%s</s></span></a>'
                % (href, media(k2,s2,'kp-sm'), a2, r2, y2))
    return ('''id="home">
    <a class="kp-lead" href="%s">
      %s
      <div class="kp-ov"></div>
      <span class="kp-c"><b>%s</b><i>%s · %s</i><s>%s</s></span>
    </a>
    <div class="kp-row">%s%s</div>
  </section>''' % (h, media(k,src,'kp-m'), ad, alt, rol, yil, kart(ikinci), kart(ucuncu)))

KAPAK_CSS = ORTAK_CSS + '''
:root{ --bg:#0d0c0a; --text:#f6f2ea; --muted:#a09889;
       --rule:rgba(246,242,234,.12); --rule-2:rgba(246,242,234,.22);
       --plate:rgba(13,12,10,.985); --ink:#f0ece2; --ink-2:#ded7c9; --ink-3:#a09889;
       --card:rgba(246,242,234,.05); --card-brd:rgba(246,242,234,.14); }
.hero{ min-height:auto; padding:var(--row1,56px) 0 0; display:block; overflow:visible }
.kp-lead{ position:relative; display:block; height:78vh; min-height:440px;
          overflow:hidden; text-decoration:none }
.kp-m{ width:100%; height:100%; object-fit:cover; display:block }
.kp-ov{ position:absolute; inset:0; z-index:1; pointer-events:none;
        background:linear-gradient(180deg,transparent 40%,rgba(13,12,10,.9)) }
.kp-c{ position:absolute; left:max(22px,4vw); bottom:clamp(28px,5vh,54px); z-index:2;
       display:block; max-width:min(760px,88%) }
.kp-c b{ display:block; font-family:'Oswald','Space Grotesk',sans-serif; font-weight:500;
         font-size:clamp(2.1rem,6.5vw,4.4rem); line-height:.96; letter-spacing:.015em; color:#fff }
.kp-c i{ display:block; font-style:normal; font-size:clamp(13px,1.5vw,15px);
         color:rgba(255,255,255,.8); margin-top:10px }
.kp-c s{ display:block; text-decoration:none; font-family:'Space Grotesk',sans-serif;
         font-size:10px; letter-spacing:.24em; color:rgba(255,255,255,.55); margin-top:8px }
.kp-row{ display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--rule) }
@media(max-width:760px){ .kp-row{grid-template-columns:1fr} }
.kp-s{ position:relative; display:block; text-decoration:none; background:var(--bg) }
.kp-sm{ width:100%; aspect-ratio:16/9; object-fit:cover; display:block }
.kp-s .cr{ padding:16px 20px 22px }
'''

# ═══════════════════════════════════════════════ 3 · DIZIN
def dizin():
    rows = []
    for i,(href,ad,alt,rol,yil,k,src) in enumerate(ISLER,1):
        rows.append('<li><a href="%s"><span class="dz-n">%02d</span>'
                    '<span class="dz-t">%s</span><span class="dz-r">%s</span>'
                    '<span class="dz-y">%s</span>%s</a></li>'
                    % (href, i, ad, rol, yil, media(k,src,'dz-p')))
    return ('id="home">\n    <div class="dz-wrap"><ol class="dz">\n      ' +
            '\n      '.join(rows) + '\n    </ol></div>\n  </section>')

DIZIN_CSS = ORTAK_CSS + '''
:root{ --bg:#111112; --text:#ededee; --muted:#83838a;
       --rule:rgba(237,237,238,.13); --rule-2:rgba(237,237,238,.24);
       --plate:rgba(17,17,18,.985); --ink:#e9e9ea; --ink-2:#cfcfd3; --ink-3:#83838a;
       --card:rgba(237,237,238,.05); --card-brd:rgba(237,237,238,.14); }
.hero{ min-height:auto; padding:calc(var(--row1,56px) + 6vh) max(22px,5vw) 9vh;
       display:block; text-align:left }
.dz-wrap{ max-width:1100px }
.dz{ list-style:none; margin:0; padding:0; border-top:1px solid var(--rule) }
.dz li{ border-bottom:1px solid var(--rule) }
.dz a{ position:relative; display:grid; grid-template-columns:auto 1fr auto auto;
       gap:0 26px; align-items:baseline; padding:20px 2px; text-decoration:none; color:inherit }
.dz-n{ font-family:'Space Grotesk',sans-serif; font-size:11px; letter-spacing:.14em; color:var(--muted) }
.dz-t{ font-family:'Oswald','Space Grotesk',sans-serif; font-weight:400;
       font-size:clamp(1.3rem,3.4vw,2.2rem); line-height:1; letter-spacing:.02em;
       text-transform:uppercase; color:var(--text); transition:color .25s }
.dz-r,.dz-y{ font-family:'Space Grotesk',sans-serif; font-size:10px; letter-spacing:.2em;
             text-transform:uppercase; color:var(--muted); white-space:nowrap }
.dz a:hover .dz-t{ color:#fff }
/* satira gelince kare acilir */
.dz-p{ position:absolute; right:0; top:50%; z-index:3; width:230px; aspect-ratio:16/9;
       object-fit:cover; border-radius:2px; pointer-events:none;
       opacity:0; transform:translate(14px,-46%) scale(.97);
       transition:opacity .3s, transform .45s cubic-bezier(.2,.7,.2,1);
       box-shadow:0 22px 60px -22px rgba(0,0,0,.9) }
@media(min-width:1000px){ .dz a:hover .dz-p{ opacity:1; transform:translate(0,-50%) scale(1) } }
@media(max-width:1000px){ .dz-p{display:none} .dz a{grid-template-columns:auto 1fr auto; row-gap:6px}
  .dz-r{grid-column:2;grid-row:2} }
'''

# ═══════════════════════════════════════════════ 4 · REEL
REEL_HTML = '''id="home">
    <video class="rl-m" autoplay muted loop playsinline preload="auto" poster="coldstart-grid.webp" src="coldstart-film.mp4"></video>
    <div class="rl-ov"></div>
    <div class="rl-c">
      <span class="rl-n">ERAY BALAT</span>
      <span class="rl-r" data-en="Director" data-tr="Yönetmen" data-de="Regisseur">Director</span>
    </div>
    <a class="rl-go" href="#docs" data-en="Work ↓" data-tr="İşler ↓" data-de="Arbeiten ↓">Work ↓</a>
  </section>'''

REEL_CSS = ORTAK_CSS + '''
:root{ --bg:#000; --text:#fff; --muted:#9a9a9a;
       --rule:rgba(255,255,255,.12); --rule-2:rgba(255,255,255,.22);
       --plate:rgba(0,0,0,.985); --ink:#fff; --ink-2:#dcdcdc; --ink-3:#9a9a9a;
       --card:rgba(255,255,255,.05); --card-brd:rgba(255,255,255,.14); }
.hero{ min-height:100vh; padding:0; overflow:hidden; display:block; position:relative }
.rl-m{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0 }
.rl-ov{ position:absolute; inset:0; z-index:1; pointer-events:none;
        background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,transparent 26%,transparent 62%,rgba(0,0,0,.78)) }
.rl-c{ position:absolute; left:max(22px,5vw); bottom:clamp(72px,11vh,120px); z-index:2 }
.rl-n{ display:block; font-family:'Oswald','Space Grotesk',sans-serif; font-weight:400;
       font-size:clamp(2.2rem,7.5vw,5.4rem); line-height:.94; letter-spacing:.12em; color:#fff }
.rl-r{ display:block; font-family:'Space Grotesk',sans-serif; font-size:11px;
       letter-spacing:.34em; text-transform:uppercase; color:rgba(255,255,255,.7); margin-top:14px }
.rl-go{ position:absolute; left:max(22px,5vw); bottom:clamp(30px,5vh,50px); z-index:2;
        font-family:'Space Grotesk',sans-serif; font-size:11px; letter-spacing:.24em;
        text-transform:uppercase; color:rgba(255,255,255,.82); text-decoration:none }
.rl-go:hover{ color:#fff }
'''

# ═══════════════════════════════════════════════ uret
for out, hero, css, ad in (
    ('_d1.html', izgara(),   IZGARA_CSS, 'IZGARA — ana sayfa isin kendisi'),
    ('_d2.html', kapak(),    KAPAK_CSS,  'KAPAK — tek one cikan is (Buck modeli)'),
    ('_d3.html', dizin(),    DIZIN_CSS,  'DIZIN — metin, satirda kare acilir'),
    ('_d4.html', REEL_HTML,  REEL_CSS,   'REEL — tek tam ekran, isim, baska hicbir sey'),
):
    s = temizle(s0[:m0.start()] + hero + s0[m0.end():])
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== %s ===== */\n' % ad + css + '\n' + s[i:]
    s = s.replace('<title>', '<!-- KABUK: %s -->\n<title>' % ad, 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    print('%-10s %-42s %7d bayt' % (out, ad, len(s)))
