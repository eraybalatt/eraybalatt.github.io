#!/usr/bin/env python3
"""Dor Brothers taktiklerinin iki farkli dizilisi.

Onlarda iki ayri hamle var ve ikisi de ayni sayfada:
  · hero'da acik iddia          -> "THE WORLD'S LEADING AI VIDEO STUDIO"
  · one cikan viral film + ses  -> APEX, "20M views in 48 hours", "tap for sound"

_i2 KANIT ONDE  Rakam basligin kendisi olur. Iddia altta destek.
                Onlarin "20M in 48 hours" hamlesi, Eray'in gercek rakamiyla.

_i3 FILM ONDE   Tek film ekrani doldurur, sesi acilabilir. Kunye ve o filme
                ait tek rakam ustunde. Iddia filmin altinda gelir.

Ikisinde de ortak (Dor Brothers'tan alinan): rakam seridi, isimli taniklik,
musteri satiri, akis icinde iletisim butonu.
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')
m0 = re.search(r'id="home">[\s\S]*?</section>', s0)
assert m0

def i18n(tag, cls, en, tr, de, extra=''):
    return ('<%s class="%s" data-en="%s" data-tr="%s" data-de="%s"%s>%s</%s>'
            % (tag, cls, en, tr, de, extra, en, tag))

KANIT = [
 ('4.8M',  'views in 9 months, from zero',
           '9 ayda, sıfırdan', 'Aufrufe in 9 Monaten, bei null'),
 ('60.8K', 'subscribers built and handed over',
           'kurulup devredilen abone', 'aufgebaute und übergebene Abonnenten'),
 ('106',   'shots generated and cut for one short film',
           'tek kısa film için üretilip kurgulanan kare', 'Einstellungen für einen Kurzfilm'),
 ('3',     'languages from one shoot, real lip sync',
           'tek çekimden üç dil, gerçek dudak senkronu', 'drei Sprachen aus einem Dreh'),
]

HIZMET = [
 ('Brand &amp; product film', 'Marka ve ürün filmi', 'Marken- und Produktfilm',
  'Built once from CAD or reference, identical in every frame. 4K, graded, mixed.',
  'CAD ya da referanstan bir kez kurulur, her karede aynı kalır. 4K, grade’li, mikslenmiş.',
  'Einmal gebaut, in jedem Bild identisch. 4K, gegradet, gemischt.'),
 ('Localisation', 'Yerelleştirme', 'Lokalisierung',
  'The same film in another language. Same performer, real lip sync, no reshoot.',
  'Aynı film, başka dilde. Aynı oyuncu, gerçek dudak senkronu, yeniden çekim yok.',
  'Derselbe Film, andere Sprache. Gleicher Darsteller, echte Lippensynchronisation.'),
 ('Documentary', 'Belgesel', 'Dokumentarfilm',
  'Events with no surviving footage, reconstructed and labelled as reconstruction.',
  'Görüntüsü kalmamış olaylar; canlandırma olarak kurulur ve öyle etiketlenir.',
  'Ereignisse ohne Material, rekonstruiert und gekennzeichnet.'),
]

def blok_kanit():
    return '\n        '.join(
      '<div class="kn"><b>%s</b>%s</div>' % (n, i18n('span','',en,tr,de))
      for n,en,tr,de in KANIT)

def blok_hizmet():
    return '\n      '.join(
      '<div class="hz">%s%s</div>' % (i18n('h3','',a,b,c), i18n('p','',d,e,f))
      for a,b,c,d,e,f in HIZMET)

TANIK = '''<figure class="tk">
      <blockquote>&ldquo;Ti sono grato per il documentario, mi piace molto.&rdquo;</blockquote>
      <figcaption><b>Leonardo Notarbartolo</b>%s</figcaption>
    </figure>''' % i18n('span','',
      'the man who planned the 2003 Antwerp diamond heist, on FLAWLESS',
      '2003 Antwerp elmas soygununu planlayan adam, FLAWLESS hakkında',
      'der Planer des Antwerpener Diamantenraubs 2003, über FLAWLESS')

BTN = i18n('a','id-btn','Start a project →','Proje başlat →','Projekt starten →',
           ' href="#contact"')

# ══════════════════════════════════════════ _i2  KANIT ONDE
I2 = '''id="home">
    <video class="id-bg" autoplay muted loop playsinline preload="auto" poster="hero-coldstart-poster.webp" src="hero-coldstart.mp4"></video>
    <div class="id-ov"></div>
    <div class="id-in">
      <div class="big-n">18.6<span>M</span></div>
      %s
      %s
      %s
    </div>
    <div class="kn-bar"><div class="kn-wrap">
        %s
    </div></div>
    %s
    <div class="hz-wrap">
      %s
    </div>
  </section>''' % (
  i18n('p','big-l','views on the channels I built and ran.',
       'kurup yönettiğim kanallarda toplam izlenme.',
       'Aufrufe auf den Kanälen, die ich aufgebaut und geführt habe.'),
  i18n('h1','id-h','Your film, in every language you sell in.',
       'Filminiz, sattığınız her dilde.',
       'Ihr Film, in jeder Sprache, in der Sie verkaufen.'),
  BTN, blok_kanit(), TANIK, blok_hizmet())

# ══════════════════════════════════════════ _i3  FILM ONDE
I3 = '''id="home">
    <div class="fm">
      <video class="fm-v" id="fmVid" autoplay muted loop playsinline preload="auto" poster="hero-coldstart-poster.webp" src="hero-coldstart.mp4"></video>
      <div class="fm-ov"></div>
      <button class="fm-snd" id="fmSnd" type="button" aria-pressed="false"
data-on="Sound on" data-off="Tap for sound">Tap for sound</button>
      <div class="fm-c">
        <span class="fm-k">COLD START</span>
        <span class="fm-t">XPRIZE · 2:19 trailer</span>
        <span class="fm-m">Editor</span>
      </div>
    </div>
    <div class="id-in">
      %s
      %s
      %s
    </div>
    <div class="kn-bar"><div class="kn-wrap">
        %s
    </div></div>
    %s
    <div class="hz-wrap">
      %s
    </div>
  </section>''' % (
  i18n('h1','id-h','Two people. The output of a crew.',
       'İki kişi. Bir ekibin çıktısı.',
       'Zwei Leute. Der Output einer Crew.'),
  i18n('p','id-p',
       'Brand films, product films and documentaries. Studio in Türkiye, clients in the US and Europe.',
       'Marka filmi, ürün filmi ve belgesel. Türkiye’de stüdyo, ABD ve Avrupa’da müşteriler.',
       'Markenfilme, Produktfilme, Dokumentationen. Studio in der Türkei, Kunden in den USA und Europa.'),
  BTN, blok_kanit(), TANIK, blok_hizmet())

SES_JS = '''
<script>
(function(){
  var b=document.getElementById('fmSnd'), v=document.getElementById('fmVid');
  if(!b||!v) return;
  b.addEventListener('click',function(){
    v.muted=!v.muted;
    var on=!v.muted;
    b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?b.dataset.on:b.dataset.off;
    if(on) v.play().catch(function(){});
  });
})();
</script>'''

ORTAK = '''
:root{ --bg:#0a0b0d; --bg-soft:#14161a; --text:#f3f4f6; --muted:#98a0a8;
       --rule:rgba(255,255,255,.11); --rule-2:rgba(255,255,255,.2);
       --plate:rgba(10,11,13,.985); --ink:#eef0f2; --ink-2:#d5d9dd; --ink-3:#98a0a8;
       --card:rgba(255,255,255,.045); --card-brd:rgba(255,255,255,.13);
       --acc:#3ddc97; }
body{background:var(--bg)}
#loader,.loader,.welcome,.wel{display:none!important}
html,body{opacity:1!important;visibility:visible!important}
.nav-work{display:none}
.hero{min-height:auto;padding:0;display:block;overflow:visible;position:relative;
      text-align:left;align-items:stretch;justify-content:flex-start}

.id-in{position:relative;z-index:2;padding:0 max(22px,5vw) 9vh;max-width:1180px}
.hero h1.id-h,.id-h{font-family:'Space Grotesk',sans-serif;font-weight:700;
      font-size:clamp(1.85rem,5.2vw,3.8rem);line-height:1.04;letter-spacing:-.025em;
      margin:0 0 20px;max-width:19ch;color:var(--text);background:none;
      -webkit-text-fill-color:currentColor;filter:none;text-wrap:balance}
.id-p{font-size:clamp(.98rem,1.8vw,1.18rem);line-height:1.5;color:var(--ink-2);
      max-width:56ch;margin:0 0 30px}
.id-btn{display:inline-flex;align-items:center;gap:10px;background:var(--acc);
        color:#06231a;text-decoration:none;font-family:'Space Grotesk',sans-serif;
        font-weight:700;font-size:15px;padding:14px 26px;border-radius:2px;
        transition:transform .2s,box-shadow .3s;
        box-shadow:0 10px 34px -14px rgba(61,220,151,.8)}
.id-btn:hover{transform:translateY(-2px);box-shadow:0 16px 44px -14px rgba(61,220,151,.95)}

.kn-bar{position:relative;z-index:2;border-top:1px solid var(--rule);
        border-bottom:1px solid var(--rule);background:var(--bg-soft)}
.kn-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(205px,1fr));
         gap:1px;background:var(--rule);max-width:1400px;margin:0 auto}
.kn{background:var(--bg-soft);padding:26px max(20px,2.4vw)}
.kn b{display:block;font-family:'Space Grotesk',sans-serif;font-weight:700;
      font-size:clamp(1.8rem,3.8vw,2.5rem);line-height:1;letter-spacing:-.02em;
      color:var(--acc);font-variant-numeric:tabular-nums;margin-bottom:9px}
.kn span{display:block;font-size:12.5px;line-height:1.42;color:var(--muted);max-width:26ch}

.tk{position:relative;z-index:2;margin:0;padding:clamp(46px,8vh,84px) max(22px,5vw);
    max-width:1000px;border-bottom:1px solid var(--rule)}
.tk blockquote{margin:0 0 18px;font-size:clamp(1.15rem,2.9vw,1.9rem);line-height:1.34;
               font-style:italic;color:var(--text);text-wrap:balance}
.tk figcaption b{display:block;font-family:'Space Grotesk',sans-serif;font-weight:600;
                 font-size:14px;color:var(--ink-2)}
.tk figcaption span{display:block;font-size:12px;color:var(--muted);margin-top:4px}

.hz-wrap{position:relative;z-index:2;display:grid;
         grid-template-columns:repeat(auto-fit,minmax(265px,1fr));
         gap:1px;background:var(--rule);border-bottom:1px solid var(--rule)}
.hz{background:var(--bg);padding:28px max(20px,2.4vw) 32px}
.hz h3{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:1.02rem;
       margin:0 0 9px;color:var(--text)}
.hz p{margin:0;font-size:13.5px;line-height:1.52;color:var(--muted);max-width:34ch}

.btn-grad::after{background:var(--acc);box-shadow:none}
.btn-grad{text-shadow:none}
.slj-divider .slj-tag{color:var(--muted)}
.slj-divider .slj-line{background:linear-gradient(90deg,transparent,var(--rule-2))}
.slj-divider .slj-line:last-child{background:linear-gradient(90deg,var(--rule-2),transparent)}
header.nav .brand::before{background:linear-gradient(180deg,var(--acc),rgba(61,220,151,.12))}
'''

CSS_I2 = ORTAK + '''
/* rakam basligin kendisi */
.id-bg{position:absolute;left:0;top:0;width:100%;height:88vh;min-height:500px;
       object-fit:cover;z-index:0;opacity:.34;filter:saturate(.8) contrast(1.05)}
.id-ov{position:absolute;left:0;top:0;right:0;height:88vh;min-height:500px;z-index:1;
       pointer-events:none;background:linear-gradient(180deg,rgba(10,11,13,.82) 0%,
       rgba(10,11,13,.46) 32%,rgba(10,11,13,.98) 100%)}
.id-in{padding-top:calc(var(--row1,56px) + 15vh)}
.big-n{font-family:'Space Grotesk',sans-serif;font-weight:700;
       font-size:clamp(5rem,17vw,13rem);line-height:.82;letter-spacing:-.045em;
       color:var(--acc);font-variant-numeric:tabular-nums;margin-bottom:10px}
.big-n span{font-size:.42em;letter-spacing:-.02em;margin-left:.04em}
.big-l{font-size:clamp(1rem,2.1vw,1.3rem);color:var(--ink-2);max-width:34ch;margin:0 0 38px}
.hero h1.id-h{font-size:clamp(1.45rem,3.4vw,2.35rem);max-width:24ch;margin-bottom:26px}
'''

CSS_I3 = ORTAK + '''
/* film onde, sesi acilabilir */
.fm{position:relative;height:86vh;min-height:480px;overflow:hidden}
.fm-v{width:100%;height:100%;object-fit:cover;display:block}
.fm-ov{position:absolute;inset:0;z-index:1;pointer-events:none;
       background:linear-gradient(180deg,rgba(10,11,13,.6) 0%,transparent 30%,
       transparent 52%,rgba(10,11,13,.94) 100%)}
.fm-snd{position:absolute;right:max(20px,4vw);top:calc(var(--row1,56px) + 22px);z-index:3;
        background:rgba(10,11,13,.62);border:1px solid rgba(255,255,255,.28);
        color:#fff;font-family:'Space Grotesk',sans-serif;font-size:10.5px;
        letter-spacing:.2em;text-transform:uppercase;padding:9px 16px;border-radius:2px;
        cursor:pointer;backdrop-filter:blur(8px);transition:background .25s,border-color .25s}
.fm-snd:hover{background:rgba(10,11,13,.85);border-color:rgba(255,255,255,.5)}
.fm-snd[aria-pressed="true"]{border-color:var(--acc);color:var(--acc)}
.fm-c{position:absolute;left:max(22px,5vw);bottom:clamp(30px,6vh,62px);z-index:2}
.fm-k{display:block;font-family:'Oswald','Space Grotesk',sans-serif;font-weight:500;
      font-size:clamp(2.2rem,7vw,4.8rem);line-height:.94;letter-spacing:.02em;color:#fff}
.fm-t{display:block;font-size:clamp(13px,1.6vw,16px);color:rgba(255,255,255,.82);margin-top:10px}
.fm-m{display:block;font-family:'Space Grotesk',sans-serif;font-size:10.5px;
      letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-top:9px}
.id-in{padding-top:clamp(46px,8vh,84px)}
'''

for out, hero, css, ad, js in (
  ('_i2.html', I2, CSS_I2, 'KANIT ONDE — rakam basligin kendisi', ''),
  ('_i3.html', I3, CSS_I3, 'FILM ONDE — tek film, sesi acilabilir', SES_JS),
):
    s = s0[:m0.start()] + hero + s0[m0.end():]
    s = re.sub(r'<div id="loader"[\s\S]*?</div>\s*(?=<)', '', s, count=1)
    s = s.replace("document.documentElement.classList.add('loading')", "void 0")
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== %s ===== */\n' % ad + css + '\n' + s[i:]
    if js:
        s = s.replace('</body>', js + '\n</body>', 1)
    s = s.replace('<title>', '<!-- KABUK: %s -->\n<title>' % ad, 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    print('%-10s %-40s %7d bayt' % (out, ad, len(s)))
