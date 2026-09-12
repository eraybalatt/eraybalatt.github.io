#!/usr/bin/env python3
"""Perde + bu oturumda duzeltilen her sey, tek sayfada.

Kaynak parcalar:
  perde mekanizmasi   _p4.html (arsiv) — dokuma kanatlar, isik dikisi, yildiz,
                      kunye karti, sessionStorage, reduced-motion
  sol ray -> ust cubuk  satis.py'deki olculmus duzeltme
  hero satis metni      _t1.html'deki metin

Perdede yapilan GELISTIRMELER (susleme degil, olculebilir):
  1 SURE     5.2 sn -> 3.0 sn. Satis odakli bir sayfada 5 saniye uzun;
             musteri beklemez, LCP'yi de geciktirir.
  2 ATLAMA   tikla / kaydir / Esc / herhangi bir tus -> perde aninda kalkar.
             Onceki surumde atlama yoktu, beklemek zorundaydin.
  3 ERISIM   #intro'ya inert + aria-hidden; klavye odagi perdeye takilmaz.
  4 GUVENLIK JS calismazsa perde hic gorunmez (noscript ile display:none),
             boylece icerik asla perde arkasinda kalmaz.
"""
import re, io, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
base = (ROOT / 'index.html').read_text(encoding='utf-8')
p4   = (ROOT / '_p4.html').read_text(encoding='utf-8')

# ── 1) perde CSS'ini arsivden cikar ───────────────────────────────────
i = p4.index('/* ===== perdeler + jenerik girisi ===== */')
j = p4.index('@media(max-width:879.98px){', i)
PERDE_CSS = p4[i:j]

# ── 2) perde markup'ini cikar ─────────────────────────────────────────
m = re.search(r'<div id="intro"[\s\S]*?</div></div>', p4)
assert m, 'intro markup bulunamadi'
PERDE_HTML = m.group(0)

# ── GELISTIRME 1: sureleri kisalt (5.2 sn -> 3.0 sn) ──────────────────
SURE = [
  ('animation:curL 3s cubic-bezier(.62,.02,.16,1) .55s both',
   'animation:curL 1.9s cubic-bezier(.62,.02,.16,1) .35s both'),
  ('animation:curR 3s cubic-bezier(.62,.02,.16,1) .55s both',
   'animation:curR 1.9s cubic-bezier(.62,.02,.16,1) .35s both'),
  ('animation:curSeam 1.9s ease-out .55s both',
   'animation:curSeam 1.2s ease-out .35s both'),
  ('animation:curStar 1.5s ease-out .35s both',
   'animation:curStar 1.05s ease-out .2s both'),
  ('animation:cardIn 3.1s cubic-bezier(.4,0,.2,1) 1.55s both',
   'animation:cardIn 1.9s cubic-bezier(.4,0,.2,1) .95s both'),
  ('animation:barIn .8s ease-out 3.9s both',
   'animation:barIn .6s ease-out 2.5s both'),
]
for a, b in SURE:
    assert PERDE_CSS.count(a) >= 1, 'sure kurali bulunamadi: %s' % a[:40]
    PERDE_CSS = PERDE_CSS.replace(a, b)

# ── GELISTIRME 2+3+4: atlama, erisim, guvenlik ────────────────────────
EK_CSS = '''
  /* atlanabilir perde: tiklama alani ac, ama sayfayi bloklama */
  #intro{ pointer-events:auto; cursor:pointer }
  #intro.bitti{ display:none !important }
  html.perde-atla #intro{ transition:opacity .28s ease; opacity:0 }
  /* JS yoksa perde hic cikmasin — icerik asla arkada kalmasin */
  html:not(.perde-oynat) #intro{ display:none }
  .perde-skip{
    position:absolute; right:18px; bottom:18px; z-index:2;
    font-family:'Space Grotesk',sans-serif; font-size:10px; letter-spacing:.24em;
    text-transform:uppercase; color:rgba(200,228,255,.72);
    background:none; border:0; cursor:pointer; padding:8px 10px;
  }
  .perde-skip:hover{ color:#eaf6ff }
'''

PERDE_HTML = PERDE_HTML.replace(
  '<div id="intro" aria-hidden="true">',
  '<div id="intro" aria-hidden="true" inert>')
PERDE_HTML = PERDE_HTML.replace(
  '</div></div>',
  '</div><button class="perde-skip" type="button" data-en="Skip" data-tr="Geç" '
  'data-de="Überspringen">Skip</button></div>')

