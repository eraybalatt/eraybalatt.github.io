#!/usr/bin/env python3
"""Iki temiz mavi site — Eray'in kendi en iyi sayfasinin dilinde.

Bulgu: /flawless zaten onun en iyi sayfasi ve su yapida:
  01 · The Film / 02 · The Story / 03 · The Interview / 04 · Production Design
  05 · Motion & Identity / 06 · Thumbnail Lab / 07 · Localization
  08 · How It Was Made / 09 · Behind the Edit
  + Craft & Scale · Tools & Stack · Credits
  Renk: --bg #0d1526, --line #2a3a5a

Yani numarali bolumler, surec anlatisi, rakam blogu, kunye. Ana sayfa da
ayni dili konussun ki site kendi icinde tek parca olsun.

_m1 VAKA    Ana sayfa numarali bolumlerle akar, /flawless'in ritmi.
_m2 STUDYO  Duz ve sakin: is izgarasi + yetenek + kanit + iletisim.

Ikisi de mavi. Elektrik mavisi (#1a86d8) degil — /flawless'in sakin
laciverti, uzerinde onun marka acik mavisi.
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')
m0 = re.search(r'id="home">[\s\S]*?</section>', s0)
assert m0

def t3(tag, cls, en, tr, de, extra=''):
    return ('<%s class="%s" data-en="%s" data-tr="%s" data-de="%s"%s>%s</%s>'
            % (tag, cls, en, tr, de, extra, en, tag))

# ad · alt · rol · meta · tur · kaynak   (kaynaklar index.html'e karsi dogrulandi)
ISLER = [
 ('#docs','FLAWLESS','The Antwerp Diamond Heist','Director, writer, editor, narrator',
  '16:56 · 4K · 2026','img','flawless/hero-vault.jpg'),
 ('#music','Modd','real life · yok uyku','AI Creator',
  'Universal Music Türkiye · 2026','vid','mv-reallife.mp4'),
 ('#docs','COLD START','XPRIZE','Editor','2:19 trailer · 2026','vid','hero-coldstart.mp4'),
 ('#ugc','Konfuse','Brand World Film','Director','Original score · 2026','img','konfuse-bagclose.jpg'),
 ('#shorts','Tesadüf Değil','7 bölüm · 106 kare','Producer, director','Short film · 2026','img','tesaduf-grid.webp'),
 ('#prodphoto','Doqu Home','Bellona','Director','Product · furniture · 2025','img','doqu-home.jpg'),
]

def mv(k, src, cls):
    if k=='vid':
        return '<video src="%s" muted loop playsinline preload="none" class="%s"></video>' % (src,cls)
    return '<img src="%s" alt="" loading="lazy" decoding="async" class="%s">' % (src,cls)

RAKAM = [
 ('18.6M','views on channels I built and ran','kurup yönettiğim kanallarda izlenme','Aufrufe auf meinen Kanälen'),
 ('4.8M','in 9 months, from zero','9 ayda, sıfırdan','in 9 Monaten, bei null'),
 ('106','shots for one short film','tek kısa film için kare','Einstellungen für einen Kurzfilm'),
 ('3','languages, one shoot','tek çekimden üç dil','drei Sprachen, ein Dreh'),
]

HIZ = [
 ('Brand &amp; product film','Marka ve ürün filmi','Marken- und Produktfilm',
  'Built once from CAD or reference, identical in every frame. 4K, graded, mixed.',
  'CAD ya da referanstan bir kez kurulur, her karede aynı. 4K, grade’li, mikslenmiş.',
  'Einmal gebaut, in jedem Bild identisch. 4K, gegradet, gemischt.'),
 ('Localisation','Yerelleştirme','Lokalisierung',
  'The same film in another language. Same performer, real lip sync, no reshoot.',
  'Aynı film, başka dilde. Aynı oyuncu, gerçek dudak senkronu, yeniden çekim yok.',
  'Derselbe Film, andere Sprache. Gleicher Darsteller, echte Lippensynchronisation.'),
 ('Documentary','Belgesel','Dokumentarfilm',
  'Events with no surviving footage, reconstructed and labelled as reconstruction.',
  'Görüntüsü kalmamış olaylar; canlandırma olarak kurulur, öyle etiketlenir.',
  'Ereignisse ohne Material, rekonstruiert und gekennzeichnet.'),
]

def blok_is(cls_a, cls_m):
    return '\n        '.join(
      '<a class="%s" href="%s"><figure>%s<figcaption>'
      '<b>%s</b><i>%s</i><span class="cr">%s</span><span class="mt">%s</span>'
      '</figcaption></figure></a>' % (cls_a, h, mv(k,src,cls_m), ad, alt, rol, meta)
      for h,ad,alt,rol,meta,k,src in ISLER)

def blok_rakam():
    return '\n        '.join(
      '<div class="rk"><b>%s</b>%s</div>' % (n, t3('span','',en,tr,de))
      for n,en,tr,de in RAKAM)

def blok_hiz():
    return '\n        '.join(
      '<div class="hz">%s%s</div>' % (t3('h3','',a,b,c), t3('p','',d,e,f))
      for a,b,c,d,e,f in HIZ)

TANIK = ('<figure class="tk"><blockquote>&ldquo;Ti sono grato per il documentario, '
 'mi piace molto.&rdquo;</blockquote><figcaption><b>Leonardo Notarbartolo</b>%s'
 '</figcaption></figure>' % t3('span','',
  'the man who planned the 2003 Antwerp diamond heist, on FLAWLESS',
  '2003 Antwerp elmas soygununu planlayan adam, FLAWLESS hakkında',
  'der Planer des Antwerpener Diamantenraubs 2003, über FLAWLESS'))

def bh(n, en, tr, de):
    return ('<h2 class="eb"><span>%s</span>%s</h2>'
            % (n, t3('em','',en,tr,de)))

# ══════════════════════════════════ _m1 VAKA
M1 = '''id="home">
    <div class="vk-top">
      <span class="vk-nm">Eray Balat</span>
      %s
      %s
    </div>

    <section class="vk-s">
      %s
      <div class="is-grid">
        %s
      </div>
    </section>

    <section class="vk-s vk-alt">
      %s
      <div class="rk-grid">
        %s
      </div>
    </section>

    <section class="vk-s">
      %s
      %s
    </section>

    <section class="vk-s vk-alt">
      %s
      <div class="hz-grid">
        %s
      </div>
    </section>
  </section>''' % (
  t3('span','vk-rl','Director · Creative AI Producer','Yönetmen · Creative AI Producer','Regisseur · Creative AI Producer'),
  t3('p','vk-ln','Brand films, product films and documentaries. Studio in Türkiye, clients in the US and Europe.',
     'Marka filmi, ürün filmi ve belgesel. Türkiye’de stüdyo, ABD ve Avrupa’da müşteriler.',
     'Markenfilme, Produktfilme, Dokumentationen. Studio in der Türkei, Kunden in den USA und Europa.'),
  bh('01','The Work','İşler','Die Arbeiten'), blok_is('is','is-m'),
  bh('02','By the Numbers','Rakamlarla','In Zahlen'), blok_rakam(),
  bh('03','The Proof','Kanıt','Der Beleg'), TANIK,
  bh('04','What I Do','Ne Yapıyorum','Was ich mache'), blok_hiz())

# ══════════════════════════════════ _m2 STUDYO
M2 = '''id="home">
    <div class="st-top">
      <div>
        <span class="st-nm">Eray Balat</span>
        %s
      </div>
      %s
    </div>
    <div class="st-line">%s</div>

    <div class="is-grid st-grid">
      %s
    </div>

    <div class="rk-bar"><div class="rk-grid">
        %s
    </div></div>

    %s

    <div class="hz-grid st-hz">
      %s
    </div>
  </section>''' % (
  t3('span','st-rl','Director','Yönetmen','Regisseur'),
  t3('a','st-ct','Start a project →','Proje başlat →','Projekt starten →',' href="#contact"'),
  t3('p','',
     'Brand films, product films and documentaries. Studio in Türkiye, clients in the US and Europe.',
     'Marka filmi, ürün filmi ve belgesel. Türkiye’de stüdyo, ABD ve Avrupa’da müşteriler.',
     'Markenfilme, Produktfilme, Dokumentationen. Studio in der Türkei, Kunden in den USA und Europa.'),
  blok_is('is','is-m'), blok_rakam(), TANIK, blok_hiz())

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Oswald:wght@300;400;500&family=Public+Sans:wght@400;500;600'
 '&family=IBM+Plex+Mono:wght@400;500&display=swap">')

ORTAK = '''
/* /flawless'in sakin laciverti + Eray'in marka acik mavisi */
:root{
  --bg:#0d1526; --bg-soft:#111c30; --line:#2a3a5a;
  --text:#e6eefa; --muted:#8ea6c6;
  --rule:rgba(120,190,255,.15); --rule-2:rgba(120,190,255,.28);
  --plate:rgba(13,21,38,.985); --ink:#dde9f8; --ink-2:#c3d6ee; --ink-3:#8ea6c6;
  --card:rgba(120,190,255,.06); --card-brd:rgba(120,190,255,.2);
  --acc:#79c9ff;
}
body{background:var(--bg);color:var(--text);font-family:'Public Sans',Helvetica,sans-serif}
#loader,.loader,.welcome,.wel{display:none!important}
html,body{opacity:1!important;visibility:visible!important}
header.nav{display:none!important}
.hero{min-height:auto;padding:0;display:block;text-align:left;overflow:visible}

/* isler */
.is-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line)}
@media(max-width:980px){.is-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.is-grid{grid-template-columns:1fr}}
.is{display:block;text-decoration:none;color:inherit;background:var(--bg);
    transition:background .3s}
.is:hover{background:var(--bg-soft)}
.is figure{margin:0}
.is-m{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;
      filter:saturate(.92);transition:filter .5s}
.is:hover .is-m{filter:saturate(1.05)}
.is figcaption{padding:16px 18px 20px}
.is figcaption b{font-family:'Oswald',sans-serif;font-weight:400;font-size:1.15rem;
                 letter-spacing:.045em;text-transform:uppercase;color:var(--text)}
.is figcaption i{font-style:normal;font-size:13px;color:var(--muted);margin-left:9px}
.is .cr{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
        letter-spacing:.16em;text-transform:uppercase;color:var(--acc);margin-top:10px}
.is .mt{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
        letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:4px}

/* rakamlar */
.rk-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
         gap:1px;background:var(--line)}
.rk{background:var(--bg);padding:24px 20px}
.rk b{display:block;font-family:'Oswald',sans-serif;font-weight:400;
      font-size:clamp(1.8rem,3.6vw,2.5rem);line-height:1;letter-spacing:.01em;
      color:var(--acc);font-variant-numeric:tabular-nums;margin-bottom:9px}
.rk span{display:block;font-size:12.5px;line-height:1.42;color:var(--muted);max-width:26ch}

/* taniklik */
.tk{margin:0;padding:clamp(40px,7vh,80px) max(20px,4vw);background:var(--bg-soft);
    border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tk blockquote{margin:0 0 18px;max-width:26ch;font-style:italic;
  font-size:clamp(1.3rem,3.4vw,2.2rem);line-height:1.24;color:var(--text);text-wrap:balance}
.tk figcaption b{display:block;font-family:'IBM Plex Mono',monospace;font-size:11px;
  letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.tk figcaption span{display:block;font-size:13px;color:var(--muted);margin-top:6px;max-width:48ch}

/* hizmetler */
.hz-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(265px,1fr));
         gap:1px;background:var(--line)}
.hz{background:var(--bg);padding:26px 20px 30px}
.hz h3{font-family:'Oswald',sans-serif;font-weight:400;font-size:1.05rem;
       letter-spacing:.05em;text-transform:uppercase;margin:0 0 10px;color:var(--text)}
.hz p{margin:0;font-size:13.5px;line-height:1.5;color:var(--muted);max-width:34ch}

/* asagidaki mevcut bolumler */
.slj-divider .slj-tag{font-family:'IBM Plex Mono',monospace;color:var(--muted)}
.slj-divider .slj-line{background:linear-gradient(90deg,transparent,var(--rule-2))}
.slj-divider .slj-line:last-child{background:linear-gradient(90deg,var(--rule-2),transparent)}
.btn-grad{text-shadow:none;font-family:'IBM Plex Mono',monospace;font-size:11px;
          letter-spacing:.18em;text-transform:uppercase}
.btn-grad::after{background:var(--acc);box-shadow:none;height:1.5px}
.btn-ghost{color:var(--muted);font-family:'IBM Plex Mono',monospace;font-size:11px;
           letter-spacing:.18em;text-transform:uppercase}
'''

CSS_M1 = ORTAK + '''
/* VAKA — /flawless'in numarali bolum ritmi */
.vk-top{padding:clamp(40px,8vh,90px) max(20px,4vw) clamp(30px,5vh,56px);
        border-bottom:1px solid var(--line)}
.vk-nm{display:block;font-family:'Oswald',sans-serif;font-weight:300;
       font-size:clamp(2.2rem,6.5vw,4.4rem);line-height:.98;letter-spacing:.06em;
       text-transform:uppercase;color:var(--text)}
.vk-rl{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.5px;
       letter-spacing:.28em;text-transform:uppercase;color:var(--acc);margin-top:14px}
.vk-ln{max-width:52ch;font-size:clamp(.98rem,1.8vw,1.14rem);line-height:1.5;
       color:var(--ink-2);margin:22px 0 0}
.vk-s{padding:clamp(38px,6vh,72px) 0 0}
.vk-s>.eb{margin:0 max(20px,4vw) clamp(20px,3vh,30px)}
.vk-alt{background:var(--bg-soft);padding-bottom:clamp(38px,6vh,72px);
        border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.eb{display:flex;align-items:baseline;gap:14px;margin:0;font-weight:400}
.eb span{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.2em;
         color:var(--acc)}
.eb em{font-style:normal;font-family:'Oswald',sans-serif;font-weight:400;
       font-size:clamp(1.05rem,2.4vw,1.5rem);letter-spacing:.08em;
       text-transform:uppercase;color:var(--text)}
.vk-alt .rk{background:var(--bg-soft)}
.vk-alt .hz{background:var(--bg-soft)}
.vk-s .tk{border:0;background:transparent;padding-left:max(20px,4vw);padding-right:max(20px,4vw)}
'''

CSS_M2 = ORTAK + '''
/* STUDYO — duz ve sakin */
.st-top{display:flex;justify-content:space-between;align-items:flex-start;gap:22px;
        padding:clamp(26px,4.5vh,48px) max(20px,4vw) clamp(18px,2.5vh,26px)}
.st-nm{display:block;font-family:'Oswald',sans-serif;font-weight:400;
       font-size:clamp(1.4rem,3vw,2rem);letter-spacing:.09em;text-transform:uppercase}
.st-rl{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
       letter-spacing:.26em;text-transform:uppercase;color:var(--acc);margin-top:7px}
.st-ct{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
       text-transform:uppercase;color:var(--acc);text-decoration:none;white-space:nowrap;
       border:1px solid var(--rule-2);padding:10px 16px;border-radius:2px;
       transition:background .25s,border-color .25s}
.st-ct:hover{background:var(--card);border-color:var(--acc)}
.st-line{padding:0 max(20px,4vw) clamp(30px,5vh,50px);border-bottom:1px solid var(--line)}
.st-line p{margin:0;max-width:56ch;font-size:clamp(.98rem,1.8vw,1.14rem);
           line-height:1.5;color:var(--ink-2)}
.st-grid{border-bottom:1px solid var(--line)}
.rk-bar{border-bottom:1px solid var(--line)}
.st-hz{border-bottom:1px solid var(--line)}
'''

for out, hero, css, ad in (('_m1.html', M1, CSS_M1, 'VAKA — numarali bolumler'),
                           ('_m2.html', M2, CSS_M2, 'STUDYO — duz ve sakin')):
    s = s0[:m0.start()] + hero + s0[m0.end():]
    s = re.sub(r'<div id="loader"[\s\S]*?</div>\s*(?=<)', '', s, count=1)
    s = s.replace("document.documentElement.classList.add('loading')", "void 0")
    s = s.replace('<title>', FONTS + '\n<!-- KABUK: %s -->\n<title>' % ad, 1)
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== %s ===== */\n' % ad + css + '\n' + s[i:]
    (ROOT / out).write_text(s, encoding='utf-8')
    print('%-10s %-28s %7d bayt' % (out, ad, len(s)))
