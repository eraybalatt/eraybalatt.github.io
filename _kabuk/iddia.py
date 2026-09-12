#!/usr/bin/env python3
"""Dor Brothers mantigi, Eray'in gercek malzemesiyle.

Yapi (soyutlanan mantik):
  1 IDDIA    tek satir, konumlandirma. Tarif degil iddia.
  2 KANIT    rakam -> isim -> logo. Guc sirasi bu.
  3 TANIKLIK Notarbartolo. Baskasinin itibari.
  4 IS       iddianin kaniti olarak, galeri olarak degil.
  5 NE       uc hizmet hatti, kisa.
  6 ILETISIM akisin icinde buton.

IDDIA satiri degistirilebilir: A / B / C icinde secim yapilir.
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')
m0 = re.search(r'id="home">[\s\S]*?</section>', s0)
assert m0

# ── IDDIA secenekleri ─────────────────────────────────────────────────
IDDIA = {
'A': dict(
  en='I make films of things that were never filmed.',
  tr='Hiç çekilmemiş şeylerin filmini yapıyorum.',
  de='Ich mache Filme von Dingen, die nie gefilmt wurden.'),
'B': dict(
  en='Two people. The output of a crew.',
  tr='İki kişi. Bir ekibin çıktısı.',
  de='Zwei Leute. Der Output einer Crew.'),
'C': dict(
  en='Your film, in every language you sell in.',
  tr='Filminiz, sattığınız her dilde.',
  de='Ihr Film, in jeder Sprache, in der Sie verkaufen.'),
}
SEC = 'A'   # <- degistir

ALT = dict(
  en='Brand films, product films and documentaries. Two-person studio in Türkiye, clients in the US and Europe.',
  tr='Marka filmi, ürün filmi ve belgesel. Türkiye’de iki kişilik stüdyo, ABD ve Avrupa’da müşteriler.',
  de='Markenfilme, Produktfilme und Dokumentationen. Zwei-Personen-Studio in der Türkei, Kunden in den USA und Europa.')

def i18n(tag, cls, d, extra=''):
    return ('<%s class="%s" data-en="%s" data-tr="%s" data-de="%s"%s>%s</%s>'
            % (tag, cls, d['en'], d['tr'], d['de'], extra, d['en'], tag))

KANIT = [
 ('18.6M', dict(en='lifetime views on channels I ran',
                tr='yönettiğim kanallarda toplam izlenme',
                de='Gesamtaufrufe auf von mir geführten Kanälen')),
 ('4.8M',  dict(en='views in 9 months, from zero',
                tr='9 ayda, sıfırdan',
                de='Aufrufe in 9 Monaten, bei null')),
 ('60.8K', dict(en='subscribers built and handed over',
                tr='kurulup devredilen abone',
                de='aufgebaute und übergebene Abonnenten')),
 ('106',   dict(en='shots generated and cut for one short film',
                tr='tek kısa film için üretilip kurgulanan kare',
                de='Einstellungen für einen Kurzfilm')),
]

HIZMET = [
 (dict(en='Brand &amp; product film', tr='Marka ve ürün filmi', de='Marken- und Produktfilm'),
  dict(en='Built once from CAD or reference, identical in every frame. Delivered 4K, graded, mixed.',
       tr='CAD ya da referanstan bir kez kurulur, her karede aynı kalır. 4K, grade’li ve mikslenmiş teslim.',
       de='Einmal aus CAD oder Referenz gebaut, in jedem Bild identisch. 4K, gegradet, gemischt.')),
 (dict(en='Localisation', tr='Yerelleştirme', de='Lokalisierung'),
  dict(en='The same film in another language. Same performer, real lip sync, no reshoot.',
       tr='Aynı film, başka dilde. Aynı oyuncu, gerçek dudak senkronu, yeniden çekim yok.',
       de='Derselbe Film in einer anderen Sprache. Gleicher Darsteller, echte Lippensynchronisation, kein Nachdreh.')),
 (dict(en='Documentary', tr='Belgesel', de='Dokumentarfilm'),
  dict(en='Events with no surviving footage, reconstructed and labelled as reconstruction.',
       tr='Görüntüsü kalmamış olaylar; canlandırma olarak kurulur ve öyle etiketlenir.',
       de='Ereignisse ohne erhaltenes Material, rekonstruiert und als solche gekennzeichnet.')),
]

def hero():
    kanit = '\n        '.join(
      '<div class="kn"><b>%s</b>%s</div>' % (n, i18n('span','', d))
      for n, d in KANIT)
    hiz = '\n        '.join(
      '<div class="hz">%s%s</div>' % (i18n('h3','', a), i18n('p','', b))
      for a, b in HIZMET)
    return '''id="home">
    <video class="id-bg" autoplay muted loop playsinline preload="auto" poster="coldstart-grid.webp" src="coldstart-film.mp4"></video>
    <div class="id-ov"></div>

    <div class="id-in">
      %s
      %s
      <a href="#contact" class="id-btn" data-en="Start a project →" data-tr="Proje başlat →" data-de="Projekt starten →">Start a project →</a>
    </div>

    <div class="kn-bar">
      <div class="kn-wrap">
        %s
      </div>
    </div>

    <figure class="tk">
      <blockquote>&ldquo;Ti sono grato per il documentario, mi piace molto.&rdquo;</blockquote>
      <figcaption><b>Leonardo Notarbartolo</b>%s</figcaption>
    </figure>

    <div class="hz-wrap">
      %s
    </div>
  </section>''' % (
    i18n('h1','id-h', IDDIA[SEC]),
    i18n('p','id-p', ALT),
    kanit,
    i18n('span','', dict(
      en='the man who planned the 2003 Antwerp diamond heist, on FLAWLESS',
      tr='2003 Antwerp elmas soygununu planlayan adam, FLAWLESS hakkında',
      de='der Planer des Antwerpener Diamantenraubs 2003, über FLAWLESS')),
    hiz)

CSS = '''
:root{ --bg:#0a0b0d; --bg-soft:#14161a; --text:#f3f4f6; --muted:#98a0a8;
       --rule:rgba(255,255,255,.11); --rule-2:rgba(255,255,255,.2);
       --plate:rgba(10,11,13,.985); --ink:#eef0f2; --ink-2:#d5d9dd; --ink-3:#98a0a8;
       --card:rgba(255,255,255,.045); --card-brd:rgba(255,255,255,.13);
       --acc:#3ddc97; }
body{background:var(--bg)}
#loader,.loader,.welcome,.wel{display:none!important}
html,body{opacity:1!important;visibility:visible!important}
.nav-work{display:none}

/* 1 — IDDIA */
.hero{min-height:auto;padding:0;display:block;overflow:visible;position:relative;text-align:left;align-items:stretch;justify-content:flex-start}
.id-bg{position:absolute;left:0;top:0;width:100%;height:82vh;min-height:460px;
       object-fit:cover;z-index:0;opacity:.42;filter:saturate(.85) contrast(1.05)}
.id-ov{position:absolute;left:0;top:0;right:0;height:82vh;min-height:460px;z-index:1;pointer-events:none;
       background:linear-gradient(180deg,rgba(10,11,13,.78) 0%,rgba(10,11,13,.42) 34%,rgba(10,11,13,.97) 100%)}
.id-in{position:relative;z-index:2;padding:calc(var(--row1,56px) + 16vh) max(22px,5vw) 10vh;max-width:1180px}
.id-h{font-family:'Space Grotesk',sans-serif;font-weight:700;
      font-size:clamp(2.1rem,6.2vw,4.6rem);line-height:1.02;letter-spacing:-.025em;
      margin:0 0 22px;max-width:17ch;color:var(--text);
      background:none;-webkit-text-fill-color:currentColor;filter:none;text-wrap:balance}
.id-p{font-size:clamp(1rem,1.9vw,1.22rem);line-height:1.5;color:var(--ink-2);
      max-width:56ch;margin:0 0 32px}
.id-btn{display:inline-flex;align-items:center;gap:10px;
        background:var(--acc);color:#06231a;text-decoration:none;
        font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:15px;
        letter-spacing:.01em;padding:14px 26px;border-radius:2px;
        transition:transform .2s,box-shadow .3s;
        box-shadow:0 10px 34px -14px rgba(61,220,151,.8)}
.id-btn:hover{transform:translateY(-2px);box-shadow:0 16px 44px -14px rgba(61,220,151,.95)}

/* 2 — KANIT */
.kn-bar{position:relative;z-index:2;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
        background:var(--bg-soft)}
.kn-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
         gap:1px;background:var(--rule);max-width:1400px;margin:0 auto}
.kn{background:var(--bg-soft);padding:28px max(20px,2.4vw)}
.kn b{display:block;font-family:'Space Grotesk',sans-serif;font-weight:700;
      font-size:clamp(1.9rem,4vw,2.7rem);line-height:1;letter-spacing:-.02em;
      color:var(--acc);font-variant-numeric:tabular-nums;margin-bottom:10px}
.kn span{display:block;font-size:13px;line-height:1.42;color:var(--muted);max-width:26ch}

/* 3 — TANIKLIK */
.tk{position:relative;z-index:2;margin:0;padding:clamp(48px,8vh,86px) max(22px,5vw);
    max-width:1000px;border-bottom:1px solid var(--rule)}
.tk blockquote{margin:0 0 18px;font-size:clamp(1.2rem,3vw,1.95rem);line-height:1.34;
               font-style:italic;color:var(--text);text-wrap:balance}
.tk figcaption b{display:block;font-family:'Space Grotesk',sans-serif;font-weight:600;
                 font-size:14px;letter-spacing:.02em;color:var(--ink-2)}
.tk figcaption span{display:block;font-size:12px;color:var(--muted);margin-top:4px}

/* 5 — NE YAPIYORUM */
.hz-wrap{position:relative;z-index:2;display:grid;
         grid-template-columns:repeat(auto-fit,minmax(270px,1fr));
         gap:1px;background:var(--rule);border-bottom:1px solid var(--rule)}
.hz{background:var(--bg);padding:30px max(20px,2.4vw) 34px}
.hz h3{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:1.05rem;
       letter-spacing:.01em;margin:0 0 10px;color:var(--text)}
.hz p{margin:0;font-size:14px;line-height:1.52;color:var(--muted);max-width:34ch}

/* iletisim butonu bolumlerde de tekrarlansin */
.btn-grad::after{background:var(--acc);box-shadow:none}
.btn-grad{text-shadow:none}
.slj-divider .slj-tag{color:var(--muted)}
.slj-divider .slj-line{background:linear-gradient(90deg,transparent,var(--rule-2))}
.slj-divider .slj-line:last-child{background:linear-gradient(90deg,var(--rule-2),transparent)}
header.nav .brand::before{background:linear-gradient(180deg,var(--acc),rgba(61,220,151,.12))}
'''

s = s0[:m0.start()] + hero() + s0[m0.end():]
s = re.sub(r'<div id="loader"[\s\S]*?</div>\s*(?=<)', '', s, count=1)
s = s.replace("document.documentElement.classList.add('loading')", "void 0")
i = s.rfind('</style>')
s = s[:i] + '\n/* ===== IDDIA — Dor Brothers mantigi ===== */\n' + CSS + '\n' + s[i:]
s = s.replace('<title>', '<!-- KABUK: IDDIA (secenek %s) -->\n<title>' % SEC, 1)
(ROOT / '_i1.html').write_text(s, encoding='utf-8')
print('_i1.html  iddia secenegi %s  %d bayt' % (SEC, len(s)))
print('  iddia:', IDDIA[SEC]['tr'])