PERDE_JS = '''
<script>
(function(){
  var kok=document.documentElement, intro=document.getElementById('intro');
  if(!intro) return;
  var oynadi=false;
  try{ oynadi = sessionStorage.getItem('eb_perde')==='1'; }catch(e){}
  if(oynadi) return;                       /* oturumda bir kez */

  kok.classList.add('perde-oynat');
  try{ sessionStorage.setItem('eb_perde','1'); }catch(e){}

  var kapandi=false;
  function kapat(){
    if(kapandi) return; kapandi=true;
    kok.classList.add('perde-atla');
    setTimeout(function(){
      intro.classList.add('bitti');
      kok.classList.remove('perde-oynat','perde-atla');
    }, 300);
    temizle();
  }
  function tus(e){ if(e.key==='Escape'||e.key===' '||e.key==='Enter') kapat(); }
  function temizle(){
    intro.removeEventListener('click',kapat);
    removeEventListener('wheel',kapat); removeEventListener('touchstart',kapat);
    removeEventListener('scroll',kapat); removeEventListener('keydown',tus);
  }
  intro.addEventListener('click',kapat);
  addEventListener('wheel',kapat,{passive:true});
  addEventListener('touchstart',kapat,{passive:true});
  addEventListener('scroll',kapat,{passive:true,once:true});
  addEventListener('keydown',tus);

  setTimeout(kapat, 3000);                 /* 5.2 sn -> 3.0 sn */
})();
</script>'''

# ── 3) sol ray duzeltmesi (satis.py'den, olculmus) ────────────────────
sp = (ROOT / '_kabuk' / 'satis.py').read_text(encoding='utf-8')
NAV_CSS = sp[sp.index("/* ===================== SOL RAY -> UST CUBUK"):
             sp.index("/* ===================== SATIS BLOGU")]

# ── 4) hero satis metni (_t1'den) ─────────────────────────────────────
EB_OLD = ('<div class="eyebrow rin" data-en="Creative AI Producer · Filmmaker" '
 'data-tr="Creative AI Producer · Yönetmen" data-de="Creative AI Producer · Filmemacher">'
 'Creative AI Producer · Filmmaker</div>')
EB_NEW = ('<div class="eyebrow rin" data-en="Brand films · Product films · Documentary" '
 'data-tr="Marka filmi · Ürün filmi · Belgesel" '
 'data-de="Markenfilme · Produktfilme · Dokumentarfilm">'
 'Brand films · Product films · Documentary</div>')
LEAD_NEW = ('<p class="lead rin" data-en="18.6M views on channels I built. Universal Music '
 'Türkiye, XPRIZE. Two-person studio in Türkiye, clients in the US and Europe." '
 'data-tr="Kurduğum kanallarda 18,6M izlenme. Universal Music Türkiye, XPRIZE. '
 'Türkiye’de iki kişilik stüdyo, ABD ve Avrupa’da müşteriler." '
 'data-de="18,6 Mio. Aufrufe auf meinen Kanälen. Universal Music Türkiye, XPRIZE. '
 'Zwei-Personen-Studio in der Türkei, Kunden in den USA und Europa.">'
 '18.6M views on channels I built. Universal Music Türkiye, XPRIZE. '
 'Two-person studio in Türkiye, clients in the US and Europe.</p>')

s = base
assert s.count(EB_OLD) == 1
s = s.replace(EB_OLD, EB_NEW, 1)
lead_old = re.search(r'<p class="lead rin" data-en="I direct music videos[\s\S]*?</p>', s).group(0)
s = s.replace(lead_old, LEAD_NEW, 1)

# perdeyi <body>'nin hemen icine koy
s = re.sub(r'(<body[^>]*>)', r'\1\n' + PERDE_HTML, s, count=1)

CSS = NAV_CSS + PERDE_CSS + EK_CSS + '''
  .hero .cta-row .btn-ghost{
    background:#79c9ff;color:#062136;padding:12px 22px;border-radius:2px;
    font-weight:700;text-shadow:none;
    box-shadow:0 10px 30px -14px rgba(121,201,255,.95);
    transition:transform .2s,box-shadow .3s}
  .hero .cta-row .btn-ghost::after{display:none}
  .hero .cta-row .btn-ghost:hover{transform:translateY(-2px)}
  .hero p.lead{max-width:56ch}
'''
k = s.rfind('</style>')
s = s[:k] + '\n/* ===== PERDE + UST CUBUK + HERO SATIS ===== */\n' + CSS + '\n' + s[k:]
s = s.replace('</body>', PERDE_JS + '\n</body>', 1)
s = s.replace('<link rel="canonical"',
              '<meta name="robots" content="noindex,nofollow" />\n<link rel="canonical"', 1)
s = s.replace('<title>', '<!-- KABUK: perde 3.0sn, atlanabilir + ust cubuk + satis -->\n<title>', 1)

(ROOT / '_v1.html').write_text(s, encoding='utf-8')
print('_v1.html  %d bayt' % len(s))
print('  perde CSS  %d bayt' % len(PERDE_CSS))
print('  sure       5.2 sn -> 3.0 sn')
print('  atlama     tikla / kaydir / Esc / Skip dugmesi')
