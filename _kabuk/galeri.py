#!/usr/bin/env python3
"""GALERI — beyaz duvar, buyuk kare, kucuk kunye.

Kirk tasarimin ortak korlugu: hepsi koyuydu. Is hep karanlik bir cercevenin
icinde kaldi. Bu sayfa tersini yapiyor — sergi mantigi:

  · kemik beyazi zemin, is renkli ve buyuk
  · kunye kucuk ve altta, tipki sergi etiketi gibi
  · tek buyuk metin ani: Notarbartolo'nun cumlesi
  · rakamlar tek sessiz satir, mono
  · iletisim buton degil satir

Tipografi: Spectral (serif, karakterli) + Public Sans + IBM Plex Mono
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')
m0 = re.search(r'id="home">[\s\S]*?</section>', s0)
assert m0

def i18n(tag, cls, en, tr, de, extra=''):
    return ('<%s class="%s" data-en="%s" data-tr="%s" data-de="%s"%s>%s</%s>'
            % (tag, cls, en, tr, de, extra, en, tag))

# baslik · alt · rol · yil · tur · kaynak
ISLER = [
 ('#docs','FLAWLESS','The Antwerp Diamond Heist',
  'Director, writer, editor, narrator','2026','16:56 · 4K','img','flawless/hero-vault.jpg'),
 ('#music','Modd','real life · yok uyku',
  'AI Creator','2026','Universal Music Türkiye','vid','mv-reallife.mp4'),
 ('#ugc','Konfuse','Brand World Film',
  'Director','2026','Original score','img','konfuse-bagclose.jpg'),
 ('#docs','COLD START','XPRIZE',
  'Editor','2026','2:19 trailer','vid','hero-coldstart.mp4'),
 ('#shorts','Tesadüf Değil','7 bölüm · 106 kare',
  'Producer, director','2026','Short film','img','tesaduf-grid.webp'),
 ('#prodphoto','Doqu Home','Bellona',
  'Director','2025','Product · furniture','img','doqu-home.jpg'),
]

def media(k, src):
    if k == 'vid':
        return ('<video src="%s" muted loop playsinline preload="none" '
                'class="gl-m"></video>' % src)
    return '<img src="%s" alt="" loading="lazy" decoding="async" class="gl-m">' % src

def isler():
    out = []
    for i,(href,ad,alt,rol,yil,tur,k,src) in enumerate(ISLER):
        wide = ' gl-w' if i in (0,4) else ''
        out.append(
          '<a class="gl%s" href="%s">'
          '<figure>%s<figcaption>'
          '<b>%s</b><i>%s</i>'
          '<span class="gl-cr">%s</span>'
          '<span class="gl-mt">%s · %s</span>'
          '</figcaption></figure></a>' % (wide, href, media(k,src), ad, alt, rol, tur, yil))
    return '\n      '.join(out)

RAKAM = [('18.6M','views'),('4.8M','in 9 months'),('60.8K','subscribers'),('3','languages')]

HERO = '''id="home">
    <header class="gl-top">
      <div class="gl-id">
        <span class="gl-nm">Eray Balat</span>
        %s
      </div>
      %s
    </header>

    <div class="gl-grid">
      %s
    </div>

    <figure class="gl-q">
      <blockquote>&ldquo;Ti sono grato per il documentario, mi piace molto.&rdquo;</blockquote>
      <figcaption><b>Leonardo Notarbartolo</b>%s</figcaption>
    </figure>

    <div class="gl-facts">%s</div>
  </section>''' % (
  i18n('span','gl-rl','Director','Yönetmen','Regisseur'),
  i18n('a','gl-ct','Start a project','Proje başlat','Projekt starten',' href="#contact"'),
  isler(),
  i18n('span','',
    'the man who planned the 2003 Antwerp diamond heist, on FLAWLESS',
    '2003 Antwerp elmas soygununu planlayan adam, FLAWLESS hakkında',
    'der Planer des Antwerpener Diamantenraubs 2003, über FLAWLESS'),
  ''.join('<span><b>%s</b>%s</span>' % (n,l) for n,l in RAKAM))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Spectral:ital,wght@0,400;0,600;1,400&family=Public+Sans:wght@400;500;600'
 '&family=IBM+Plex+Mono:wght@400;500&display=swap">')

CSS = '''
:root{
  --bg:#faf8f3; --bg-soft:#f0ece3; --text:#17160f; --muted:#6b675c;
  --rule:rgba(23,22,15,.14); --rule-2:rgba(23,22,15,.3);
  --plate:rgba(250,248,243,.985); --ink:#17160f; --ink-2:#3a372c; --ink-3:#6b675c;
  --card:rgba(23,22,15,.04); --card-brd:rgba(23,22,15,.14);
  --acc:#8a3417;
}
body{background:var(--bg);color:var(--text);font-family:'Public Sans',Helvetica,sans-serif}
#loader,.loader,.welcome,.wel{display:none!important}
html,body{opacity:1!important;visibility:visible!important}

/* sayfanin kendi ust cubugu gizlensin — galeri kendi basligini tasiyor */
header.nav{display:none!important}

.hero{min-height:auto;padding:0;display:block;text-align:left;overflow:visible}

/* baslik satiri */
.gl-top{display:flex;justify-content:space-between;align-items:flex-start;
        gap:24px;padding:clamp(26px,5vh,54px) max(20px,4vw) clamp(24px,4vh,40px);
        border-bottom:1px solid var(--rule)}
.gl-id{display:flex;flex-direction:column;gap:4px}
.gl-nm{font-family:'Spectral',Georgia,serif;font-weight:600;
       font-size:clamp(1.25rem,2.6vw,1.75rem);letter-spacing:-.01em;line-height:1}
.gl-rl{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.26em;
       text-transform:uppercase;color:var(--muted)}
.gl-ct{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
       text-transform:uppercase;color:var(--acc);text-decoration:none;
       border-bottom:1px solid currentColor;padding-bottom:3px;white-space:nowrap}
.gl-ct:hover{color:var(--ink)}

/* sergi duvari */
.gl-grid{display:grid;grid-template-columns:repeat(2,1fr);
         gap:clamp(38px,6vw,86px) clamp(26px,4vw,60px);
         padding:clamp(40px,7vh,86px) max(20px,4vw) clamp(46px,8vh,96px)}
@media(max-width:820px){.gl-grid{grid-template-columns:1fr;gap:44px}}
.gl{display:block;text-decoration:none;color:inherit}
.gl-w{grid-column:1/-1}
.gl figure{margin:0}
.gl-m{width:100%;display:block;background:var(--bg-soft);
      aspect-ratio:3/2;object-fit:cover;
      transition:filter .5s cubic-bezier(.2,.7,.2,1)}
.gl-w .gl-m{aspect-ratio:21/9}
.gl:hover .gl-m{filter:brightness(1.04) saturate(1.06)}
.gl figcaption{padding-top:14px}
.gl figcaption b{font-family:'Spectral',Georgia,serif;font-weight:600;
                 font-size:clamp(1.05rem,2.1vw,1.35rem);letter-spacing:-.005em;
                 display:inline}
.gl figcaption i{font-style:normal;font-size:clamp(1.05rem,2.1vw,1.35rem);
                 color:var(--muted);margin-left:9px}
.gl-cr{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.5px;
       letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2);margin-top:9px}
.gl-mt{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
       letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:3px}

/* tek buyuk metin ani */
.gl-q{margin:0;padding:clamp(50px,10vh,110px) max(20px,4vw);
      border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
      background:var(--bg-soft)}
.gl-q blockquote{margin:0 0 20px;max-width:24ch;
  font-family:'Spectral',Georgia,serif;font-style:italic;font-weight:400;
  font-size:clamp(1.6rem,4.6vw,3.1rem);line-height:1.16;letter-spacing:-.015em;
  color:var(--ink);text-wrap:balance}
.gl-q figcaption b{display:block;font-family:'IBM Plex Mono',monospace;font-weight:500;
  font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-2)}
.gl-q figcaption span{display:block;font-size:13px;color:var(--muted);margin-top:6px;
  max-width:46ch;line-height:1.45}

/* rakamlar: tek sessiz satir */
.gl-facts{display:flex;flex-wrap:wrap;gap:0 clamp(28px,5vw,64px);
          padding:clamp(26px,4vh,44px) max(20px,4vw);border-bottom:1px solid var(--rule)}
.gl-facts span{display:flex;align-items:baseline;gap:8px;
               font-family:'IBM Plex Mono',monospace;font-size:10.5px;
               letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.gl-facts b{font-family:'Spectral',Georgia,serif;font-weight:600;font-size:1.2rem;
            letter-spacing:-.01em;color:var(--ink);text-transform:none}

/* asagidaki mevcut bolumler acik zemine uysun */
.slj-divider .slj-tag{font-family:'IBM Plex Mono',monospace;color:var(--muted)}
.slj-divider .slj-line{background:linear-gradient(90deg,transparent,var(--rule))}
.slj-divider .slj-line:last-child{background:linear-gradient(90deg,var(--rule),transparent)}
.btn-grad{color:var(--ink);text-shadow:none;font-family:'IBM Plex Mono',monospace;
          font-size:11px;letter-spacing:.18em;text-transform:uppercase}
.btn-grad::after{background:var(--acc);box-shadow:none;height:1.5px}
.btn-ghost{color:var(--muted);font-family:'IBM Plex Mono',monospace;
           font-size:11px;letter-spacing:.18em;text-transform:uppercase}
h2,h3{color:var(--ink)}
.trust-label{color:var(--muted)!important}
#trust,#trust *,.trust,.trust *{color:var(--ink-2)}
'''

s = s0[:m0.start()] + HERO + s0[m0.end():]
s = re.sub(r'<div id="loader"[\s\S]*?</div>\s*(?=<)', '', s, count=1)
s = s.replace("document.documentElement.classList.add('loading')", "void 0")
s = s.replace('<title>', FONTS + '\n<!-- KABUK: GALERI — beyaz duvar -->\n<title>', 1)
i = s.rfind('</style>')
s = s[:i] + '\n/* ===== GALERI ===== */\n' + CSS + '\n' + s[i:]
(ROOT / '_g1.html').write_text(s, encoding='utf-8')
print('_g1.html  GALERI  %d bayt  ·  %d is' % (len(s), len(ISLER)))
