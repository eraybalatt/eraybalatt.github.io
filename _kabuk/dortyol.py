#!/usr/bin/env python3
"""Dort farkli SITE YAPISI. Renk secenegi degil — ilk ekranda ne gorundugu farkli.

_y1 KATALOG  Hero yok. Sayfa dogrudan islerin mozaigiyle aciliyor. Is kendisi kapak.
_y2 AFIS     Tek tam kare: FLAWLESS kasa kapisi. Film afisi mantigi. Amber-noir, mavi yok.
_y3 KUNYE    Ilk ekranda gorsel yok. Buyuk tipografi + numarali is dizini. Acik zemin.
_y4 KANIT    Rakamlarla aciliyor. Valid'de eksik kalan sey tam buydu.

Taban: _a2.html (Konusan Ayrac) — header ve ayraclar korunuyor.
"""
import re, pathlib

ROOT = pathlib.Path('/Users/eraybalat/eraybalat-portfolio')
s0 = (ROOT / '_a2.html').read_text(encoding='utf-8')

HOME_RE = re.compile(r'id="home">[\s\S]*?</section>')
m0 = HOME_RE.search(s0)
assert m0, '#home bulunamadi'

def build(out, hero_html, css, note):
    s = s0[:m0.start()] + hero_html + s0[m0.end():]
    i = s.rfind('</style>')
    s = s[:i] + '\n/* ===== %s ===== */\n' % note + css + '\n' + s[i:]
    s = s.replace('<title>', '<!-- KABUK: %s -->\n<title>' % note, 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    return len(s)

# ═══════════════════════════════════════════════════ 1 · KATALOG
KATALOG_HTML = '''id="home">
    <div class="kat-grid" aria-label="Selected work">
      <a class="kat" href="#docs"  style="--sp:2"><video src="coldstart-film.mp4" muted loop playsinline preload="none" poster="coldstart-grid.webp"></video><span class="kat-t">COLD START</span></a>
      <a class="kat" href="#music"><video src="dtc-1.mp4" muted loop playsinline preload="none"></video><span class="kat-t">Modd — real life</span></a>
      <a class="kat" href="#ugc"><video src="konfuse.mp4" muted loop playsinline preload="none"></video><span class="kat-t">Konfuse</span></a>
      <a class="kat" href="#prodphoto" style="--sp:2"><img src="konfuse-bagclose.jpg" alt="" loading="lazy"><span class="kat-t">Product</span></a>
      <a class="kat" href="#ugc"><video src="tenniscut-3.mp4" muted loop playsinline preload="none"></video><span class="kat-t">TennisCut</span></a>
      <a class="kat" href="#docs"><img src="flawless/hero-vault.jpg" alt="" loading="lazy"><span class="kat-t">FLAWLESS</span></a>
      <a class="kat" href="#shorts"><img src="tesaduf-grid.webp" alt="" loading="lazy"><span class="kat-t">Tesadüf Değil</span></a>
      <a class="kat" href="#brands"><img src="doqu-home.jpg" alt="" loading="lazy"><span class="kat-t">Doqu Home</span></a>
    </div>
    <div class="kat-foot">
      <h1 data-en="Eray Balat directs film for brands." data-tr="Eray Balat markalar için film yönetir." data-de="Eray Balat inszeniert Filme für Marken.">Eray Balat directs film for brands.</h1>
      <a href="#contact" class="btn btn-grad" data-en="Start a project →" data-tr="Proje başlat →" data-de="Projekt starten →">Start a project →</a>
    </div>
  </section>'''

KATALOG_CSS = '''
:root{ --bg:#0a0b0d; --bg-soft:#131519; --text:#f2f4f6; --muted:#9aa3ad;
       --card:rgba(255,255,255,.045); --card-brd:rgba(255,255,255,.12);
       --rule:rgba(255,255,255,.10); --rule-2:rgba(255,255,255,.18);
       --plate:rgba(8,9,11,.985); --ink:#e8ebee; --ink-2:#d8dde2; --ink-3:#96a0aa; }
body{background:var(--bg)}
.hero{min-height:auto;padding:0;display:block;overflow:visible}
.kat-grid{
  display:grid; grid-template-columns:repeat(4,1fr); gap:2px;
  padding-top:var(--row1,56px);
}
@media(max-width:900px){ .kat-grid{grid-template-columns:repeat(2,1fr)} }
.kat{
  position:relative; display:block; aspect-ratio:4/3; overflow:hidden;
  grid-column:span var(--sp,1); background:#0f1115; text-decoration:none;
}
@media(max-width:900px){ .kat{grid-column:span 1; aspect-ratio:1/1} }
.kat img,.kat video{
  width:100%; height:100%; object-fit:cover; display:block;
  filter:grayscale(.55) contrast(1.04); transition:filter .5s, transform .7s;
}
.kat:hover img,.kat:hover video{ filter:none; transform:scale(1.035) }
.kat-t{
  position:absolute; left:14px; bottom:12px; z-index:2;
  font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:600;
  letter-spacing:.2em; text-transform:uppercase; color:#fff;
  text-shadow:0 1px 12px rgba(0,0,0,.9); opacity:0; transition:opacity .35s;
}
.kat:hover .kat-t,.kat:focus-visible .kat-t{ opacity:1 }
.kat::after{
  content:""; position:absolute; inset:0; z-index:1;
  background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.6));
  opacity:0; transition:opacity .35s;
}
.kat:hover::after{ opacity:1 }
.kat-foot{
  display:flex; flex-wrap:wrap; align-items:baseline; justify-content:space-between;
  gap:18px; padding:38px max(22px,4vw) 34px; border-bottom:1px solid var(--rule);
}
.kat-foot h1{
  font-size:clamp(1.35rem,3vw,2.05rem); font-weight:600; margin:0;
  color:var(--text); background:none; -webkit-text-fill-color:currentColor;
  filter:none; max-width:none;
}
.btn-grad::after{ background:linear-gradient(90deg,#fff,#8d97a1); box-shadow:none }
.btn-grad{ text-shadow:none }
'''

# ═══════════════════════════════════════════════════ 2 · AFIS
AFIS_HTML = '''id="home">
    <img class="afis-bg" src="flawless/hero-vault.jpg" alt="" fetchpriority="high" decoding="async">
    <div class="afis-ov"></div>
    <div class="afis-in">
      <div class="afis-kick" data-en="A film by Eray Balat" data-tr="Bir Eray Balat filmi" data-de="Ein Film von Eray Balat">A film by Eray Balat</div>
      <h1 class="afis-h">FLAWLESS</h1>
      <div class="afis-sub" data-en="The Antwerp Diamond Heist" data-tr="Antwerp Elmas Soygunu" data-de="Der Antwerpener Diamantenraub">The Antwerp Diamond Heist</div>
      <p class="afis-q">“Ti sono grato per il documentario, mi piace molto.”<span data-en="Leonardo Notarbartolo, the man who planned it" data-tr="Leonardo Notarbartolo, soygunu planlayan adam" data-de="Leonardo Notarbartolo, der Planer des Raubs">Leonardo Notarbartolo, the man who planned it</span></p>
      <div class="afis-cta">
        <a href="/flawless/" class="btn btn-grad" data-en="See the case study →" data-tr="Vaka çalışmasına git →" data-de="Zur Fallstudie →">See the case study →</a>
        <a href="#music" class="btn btn-ghost" data-en="All work →" data-tr="Tüm işler →" data-de="Alle Arbeiten →">All work →</a>
      </div>
    </div>
  </section>'''

AFIS_CSS = '''
:root{ --bg:#0b0906; --bg-soft:#17120a; --text:#f7f0e2; --muted:#c3b393;
       --card:rgba(252,195,0,.055); --card-brd:rgba(252,195,0,.22);
       --rule:rgba(252,195,0,.13); --rule-2:rgba(252,195,0,.24);
       --plate:rgba(11,9,6,.985); --ink:#f0e6d2; --ink-2:#e2d5bb; --ink-3:#b3a488; }
body{background:var(--bg)}
.hero{min-height:100vh;padding:0;overflow:hidden;justify-content:flex-end}
.afis-bg{
  position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
  z-index:0; filter:contrast(1.06) saturate(1.05);
}
.afis-ov{
  position:absolute; inset:0; z-index:1; pointer-events:none;
  background:
    radial-gradient(ellipse at 62% 46%,transparent 8%,rgba(11,9,6,.5) 62%,rgba(11,9,6,.93) 100%),
    linear-gradient(180deg,rgba(11,9,6,.75) 0%,transparent 26%,transparent 46%,rgba(11,9,6,.96) 96%);
}
.afis-in{
  position:relative; z-index:2; width:100%;
  padding:0 max(22px,5vw) clamp(44px,7vh,88px); text-align:left;
}
.afis-kick{
  font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:600;
  letter-spacing:.34em; text-transform:uppercase; color:#fcc300; margin-bottom:14px;
}
.afis-h{
  font-family:'Oswald','Space Grotesk',sans-serif; font-weight:600;
  font-size:clamp(3.4rem,13vw,9.5rem); line-height:.86; letter-spacing:.02em;
  margin:0 0 10px; color:#fdf6e6; background:none;
  -webkit-text-fill-color:#fdf6e6; filter:drop-shadow(0 6px 40px rgba(0,0,0,.8));
  max-width:none;
}
.afis-sub{
  font-family:'Space Grotesk',sans-serif; font-size:clamp(.95rem,2vw,1.3rem);
  letter-spacing:.22em; text-transform:uppercase; color:#d9c79c; margin-bottom:26px;
}
.afis-q{
  max-width:46ch; font-style:italic; font-size:1.02rem; line-height:1.5;
  color:#e8dcc2; margin:0 0 26px; padding-left:16px;
  border-left:2px solid rgba(252,195,0,.55);
}
.afis-q span{
  display:block; font-style:normal; font-family:'Space Grotesk',sans-serif;
  font-size:10.5px; letter-spacing:.2em; text-transform:uppercase;
  color:#b09a6c; margin-top:9px;
}
.afis-cta{ display:flex; flex-wrap:wrap; gap:26px }
.btn-grad{ color:#fdf6e6; text-shadow:0 0 16px rgba(252,195,0,.35) }
.btn-grad::after{ background:linear-gradient(90deg,#fcc300,#fff0c2); box-shadow:0 2px 14px rgba(252,195,0,.45) }
.slj-divider .slj-tag{ color:rgba(252,195,0,.85) }
.slj-divider .slj-line{ background:linear-gradient(90deg,transparent,rgba(252,195,0,.34)) }
.slj-divider .slj-line:last-child{ background:linear-gradient(90deg,rgba(252,195,0,.34),transparent) }
header.nav .brand::before{ background:linear-gradient(180deg,rgba(252,195,0,.95),rgba(252,195,0,.12)) }
.loader-word{ color:#fcc300 }
'''

# ═══════════════════════════════════════════════════ 3 · KUNYE
KUNYE_HTML = '''id="home">
    <div class="kun-in">
      <p class="kun-state" data-en="I direct film for brands and artists. I work from Kayseri, Türkiye, and almost everyone I work with is somewhere else." data-tr="Markalar ve sanatçılar için film yönetiyorum. Kayseri'de çalışıyorum, birlikte çalıştığım hemen herkes başka bir yerde." data-de="Ich inszeniere Filme für Marken und Künstler. Ich arbeite aus Kayseri, und fast alle meine Auftraggeber sind anderswo.">I direct film for brands and artists. I work from Kayseri, Türkiye, and almost everyone I work with is somewhere else.</p>
      <ol class="kun-ix">
        <li><a href="#docs"><span class="n">01</span><span class="t">FLAWLESS — The Antwerp Diamond Heist</span><span class="y">Documentary · 2026</span></a></li>
        <li><a href="#music"><span class="n">02</span><span class="t">Modd — real life / yok uyku</span><span class="y">Universal Music Türkiye</span></a></li>
        <li><a href="#docs"><span class="n">03</span><span class="t">COLD START</span><span class="y">Trailer · XPRIZE</span></a></li>
        <li><a href="#ugc"><span class="n">04</span><span class="t">Konfuse — Brand World Film</span><span class="y">Brand · 2026</span></a></li>
        <li><a href="#shorts"><span class="n">05</span><span class="t">Tesadüf Değil</span><span class="y">Short film · 2026</span></a></li>
        <li><a href="#prodphoto"><span class="n">06</span><span class="t">Doqu Home · Bellona</span><span class="y">Product · Furniture</span></a></li>
      </ol>
      <div class="kun-cta">
        <a href="#music" class="btn btn-grad" data-en="Watch my work →" data-tr="İşlerimi İzle →" data-de="Meine Arbeiten ansehen →">Watch my work →</a>
        <a href="#contact" class="btn btn-ghost" data-en="Start a project →" data-tr="Proje başlat →" data-de="Projekt starten →">Start a project →</a>
      </div>
    </div>
  </section>'''

KUNYE_CSS = '''
:root{ --bg:#f4f1ec; --bg-soft:#e9e4db; --text:#16181a; --muted:#5c625f;
       --card:rgba(20,22,24,.035); --card-brd:rgba(20,22,24,.14);
       --rule:rgba(20,22,24,.13); --rule-2:rgba(20,22,24,.24);
       --plate:rgba(244,241,236,.985); --ink:#1a1d1f; --ink-2:#2c3134; --ink-3:#666d70; }
body{background:var(--bg);color:var(--text)}
header.nav{ color:var(--ink) }
header.nav .brand-wm b{ color:#16181a; -webkit-text-fill-color:#16181a }
header.nav .brand::before{ background:linear-gradient(180deg,#16181a,rgba(22,24,26,.15)) }
.hero{ min-height:auto; padding:calc(var(--row1,56px) + 8vh) max(22px,5vw) 7vh; text-align:left; align-items:flex-start; justify-content:flex-start }
.kun-in{ width:100%; max-width:900px }
.kun-state{
  font-size:clamp(1.25rem,2.9vw,2rem); line-height:1.34; font-weight:400;
  color:#16181a; max-width:22ch; margin:0 0 clamp(38px,7vh,74px); text-wrap:balance;
}
.kun-ix{ list-style:none; margin:0 0 40px; padding:0; border-top:1px solid var(--rule) }
.kun-ix li{ border-bottom:1px solid var(--rule) }
.kun-ix a{
  display:grid; grid-template-columns:auto 1fr auto; gap:18px; align-items:baseline;
  padding:15px 2px; text-decoration:none; color:inherit; transition:padding .3s, background .3s;
}
.kun-ix a:hover{ padding-left:14px; background:rgba(20,22,24,.035) }
.kun-ix .n{ font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:600; letter-spacing:.12em; color:#8a9092 }
.kun-ix .t{ font-size:clamp(1rem,2.1vw,1.34rem); font-weight:500; color:#16181a }
.kun-ix .y{ font-family:'Space Grotesk',sans-serif; font-size:10.5px; letter-spacing:.18em; text-transform:uppercase; color:#7d8385; white-space:nowrap }
@media(max-width:640px){
  .kun-ix a{ grid-template-columns:auto 1fr; row-gap:4px }
  .kun-ix .y{ grid-column:2 }
}
.kun-cta{ display:flex; flex-wrap:wrap; gap:26px }
.btn-grad{ color:#16181a; text-shadow:none }
.btn-grad::after{ background:#16181a; box-shadow:none }
.btn-ghost{ color:#3d4346 }
.slj-divider .slj-tag{ color:#6d7477 }
.slj-divider .slj-line{ background:linear-gradient(90deg,transparent,rgba(20,22,24,.22)) }
.slj-divider .slj-line:last-child{ background:linear-gradient(90deg,rgba(20,22,24,.22),transparent) }
.loader{ background:#f4f1ec }
.loader-word{ color:#16181a }

/* --- acik tema: header'i boyayan sabit koyu katmanlar --- */
header.nav::before{
  background:linear-gradient(180deg,rgba(244,241,236,.96) 0%,rgba(244,241,236,.88) 62%,rgba(244,241,236,.55) 100%) !important;
  -webkit-mask:none !important; mask:none !important;
}
header.nav::after{ background:var(--grain) 0 0/140px repeat,var(--plate) !important }
header.nav{
  background:none !important;
  border-bottom:1px solid rgba(20,22,24,.14) !important;
  box-shadow:0 6px 26px -20px rgba(0,0,0,.45) !important;
}
header.nav.stuck{ box-shadow:0 8px 30px -18px rgba(0,0,0,.35) !important }
.nav-links a,.nav-work a,.lang-btn,.avail{ color:#2c3134 }
.nav-links a.active{ --nd:#16181a; color:#16181a }
.nav-toggle,.nav-toggle span{ color:#16181a }
.nav-toggle span,.nav-toggle::before,.nav-toggle::after{ background:#16181a }
.avail{ border-color:rgba(20,22,24,.2) }

/* alt seritler de acik zemine gecsin */
.trust,.trust-strip,.brands-strip{ background:transparent }
.trust-label{ color:#6d7477 }

/* acik zeminde okunmayan iki yer */
.lang-btn,.lang-btn *{ color:#3d4346 !important }
.lang-btn[aria-pressed="true"],.lang-btn.active{ color:#16181a !important; font-weight:700 }
#trust,#trust *,.trust,.trust *{ color:#3d4346 }
.trust-label{ color:#7d8385 !important }
#trust img,.trust img{ filter:invert(1) brightness(.35) contrast(1.2) }
'''

# ═══════════════════════════════════════════════════ 4 · KANIT
KANIT_HTML = '''id="home">
    <div class="kan-in">
      <h1 class="kan-h" data-en="The work has receipts." data-tr="İşin karşılığı var." data-de="Die Arbeit hat Belege.">The work has receipts.</h1>
      <div class="kan-grid">
        <div class="kan"><b>18.6M</b><span data-en="lifetime views on channels I ran" data-tr="yönettiğim kanallarda toplam izlenme" data-de="Gesamtaufrufe auf von mir geführten Kanälen">lifetime views on channels I ran</span></div>
        <div class="kan"><b>4.8M</b><span data-en="views in 9 months, from zero" data-tr="9 ayda, sıfırdan" data-de="Aufrufe in 9 Monaten, bei null gestartet">views in 9 months, from zero</span></div>
        <div class="kan"><b>60.8K</b><span data-en="subscribers built and handed over" data-tr="kurulup devredilen abone" data-de="aufgebaute und übergebene Abonnenten">subscribers built and handed over</span></div>
        <div class="kan"><b>2</b><span data-en="music videos for Universal Music Türkiye" data-tr="Universal Music Türkiye için müzik videosu" data-de="Musikvideos für Universal Music Türkiye">music videos for Universal Music Türkiye</span></div>
      </div>
      <p class="kan-q">“Ti sono grato per il documentario, mi piace molto.”<span data-en="Leonardo Notarbartolo, subject of FLAWLESS" data-tr="Leonardo Notarbartolo, FLAWLESS'ın konusu" data-de="Leonardo Notarbartolo, Thema von FLAWLESS">Leonardo Notarbartolo, subject of FLAWLESS</span></p>
      <div class="kan-cta">
        <a href="#music" class="btn btn-grad" data-en="See the work →" data-tr="İşleri gör →" data-de="Die Arbeiten ansehen →">See the work →</a>
        <a href="#contact" class="btn btn-ghost" data-en="Start a project →" data-tr="Proje başlat →" data-de="Projekt starten →">Start a project →</a>
      </div>
    </div>
  </section>'''

KANIT_CSS = '''
:root{ --bg:#07110f; --bg-soft:#0d1d1a; --text:#eaf6f2; --muted:#9dbdb4;
       --card:rgba(70,230,190,.06); --card-brd:rgba(70,230,190,.22);
       --rule:rgba(70,230,190,.13); --rule-2:rgba(70,230,190,.24);
       --plate:rgba(7,17,15,.985); --ink:#dff0ea; --ink-2:#cfe8e0; --ink-3:#8fb0a8; }
body{background:var(--bg)}
.hero{ min-height:auto; padding:calc(var(--row1,56px) + 7vh) max(22px,5vw) 7vh; text-align:left; align-items:flex-start; justify-content:flex-start }
.kan-in{ width:100%; max-width:1000px }
.kan-h{
  font-size:clamp(2rem,5.6vw,3.6rem); font-weight:600; margin:0 0 clamp(34px,6vh,60px);
  color:var(--text); background:none; -webkit-text-fill-color:currentColor; filter:none; max-width:none;
}
.kan-grid{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:1px; background:var(--rule); border:1px solid var(--rule);
  margin-bottom:clamp(30px,5vh,48px);
}
.kan{ background:var(--bg); padding:22px 20px 20px }
.kan b{
  display:block; font-family:'Space Grotesk',sans-serif; font-weight:700;
  font-size:clamp(1.9rem,4.4vw,2.9rem); line-height:1; letter-spacing:-.02em;
  color:#46e6be; font-variant-numeric:tabular-nums; margin-bottom:10px;
}
.kan span{ display:block; font-size:13.5px; line-height:1.42; color:var(--muted); max-width:24ch }
.kan-q{
  max-width:50ch; font-style:italic; font-size:1.02rem; line-height:1.5;
  color:var(--ink-2); margin:0 0 30px; padding-left:16px;
  border-left:2px solid rgba(70,230,190,.5);
}
.kan-q span{
  display:block; font-style:normal; font-family:'Space Grotesk',sans-serif;
  font-size:10.5px; letter-spacing:.2em; text-transform:uppercase;
  color:#7ca79c; margin-top:9px;
}
.kan-cta{ display:flex; flex-wrap:wrap; gap:26px }
.btn-grad{ text-shadow:0 0 16px rgba(70,230,190,.35) }
.btn-grad::after{ background:linear-gradient(90deg,#199e7e,#7ff0d4); box-shadow:0 2px 14px rgba(70,230,190,.4) }
.slj-divider .slj-tag{ color:rgba(70,230,190,.85) }
.slj-divider .slj-line{ background:linear-gradient(90deg,transparent,rgba(70,230,190,.34)) }
.slj-divider .slj-line:last-child{ background:linear-gradient(90deg,rgba(70,230,190,.34),transparent) }
header.nav .brand::before{ background:linear-gradient(180deg,rgba(70,230,190,.95),rgba(70,230,190,.12)) }
.loader-word{ color:#46e6be }
'''

for out, html, css, note in (
    ('_y1.html', KATALOG_HTML, KATALOG_CSS, 'KATALOG — is kendisi kapak'),
    ('_y2.html', AFIS_HTML,    AFIS_CSS,    'AFIS — tek film, amber-noir'),
    ('_y3.html', KUNYE_HTML,   KUNYE_CSS,   'KUNYE — gorselsiz acilis, acik zemin'),
    ('_y4.html', KANIT_HTML,   KANIT_CSS,   'KANIT — rakamlarla acilis'),
):
    print('%-10s %-40s %7d bayt' % (out, note, build(out, html, css, note)))
