#!/usr/bin/env python3
"""Mevcut index.html + sol ray kaldirildi + en uste satis blogu.

Eray'in brief'i: "mevcut sitenin su anki hali, sadece sol bari kaldirip
biraz daha iyi bir hale getirmek", "satis odakli bir site olmali",
"direkt olarak ust kismina koyalim".

Yani site degismiyor. Iki sey oluyor:
  1 sol ray -> ust cubuk
  2 hero'nun USTUNE tek satis blogu

Dort alternatif, dort farkli SATIS ARGUMANI (susleme degil):
  _s1 KANIT    rakamlar. "bu adam is yapmis."
  _s2 TEKLIF   ne aldigin ve kacadan. en sert filtre, en nitelikli lead.
  _s3 TANIKLIK Notarbartolo. baskasinin agzindan.
  _s4 HIZ      ucuz ve hizli uretim. rakiplerden ayrilan yer.
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / 'index.html').read_text(encoding='utf-8')

HERO = '<section class="hero" id="home">'
assert s0.count(HERO) == 1, 'hero tekil degil'

def t3(tag, cls, en, tr, de, extra=''):
    return ('<%s class="%s" data-en="%s" data-tr="%s" data-de="%s"%s>%s</%s>'
            % (tag, cls, en, tr, de, extra, en, tag))

CTA = t3('a','sb-cta','Start a project →','Proje başlat →','Projekt starten →',
         ' href="#contact"')

# ─────────────────────────────────────────────── 1 KANIT
S1 = '''<div class="sb sb-kanit">
  <div class="sb-in">
    <div class="sb-nums">
      <span><b>18.6M</b>%s</span>
      <span><b>4.8M</b>%s</span>
      <span><b>60.8K</b>%s</span>
      <span><b>Universal</b>%s</span>
    </div>
    %s
  </div>
</div>''' % (
 t3('i','','views','izlenme','Aufrufe'),
 t3('i','','in 9 months','9 ayda','in 9 Monaten'),
 t3('i','','subscribers','abone','Abonnenten'),
 t3('i','','Music Türkiye','Music Türkiye','Music Türkiye'),
 CTA)

# ─────────────────────────────────────────────── 2 TEKLIF
S2 = '''<div class="sb sb-teklif">
  <div class="sb-in">
    <div class="sb-offer">
      <span><b>%s</b><i>from $3,000</i></span>
      <span><b>%s</b><i>from $1,500</i></span>
      <span><b>%s</b><i>from €900</i></span>
    </div>
    %s
  </div>
</div>''' % (
 '<em data-en="Brand &amp; product film" data-tr="Marka ve ürün filmi" data-de="Marken- und Produktfilm">Brand &amp; product film</em>',
 '<em data-en="Short-form &amp; UGC" data-tr="Kısa form ve UGC" data-de="Short-Form &amp; UGC">Short-form &amp; UGC</em>',
 '<em data-en="Localisation" data-tr="Yerelleştirme" data-de="Lokalisierung">Localisation</em>',
 CTA)

# ─────────────────────────────────────────────── 3 TANIKLIK
S3 = '''<div class="sb sb-tanik">
  <div class="sb-in">
    <blockquote>&ldquo;Ti sono grato per il documentario, mi piace molto.&rdquo;
      <cite><b>Leonardo Notarbartolo</b>%s</cite></blockquote>
    %s
  </div>
</div>''' % (
 t3('span','',
   'the man who planned the 2003 Antwerp diamond heist, on FLAWLESS',
   '2003 Antwerp elmas soygununu planlayan adam, FLAWLESS hakkında',
   'der Planer des Antwerpener Diamantenraubs 2003, über FLAWLESS'),
 CTA)

# ─────────────────────────────────────────────── 4 HIZ
S4 = '''<div class="sb sb-hiz">
  <div class="sb-in">
    <div class="sb-speed">
      <span><b>106</b>%s</span>
      <span><b>5</b>%s</span>
      <span><b>3</b>%s</span>
    </div>
    %s
  </div>
</div>''' % (
 t3('i','','shots in one week','bir haftada kare','Einstellungen in einer Woche'),
 t3('i','','revision rounds, one night','revizyon turu, tek gece','Korrekturrunden, eine Nacht'),
 t3('i','','languages, one shoot','tek çekimden dil','Sprachen, ein Dreh'),
 CTA)

# ─────────────────────────────────────────────── ortak CSS
CSS = '''
/* ===================== SOL RAY -> UST CUBUK ===================== */
:root{ --sb:0px; --bar:58px }
@media (min-width:880px){
  body{ padding-left:0; padding-top:0 }
  header.nav{
    top:0; left:0; right:0; bottom:auto;
    width:auto; height:var(--bar); min-height:var(--bar);
    border-right:none;
    border-bottom:1px solid rgba(120,210,255,.22);
    background:linear-gradient(180deg,rgba(18,52,100,.94) 0%,rgba(9,28,56,.88) 100%);
    background-size:auto; animation:none; overflow:visible;
    box-shadow:0 12px 40px -26px rgba(28,74,146,.8);
  }
  header.nav::before{ display:none }

  .nav-inner{
    flex-direction:row; align-items:center; justify-content:flex-start;
    height:var(--bar); max-width:1440px; margin:0 auto; gap:0 26px;
    padding:0 max(20px,3vw); overflow:visible;
  }

  /* marka: yatay ve kompakt */
  .brand{ flex:0 0 auto; flex-direction:row; align-items:center; gap:10px;
          margin:0; padding:0; border:0 }
  .brand-mark,.brand-mark svg{ width:30px; height:30px }
  .brand-wm{ flex-direction:column; align-items:flex-start; gap:2px }
  .brand-wm b{ font-size:13px; letter-spacing:.08em }
  .brand-wm i{ font-size:8.5px; letter-spacing:.16em }

  /* menu: yatay, numarasiz, tek satir */
  .nav-links{ flex:1 1 auto; flex-direction:row; align-items:center;
              gap:0 clamp(12px,1.5vw,22px); margin:0; padding:0; border:0;
              overflow:visible; flex-wrap:nowrap }
  .nav-links a{ padding:6px 0; margin:0; border:0; font-size:12.5px; white-space:nowrap }
  .nav-links a::before,.nav-links a::marker{ display:none; content:none }
  .nav-links a::after{ bottom:-2px }

  .lang-switch,.lang-wrap,.lang-row{ flex:0 0 auto; margin:0; padding:0; border:0 }
  .avail{ flex:0 0 auto; margin:0 }
}
/* ===================== SATIS BLOGU (en ust) ===================== */
.sb{ position:relative; z-index:6; background:#08182e;
     border-bottom:1px solid rgba(120,210,255,.2) }
@media (min-width:880px){ .sb{ margin-top:var(--bar) } }
.sb-in{ max-width:1440px; margin:0 auto; padding:16px max(20px,3vw);
        display:flex; flex-wrap:wrap; align-items:center;
        justify-content:space-between; gap:16px 28px }
.sb-cta{
  flex:0 0 auto; display:inline-flex; align-items:center;
  background:#79c9ff; color:#062136; text-decoration:none;
  font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:13px;
  letter-spacing:.01em; padding:11px 20px; border-radius:2px;
  transition:transform .2s, box-shadow .3s;
  box-shadow:0 8px 26px -12px rgba(121,201,255,.9);
}
.sb-cta:hover{ transform:translateY(-1px); box-shadow:0 12px 32px -12px rgba(121,201,255,1) }

/* rakam ve hiz seritleri */
.sb-nums,.sb-speed{ display:flex; flex-wrap:wrap; gap:10px clamp(20px,3.4vw,46px) }
.sb-nums span,.sb-speed span{ display:flex; align-items:baseline; gap:8px }
.sb-nums b,.sb-speed b{
  font-family:'Space Grotesk',sans-serif; font-weight:700;
  font-size:clamp(1.15rem,2.2vw,1.55rem); line-height:1; letter-spacing:-.015em;
  color:#79c9ff; font-variant-numeric:tabular-nums;
}
.sb-nums i,.sb-speed i{
  font-style:normal; font-family:'Space Grotesk',sans-serif; font-size:10.5px;
  letter-spacing:.16em; text-transform:uppercase; color:#9fc0dc;
}

/* teklif seridi */
.sb-offer{ display:flex; flex-wrap:wrap; gap:12px clamp(20px,3.4vw,46px) }
.sb-offer span{ display:flex; flex-direction:column; gap:4px }
.sb-offer em{ font-style:normal; font-family:'Space Grotesk',sans-serif;
  font-weight:600; font-size:13.5px; color:#e6f1fb }
.sb-offer i{ font-style:normal; font-family:'Space Grotesk',sans-serif;
  font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:#79c9ff }

/* taniklik */
.sb-tanik blockquote{ margin:0; max-width:62ch; font-style:italic;
  font-size:clamp(.98rem,1.9vw,1.2rem); line-height:1.4; color:#e6f1fb }
.sb-tanik cite{ display:block; font-style:normal; margin-top:8px }
.sb-tanik cite b{ font-family:'Space Grotesk',sans-serif; font-weight:600;
  font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:#79c9ff }
.sb-tanik cite span{ display:block; font-size:11.5px; color:#9fc0dc; margin-top:3px }

@media(max-width:600px){
  .sb-in{ padding:14px 18px; gap:14px }
  .sb-cta{ width:100%; justify-content:center }
}
'''

for out, blok, ad in (('_s1.html', S1, 'KANIT — rakamlar ustte'),
                      ('_s2.html', S2, 'TEKLIF — ne aldigin ve kacadan'),
                      ('_s3.html', S3, 'TANIKLIK — Notarbartolo ustte'),
                      ('_s4.html', S4, 'HIZ — uretim hizi ustte')):
    s = s0.replace(HERO, blok + '\n\n  ' + HERO, 1)
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== SATIS: %s ===== */\n' % ad + CSS + '\n' + s[i:]
    s = s.replace('<link rel="canonical"',
                  '<meta name="robots" content="noindex,nofollow" />\n<link rel="canonical"', 1)
    s = s.replace('<title>', '<!-- KABUK: %s -->\n<title>' % ad, 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    print('%-10s %-34s %7d bayt' % (out, ad, len(s)))
